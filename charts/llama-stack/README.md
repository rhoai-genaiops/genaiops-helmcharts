# Llama Stack Helm Chart

A Helm chart for deploying Llama Stack server on Kubernetes with support for AI model inference, agents, and tool runtime.

## Description

This Helm chart deploys the Llama Stack distribution with remote VLLM inference capabilities. It supports various AI workflows including:
- Model inference via remote VLLM endpoints
- AI agents with persistence
- Tool runtime with Model Context Protocol (MCP) support
- OpenTelemetry observability integration
- RAG (Retrieval-Augmented Generation) capabilities

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- A running VLLM model server endpoint

## Installation

### Quick Start

```bash
helm install llama-stack ./llama-stack
```

### Custom Installation

```bash
helm install llama-stack ./llama-stack \
  --set MODEL_NAME=llama32-full \
  --set MODEL_URL=https://your-model-endpoint.com \
  --set otelCollector.enabled=true
```

## Configuration

The following table lists the configurable parameters and their default values:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `MODEL_NAME` | Name of the model to use | `llama32-full` |
| `MODEL_URL` | URL of the remote VLLM model endpoint | `https://llama32-ai501.apps.cluster-gm86c.gm86c.sandbox1062.opentlc.com` |
| `configMap.enabled` | Enable ConfigMap creation | `true` |
| `otelCollector.enabled` | Enable OpenTelemetry collector integration | `false` |
| `rag.enabled` | Enable RAG capabilities with Milvus | `false` |
| `mcp.enabled` | Enable Model Context Protocol support | `false` |

## Features

### Core Components

- **Llama Stack Server**: Main application container running the distribution
- **ConfigMap**: Configuration for the Llama Stack runtime
- **PVC**: Persistent storage for model data and cache
- **Service**: ClusterIP service exposing the application on port 80

### Optional Features

#### OpenTelemetry Integration
Enable observability with OpenTelemetry traces and metrics:
```yaml
otelCollector:
  enabled: true
```

#### RAG Support
Enable Retrieval-Augmented Generation with Milvus vector database:
```yaml
rag:
  enabled: true
```

#### Model Context Protocol (MCP)
Enable MCP for enhanced tool runtime capabilities:
```yaml
mcp:
  enabled: true
```

## Environment Variables

The deployment sets the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MAX_TOKENS` | Maximum tokens for responses | `128000` |
| `VLLM_MAX_TOKENS` | Maximum tokens for VLLM | `128000` |
| `MODEL_NAME` | Model name from values | From `MODEL_NAME` |
| `MODEL_URL` | Model URL from values | From `MODEL_URL` |
| `LLAMA_STACK_LOG` | Log level | `debug` |
| `LLAMA_STACK_PORT` | Server port | `8321` |

## Volumes

- **run-config-volume**: ConfigMap volume for runtime configuration
- **llama-persist**: PVC for persistent data storage
- **cache**: EmptyDir for temporary cache
- **pythain**: EmptyDir for Python NLP data

## Ports

- **8321**: Main application port (mapped to service port 80)

## Upgrading

To upgrade the chart:

```bash
helm upgrade llama-stack ./llama-stack
```

## Uninstalling

To uninstall the chart:

```bash
helm uninstall llama-stack
```

## Troubleshooting

### Common Issues

1. **Pod not starting**: Check if the MODEL_URL is accessible
2. **Configuration errors**: Verify the ConfigMap is properly mounted
3. **Storage issues**: Ensure PVC is bound correctly

### Logs

Check application logs:
```bash
kubectl logs deployment/llama-stack
```

## Support

For issues and support:
- Chart Repository: https://github.com/company/llama-stack-mcp-server
- Documentation: https://docs.company.com/llama-stack
- Support: https://support.company.com

## License

This chart is licensed under the same terms as the Llama Stack project.