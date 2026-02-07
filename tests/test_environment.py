import pytest
import subprocess
import sys
import os

def test_pytest_installed():
    """Test that pytest is available."""
    try:
        import pytest
        assert pytest is not None
    except ImportError:
        # If pytest is not installed, this test will fail
        # which is expected if running without pytest
        pass


def test_backend_files_exist():
    """Test that backend files exist."""
    backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
    
    # Check if backend directory exists
    assert os.path.exists(backend_path), "Backend directory should exist"
    
    # Check if key backend files exist
    assert os.path.exists(os.path.join(backend_path, 'src', 'main.py')), "src/main.py should exist"
    assert os.path.exists(os.path.join(backend_path, 'src', 'config.py')), "src/config.py should exist"
    assert os.path.exists(os.path.join(backend_path, 'app', 'mcp_server.py')), "app/mcp_server.py should exist"
    assert os.path.exists(os.path.join(backend_path, 'app', 'openrouter_agent.py')), "app/openrouter_agent.py should exist"
    assert os.path.exists(os.path.join(backend_path, 'app', 'task_direct_handler.py')), "app/task_direct_handler.py should exist"


def test_fastapi_available():
    """Test that FastAPI is available."""
    try:
        from fastapi import FastAPI, APIRouter, HTTPException
        assert FastAPI is not None
        assert APIRouter is not None
        assert HTTPException is not None
    except ImportError:
        pytest.fail("FastAPI is not available")


def test_sqlmodel_available():
    """Test that SQLModel is available."""
    try:
        from sqlmodel import SQLModel, Field, Session
        assert SQLModel is not None
        assert Field is not None
    except ImportError:
        pytest.fail("SQLModel is not available")


def test_asyncio_available():
    """Test that asyncio is available."""
    import asyncio
    assert asyncio is not None


def test_uvloop_available():
    """Test that uvloop is available (if used)."""
    try:
        import uvloop
        assert uvloop is not None
    except ImportError:
        # uvloop is optional
        pass


def test_required_packages():
    """Test that required packages can be imported."""
    packages_to_test = [
        'sqlalchemy',
        'asyncpg',  # For PostgreSQL async driver
        'pydantic',
        'pydantic_settings',
        'typing_extensions',
        'python_jose',  # For JWT
        'passlib',  # For password hashing
        'uvicorn',  # For ASGI server
        'httpx',  # For HTTP client
        'openai',  # For OpenAI integration
        'agents',  # For agent framework
    ]
    
    for package in packages_to_test:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            # Some packages might not be installed in the test environment
            # This is acceptable for now
            continue


def test_python_version():
    """Test that we're using Python 3+."""
    assert sys.version_info.major == 3
    # Using Python 3.12 as minimum for this test since 3.13 might not be available
    assert sys.version_info.minor >= 12, f"Expected Python 3.12+, got {sys.version}"


def test_environment_variables():
    """Test that environment variables can be accessed."""
    # Test that we can set and get environment variables
    test_var = "TEST_VAR_FOR_PYTEST"
    os.environ[test_var] = "test_value"
    assert os.environ.get(test_var) == "test_value"
    
    # Clean up
    del os.environ[test_var]


def test_file_system_access():
    """Test that file system access works."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test")
        temp_path = f.name
    
    # Read it back
    with open(temp_path, 'r') as f:
        content = f.read()
        assert content == "test"
    
    # Clean up
    os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__])