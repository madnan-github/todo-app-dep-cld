# Health Check Endpoints Documentation

This document describes the health check endpoints implemented for both the frontend and backend services as part of the Docker containerization feature.

## Overview

Health check endpoints are essential for containerized environments, particularly for Kubernetes deployments. They allow orchestration platforms to monitor service availability and readiness, enabling proper load balancing and automatic recovery from failures.

## Backend Health Endpoints

### Primary Health Check
- **Endpoint**: `GET /api/health`
- **Purpose**: Kubernetes liveness and readiness probe
- **Response Format**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-01-20T13:05:35.388463Z",
    "service": "backend",
    "version": "1.0.0",
    "database": "connected",
    "environment": "development"
  }
  ```
- **Status Codes**:
  - `200 OK`: Service is operational and healthy
  - `503 Service Unavailable`: Service is unhealthy (database connectivity issues)

### Legacy Health Check
- **Endpoint**: `GET /health`
- **Purpose**: Backward compatibility and alternative health check
- **Response Format**:
  ```json
  {
    "status": "ok",
    "database": "connected",
    "environment": "development"
  }
  ```

## Frontend Health Endpoints

### Health Check
- **Endpoint**: `GET /api/health`
- **Purpose**: Kubernetes liveness and readiness probe
- **Response Format**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-01-20T13:14:27.434Z",
    "service": "frontend",
    "version": "0.1.0",
    "environment": "production"
  }
  ```
- **Status Codes**:
  - `200 OK`: Service is operational and healthy

## Container Integration

### Health Check Configuration

#### Backend Dockerfile
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1
```

#### Frontend Dockerfile
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1
```

## Best Practices

1. **Response Time**: Health check endpoints respond within 2 seconds to meet Kubernetes requirements
2. **Minimal Processing**: Health endpoints perform minimal processing to avoid impacting service performance
3. **Database Connectivity**: Backend health check verifies database connectivity
4. **Environment Information**: Health responses include environment information for debugging
5. **Service Identification**: Responses include service name for multi-service deployments

## Kubernetes Integration

These endpoints are designed for use with Kubernetes liveness and readiness probes:

```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 30
  timeoutSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /api/health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

## Testing

To test the health endpoints manually:

```bash
# Backend
curl http://localhost:8001/api/health

# Frontend
curl http://localhost:3001/api/health
```

## Security Considerations

- Health endpoints do not expose sensitive information
- Database credentials and other secrets are not included in responses
- Endpoints are publicly accessible for monitoring tools