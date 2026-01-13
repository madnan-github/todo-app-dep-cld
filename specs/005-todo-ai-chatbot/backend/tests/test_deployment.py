"""
Test deployment readiness of the Todo AI Chatbot application
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

def test_app_startup():
    """Test that the application can be imported and initialized without errors"""
    try:
        # Try to import the main app
        from app.main import app

        # Verify that app is a FastAPI instance
        assert hasattr(app, 'title'), "App should have a title"
        assert hasattr(app, 'routes'), "App should have routes"

        print(f"✓ App title: {app.title}")
        print("✓ App routes loaded successfully")

    except ImportError as e:
        pytest.fail(f"Failed to import app: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during app import: {e}")

def test_required_modules():
    """Test that all required modules can be imported"""
    required_modules = [
        'fastapi',
        'sqlmodel',
        'asyncpg',
        'python_jose',
        'passlib',
        'uvicorn',
        'dotenv',
    ]

    for module_name in required_modules:
        try:
            if module_name == 'python_jose':
                __import__('jose')
            else:
                __import__(module_name)
            print(f"✓ Module {module_name} is available")
        except ImportError:
            pytest.fail(f"Module {module_name} is not available")

def test_database_connection():
    """Test that database connection can be configured"""
    try:
        from app.database import DATABASE_URL
        assert DATABASE_URL is not None, "DATABASE_URL should be defined"
        print(f"✓ Database URL configured: {DATABASE_URL[:20]}...")
    except Exception as e:
        pytest.fail(f"Database configuration error: {e}")

def test_models_import():
    """Test that all models can be imported"""
    try:
        from app.models import Task, Conversation, Message
        print("✓ All models imported successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import models: {e}")

def test_routes_import():
    """Test that all routes can be imported"""
    try:
        from app.routes import router
        print("✓ Routes imported successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import routes: {e}")

def test_mcp_server_import():
    """Test that MCP server can be imported"""
    try:
        from app.mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
        print("✓ MCP server functions imported successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import MCP server: {e}")

if __name__ == "__main__":
    test_app_startup()
    test_required_modules()
    test_database_connection()
    test_models_import()
    test_routes_import()
    test_mcp_server_import()
    print("\n✓ All deployment readiness tests passed!")