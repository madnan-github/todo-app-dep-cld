#!/bin/bash

# Script to build and run the complete TaskFlow application

set -e  # Exit on any error

echo "🚀 Starting TaskFlow application setup..."

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube is not installed. Please install Minikube first."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

if ! command -v dapr &> /dev/null; then
    echo "❌ Dapr CLI is not installed. Please install Dapr CLI first."
    exit 1
fi

echo "✅ All prerequisites are installed"

# Start Minikube if not already running
MINIKUBE_STATUS=$(minikube status --format='{{.Host}}' 2>/dev/null || echo "stopped")
if [ "$MINIKUBE_STATUS" != "Running" ]; then
    echo "🔄 Starting Minikube..."
    minikube start --memory=4096 --cpus=2
else
    echo "✅ Minikube is already running"
fi

# Enable required addons
echo "🔧 Enabling required addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Install Dapr to the cluster
echo "📦 Installing Dapr to Minikube..."
dapr init -k
echo "✅ Dapr installed successfully"

# Wait a bit for Dapr to be ready
sleep 10

# Install Strimzi Kafka operator if not already installed
if ! kubectl get deployment strimzi-cluster-operator -n kafka &> /dev/null; then
    echo "📦 Installing Strimzi Kafka operator..."
    kubectl create namespace kafka
    kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
    echo "⏳ Waiting for Strimzi operator to be ready..."
    kubectl wait --for=condition=available deployment/strimzi-cluster-operator -n kafka --timeout=300s
else
    echo "✅ Strimzi Kafka operator is already installed"
fi

# Deploy Kafka cluster if not already deployed
if ! kubectl get kafka taskflow-kafka -n kafka &> /dev/null; then
    echo "📡 Deploying Kafka cluster..."
    kubectl apply -f kubernetes/kafka-cluster.yaml -n kafka
    kubectl apply -f kubernetes/kafka-nodepool.yaml -n kafka
    
    # Wait for Kafka to be ready
    echo "⏳ Waiting for Kafka cluster to be ready..."
    kubectl wait --for=condition=Ready kafka/taskflow-kafka --timeout=600s -n kafka
else
    echo "✅ Kafka cluster is already deployed"
fi

# Deploy Kafka topics if not already deployed
if ! kubectl get kafkatopic task-events &> /dev/null; then
    echo "📡 Creating Kafka topics..."
    kubectl apply -f kubernetes/kafka-topics.yaml
else
    echo "✅ Kafka topics are already created"
fi

# Deploy Redis for Dapr state store if not already deployed
if ! kubectl get deployment redis &> /dev/null; then
    echo "💾 Deploying Redis for Dapr state store..."
    kubectl apply -f kubernetes/redis-deployment.yaml
    
    # Wait for Redis to be ready
    echo "⏳ Waiting for Redis to be ready..."
    kubectl wait --for=condition=ready pod -l app=redis --timeout=120s
else
    echo "✅ Redis is already deployed"
fi

# Deploy Dapr components if not already deployed
if ! kubectl get component kafka-pubsub &> /dev/null; then
    echo "⚙️ Deploying Dapr components..."
    kubectl apply -f backend/dapr/
else
    echo "✅ Dapr components are already deployed"
fi

# Build Docker images
echo "🐳 Setting Docker environment to Minikube..."
eval $(minikube docker-env)

# Build backend image
if [[ $(docker images -q taskflow-backend:latest 2> /dev/null) ]]; then
    echo "✅ Backend image already exists"
else
    echo "🏗️ Building backend Docker image..."
    cd backend
    docker build -t taskflow-backend:latest .
    cd ..
fi

# Build frontend image
if [[ $(docker images -q taskflow-frontend:latest 2> /dev/null) ]]; then
    echo "✅ Frontend image already exists"
else
    echo "🏗️ Building frontend Docker image..."
    cd frontend
    docker build -t taskflow-frontend:latest .
    cd ..
fi

# Create database secret if not already created
if kubectl get secret db-secret &> /dev/null; then
    echo "✅ Database secret already exists"
else
    echo "🔒 Creating database secret..."
    kubectl create secret generic db-secret \
      --from-literal=database-url="postgresql://username:password@host:port/dbname"
fi

# Deploy the applications
echo "🚢 Deploying TaskFlow backend..."
kubectl apply -f kubernetes/backend-deployment.yaml

echo "🚢 Deploying TaskFlow frontend..."
kubectl apply -f kubernetes/frontend-deployment.yaml

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=taskflow-backend --timeout=300s || echo "⚠️ Backend deployment may still be starting"
kubectl wait --for=condition=ready pod -l app=taskflow-frontend --timeout=300s || echo "⚠️ Frontend deployment may still be starting"

# Get the external IP addresses
echo ""
echo "✅ TaskFlow application deployed successfully!"
echo ""
echo "🌐 Access the services:"
FRONTEND_URL=$(minikube service taskflow-frontend-service --url 2>/dev/null || echo "Pending...")
BACKEND_URL=$(minikube service taskflow-backend-service --url 2>/dev/null || echo "Pending...")

echo "💡 Frontend: $FRONTEND_URL"
echo "💡 Backend API: $BACKEND_URL"
echo "💡 Backend API Documentation: $BACKEND_URL/docs"
echo ""
echo "📋 To view application logs:"
echo "   kubectl logs -l app=taskflow-backend"
echo "   kubectl logs -l app=taskflow-frontend"
echo ""
echo "可观 To access Dapr dashboard:"
echo "   dapr dashboard"
echo ""
echo "💡 Tip: If services are still pending, wait a few more minutes and run:"
echo "   minikube service taskflow-frontend-service --url"
echo "   minikube service taskflow-backend-service --url"