# Skill: Health Check Endpoint Builder

## Purpose
Add Kubernetes-compatible health check endpoints to frontend and backend applications.

## Input Parameters
- service_type: "frontend" | "backend"
- framework: "nextjs" | "fastapi"

## Output
Health check route implementation that returns 200 OK.

## Templates

### Frontend (Next.js)
Create `app/health/route.ts`:
```typescript
// app/health/route.ts
export async function GET() {
  return Response.json(
    { status: 'healthy', timestamp: new Date().toISOString() },
    { status: 200 }
  )
}
```

### Backend (FastAPI)
Add to `main.py`:
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
async def health_check():
    """Health check endpoint for Kubernetes probes"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

## Kubernetes Probe Configuration
Use in Deployment manifest:
```yaml
livenessProbe:
  httpGet:
    path: /health  # or /api/health for backend
    port: 3000  # or 8000 for backend
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

## Testing
```bash
# Frontend
curl http://localhost:3000/health
# Expected: {"status":"healthy","timestamp":"2025-01-21T10:00:00.000Z"}

# Backend
curl http://localhost:8000/api/health
# Expected: {"status":"healthy","timestamp":"2025-01-21T10:00:00.000000"}
```

## Usage Example
Input: service_type="frontend", framework="nextjs"
Output: app/health/route.ts file created