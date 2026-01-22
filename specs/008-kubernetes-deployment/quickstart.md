# Quickstart Guide: Local Kubernetes Deployment

## Overview
This guide provides step-by-step instructions to deploy the TodoFlow application to Minikube using Helm charts.

## Prerequisites

- **Minikube**: v1.20 or higher
- **Helm**: v3.0 or higher
- **kubectl**: Matching your Kubernetes version
- **Docker**: Required for Minikube

## Setup Instructions

### 1. Start Minikube
```bash
minikube start
```

### 2. Verify Minikube Status
```bash
minikube status
kubectl cluster-info
```

### 3. Build and Load Images (if using local images)
```bash
# Build your frontend and backend images
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend

# Load images into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 4. Navigate to Helm Chart Directory
```bash
cd charts/todo-app
```

### 5. Install the Helm Chart
```bash
helm install todo-app ./
```

### 6. Verify Installation
```bash
# Check all pods are running
kubectl get pods

# Check services are available
kubectl get services

# Check deployments are ready
kubectl get deployments
```

## Access the Application

### Get the Frontend URL
```bash
minikube service todo-app-frontend --url
```

Or use the convenient command:
```bash
minikube service todo-app-frontend
```
This will open the application in your default browser.

## Configuration

### Custom Values
Create a `custom-values.yaml` file to override default settings:
```yaml
frontend:
  image:
    tag: "1.2.3"  # Use specific image tag
  replicas: 2     # Increase replicas
  resources:
    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "200m"
      memory: "256Mi"

backend:
  image:
    tag: "1.2.3"  # Use specific image tag
  replicas: 2     # Increase replicas

global:
  environment: "staging"
```

Install with custom values:
```bash
helm install todo-app ./ -f custom-values.yaml
```

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods -o wide
kubectl describe pod <pod-name>
```

### Check Logs
```bash
kubectl logs -l app=frontend
kubectl logs -l app=backend
```

### Check Service Status
```bash
kubectl get svc
kubectl describe svc todo-app-frontend
```

### Helm Commands
```bash
# List releases
helm list

# Upgrade release
helm upgrade todo-app ./

# Uninstall release
helm uninstall todo-app
```

## Cleanup

### Uninstall the Release
```bash
helm uninstall todo-app
```

### Stop Minikube
```bash
minikube stop
```

### Delete Minikube Cluster (optional)
```bash
minikube delete
```

## Verification Steps

After installation, verify all acceptance criteria are met:

1. All pods reach Running state within 2 minutes:
   ```bash
   kubectl get pods --watch
   ```

2. Liveness and readiness probes are passing:
   ```bash
   kubectl get pods -o json | jq '.items[].status.containerStatuses[].ready'
   ```

3. Frontend can communicate with backend:
   ```bash
   kubectl exec -it deployment/todo-app-frontend -- curl http://todo-app-backend:8000/api/health
   ```

4. Application is accessible via NodePort service:
   ```bash
   minikube service todo-app-frontend
   ```

## Common Issues and Solutions

- **Images not found**: Ensure images are loaded with `minikube image load`
- **Service not accessible**: Check NodePort allocation with `kubectl get svc`
- **Pods stuck in Pending**: Check resource limits and available Minikube resources
- **Health checks failing**: Check application logs for startup errors