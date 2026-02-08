# TaskFlow Application - Complete Setup Guide

This guide explains how to build and run the complete TaskFlow application with all Phase V features.

## Prerequisites

- Docker
- Minikube
- kubectl
- Dapr CLI
- Git

## Step 1: Start Minikube and Enable Required Addons

```bash
# Start Minikube
minikube start --memory=4096 --cpus=2

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify Minikube is running
minikube status
```

## Step 2: Install Dapr

```bash
# Install Dapr to the cluster
dapr init -k

# Verify Dapr is running
dapr status -k
```

## Step 3: Install Strimzi Kafka Operator

```bash
# Create Kafka namespace
kubectl create namespace kafka

# Install Strimzi Kafka operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for the operator to be ready
kubectl wait --for=condition=available deployment/strimzi-cluster-operator -n kafka --timeout=300s
```

## Step 4: Deploy Kafka Cluster

```bash
# Apply the Kafka cluster configuration
kubectl apply -f kubernetes/kafka-cluster.yaml -n kafka

# Apply the Kafka node pool
kubectl apply -f kubernetes/kafka-nodepool.yaml -n kafka

# Wait for Kafka to be ready
kubectl wait --for=condition=Ready kafka/taskflow-kafka --timeout=600s -n kafka
```

## Step 5: Deploy Kafka Topics

```bash
kubectl apply -f kubernetes/kafka-topics.yaml
```

## Step 6: Deploy Redis for Dapr State Store

```bash
kubectl apply -f kubernetes/redis-deployment.yaml
kubectl wait --for=condition=ready pod -l app=redis --timeout=120s
```

## Step 7: Deploy Dapr Components

```bash
kubectl apply -f backend/dapr/
```

## Step 8: Build Application Images

```bash
# Set Docker environment to Minikube
eval $(minikube docker-env)

# Build backend image
cd backend
docker build -t taskflow-backend:latest .
cd ..

# Build frontend image
cd frontend
docker build -t taskflow-frontend:latest .
cd ..
```

## Step 9: Create Database Secret

```bash
# Create a database secret (update with your actual database credentials)
kubectl create secret generic db-secret \
  --from-literal=database-url="postgresql://username:password@host:port/dbname"
```

## Step 10: Deploy Applications

```bash
# Deploy backend
kubectl apply -f kubernetes/backend-deployment.yaml

# Deploy frontend
kubectl apply -f kubernetes/frontend-deployment.yaml

# Wait for deployments to be ready
kubectl wait --for=condition=ready pod -l app=taskflow-backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=taskflow-frontend --timeout=300s
```

## Step 11: Access the Applications

### Option 1: Using Minikube Service URLs
```bash
# Get frontend URL
minikube service taskflow-frontend-service --url

# Get backend URL
minikube service taskflow-backend-service --url
```

### Option 2: Using Port Forwarding
```bash
# Forward frontend port
kubectl port-forward svc/taskflow-frontend-service 3000:80

# Forward backend port
kubectl port-forward svc/taskflow-backend-service 8000:80
```

Then access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs

## Alternative: Quick Setup Script

For convenience, you can use the provided setup script:

```bash
# Make sure you're in the project root directory
chmod +x start-all-features.sh
./start-all-features.sh
```

Note: You may need to manually build the Docker images before running the script.

## Verification

To verify everything is working:

```bash
# Check all pods are running
kubectl get pods

# Check all services are available
kubectl get svc

# Check Dapr sidecars are injected
kubectl get pods -l app=taskflow-backend -o yaml | grep dapr
kubectl get pods -l app=taskflow-frontend -o yaml | grep dapr

# Check Kafka topics are created
kubectl get kafkatopics -n kafka

# View application logs
kubectl logs -l app=taskflow-backend
kubectl logs -l app=taskflow-frontend
```

## Troubleshooting

### If Pods Are in CrashLoopBackOff
- Check the logs: `kubectl logs -l app=taskflow-backend`
- Verify database connectivity
- Ensure Kafka is accessible
- Check environment variables in the deployment

### If Dapr Sidecars Aren't Starting
- Verify Dapr is installed: `dapr status -k`
- Check Dapr logs: `kubectl logs -l app=dapr-placement-server -n dapr-system`

### If Kafka Isn't Ready
- Check Kafka logs: `kubectl logs -l strimzi.io/name=taskflow-kafka-kafka -n kafka`
- Verify the Kafka cluster configuration

## Features Available

Once running, the application provides:

- **Advanced Task Management**: Recurring tasks, due dates, reminders
- **Event-Driven Architecture**: All operations publish events to Kafka
- **Dapr Integration**: Service-to-service invocation, state management, pub/sub
- **Full CRUD Operations**: Create, read, update, delete tasks
- **Filtering and Sorting**: Advanced filtering and sorting capabilities
- **Tags and Priorities**: Organize tasks with tags and priority levels
- **API Documentation**: Interactive API docs at `/docs`

## Scaling

To scale the application:

```bash
# Scale backend
kubectl scale deployment taskflow-backend --replicas=3

# Scale frontend
kubectl scale deployment taskflow-frontend --replicas=3
```

## Clean Up

To remove all resources:

```bash
kubectl delete -f kubernetes/
kubectl delete -f backend/dapr/
kubectl delete -f kubernetes/redis-deployment.yaml
kubectl delete -f kubernetes/kafka-topics.yaml
kubectl delete -f kubernetes/kafka-nodepool.yaml
kubectl delete -f kubernetes/kafka-cluster.yaml -n kafka
kubectl delete namespace kafka
kubectl delete secret db-secret
```

## Architecture Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │────│   Backend   │────│   Database  │
│   (Next.js) │    │  (FastAPI)  │    │  (PostgreSQL)│
└─────────────┘    └─────────────┘    └─────────────┘
                    │           │
              ┌─────▼───────────▼─────┐
              │      Dapr Sidecar     │
              │   (Pub/Sub, State)    │
              └───────────────────────┘
                           │
                   ┌───────▼────────┐
                   │   Kafka/Redpanda  │
                   │   Event Stream    │
                   └──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐  ┌─────▼──────┐   ┌──────▼──────────┐
│ Notification   │  │ Recurring  │   │ Audit Service   │
│ Service        │  │ Task       │   │                 │
└────────────────┘  │ Service    │   └─────────────────┘
                    └────────────┘
```

The application is now ready for use with all Phase V features implemented!