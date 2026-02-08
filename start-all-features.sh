#!/bin/bash

# Script to deploy TaskFlow application to Minikube with Dapr and Kafka

set -e  # Exit on any error

echo "🚀 Starting TaskFlow deployment to Minikube..."

# Check if minikube is available
if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube is not installed. Please install minikube first."
    exit 1
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Start minikube if not already running
MINIKUBE_STATUS=$(minikube status --format='{{.Host}}')
if [ "$MINIKUBE_STATUS" != "Running" ]; then
    echo "🔄 Starting Minikube..."
    minikube start --memory=3072 --cpus=2
else
    echo "✅ Minikube is already running"
fi

# Enable required minikube addons
echo "🔧 Enabling required addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Check if Dapr CLI is available
if command -v dapr &> /dev/null; then
    # Install Dapr to the cluster
    echo "📦 Installing Dapr to Minikube..."
    dapr init -k
    echo "✅ Dapr installed successfully"
else
    echo "⚠️ Dapr CLI not found. Please install Dapr CLI to manage Dapr installation."
fi

# Build Docker images inside Minikube environment
echo "🐳 Setting Docker environment to Minikube..."
eval $(minikube docker-env)

echo "🏗️ Building backend Docker image..."
cd backend
docker build -t taskflow-backend:latest .
cd ..

echo "🏗️ Building frontend Docker image..."
cd frontend
docker build -t taskflow-frontend:latest .
cd ..

# Install Strimzi Kafka operator if not already installed
if ! kubectl get deployment strimzi-cluster-operator &> /dev/null; then
    echo "📦 Installing Strimzi Kafka operator..."
    kubectl create namespace kafka
    kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
    echo "⏳ Waiting for Strimzi operator to be ready..."
    kubectl wait --for=condition=available deployment/strimzi-cluster-operator -n kafka --timeout=300s
else
    echo "✅ Strimzi Kafka operator is already installed"
fi

# Deploy Kafka cluster
echo "📡 Deploying Kafka cluster..."
kubectl apply -f kubernetes/kafka-cluster.yaml -n default

# Wait for Kafka to be ready
echo "⏳ Waiting for Kafka cluster to be ready..."
kubectl wait --for=condition=Ready kafka/taskflow-kafka --timeout=300s

# Deploy Kafka topics
echo "📡 Creating Kafka topics..."
kubectl apply -f kubernetes/kafka-topics.yaml -n default

# Deploy Redis for Dapr state store
echo "💾 Deploying Redis for Dapr state store..."
kubectl apply -f kubernetes/redis-deployment.yaml -n default

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."
kubectl wait --for=condition=ready pod -l app=redis --timeout=120s

# Deploy Dapr components
echo "⚙️ Deploying Dapr components..."
kubectl apply -f backend/dapr/

# Create database secret (you'll need to update this with your actual database credentials)
echo "🔒 Creating database secret..."
kubectl create secret generic db-secret \
  --from-literal=database-url="postgresql://username:password@host:port/dbname" \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy the applications
echo "🚢 Deploying TaskFlow backend..."
kubectl apply -f kubernetes/backend-deployment.yaml -n default

echo "🚢 Deploying TaskFlow frontend..."
kubectl apply -f kubernetes/frontend-deployment.yaml -n default

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=taskflow-backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=taskflow-frontend --timeout=300s

# Get the external IP addresses
echo "🌐 Retrieving service information..."
echo "Backend service:"
kubectl get svc taskflow-backend-service
echo ""
echo "Frontend service:"
kubectl get svc taskflow-frontend-service

echo ""
echo "✅ TaskFlow application deployed successfully!"
echo "💡 Access the frontend at: $(minikube service taskflow-frontend-service --url)"
echo "💡 Access the backend API at: $(minikube service taskflow-backend-service --url)/docs"
echo ""
echo "📋 To view application logs:"
echo "   kubectl logs -l app=taskflow-backend"
echo "   kubectl logs -l app=taskflow-frontend"
echo ""
echo "可观 To access Dapr dashboard (if enabled):"
echo "   dapr dashboard"