# Quickstart: Docker Containerization

## Overview
This guide provides quick instructions to build and run the containerized TaskFlow application.

## Prerequisites
- Docker Engine (version 20.10 or higher)
- Docker Compose (optional, for local development)
- Git
- Access to the source code repository

## Build Instructions

### Build Frontend Container
```bash
cd frontend
docker build -t taskflow-frontend:latest .
```

### Build Backend Container
```bash
cd backend
docker build -t taskflow-backend:latest .
```

### Alternative: Build with Specific Version
```bash
# Frontend
docker build -t taskflow-frontend:0.1.0 .

# Backend
docker build -t taskflow-backend:0.1.0 .
```

## Run Instructions

### Run Individual Containers
```bash
# Run backend (make sure database is available)
docker run -d \
  --name taskflow-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/dbname \
  -e OPENROUTER_API_KEY=your_key_here \
  taskflow-backend:latest

# Run frontend
docker run -d \
  --name taskflow-frontend \
  -p 3000:3000 \
  -e API_URL=http://localhost:8000/api \
  --link taskflow-backend \
  taskflow-frontend:latest
```

### Run with Docker Compose (Recommended for Development)
```bash
# From the project root
docker-compose up -d
```

## Health Check Verification
```bash
# Check frontend health
curl http://localhost:3000/health

# Check backend health
curl http://localhost:8000/api/health
```

Both endpoints should return HTTP 200 status.

## Kubernetes Deployment (Minikube)
```bash
# Start Minikube
minikube start

# Build images for Minikube
eval $(minikube docker-env)
docker build -t taskflow-frontend:latest ./frontend
docker build -t taskflow-backend:latest ./backend

# Deploy with Helm
helm install taskflow ./helm/taskflow/
```

## Environment Variables

### Frontend Container
- `API_URL`: URL of the backend API (e.g., http://backend-service:8000/api)
- `NODE_ENV`: Environment mode (production/development)

### Backend Container
- `DATABASE_URL`: PostgreSQL connection string
- `OPENROUTER_API_KEY`: API key for OpenRouter service
- `UVICORN_HOST`: Host binding (defaults to 0.0.0.0)
- `UVICORN_PORT`: Port binding (defaults to 8000)

## Image Sizes
Check image sizes after building:
```bash
docker images | grep taskflow
```

Expected sizes:
- Frontend image: < 200MB
- Backend image: < 300MB

## Troubleshooting
- If health checks fail, verify environment variables are set correctly
- Check container logs: `docker logs <container-name>`
- Ensure non-root user has proper file permissions
- Verify port availability on host system