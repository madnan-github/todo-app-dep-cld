# Skill: Helm Chart Scaffolding

## Purpose
Generate complete Helm chart directory structure with templates and values.

## Input Parameters
- chart_name: "taskflow"
- chart_version: "0.1.0"
- app_version: "0.1.0"
- services: ["frontend", "backend"]

## Output
Complete Helm chart directory with all necessary files.

## Directory Structure Created
```
helm/taskflow/
├── Chart.yaml
├── values.yaml
├── values-local.yaml
├── values-cloud.yaml
└── templates/
    ├── _helpers.tpl
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── configmap.yaml
    ├── secret.yaml
    └── NOTES.txt
```

## File Templates

### Chart.yaml
```yaml
apiVersion: v2
name: taskflow
description: AI-powered todo application with chatbot
type: application
version: 0.1.0
appVersion: "0.1.0"
keywords:
  - todo
  - chatbot
  - ai
  - kubernetes
maintainers:
  - name: Your Name
    email: your.email@example.com
```

### values.yaml
```yaml
global:
  environment: local
  imageRegistry: ""
  imagePullPolicy: IfNotPresent

frontend:
  enabled: true
  image:
    repository: taskflow-frontend
    tag: "0.1.0"
  replicas: 2
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"
  service:
    type: NodePort
    port: 3000
    nodePort: 30001
  env:
    NEXT_PUBLIC_API_URL: "http://localhost:8000"

backend:
  enabled: true
  image:
    repository: taskflow-backend
    tag: "0.1.0"
  replicas: 2
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "250m"
  service:
    type: ClusterIP
    port: 8000
  env:
    DATABASE_URL: ""  # From secret
    OPENROUTER_API_KEY: ""  # From secret
    BETTER_AUTH_SECRET: ""  # From secret

database:
  external: true
  host: "ep-xxx.neon.tech"
  port: 5432
  name: "taskflow"
```

### templates/_helpers.tpl
```yaml
{{- define "taskflow.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "taskflow.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "taskflow.labels" -}}
helm.sh/chart: {{ include "taskflow.chart" . }}
{{ include "taskflow.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "taskflow.selectorLabels" -}}
app.kubernetes.io/name: {{ include "taskflow.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## Usage Example
Input: chart_name="taskflow", services=["frontend", "backend"]
Output: Complete helm/taskflow/ directory structure