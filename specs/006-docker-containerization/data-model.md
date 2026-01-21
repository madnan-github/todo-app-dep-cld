# Data Model: Docker Containerization

## Overview
This document describes the containerization entities and their configurations for the TaskFlow application. Rather than traditional data models, this focuses on container entities and their properties.

## Container Entity: Frontend Service

**Description:** The frontend service container that serves the web interface of the TaskFlow application.

**Configuration Properties:**
- **Base Image:** node:lts-alpine or node:20-alpine (to be determined based on frontend dependencies)
- **Build Stage Image:** node:lts as builder stage for compilation
- **Runtime User:** UID 1001 (non-root user)
- **Exposed Port:** 3000 (standard Next.js port)
- **Environment Variables:**
  - API_URL: URL of the backend API service
  - NODE_ENV: Production or development
- **Health Check Endpoint:** GET /health returning HTTP 200
- **Resource Limits:** Memory < 200MB as per spec

**Volume Mounts:**
- /app/public for static assets (read-only in production)

**Security Context:**
- Run as non-root user (UID 1001)
- ReadOnlyRootFilesystem: true (where possible)
- AllowPrivilegeEscalation: false

## Container Entity: Backend Service

**Description:** The backend service container that provides the API for the TaskFlow application.

**Configuration Properties:**
- **Base Image:** python:3.13-slim
- **Build Stage Image:** python:3.13 as builder if needed
- **Runtime User:** UID 1001 (non-root user)
- **Exposed Port:** 8000 (standard FastAPI port)
- **Environment Variables:**
  - DATABASE_URL: Connection string for Neon PostgreSQL
  - OPENROUTER_API_KEY: API key for OpenRouter (if needed)
  - PYTHONPATH: /app/src
- **Health Check Endpoint:** GET /api/health returning HTTP 200
- **Resource Limits:** Memory < 300MB as per spec

**Volume Mounts:**
- /app/data for any local data (if needed for debugging)

**Security Context:**
- Run as non-root user (UID 1001)
- ReadOnlyRootFilesystem: true (where possible)
- AllowPrivilegeEscalation: false

## Shared Container Elements

**Docker Build Context:**
- Multi-stage build pattern
- Efficient layer caching
- Minimal base images
- .dockerignore for build optimization

**Health Check Mechanism:**
- Lightweight endpoint implementation
- Dependency status checking (DB connectivity for backend)
- Standard HTTP 200 response on healthy state
- Appropriate timeouts and intervals for Kubernetes

**Image Tagging:**
- Semantic versioning (e.g., taskflow-frontend:0.1.0)
- Git commit-based tags for development builds
- Release version tags for production builds

## Container Relationships

The frontend and backend containers are designed to work independently but communicate through standard API calls. The frontend requires the API_URL environment variable to connect to the backend service. Both containers follow the same security practices (non-root user, resource limits) but have different runtime requirements based on their technology stacks.