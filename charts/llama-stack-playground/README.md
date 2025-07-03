# Llama Stack Playground

A Helm chart for deploying the Llama Stack Playground UI on Kubernetes/OpenShift.

## Description

This chart deploys a Streamlit-based web interface for interacting with Llama Stack, providing a user-friendly playground for chat, agents, and tools functionality.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- A running Llama Stack instance

## Installation

### Add the repository

```bash
helm repo add genaiops https://rhoai-genaiops.github.io/genaiops-helmcharts
helm repo update
```

### Install the chart

```bash
helm install llama-stack-playground genaiops/llama-stack-playground
```

### Install with custom values

```bash
helm install llama-stack-playground genaiops/llama-stack-playground -f values.yaml
```

## Configuration

The following table lists the configurable parameters and their default values:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Container image repository | `quay.io/rhoai-genaiops/llama-stack-playground` |
| `image.tag` | Container image tag | `0.2.11` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `80` |
| `service.targetPort` | Container port | `8501` |
| `route.enabled` | Enable OpenShift route | `true` |
| `route.tls.enabled` | Enable TLS for route | `true` |
| `ingress.enabled` | Enable ingress | `false` |
| `resources.limits.memory` | Memory limit | `1Gi` |
| `resources.requests.cpu` | CPU request | `500m` |
| `resources.requests.memory` | Memory request | `512Mi` |
| `playground.llamaStackUrl` | Llama Stack backend URL | `http://llama-stack` |
| `playground.defaultModel` | Default model to use | `meta-llama/Llama-3.2-3B-Instruct` |
| `playground.enableChat` | Enable chat functionality | `true` |
| `playground.enableAgents` | Enable agents functionality | `true` |
| `playground.enableTools` | Enable tools functionality | `true` |
| `networkPolicy.enabled` | Enable network policies | `true` |
| `autoscaling.enabled` | Enable HPA | `false` |
| `podDisruptionBudget.enabled` | Enable PDB | `false` |

## Examples

### Basic installation

```bash
helm install my-playground genaiops/llama-stack-playground
```

### With custom Llama Stack URL

```bash
helm install my-playground genaiops/llama-stack-playground \
  --set playground.llamaStackUrl=http://my-llama-stack:8000
```

### With custom resources

```bash
helm install my-playground genaiops/llama-stack-playground \
  --set resources.requests.cpu=1000m \
  --set resources.requests.memory=2Gi \
  --set resources.limits.memory=4Gi
```

### With ingress instead of route

```bash
helm install my-playground genaiops/llama-stack-playground \
  --set route.enabled=false \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=playground.example.com
```

## Uninstalling

```bash
helm uninstall llama-stack-playground
```

## Security

This chart includes several security features:

- Non-root container execution
- Read-only root filesystem (configurable)
- Network policies for traffic control
- Security contexts with dropped capabilities
- OpenShift-compatible security constraints

## Monitoring

The chart includes liveness and readiness probes configured for the Streamlit application:

- **Liveness probe**: HTTP GET on `/` with 30s initial delay
- **Readiness probe**: HTTP GET on `/` with 5s initial delay

## Troubleshooting

### Common issues

1. **Pod not starting**: Check if the Llama Stack backend is accessible
2. **Network connectivity**: Ensure network policies allow traffic to Llama Stack
3. **Resource constraints**: Verify resource limits are appropriate for your cluster

### Debugging

```bash
# Check pod logs
kubectl logs -f deployment/llama-stack-playground

# Check service endpoints
kubectl get endpoints llama-stack-playground

# Test connectivity to Llama Stack
kubectl exec -it deployment/llama-stack-playground -- curl http://llama-stack
```

## Support

For issues and questions:

- GitHub Issues: https://github.com/rhoai-genaiops/genaiops-helmcharts/issues
- Documentation: https://docs.company.com/llama-stack-playground

## License

This project is licensed under the Apache License 2.0.