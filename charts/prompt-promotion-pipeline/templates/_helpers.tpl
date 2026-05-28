{{/*
Expand the name of the chart.
*/}}
{{- define "prompt-promotion-pipeline.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "prompt-promotion-pipeline.fullname" -}}
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
{{- define "prompt-promotion-pipeline.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "prompt-promotion-pipeline.labels" -}}
helm.sh/chart: {{ include "prompt-promotion-pipeline.chart" . }}
{{ include "prompt-promotion-pipeline.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app: prompt-promotion-pipeline
component: gitops
{{- end }}

{{/*
Selector labels
*/}}
{{- define "prompt-promotion-pipeline.selectorLabels" -}}
app.kubernetes.io/name: {{ include "prompt-promotion-pipeline.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Common annotations
*/}}
{{- define "prompt-promotion-pipeline.annotations" -}}
description: "Prompt promotion pipeline - updates production config via GitOps"
{{- end }}
