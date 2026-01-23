# Quickstart: AI DevOps Tools Integration

## Overview
This guide explains how to use the AI-enhanced DevOps tools integrated into the TodoFlow application deployment workflow.

## Prerequisites
- Kubernetes cluster (tested with Minikube)
- kubectl installed and configured
- Docker installed with AI plugin (if available)
- Access to AI service APIs (for kubectl-ai and kagent)

## Setup AI DevOps Tools

### 1. Install kubectl-ai Plugin
```bash
# Install krew package manager if not already installed
kubectl krew install ai

# Or update if already installed
kubectl krew upgrade ai
```

### 2. Install kagent (Conceptual Tool)
*Note: kagent is a conceptual AI-powered cluster analysis tool. In practice, you might use tools like kube-bench, goldilocks, or other cluster analysis tools.*

### 3. Enable Docker AI (Gordon)
```bash
# Verify Docker AI is available
docker ai --help

# Note: Requires Docker Desktop with AI features enabled
```

## Using AI DevOps Tools

### 1. Natural Language Kubernetes Commands with kubectl-ai
```bash
# Deploy frontend with 2 replicas
kubectl-ai "scale frontend deployment to 2 replicas"

# Check cluster status
kubectl-ai "show me all pods in all namespaces"

# Get service details
kubectl-ai "get service todo-app-frontend details"
```

### 2. Cluster Analysis with kagent
```bash
# Analyze cluster health
kagent analyze cluster

# Check resource allocation
kagent check resources

# Diagnose performance issues
kagent diagnose performance
```

### 3. Dockerfile Generation with Gordon
```bash
# Generate Dockerfile for frontend
cd frontend/
docker ai "Generate a secure, optimized Dockerfile for Next.js 15+ application"

# Generate Dockerfile for backend
cd ../backend/
docker ai "Generate a secure, optimized Dockerfile for FastAPI application"
```

## Generated Assets

### Kubernetes Manifests
- `kubectl-ai-simulated-output.yaml`: AI-generated Kubernetes resources
- Located in the repository root
- Contains Deployments, Services, and Ingress configurations

### Optimized Dockerfiles
- `frontend/Dockerfile.gordon`: AI-optimized frontend Dockerfile
- `backend/Dockerfile.gordon`: AI-optimized backend Dockerfile
- Include security best practices and multi-stage builds

### Cluster Analysis
- `kagent-simulated-analysis.txt`: AI-generated cluster analysis report
- Contains resource utilization, optimization opportunities, and security findings

## Verification Steps

### 1. Validate Generated Kubernetes YAML
```bash
# Check syntax
python3 -c "import yaml; print('Valid:', yaml.safe_load(open('kubectl-ai-simulated-output.yaml')) is not None)"

# Apply to cluster (after review)
kubectl apply -f kubectl-ai-simulated-output.yaml
```

### 2. Build Docker Images with Generated Files
```bash
# Build frontend with AI-generated Dockerfile
docker build -f frontend/Dockerfile.gordon -t todo-frontend-ai .

# Build backend with AI-generated Dockerfile
docker build -f backend/Dockerfile.gordon -t todo-backend-ai .
```

### 3. Check AI Interaction Logs
- Review PHR at `history/prompts/009-ai-devops-tools-integration/`
- Verify all AI interactions are documented

## Best Practices

1. **Always Review AI-Generated Configurations**
   - Human validation is required before applying to production
   - Check for security implications
   - Verify resource limits and requests

2. **Keep AI Prompts Specific**
   - Detailed prompts yield better results
   - Include context about your specific requirements

3. **Document Changes**
   - All AI-generated configurations must be saved to the repository
   - Update PHRs with new AI interactions

4. **Validate Before Applying**
   - Run syntax checks on generated YAML
   - Test Dockerfiles locally before using in CI/CD

## Troubleshooting

### kubectl-ai Not Working
- Verify API key is configured: `export GEMINI_API_KEY=your_key_here`
- Check krew installation: `kubectl krew list`

### Docker AI Not Available
- Ensure Docker Desktop is running with AI features enabled
- Check Docker version: `docker --version`

### Invalid Generated YAML
- Verify the AI tool output manually
- Use online YAML validators
- Compare with existing working configurations