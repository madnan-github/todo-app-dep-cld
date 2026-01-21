# Quickstart Guide: Helm Chart Packaging

**Feature**: Helm Chart Packaging (007-helm-chart-packaging)
**Date**: 2026-01-22
**Status**: Complete

## Overview

This guide provides a quick introduction to using the Helm charts for the TodoFlow application. It covers installation, configuration, and basic operations.

## Prerequisites

- Kubernetes cluster (v1.20+)
- Helm 3 installed
- Docker images for frontend and backend services built and accessible
- kubectl configured to connect to your Kubernetes cluster

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Navigate to Charts Directory
```bash
cd charts/todo-app
```

### 3. Install the Chart
```bash
# Install with default values
helm install todo-app .

# Install with custom values
helm install todo-app . -f custom-values.yaml

# Install in specific namespace
helm install todo-app . --namespace todo-app --create-namespace
```

### 4. Verify Installation
```bash
# Check release status
helm status todo-app

# List pods
kubectl get pods

# Check services
kubectl get services
```

## Configuration

### Default Configuration
The chart comes with sensible defaults for local development:

```yaml
frontend:
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  replicaCount: 1
  service:
    type: ClusterIP
    port: 3000
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"

backend:
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  replicaCount: 1
  service:
    type: ClusterIP
    port: 8000
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
```

### Custom Configuration
Create a custom values file to override defaults:

```yaml
# custom-values.yaml
frontend:
  replicaCount: 3
  image:
    tag: v1.2.0
  resources:
    limits:
      memory: "512Mi"
      cpu: "500m"

backend:
  replicaCount: 2
  image:
    tag: v1.2.0
  resources:
    limits:
      memory: "1Gi"
      cpu: "1000m"

database:
  url: "postgresql://user:pass@external-db:5432/todo"
```

## Common Operations

### Upgrade
```bash
# Upgrade with new values
helm upgrade todo-app . -f custom-values.yaml

# Upgrade to new chart version
helm upgrade todo-app . --version 1.2.0
```

### Uninstall
```bash
# Uninstall the release
helm uninstall todo-app
```

### Rollback
```bash
# List revisions
helm history todo-app

# Rollback to previous revision
helm rollback todo-app 1
```

## Local Development

### Using Minikube
```bash
# Start minikube
minikube start

# Install chart
helm install todo-app . --wait

# Access services
minikube service todo-app-frontend --url
minikube service todo-app-backend --url
```

### Using Kind (Kubernetes in Docker)
```bash
# Create kind cluster
kind create cluster

# Install chart
helm install todo-app . --wait

# Port forward for local access
kubectl port-forward svc/todo-app-frontend 3000:3000
kubectl port-forward svc/todo-app-backend 8000:8000
```

## Troubleshooting

### Check Release Status
```bash
helm status todo-app
```

### View Chart Information
```bash
# Show chart information
helm show chart .

# Show default values
helm show values .
```

### Debug Installation
```bash
# Dry run (don't actually install)
helm install todo-app . --dry-run --debug

# Template only (show generated manifests)
helm template todo-app .
```

### Common Issues
- **Image pull errors**: Ensure your container images are accessible from the Kubernetes cluster
- **Resource limit errors**: Adjust resource requests/limits in values.yaml based on cluster capacity
- **Service access**: Use `kubectl port-forward` or Ingress to access services from outside the cluster

## Advanced Configuration

### Environment-Specific Values
Create separate values files for different environments:

```bash
# Development
helm install todo-app . -f values-dev.yaml

# Staging
helm install todo-app . -f values-staging.yaml

# Production
helm install todo-app . -f values-prod.yaml
```

### Secrets Management
Sensitive information should be stored in Kubernetes Secrets:

```yaml
# In your values file
backend:
  env:
    DATABASE_URL: "postgresql://user:{{ .Values.secrets.dbPassword }}@db:5432/todo"
```

Then provide the secret separately or use a secrets management solution like Sealed Secrets or HashiCorp Vault.

## Verification

### Post-Installation Checks
After installation, verify the following:

1. All pods are running:
   ```bash
   kubectl get pods
   ```

2. Services are available:
   ```bash
   kubectl get services
   ```

3. Applications are responding:
   ```bash
   kubectl logs -l app=todo-app-frontend
   kubectl logs -l app=todo-app-backend
   ```

4. Health endpoints are accessible:
   ```bash
   # Access through port forwarding
   kubectl port-forward svc/todo-app-backend 8000:8000 &
   curl http://localhost:8000/api/health
   ```