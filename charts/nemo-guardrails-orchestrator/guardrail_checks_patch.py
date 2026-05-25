# Patch: adds /v1/guardrail/checks for llama stack remote::nvidia safety provider compatibility.
# Appended to nemoguardrails/server/api.py at image build time.
# Runs in the same module scope as api.py — app, log, registered_loggers, asyncio,
# _get_rails, LLMRails, RailsConfig, api_request_headers are all already defined.

import json as _json

from typing import Dict, List, Literal, Optional

# Stub LLM that returns "" immediately, used during input-only rail checks.
# NeMo always calls the LLM after input rails complete (even with dialog=False).
# Its streaming response is re-fed into the pipeline as new user messages, causing
# input rails (HF classifiers, self_check_input) to falsely flag LLM output.
# The stub breaks this loop: "" fires one harmless UtteranceUserActionFinished
# event that passes all classifiers and terminates cleanly.
try:
    from langchain_core.language_models.chat_models import BaseChatModel as _BaseChatModel
    from langchain_core.messages import AIMessage as _AIMessage
    from langchain_core.outputs import ChatGeneration as _ChatGeneration, ChatResult as _ChatResult

    class _NoopLLM(_BaseChatModel):
        @property
        def _llm_type(self):
            return "noop"

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            return _ChatResult(generations=[_ChatGeneration(message=_AIMessage(content=""))])

        async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs):
            return _ChatResult(generations=[_ChatGeneration(message=_AIMessage(content=""))])

    _NOOP_LLM = _NoopLLM()
except Exception:
    _NOOP_LLM = None


def _make_input_check_rails(llm_rails):
    """Return a shallow copy of llm_rails with the LLM replaced by the no-op stub."""
    if _NOOP_LLM is None:
        return llm_rails
    rails_copy = object.__new__(type(llm_rails))
    rails_copy.__dict__.update(llm_rails.__dict__)
    rails_copy.llm = _NOOP_LLM
    return rails_copy

from fastapi import Request as _Request
from pydantic import BaseModel, Field
from starlette.responses import StreamingResponse as _StreamingResponse

from nemoguardrails.rails.llm.options import (
    ActivatedRail,
    GenerationLog,
    GenerationLogOptions,
    GenerationOptions,
    GenerationRailsOptions,
    GenerationStats,
)


class GuardrailCheckRequestBody(BaseModel):
    model: str = Field(description="Model identifier (informational).")
    messages: List[dict] = Field(description="Messages to check against guardrails.")
    guardrails: Optional[dict] = Field(
        default=None,
        description="'config_id' or 'config' key. Omit to use server default.",
    )
    stream: Optional[bool] = Field(default=False)
    top_p: Optional[float] = Field(default=None)
    temperature: Optional[float] = Field(default=None)
    max_tokens: Optional[int] = Field(default=None)


class MessageCheckResult(BaseModel):
    index: int
    role: str
    rails: Dict[str, dict] = Field(default_factory=dict)


class GuardrailCheckResponseBody(BaseModel):
    status: Literal["success", "blocked", "error"]
    rails_status: Dict[str, dict] = Field(default_factory=dict)
    messages: List[MessageCheckResult] = Field(default_factory=list)
    guardrails_data: Optional[dict] = Field(default=None)
    blocked_message: Optional[str] = Field(default=None)


def _gc_create_error_response(error: str, details: Optional[str] = None) -> GuardrailCheckResponseBody:
    guardrails_data = {"error": error}
    if details:
        guardrails_data["details"] = details
    return GuardrailCheckResponseBody(status="error", rails_status={}, guardrails_data=guardrails_data)


async def _gc_load_rails(config_id=None, inline_config=None):
    if inline_config:
        if isinstance(inline_config, dict):
            models = inline_config.get("models", [])
            if not models and app.default_config_id:
                try:
                    default_rails = await _get_rails([app.default_config_id])
                    if default_rails.config.models:
                        inline_config = inline_config.copy()
                        inline_config["models"] = []
                        for model in default_rails.config.models:
                            model_dict = {"type": model.type, "engine": model.engine}
                            params = dict(model.parameters) if model.parameters else {}
                            if model.model:
                                params["model_name"] = model.model
                            if params:
                                model_dict["parameters"] = params
                            inline_config["models"].append(model_dict)
                except Exception as e:
                    log.warning(f"Could not inherit models from default config: {e}")
        rails_config = (
            RailsConfig.from_content(yaml_content=inline_config)
            if isinstance(inline_config, str)
            else RailsConfig.from_content(config=inline_config)
        )
        return LLMRails(config=rails_config, verbose=True)
    if not config_id:
        raise ValueError("Either config_id or inline_config must be provided")
    return await _get_rails([config_id])


