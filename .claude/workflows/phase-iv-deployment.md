# Phase IV: Kubernetes Deployment Workflow

## Orchestration Sequence

### Pre-Flight Check
````bash
# Verify tools installed
docker --version
kubectl version --client
minikube version
helm version
kubectl-ai --version
kagent --version

# Verify Phase III completed
ls frontend/Dockerfile backend/Dockerfile || echo "⚠️  Phase III incomplete"
````

### Day 1-2: Containerization
1. Activate @agents/docker-agent.md
2. Read @specs/features/containerization.md
3. Generate Dockerfiles using @skills/dockerfile-builder.md
4. Add health endpoints using @skills/health-check-builder.md
5. Optimize images using @skills/image-optimizer.md
6. Test locally: `docker build && docker run`
7. Create PHR: history/prompts/phase4-containerization.md

### Day 3: Helm Charts
1. Activate @agents/helm-agent.md
2. Read @specs/features/helm-charts.md
3. Scaffold chart using @skills/helm-chart-builder.md
4. Generate manifests using @skills/k8s-manifest-builder.md
5. Test: `helm lint && helm template`
6. Create PHR: history/prompts/phase4-helm.md

### Day 4-5: Minikube Deployment
1. Activate @agents/kubernetes-agent.md
2. Read @specs/features/minikube-deployment.md
3. Deploy using @skills/minikube-deployer.md
4. Verify with kubectl-ai (3+ operations)
5. Run kagent cluster analysis
6. Test chatbot end-to-end
7. Create PHR: history/prompts/phase4-deployment.md

### Day 6: Documentation & Verification
1. Activate @agents/devops-agent.md
2. Generate DEPLOYMENT.md
3. Update Constitution success criteria
4. Create final PHR summary
5. Prepare for Phase V

## Success Criteria Verification

Run this checklist:
````bash
# ✅ Docker images built
docker images | grep taskflow

# ✅ Helm chart valid
helm lint helm/taskflow
helm template taskflow helm/taskflow

# ✅ Minikube deployment
kubectl get pods -n taskflow
kubectl get services -n taskflow

# ✅ Pods healthy
kubectl get pods -n taskflow -o wide

# ✅ Health checks passing
kubectl describe pod -n taskflow | grep -A5 "Liveness\|Readiness"

# ✅ Application accessible
minikube service taskflow-frontend -n taskflow --url

# ✅ kubectl-ai usage documented
ls history/prompts/kubectl-ai-*.md

# ✅ kagent analysis complete
ls history/prompts/kagent-analysis.md
````

## Troubleshooting Decision Tree
````
Pod not starting?
├─ ImagePullBackOff → minikube image load <image>
├─ CrashLoopBackOff → kubectl logs <pod> -n taskflow
├─ Pending → kubectl describe pod <pod> -n taskflow
└─ ErrImagePull → Check image name/tag in values.yaml

Service not accessible?
├─ Check service type (NodePort for local)
├─ Verify selector matches pod labels
├─ Test: kubectl port-forward service/... 3000:3000
└─ Use: kubectl-ai "why can't I access frontend service"

Health checks failing?
├─ Verify /health endpoint exists
├─ Check initialDelaySeconds (app needs time to start)
├─ Test manually: kubectl exec <pod> -- curl localhost:3000/health
└─ Increase timeoutSeconds if slow startup
````

## Output Artifacts

At end of Phase IV, you should have:
````
taskflow/
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── app/health/route.ts
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── main.py (with /api/health)
├── helm/
│   └── taskflow/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-local.yaml
│       └── templates/
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── configmap.yaml
│           ├── secret.yaml
│           └── NOTES.txt
├── scripts/
│   ├── deploy-minikube.sh
│   └── verify-deployment.sh
├── docs/
│   └── DEPLOYMENT.md
└── history/prompts/
    ├── phase4-containerization.md
    ├── phase4-helm.md
    ├── phase4-deployment.md
    ├── kubectl-ai-usage.md
    └── kagent-analysis.md
````