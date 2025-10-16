# Canopy Tekton Pipeline Helm Chart

A Helm chart for deploying Canopy LLM testing pipeline using Tekton and Kubeflow.

## Overview

This chart deploys:
- Tekton Pipeline for orchestrating test execution
- Tekton Task for running Kubeflow Pipelines
- Git webhook triggers for automatic pipeline execution
- PVC for shared workspace storage

## Prerequisites

- OpenShift/Kubernetes cluster with Tekton Pipelines installed
- Kubeflow Pipelines (Data Science Pipelines) available
- GitHub webhook access for automatic triggering

## Installation

```bash
helm install canopy-pipeline ./canopy-tekton-pipeline
```

## Configuration

The following table lists the configurable parameters and their default values.

### Git Configuration
| Parameter | Description | Default |
|-----------|-------------|---------|
| `git.url` | Git repository URL | `https://github.com/rhoai-genaiops/canopy-prompts` |
| `git.revision` | Git branch/revision | `main` |

### Kubeflow Pipeline Configuration
| Parameter | Description | Default |
|-----------|-------------|---------|
| `kfp.baseUrl` | LlamaStack base URL | `http://llama-stack.genaiops-rag.svc.cluster.local:80` |
| `kfp.backendUrl` | Canopy backend URL | `https://canopy-backend-user1-canopy.apps...` |

### Storage Configuration
| Parameter | Description | Default |
|-----------|-------------|---------|
| `pvc.name` | PVC name | `canopy-workspace-pvc` |
| `pvc.size` | PVC size | `1Gi` |
| `pvc.storageClass` | Storage class | `ocs-storagecluster-cephfs` |

### Secrets Configuration
| Parameter | Description | Default |
|-----------|-------------|---------|
| `secrets.github.name` | GitHub webhook secret name | `github-secret` |
| `secrets.s3.name` | S3 credentials secret name | `test-results` |

## Required Secrets

### GitHub Webhook Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: github-secret
type: Opaque
data:
  secretToken: <base64-encoded-webhook-token>
```

### S3 Credentials Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-results
type: Opaque
data:
  AWS_ACCESS_KEY_ID: <base64-encoded-access-key>
  AWS_SECRET_ACCESS_KEY: <base64-encoded-secret-key>
  AWS_S3_ENDPOINT: <base64-encoded-s3-endpoint>
  AWS_S3_BUCKET: <base64-encoded-bucket-name>
  AWS_DEFAULT_REGION: <base64-encoded-region>
```

## Usage

1. Deploy the chart with appropriate values
2. Configure GitHub webhook to point to the EventListener URL
3. Push changes to the monitored branch to trigger pipeline execution

### Get EventListener URL
```bash
kubectl get eventlistener canopy-test-event-listener -o jsonpath='{.status.address.url}'
```

## Architecture

The pipeline follows this flow:
1. **Git Webhook** → Triggers on push to main branch
2. **Tekton Pipeline** → Clones repository and runs KFP
3. **Kubeflow Pipeline** → Executes LLM tests and uploads results to S3

## Dependencies

- The KFP pipeline file (`kfp_pipeline_simple.py`) should be present in the `test_pipeline/` directory of the cloned repository
- OpenShift Pipelines (Tekton) operator
- Red Hat OpenShift Data Science / Open Data Hub with Kubeflow Pipelines