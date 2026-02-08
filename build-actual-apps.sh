#!/bin/bash

# Script to build actual TaskFlow application images

echo "Building actual TaskFlow application images..."

# Set Docker environment to minikube
eval $(minikube docker-env)

echo "Building backend image with actual application..."
cd /home/ruser/q4/todo-app-dep-cld/backend

# Create a simplified Dockerfile for the backend that installs dependencies and runs the app
cat > Dockerfile.actual << 'EOF'
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
RUN pip install uv

# Copy requirements and install dependencies
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

docker build -f Dockerfile.actual -t taskflow-backend:latest .
rm Dockerfile.actual

echo "Building frontend image with actual application..."
cd /home/ruser/q4/todo-app-dep-cld/frontend

# Create a simplified Dockerfile for the frontend
cat > Dockerfile.actual << 'EOF'
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
EOF

docker build -f Dockerfile.actual -t taskflow-frontend:latest .
rm Dockerfile.actual

echo "Images built successfully!"
echo "Backend image: taskflow-backend:latest"
echo "Frontend image: taskflow-frontend:latest"