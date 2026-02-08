"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.config import settings
from src.database import init_db, engine
from sqlalchemy import text
from src.routes.auth import router as auth_router
from src.routes.tasks import router as tasks_router
from src.routes.tags import router as tags_router
from src.routes.better_auth import router as better_auth_router, router_v1 as better_auth_v1_router
from app.routes import router as main_router
from src.middleware import rate_limiter
import asyncio
import logging

# Import Kafka and Dapr components
from src.kafka_producer import KafkaTaskProducer
from src.background_tasks import BackgroundTaskManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to hold Kafka producer and background task manager
kafka_producer = None
background_manager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    import sys
    import os

    global kafka_producer, background_manager

    # Startup: Initialize database tables
    print(f"Starting TaskFlow API in {settings.environment} mode", flush=True)
    sys.stdout.flush()
    print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}", flush=True)
    sys.stdout.flush()
    print(f"Database URL: {settings.database_url[:50]}...", flush=True)
    sys.stdout.flush()
    print(f"CORS Origins: {settings.cors_origins}", flush=True)
    sys.stdout.flush()

    try:
        print("Initializing database...", flush=True)
        sys.stdout.flush()
        await init_db()
        print("✓ Database initialized successfully", flush=True)
        sys.stdout.flush()
    except Exception as e:
        print(f"✗ Warning: Database initialization failed: {e}", flush=True)
        sys.stdout.flush()
        print("Server will start but database operations may fail", flush=True)
        sys.stdout.flush()
        import traceback
        traceback.print_exc()

    # Initialize Kafka producer
    try:
        print("Initializing Kafka producer...", flush=True)
        sys.stdout.flush()
        kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        kafka_producer = KafkaTaskProducer(bootstrap_servers=kafka_bootstrap_servers)
        await kafka_producer.start()
        print("✓ Kafka producer initialized successfully", flush=True)
        sys.stdout.flush()
    except Exception as e:
        print(f"✗ Warning: Kafka producer initialization failed: {e}", flush=True)
        sys.stdout.flush()
        print("App will start but Kafka events will not be published", flush=True)
        sys.stdout.flush()

    # Initialize background task manager
    try:
        print("Initializing background task manager...", flush=True)
        sys.stdout.flush()
        background_manager = BackgroundTaskManager(kafka_producer)
        await background_manager.start()
        print("✓ Background task manager initialized successfully", flush=True)
        sys.stdout.flush()
    except Exception as e:
        print(f"✗ Warning: Background task manager initialization failed: {e}", flush=True)
        sys.stdout.flush()
        print("App will start but background tasks will not run", flush=True)
        sys.stdout.flush()

    print("✓ Server startup complete", flush=True)
    sys.stdout.flush()
    yield
    
    # Shutdown: Cleanup
    print("Shutting down server...", flush=True)
    
    # Stop background task manager
    if background_manager:
        await background_manager.stop()
        print("✓ Background task manager stopped", flush=True)
    
    # Stop Kafka producer
    if kafka_producer:
        await kafka_producer.stop()
        print("✓ Kafka producer stopped", flush=True)

    print("✓ Server shutdown complete", flush=True)


# Create FastAPI application
app = FastAPI(
    title="TaskFlow API",
    description="REST API for TaskFlow full-stack todo application with Dapr and Kafka integration",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
cors_origins = [origin.strip() for origin in settings.cors_origins.split(",")]
if "http://localhost:3000" not in cors_origins:
    cors_origins.append("http://localhost:3000")
if "http://frontend:3000" not in cors_origins:
    cors_origins.append("http://frontend:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# T179: Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to all API endpoints except health check."""
    # Skip rate limiting for health check and docs
    if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)

    is_limited, remaining, reset_time = rate_limiter.is_rate_limited(request)

    if is_limited:
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Please wait {reset_time} seconds.",
                "retry_after": reset_time,
            },
            headers={"Retry-After": str(reset_time)},
        )

    response = await call_next(request)
    # Add rate limit headers
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Limit"] = str(rate_limiter.max_requests)
    return response


# Health check endpoints
@app.get("/health")
async def health_check_legacy():
    """Legacy health check endpoint with database verification."""
    db_status = "disconnected"
    try:
        # Verify database connection
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        print(f"Database health check failed: {e}")

    # Check Kafka producer status
    kafka_status = "disconnected"
    if kafka_producer and kafka_producer.started:
        kafka_status = "connected"

    return {
        "status": "ok",
        "database": db_status,
        "kafka": kafka_status,
        "environment": settings.environment
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint with database and Kafka verification for Kubernetes."""
    # For basic health, we just need to verify the service is running
    # Database connectivity is optional for basic health status
    db_status = "disconnected"
    try:
        # Verify database connection
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        print(f"Database health check failed: {e}")
        # Don't treat database disconnection as fatal for health check

    # Check Kafka producer status
    kafka_status = "disconnected"
    if kafka_producer and kafka_producer.started:
        kafka_status = "connected"

    health_status = {
        "status": "healthy",  # Service is running
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "backend",
        "version": "1.0.0",
        "database": db_status,
        "kafka": kafka_status,
        "environment": settings.environment
    }

    # Return 503 only if you want strict database connectivity check
    # For basic readiness, we'll return 200 to indicate service is running
    # You can uncomment the next lines if strict DB check is needed
    # if db_status == "disconnected":
    #     return JSONResponse(content=health_status, status_code=503)

    return health_status


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "TaskFlow API",
        "version": "1.0.0",
        "description": "REST API with Dapr and Kafka integration",
        "docs": "/docs",
        "health": "/health",
    }

# Include routers
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(tags_router)
app.include_router(better_auth_router)  # Better Auth compatible endpoints at /api/auth
app.include_router(better_auth_v1_router)  # Better Auth compatible endpoints at /api/v1
app.include_router(main_router)  # Main routes including AI chat functionality
