# Llama Stack Operator Instance Helm Chart

A Helm chart for creating and managing Llama Stack Operator instances on OpenShift with support for AI model inference, agents, and tool runtime.

## Description

This Helm chart creates LlamaStackDistribution custom resources to deploy Llama Stack instances via the Llama Stack Operator. It supports various AI workflows including:
- Model inference via remote VLLM endpoints
- AI agents with persistence
- Tool runtime with Model Context Protocol (MCP) support
- OpenTelemetry observability integration

## Installation

### Quick Start

```bash
helm install my-llama-instance ./llama-stack-operator-instance
```

### Custom Installation

```bash
helm install my-llama-instance ./llama-stack-operator-instance \
  --set MODEL_NAME=llama32 \
  --set MODEL_URL=http://your-model-endpoint:8080/v1 \
  --set otelCollector.enabled=true
```

## Configuration

The following table lists the configurable parameters and their default values:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `MODEL_NAME` | Name of the model to use | `llama32` |
| `MODEL_URL` | URL of the remote VLLM model endpoint | `http://llama-32-predictor.ai501.svc.cluster.local:8080/v1` |
| `configMap.enabled` | Enable ConfigMap creation | `true` |
| `otelCollector.enabled` | Enable OpenTelemetry collector integration | `false` |
| `rag.enabled` | Enable RAG capabilities | `false` |
| `mcp.enabled` | Enable Model Context Protocol support | `false` |
| `eval.enabled` | Enable evaluation capabilities | `false` |