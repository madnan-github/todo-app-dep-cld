# Skill: Kubernetes Manifest Generator

## Purpose
Generate Kubernetes YAML manifests for Deployments, Services, ConfigMaps, and Secrets.

## Input Parameters
- resource_type: "deployment" | "service" | "configmap" | "secret"
- service_name: "frontend" | "backend"
- values: Configuration from values.yaml

## Output
Templated Kubernetes manifest following best practices.

## Templates

### Deployment Template
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "taskflow.fullname" . }}-{{ .Values.serviceName }}
  labels:
    {{- include "taskflow.labels" . | nindent 4 }}
    app.kubernetes.io/component: {{ .Values.serviceName }}
spec:
  replicas: {{ .Values[.Values.serviceName].replicas }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      {{- include "taskflow.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: {{ .Values.serviceName }}
  template:
    metadata:
      labels:
        {{- include "taskflow.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: {{ .Values.serviceName }}
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001
      containers:
      - name: {{ .Values.serviceName }}
        image: "{{ .Values.global.imageRegistry }}{{ .Values[.Values.serviceName].image.repository }}:{{ .Values[.Values.serviceName].image.tag }}"
        imagePullPolicy: {{ .Values.global.imagePullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values[.Values.serviceName].service.port }}
          protocol: TCP
        livenessProbe:
          httpGet:
            path: {{ if eq .Values.serviceName "backend" }}/api/health{{ else }}/health{{ end }}
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: {{ if eq .Values.serviceName "backend" }}/api/health{{ else }}/health{{ end }}
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        resources:
          {{- toYaml .Values[.Values.serviceName].resources | nindent 10 }}
        env:
        {{- if eq .Values.serviceName "frontend" }}
        - name: NEXT_PUBLIC_API_URL
          value: {{ .Values.frontend.env.NEXT_PUBLIC_API_URL | quote }}
        {{- else }}
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{ include "taskflow.fullname" . }}-secrets
              key: database-url
        - name: OPENROUTER_API_KEY
          valueFrom:
            secretKeyRef:
              name: {{ include "taskflow.fullname" . }}-secrets
              key: openrouter-api-key
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: {{ include "taskflow.fullname" . }}-secrets
              key: better-auth-secret
        {{- end }}
```

### Service Template
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "taskflow.fullname" . }}-{{ .Values.serviceName }}
  labels:
    {{- include "taskflow.labels" . | nindent 4 }}
    app.kubernetes.io/component: {{ .Values.serviceName }}
spec:
  type: {{ .Values[.Values.serviceName].service.type }}
  ports:
  - port: {{ .Values[.Values.serviceName].
  service.port }}
targetPort: http
protocol: TCP
name: http
{{- if and (eq .Values[.Values.serviceName].service.type "NodePort") .Values[.Values.serviceName].service.nodePort }}
nodePort: {{ .Values[.Values.serviceName].service.nodePort }}
{{- end }}
selector:
{{- include "taskflow.selectorLabels" . | nindent 4 }}
app.kubernetes.io/component: {{ .Values.serviceName }}
### Secret Template
````yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "taskflow.fullname" . }}-secrets
  labels:
    {{- include "taskflow.labels" . | nindent 4 }}
type: Opaque
data:
  database-url: {{ .Values.backend.env.DATABASE_URL | b64enc | quote }}
  openrouter-api-key: {{ .Values.backend.env.OPENROUTER_API_KEY | b64enc | quote }}
  better-auth-secret: {{ .Values.backend.env.BETTER_AUTH_SECRET | b64enc | quote }}
````

## Usage Example
Input: resource_type="deployment", service_name="frontend"
Output: Complete frontend-deployment.yaml template