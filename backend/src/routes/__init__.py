"""Routes package."""
from src.routes.auth import router as auth_router
from src.routes.tasks import router as tasks_router

__all__ = ["auth_router", "tasks_router"]
