# Skill: Multi-Stage Dockerfile Builder

## Purpose
Generate production-ready, multi-stage Dockerfiles optimized for size, security, and caching.

## Input Parameters
- service_name: "frontend" | "backend"
- base_image: Base image (e.g., "node:20-alpine", "python:3.13-slim")
- build_command: Command to build the app (e.g., "npm run build", "uv sync")
- runtime_command: Command to start the app (e.g., "npm start", "uvicorn main:app")
- port: Exposed port (e.g., 3000, 8000)

## Output
Complete Dockerfile with multi-stage build following best practices.

## Template

### Frontend (Next.js)
```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Install dependencies only when needed
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### Backend (FastAPI)
```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM python:3.13-slim AS deps
WORKDIR /app

# Install UV
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.13-slim AS runner
WORKDIR /app

# Create non-root user
RUN useradd --uid 1001 --create-home appuser

# Copy dependencies from deps stage
COPY --from=deps /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Quality Standards
- [ ] Multi-stage build (minimize final image)
- [ ] Non-root user (security)
- [ ] Specific base image tags (reproducibility)
- [ ] Only production dependencies in final stage
- [ ] Layer caching optimized (COPY package files before code)
- [ ] .dockerignore file present
- [ ] Health check compatible (app exposes /health endpoint)

## Usage Example
Input: service_name="frontend", base_image="node:20-alpine"
Output: Complete frontend/Dockerfile as shown above