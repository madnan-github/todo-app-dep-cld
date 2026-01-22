# Data Model: Local Kubernetes Deployment

## Overview
This document describes the Kubernetes resource configurations for the TodoFlow application deployment to Minikube.

## Kubernetes Resources

### 1. Deployment Resources

#### Frontend Deployment
- **Name**: `todo-frontend`
- **Replicas**: 1 (configurable)
- **Image**: `todo-frontend:{tag}` (configurable)
- **Ports**: 3000
- **Environment Variables**:
  - `NEXT_PUBLIC_API_URL`: Backend API URL
  - `NODE_ENV`: Environment setting
- **Resources**:
  - Requests: 100m CPU, 128Mi memory
  - Limits: 500m CPU, 512Mi memory
- **Health Checks**:
  - Liveness probe: `/api/health`
  - Readiness probe: `/api/health`

#### Backend Deployment
- **Name**: `todo-backend`
- **Replicas**: 1 (configurable)
- **Image**: `todo-backend:{tag}` (configurable)
- **Ports**: 8000
- **Environment Variables**:
  - `DATABASE_URL`: Database connection string
  - `API_HOST`: Host binding (0.0.0.0)
  - `API_PORT`: Port binding (8000)
  - `CORS_ORIGINS`: Allowed origins
  - `DEBUG`: Debug mode flag
  - `ENVIRONMENT`: Environment setting
- **Resources**:
  - Requests: 100m CPU, 128Mi memory
  - Limits: 500m CPU, 512Mi memory
- **Health Checks**:
  - Liveness probe: `/api/health`
  - Readiness probe: `/api/health`

### 2. Service Resources

#### Frontend Service
- **Name**: `todo-frontend-service`
- **Type**: NodePort (for local access)
- **Port**: 3000
- **Target Port**: 3000
- **NodePort**: Dynamically assigned or configured

#### Backend Service
- **Name**: `todo-backend-service`
- **Type**: ClusterIP (internal access)
- **Port**: 8000
- **Target Port**: 8000

### 3. Configuration Resources

#### ConfigMap
- **Name**: `todo-app-config`
- **Data**:
  - `NEXT_PUBLIC_API_URL`: API URL for frontend-backend communication
  - `API_HOST`: Backend host configuration
  - `API_PORT`: Backend port configuration
  - `CORS_ORIGINS`: Cross-origin resource sharing settings
  - `DEBUG`: Debug mode setting
  - `ENVIRONMENT`: Environment configuration

#### Secret
- **Name**: `todo-app-secret`
- **Data**:
  - `DATABASE_URL`: Encrypted database connection string
  - `JWT_SECRET_KEY`: Encryption key for JWT tokens
  - `JWT_ALGORITHM`: Algorithm for JWT signing

### 4. Namespace (Optional)
- **Name**: `todo-app` (configurable)
- **Purpose**: Isolate application resources

## Relationships

- Frontend deployment connects to backend service via internal DNS
- Backend deployment connects to database using credentials from secret
- Both deployments reference the configmap for configuration
- Services expose deployments to internal/external traffic as appropriate

## Validation Rules

- All deployments must have resource limits defined
- All deployments must have health checks configured
- Secrets must not be stored in plain text
- Environment-specific configurations must be customizable via values
- Service types must match deployment requirements (NodePort for external access)

## State Transitions

- Deployments transition from `Pending` to `Running` when healthy
- Pods transition through `ContainerCreating` to `Running` to `Terminating`
- Services remain `Active` while associated pods are available