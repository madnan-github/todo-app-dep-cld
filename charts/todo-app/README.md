# TodoFlow Helm Chart

A Helm chart for deploying the TodoFlow application, which consists of a Next.js frontend and a FastAPI backend.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installation

```bash
# Add the repository (if hosted)
helm repo add todo-app https://repo-url

# Install the chart
helm install my-release charts/todo-app
```

## Uninstallation

```bash
# Uninstall the release
helm uninstall my-release
```

## Configuration

The following table lists the configurable parameters of the TodoFlow chart and their default values.

### Global Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.imageRegistry` | Global image registry to use | `""` |
| `global.environment` | Global environment setting | `"development"` |
| `global.ingress.enabled` | Enable ingress resource | `false` |
| `global.ingress.className` | Ingress class name | `"nginx"` |
| `global.ingress.hosts[].host` | Hostname for the ingress | `"chart-example.local"` |
| `global.ingress.hosts[].paths[].path` | Path for the ingress | `"/"` |
| `global.ingress.hosts[].paths[].pathType` | Path type for the ingress | `"ImplementationSpecific"` |

### Frontend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.image.repository` | Frontend image repository | `"todo-frontend"` |
| `frontend.image.tag` | Frontend image tag | `"latest"` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `"IfNotPresent"` |
| `frontend.replicas` | Number of frontend replicas | `1` |
| `frontend.service.type` | Frontend service type | `"ClusterIP"` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.healthPath` | Frontend health check path | `"/api/health"` |
| `frontend.resources.limits.cpu` | CPU limit for frontend | `"500m"` |
| `frontend.resources.limits.memory` | Memory limit for frontend | `"512Mi"` |
| `frontend.resources.requests.cpu` | CPU request for frontend | `"100m"` |
| `frontend.resources.requests.memory` | Memory request for frontend | `"128Mi"` |

### Backend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.image.repository` | Backend image repository | `"todo-backend"` |
| `backend.image.tag` | Backend image tag | `"latest"` |
| `backend.image.pullPolicy` | Backend image pull policy | `"IfNotPresent"` |
| `backend.replicas` | Number of backend replicas | `1` |
| `backend.service.type` | Backend service type | `"ClusterIP"` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.healthPath` | Backend health check path | `"/api/health"` |
| `backend.cors.origins` | Allowed CORS origins | `"http://localhost:3000"` |
| `backend.debug` | Enable debug mode | `"false"` |
| `backend.api.url` | Backend API URL | `""` |
| `backend.resources.limits.cpu` | CPU limit for backend | `"500m"` |
| `backend.resources.limits.memory` | Memory limit for backend | `"512Mi"` |
| `backend.resources.requests.cpu` | CPU request for backend | `"100m"` |
| `backend.resources.requests.memory` | Memory request for backend | `"128Mi"` |

### Database Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `database.url` | Database connection URL | `"postgresql://todo_user:todo_password@postgres:5432/todo_app"` |

### Common Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `nameOverride` | Override the name of the chart | `""` |
| `fullnameOverride` | Override the fully qualified app name | `""` |
| `serviceAccount.create` | Specifies whether a service account should be created | `false` |
| `serviceAccount.name` | Name of the service account to use | `""` (generated using fullname template) |
| `podAnnotations` | Annotations for pods | `{}` |
| `podSecurityContext` | Security context for pods | `{}` |
| `securityContext` | Security context for containers | `{}` |

## Example Values

Here's an example `values.yaml` file for a production deployment:

```yaml
global:
  environment: "production"
  ingress:
    enabled: true
    className: "nginx"
    hosts:
      - host: "todo.example.com"
        paths:
          - path: "/"
            pathType: "Prefix"

frontend:
  image:
    tag: "v1.0.0"
  replicas: 3
  resources:
    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "200m"
      memory: "256Mi"

backend:
  image:
    tag: "v1.0.0"
  replicas: 2
  resources:
    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "200m"
      memory: "256Mi"

database:
  url: "postgresql://prod-user:prod-password@prod-db:5432/prod-todo"
```

## Testing the Chart

Run the following command to execute the chart's tests:

```bash
helm install test-release charts/todo-app
helm test test-release
```

## Chart Structure

```
charts/todo-app/
├── Chart.yaml
├── values.yaml
├── README.md
├── templates/
│   ├── _helpers.tpl
│   ├── NOTES.txt
│   ├── frontend-deployment.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── backend-service.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── ingress.yaml
│   └── tests/
│       ├── test-frontend-deployment.yaml
│       └── test-backend-deployment.yaml
└── .helmignore
```

## Maintainers

- TodoFlow Team (team@todo-flow.com)

## License

Apache 2.0