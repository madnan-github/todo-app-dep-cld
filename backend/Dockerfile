# Multi-stage Dockerfile for backend service
# Stage 1: Dependencies installation
FROM python:3.13-slim AS dependencies
WORKDIR /app

# Install uv for fast package management
ENV UV_SYSTEM=1
RUN pip install uv

# Copy requirements and install dependencies
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

# Stage 2: Build stage
FROM python:3.13-slim AS build
WORKDIR /app

# Copy dependencies from dependencies stage
COPY --from=dependencies /usr/local /usr/local

# Copy application code
COPY . .

# Stage 3: Production runtime
FROM python:3.13-slim AS production
WORKDIR /app

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1001 appuser

# Create cache directory for the user and set proper permissions
RUN mkdir -p /home/appuser/.cache/uv && chown -R appuser:appgroup /home/appuser

# Copy dependencies from dependencies stage
COPY --from=dependencies /usr/local /usr/local

# Copy application code from build stage
COPY --from=build --chown=appuser:appgroup /app /app

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check - will be updated after health endpoint is implemented
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
