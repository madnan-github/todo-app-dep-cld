#!/bin/bash

# Script to build the actual application images in minikube environment

echo "Building application images in minikube environment..."

# Set Docker environment to minikube
eval $(minikube docker-env)

echo "Building backend image..."
cd /home/ruser/q4/todo-app-dep-cld/backend
docker build -t taskflow-backend:latest . --no-cache

echo "Building frontend image..."
cd /home/ruser/q4/todo-app-dep-cld/frontend
docker build -t taskflow-frontend:latest . --no-cache

echo "Images built successfully!"
echo "Backend image: taskflow-backend:latest"
echo "Frontend image: taskflow-frontend:latest"