def _gc_create_check_options(run_input=False, run_output=False, run_tool_input=False, run_tool_output=False):
    return GenerationOptions(
        rails=GenerationRailsOptions(
            input=run_input,
            output=run_output,
            retrieval=False,
            dialog=False,
            tool_input=run_tool_input,
            tool_output=run_tool_output,
        ),
        log=GenerationLogOptions(activated_rails=True, internal_events=True, llm_calls=True),
    )


def _gc_calculate_status(rails_status: dict) -> str:
    return "blocked" if any(s.get("status") == "blocked" for s in rails_status.values()) else "success"


@app.post("/v1/guardrail/checks", response_model=GuardrailCheckResponseBody)
async def guardrail_checks(body: GuardrailCheckRequestBody, request: _Request):
    """Check messages against guardrails without generating LLM responses."""
    log.info("Got guardrail check request")
    for logger in registered_loggers:
        asyncio.get_event_loop().create_task(
            logger({"endpoint": "/v1/guardrail/checks", "body": body.model_dump_json()})
        )
    api_request_headers.set(request.headers)

    async def process_checks():
        try:
            if not body.messages:
                yield _json.dumps(_gc_create_error_response("Messages list cannot be empty.").model_dump()) + "\n"
                return

            config_id, inline_config = None, None
            if body.guardrails:
                config_id = body.guardrails.get("config_id")
                inline_config = body.guardrails.get("config")
                if config_id and inline_config:
                    yield _json.dumps(_gc_create_error_response(
                        "Only one of 'config_id' or 'config' should be provided."
                    ).model_dump()) + "\n"
                    return
                if not (config_id or inline_config):
                    yield _json.dumps(_gc_create_error_response(
                        "Either 'config_id' or 'config' must be provided in guardrails field."
                    ).model_dump()) + "\n"
                    return
            else:
                config_id = app.default_config_id
                if not config_id:
                    yield _json.dumps(_gc_create_error_response(
                        "No guardrails configuration provided and no default configuration set on server."
                    ).model_dump()) + "\n"
                    return

            try:
                llm_rails = await _gc_load_rails(config_id, inline_config)
            except Exception as ex:
                log.exception(ex)
                yield _json.dumps(_gc_create_error_response("Could not load guardrails configuration.", str(ex)).model_dump()) + "\n"
                return

            rails_status = {}
            message_results = []
            aggregated_log = GenerationLog(activated_rails=[], stats=GenerationStats())
            first_blocked_message = None

            prev_user_content = ""
            for msg_idx, msg in enumerate(body.messages):
                if not isinstance(msg, dict) or "role" not in msg:
                    continue

                role = msg.get("role")
                content = msg.get("content", "")
                message_rails = {}

                if role == "user":
                    next_role = body.messages[msg_idx + 1].get("role") if msg_idx + 1 < len(body.messages) else None
                    if next_role == "assistant":
                        # This user message is context for the output check — skip input rails, just track it
                        prev_user_content = content
                        continue
                    options = _gc_create_check_options(run_input=True)
                    input_rails = _make_input_check_rails(llm_rails)
                    result = await input_rails.generate_async(messages=[{"role": "user", "content": content}], options=options)
                    prev_user_content = content
                elif role == "assistant":
                    if "tool_calls" in msg:
                        from nemoguardrails.utils import new_event_dict
                        nemo_tool_calls = []
                        for tc in msg["tool_calls"]:
                            if "function" in tc:
                                tool_call = {
                                    "id": tc.get("id", ""),
                                    "name": tc["function"]["name"],
                                    "args": (
                                        _json.loads(tc["function"]["arguments"])
                                        if isinstance(tc["function"]["arguments"], str)
                                        else tc["function"]["arguments"]
                                    ),
                                    "type": "tool_call",
                                }
                            else:
                                tool_call = tc
                            nemo_tool_calls.append(tool_call)
                        events = [new_event_dict("BotToolCalls", tool_calls=nemo_tool_calls)]
                        result_events = await llm_rails.runtime.generate_events(events)
                        activated_rail_names = [
                            e.get("flow_id") for e in result_events
                            if e.get("type") == "StartToolOutputRail" and e.get("flow_id")
                        ]
                        blocked_message = next(
                            (e.get("script") for e in result_events if e.get("type") == "StartUtteranceBotAction"),
                            None,
                        )
                        rail_objects = [
                            ActivatedRail(type="tool_output", name=n, stop=(blocked_message is not None), decisions=[], executed_actions=[])
                            for n in activated_rail_names
                        ]
                        result = type("obj", (object,), {
                            "response": ([{"role": "assistant", "content": blocked_message}] if blocked_message else []),
                            "log": type("obj", (object,), {"activated_rails": rail_objects, "stats": None})(),
                        })()
                    else:
                        options = _gc_create_check_options(run_output=True)
                        result = await llm_rails.generate_async(
                            messages=[{"role": "user", "content": prev_user_content}, {"role": "assistant", "content": content}],
                            options=options,
                        )
                elif role == "tool":
                    options = _gc_create_check_options(run_tool_input=True)
                    tool_msg = {"role": "tool", "content": content}
                    if "name" in msg:
                        tool_msg["name"] = msg["name"]
                    if "tool_call_id" in msg:
                        tool_msg["tool_call_id"] = msg["tool_call_id"]
                    result = await llm_rails.generate_async(messages=[tool_msg], options=options)
                else:
                    continue

                if hasattr(result, "log") and result.log:
                    tool_input_blocked = (
                        role == "tool"
                        and hasattr(result, "response")
                        and result.response
                        and result.response[0].get("content", "").strip() != ""
                    )
                    tool_output_blocked = (
                        role == "assistant"
                        and "tool_calls" in msg
                        and hasattr(result, "response")
                        and result.response
                    )
                    if hasattr(result.log, "activated_rails") and result.log.activated_rails:
                        for rail in result.log.activated_rails:
                            is_blocked = (
                                getattr(rail, "stop", False)
                                or (tool_input_blocked and getattr(rail, "type", "") in ["dialog", "tool_input"])
                                or (tool_output_blocked and getattr(rail, "type", "") == "tool_output")
                            )
                            status = "blocked" if is_blocked else "success"
                            rail_name = getattr(rail, "name", "unknown")
                            if rail_name not in rails_status or status == "blocked":
                                rails_status[rail_name] = {"status": status}
                            message_rails[rail_name] = {"status": status}
                            aggregated_log.activated_rails.append(rail)
                    if hasattr(result.log, "stats") and result.log.stats:
                        new_stats_dict = result.log.stats.model_dump()
                        for field_name, new_value in new_stats_dict.items():
                            if new_value is not None and isinstance(new_value, (int, float)):
                                current_value = getattr(aggregated_log.stats, field_name) or 0
                                setattr(aggregated_log.stats, field_name, current_value + new_value)

                if first_blocked_message is None and hasattr(result, "response") and result.response:
                    content = result.response[0].get("content", "").strip() if isinstance(result.response[0], dict) else ""
                    if content and any(s.get("status") == "blocked" for s in message_rails.values()):
                        first_blocked_message = content

                message_results.append(MessageCheckResult(index=msg_idx, role=role, rails=message_rails))

                if body.stream:
                    yield _json.dumps({
                        "status": _gc_calculate_status(rails_status),
                        "rails_status": rails_status.copy(),
                        "guardrails_data": None,
                    }) + "\n"

            guardrails_data = {
                "log": {
                    "activated_rails": [r.name for r in aggregated_log.activated_rails if r.stop],
                    "stats": aggregated_log.stats.model_dump() if aggregated_log.stats else {},
                }
            }
            final_result = GuardrailCheckResponseBody(
                status=_gc_calculate_status(rails_status),
                rails_status=rails_status,
                messages=message_results,
                guardrails_data=guardrails_data,
                blocked_message=first_blocked_message,
            )
            yield _json.dumps(final_result.model_dump()) + "\n"

        except Exception as ex:
            log.exception(ex)
            yield _json.dumps(_gc_create_error_response("Internal server error.", str(ex)).model_dump()) + "\n"

    if body.stream:
        return _StreamingResponse(process_checks(), media_type="application/x-ndjson")
    else:
        results = []
        async for result in process_checks():
            results.append(result)
        if results:
            return GuardrailCheckResponseBody.model_validate_json(results[-1])
        return _gc_create_error_response("No results generated.")
