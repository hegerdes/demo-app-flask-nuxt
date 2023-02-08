{{/*
Expand the name of the chart.
*/}}
{{- define "flask-frontend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "flask-frontend.fullname" -}}
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
{{- define "flask-frontend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "flask-frontend.labels" -}}
helm.sh/chart: {{ include "flask-frontend.chart" . }}
{{ include "flask-frontend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "flask-frontend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "flask-frontend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Pod annotations
*/}}
{{- define "flask-frontend.pod.annotations" -}}
{{- range $k, $v := .Values.podAnnotations }}
{{- $k }}: {{ $v }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
checksum: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
{{- end }}

{{/*
Service annotations
*/}}
{{- define "flask-frontend.service.annotations" -}}
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
Create the name of the service account to use
*/}}
{{- define "flask-frontend.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "flask-frontend.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
