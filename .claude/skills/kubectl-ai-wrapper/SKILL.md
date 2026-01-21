# Skill: kubectl-ai Natural Language Operations

## Purpose
Provide wrapper functions for kubectl-ai operations with proper documentation and error handling.

## Input Parameters
- operation: Type of operation (deploy, scale, debug, analyze)
- context: Natural language description
- namespace: Target namespace

## Output
kubectl-ai command execution with PHR documentation.

## Operation Templates

### Deployment Operations
````bash
# Deploy application
kubectl-ai "deploy taskflow frontend with 2 replicas in taskflow namespace"

# Update image
kubectl-ai "update taskflow-frontend deployment to use image version 0.2.0"

# Rollback
kubectl-ai "rollback taskflow-backend deployment to previous version"
````

### Scaling Operations
````bash
# Scale up
kubectl-ai "scale taskflow-backend deployment to 3 replicas"

# Scale down
kubectl-ai "reduce taskflow-frontend to 1 replica"

# Autoscale
kubectl-ai "create horizontal pod autoscaler for backend with min 2 max 5 replicas"
````

### Debugging Operations
````bash
# Pod issues
kubectl-ai "why is my pod in CrashLoopBackOff state"
kubectl-ai "show me logs of failing pods in taskflow namespace"
kubectl-ai "describe pods with status not Running"

# Network issues
kubectl-ai "test connectivity between frontend and backend pods"
kubectl-ai "show me all services in taskflow namespace"

# Resource issues
kubectl-ai "show pods using more than 80% memory"
kubectl-ai "which pods are being throttled"
````

### Analysis Operations
````bash
# Resource usage
kubectl-ai "show resource usage of all pods in taskflow namespace"
kubectl-ai "which pods are using the most CPU"

# Events
kubectl-ai "show recent warning events"
kubectl-ai "what happened in the last 10 minutes"

# Configuration
kubectl-ai "show environment variables of taskflow-backend pod"
kubectl-ai "display secrets used by deployments"
````

## PHR Documentation Template

For each kubectl-ai usage, document in `history/prompts/kubectl-ai-phase4.md`:
````markdown
## kubectl-ai Operation: [Operation Name]

**Timestamp:** 2025-01-21T14:30:00Z

**Command:**
```bash
kubectl-ai "[natural language command]"
```

**Generated YAML/Output:**
```yaml
[kubectl-ai generated output]
```

**Action Taken:**
- [ ] Reviewed generated output
- [ ] Applied to cluster
- [ ] Verified result
- [ ] Saved to file: [path/to/file.yaml]

**Result:**
[Success/Failure description]

**Verification:**
```bash
kubectl get [resource] -n taskflow
```

**Notes:**
[Any observations, modifications, or lessons learned]

---
````

## Usage Example
Input: operation="scale", context="increase backend to 3 replicas"
Output: kubectl-ai command + PHR documentation entry