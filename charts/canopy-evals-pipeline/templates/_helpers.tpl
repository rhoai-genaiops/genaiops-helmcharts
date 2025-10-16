{{/*
Expand the name of the chart.
*/}}
{{- define "canopy-tekton-pipeline.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "canopy-tekton-pipeline.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "canopy-tekton-pipeline.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "canopy-tekton-pipeline.labels" -}}
helm.sh/chart: {{ include "canopy-tekton-pipeline.chart" . }}
{{ include "canopy-tekton-pipeline.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app: canopy-tekton-pipeline
component: testing
{{- end }}

{{/*
Selector labels
*/}}
{{- define "canopy-tekton-pipeline.selectorLabels" -}}
app.kubernetes.io/name: {{ include "canopy-tekton-pipeline.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Common annotations
*/}}
{{- define "canopy-tekton-pipeline.annotations" -}}
description: "Canopy LLM testing pipeline using Tekton and Kubeflow"
{{- end }}