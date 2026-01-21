# Skill: Minikube Deployment Automation

## Purpose
Automate the complete deployment process to Minikube including image loading, secret creation, and Helm installation.

## Input Parameters
- chart_path: "helm/taskflow"
- namespace: "taskflow"
- images: ["taskflow-frontend:0.1.0", "taskflow-backend:0.1.0"]
- secrets: {DATABASE_URL, OPENROUTER_API_KEY, BETTER_AUTH_SECRET}

## Output
Deployment automation script and verification commands.

## Script Template

### deploy-minikube.sh
````bash
#!/bin/bash
set -e

echo "🚀 Deploying TaskFlow to Minikube..."

# Colors for output
GREEN='\033[0.32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="taskflow"
CHART_PATH="helm/taskflow"
FRONTEND_IMAGE="taskflow-frontend:0.1.0"
BACKEND_IMAGE="taskflow-backend:0.1.0"

# Step 1: Start Minikube
echo "📦 Starting Minikube..."
minikube status || minikube start --cpus=4 --memory=8192

# Step 2: Load Docker images
echo "🐳 Loading Docker images to Minikube..."
minikube image load $FRONTEND_IMAGE
minikube image load $BACKEND_IMAGE

# Verify images loaded
echo "✅ Verifying images..."
minikube image ls | grep taskflow

# Step 3: Create namespace
echo "📁 Creating namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Step 4: Create secrets
echo "🔐 Creating secrets..."
if [ -f ".env.local" ]; then
  source .env.local
  kubectl create secret generic taskflow-secrets \
    --from-literal=database-url="$DATABASE_URL" \
    --from-literal=openrouter-api-key="$OPENROUTER_API_KEY" \
    --from-literal=better-auth-secret="$BETTER_AUTH_SECRET" \
    --namespace=$NAMESPACE \
    --dry-run=client -o yaml | kubectl apply -f -
else
  echo "${RED}❌ Error: .env.local not found${NC}"
  echo "Create .env.local with:"
  echo "  DATABASE_URL=postgresql://..."
  echo "  OPENROUTER_API_KEY=sk-..."
  echo "  BETTER_AUTH_SECRET=your-secret"
  exit 1
fi

# Step 5: Install Helm chart
echo "⎈ Installing Helm chart..."
helm upgrade --install taskflow $CHART_PATH \
  --namespace=$NAMESPACE \
  --values=$CHART_PATH/values-local.yaml \
  --wait \
  --timeout=5m

# Step 6: Verify deployment
echo "🔍 Verifying deployment..."
kubectl get pods -n $NAMESPACE
kubectl get services -n $NAMESPACE

# Step 7: Wait for pods to be ready
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod \
  --selector=app.kubernetes.io/name=taskflow \
  --namespace=$NAMESPACE \
  --timeout=300s

# Step 8: Get access URL
echo "🌐 Getting access URL..."
FRONTEND_URL=$(minikube service taskflow-frontend -n $NAMESPACE --url)

echo ""
echo "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📱 Access the application at:"
echo "   $FRONTEND_URL"
echo ""
echo "📊 Useful commands:"
echo "   kubectl get pods -n $NAMESPACE"
echo "   kubectl logs -f <pod-name> -n $NAMESPACE"
echo "   kubectl-ai 'show me pod status in taskflow namespace'"
echo "   minikube dashboard"
echo ""
````

### verify-deployment.sh
````bash
#!/bin/bash

NAMESPACE="taskflow"

echo "🔍 Verifying TaskFlow deployment..."

# Check namespace
echo "1️⃣  Checking namespace..."
kubectl get namespace $NAMESPACE

# Check pods
echo "2️⃣  Checking pods..."
kubectl get pods -n $NAMESPACE

# Check services
echo "3️⃣  Checking services..."
kubectl get services -n $NAMESPACE

# Check deployments
echo "4️⃣  Checking deployments..."
kubectl get deployments -n $NAMESPACE

# Check secrets
echo "5️⃣  Checking secrets..."
kubectl get secrets -n $NAMESPACE

# Check pod health
echo "6️⃣  Checking pod health..."
kubectl get pods -n $NAMESPACE -o wide

# Test frontend health
echo "7️⃣  Testing frontend health endpoint..."
FRONTEND_POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n $NAMESPACE $FRONTEND_POD -- curl -s http://localhost:3000/health

# Test backend health
echo "8️⃣  Testing backend health endpoint..."
BACKEND_POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n $NAMESPACE $BACKEND_POD -- curl -s http://localhost:8000/api/health

echo "✅ Verification complete!"
````

## Troubleshooting Commands
````bash
# Check pod status
kubectl get pods -n taskflow

# Describe problematic pod
kubectl describe pod <pod-name> -n taskflow

# View logs
kubectl logs -f <pod-name> -n taskflow

# Get events
kubectl get events -n taskflow --sort-by='.lastTimestamp'

# Use kubectl-ai
kubectl-ai "why is pod <name> failing in taskflow namespace"

# Access pod shell
kubectl exec -it <pod-name> -n taskflow -- /bin/sh

# Port forward for testing
kubectl port-forward service/taskflow-frontend 3000:3000 -n taskflow
kubectl port-forward service/taskflow-backend 8000:8000 -n taskflow
````

## Usage Example
Input: images=["taskflow-frontend:0.1.0", "taskflow-backend:0.1.0"]
Output: Complete scripts/deploy-minikube.sh and scripts/verify-deployment.sh