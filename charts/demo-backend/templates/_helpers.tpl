{{/*
Expand the name of the chart.
*/}}
{{- define "demo-backend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "demo-backend.fullname" -}}
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
{{- define "demo-backend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "demo-backend.labels" -}}
helm.sh/chart: {{ include "demo-backend.chart" . }}
{{ include "demo-backend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Pod annotations
*/}}
{{- define "demo-backend.pod.annotations" -}}
{{- range $k, $v := .Values.podAnnotations }}
{{- $k }}: {{ $v }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
checksum: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
{{- end }}

{{/*
Service annotations
*/}}
{{- define "demo-backend.service.annotations" -}}
prometheus/scrape: {{ .Values.service.prometheus.enabled | quote }}
{{- range $k, $v := .Values.service.annotations }}
{{- $k }}: {{ $v }}
{{- end }}
{{- if .Values.service.prometheus.enabled }}
prometheus/scheme: {{ .Values.service.prometheus.scheme | quote}}
prometheus/path: {{ .Values.service.prometheus.path | quote}}
prometheus/port: {{ .Values.service.prometheus.port | quote}}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "demo-backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "demo-backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "demo-backend.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "demo-backend.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
