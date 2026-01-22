# TodoFlow Helm Chart Quickstart Guide

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- `kubectl` configured to connect to your cluster

## Installation

### Add the Repository (Optional)

```bash
# Add the repository (if hosted)
helm repo add todo-app https://repo-url
helm repo update
```

### Install the Chart

```bash
# Install the chart with default values
helm install my-release charts/todo-app

# Install with custom values
helm install my-release charts/todo-app -f values.yaml

# Install with specific values overrides
helm install my-release charts/todo-app --set frontend.replicas=2 --set backend.replicas=2
```

### Verify Installation

```bash
# Check the status of your release
helm status my-release

# List all releases
helm list

# Get all resources created by the release
helm get all my-release
```

## Accessing the Application

### For NodePort Service (Default)

```bash
# Get the service information
kubectl get svc

# Get the external IP of your node (for Minikube)
minikube service my-release-todo-app-frontend --url
```

### For LoadBalancer Service

```bash
# Wait for external IP to be assigned
kubectl get svc --watch

# Once assigned, access the application at http://<EXTERNAL-IP>:<PORT>
```

### For Port Forwarding (Development)

```bash
# Get the pod name
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=todo-app,app.kubernetes.io/instance=my-release" -o jsonpath="{.items[0].metadata.name}")

# Forward the port
kubectl port-forward $POD_NAME 8080:3000
```

## Configuration

### Custom Values File

Create a `custom-values.yaml` file to override default settings:

```yaml
frontend:
  image:
    repository: my-frontend-repo
    tag: v1.2.3
  replicas: 2
  resources:
    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "200m"
      memory: "256Mi"
  service:
    type: NodePort
    port: 3000

backend:
  image:
    repository: my-backend-repo
    tag: v1.2.3
  replicas: 2
  resources:
    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "200m"
      memory: "256Mi"
  service:
    type: ClusterIP
    port: 8000

database:
  url: "postgresql://myuser:mypassword@myhost:5432/mydb"
```

Install with custom values:

```bash
helm install my-release charts/todo-app -f custom-values.yaml
```

## Uninstallation

```bash
# Uninstall the release
helm uninstall my-release

# Verify it's gone
helm status my-release
```

## Troubleshooting

### Common Issues

1. **Images not pulling**
   - Check that image repository and tag are correct
   - Verify image pull secrets if using private registries

2. **Services not accessible**
   - Check service type and ports
   - Verify that pods are running and ready

3. **Health checks failing**
   - Check application logs for startup errors
   - Verify environment variables and configuration

### Useful Commands

```bash
# Check pod status
kubectl get pods

# Check logs of a specific pod
kubectl logs <pod-name>

# Describe a pod for detailed information
kubectl describe pod <pod-name>

# Check service configuration
kubectl get svc
kubectl describe svc <service-name>

# Check deployment status
kubectl get deployments
```

### Debugging Helm Releases

```bash
# Get all information about a release
helm get all my-release

# Rollback to a previous revision
helm rollback my-release 1

# Check the template that would be generated (without installing)
helm template my-release charts/todo-app
```

## Scaling

### Scale Frontend

```bash
# Scale frontend deployment
kubectl scale deployment my-release-todo-app-frontend --replicas=3
```

### Scale Backend

```bash
# Scale backend deployment
kubectl scale deployment my-release-todo-app-backend --replicas=3
```

## Upgrading

```bash
# Upgrade with new values
helm upgrade my-release charts/todo-app -f new-values.yaml

# Upgrade with specific parameter
helm upgrade my-release charts/todo-app --set frontend.image.tag=v1.2.3

# Check history of releases
helm history my-release

# Rollback to a specific revision
helm rollback my-release 2
```

## Monitoring

### Check Pod Health

```bash
# Check if all pods are ready
kubectl get pods

# Check health of deployments
kubectl get deployments

# Check service endpoints
kubectl get endpoints
```

### Check Resource Utilization

```bash
# Get resource usage
kubectl top pods

# Get resource usage for a specific pod
kubectl top pod <pod-name>
```

## Security Considerations

- Store sensitive data in Kubernetes Secrets, not ConfigMaps
- Use appropriate resource limits to prevent resource exhaustion
- Regularly update base images to patch security vulnerabilities
- Use least-privileged principle for service accounts