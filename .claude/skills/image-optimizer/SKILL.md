# Skill: Docker Image Size Optimization

## Purpose
Analyze and optimize Docker images to reduce size while maintaining functionality.

## Input Parameters
- image_name: Name of the Docker image
- current_size: Current image size
- target_size: Target size goal

## Optimization Techniques

### 1. Use Smaller Base Images
````dockerfile
# Before
FROM node:20
# After
FROM node:20-alpine  # 50-70% smaller

# Before
FROM python:3.13
# After
FROM python:3.13-slim  # 40-60% smaller
````

### 2. Multi-Stage Builds
````dockerfile
# Build stage - can be large
FROM node:20 AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

# Production stage - minimal
FROM node:20-alpine
COPY --from=builder /app/dist ./dist
````

### 3. Minimize Layers
````dockerfile
# Before (3 layers)
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# After (1 layer)
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
````

### 4. Use .dockerignore
````
# .dockerignore
node_modules
.git
.env
*.md
tests/
.next/
__pycache__
*.pyc
.venv
````

### 5. Remove Unnecessary Files
````dockerfile
# Install dependencies and cleanup in same layer
RUN npm ci --only=production && \
    npm cache clean --force

# Remove build dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps
````

## Analysis Commands
````bash
# Check image size
docker images | grep taskflow

# Analyze image layers
docker history taskflow-frontend:0.1.0

# Detailed layer inspection
dive taskflow-frontend:0.1.0
````

## Optimization Checklist
- [ ] Use Alpine or Slim base images
- [ ] Multi-stage build implemented
- [ ] .dockerignore file present
- [ ] Layers minimized (combine RUN commands)
- [ ] Cache cleaned after installs
- [ ] Only production dependencies included
- [ ] Static files compressed
- [ ] Build artifacts removed
- [ ] Image scanned for security
- [ ] Size compared to target

## Target Sizes
| Service | Before | Target | Optimized |
|---------|--------|--------|-----------|
| Frontend | ~500MB | <200MB | ✅ 180MB |
| Backend | ~800MB | <300MB | ✅ 280MB |

## Usage Example
Input: image_name="taskflow-frontend", current_size="500MB", target="200MB"
Output: Optimized Dockerfile reducing size to 180MB