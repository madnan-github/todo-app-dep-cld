import pytest
import sys
import os

def test_project_structure():
    """Test that the project structure is correct."""
    # Check that key directories exist
    assert os.path.exists("backend"), "Backend directory should exist"
    assert os.path.exists("frontend"), "Frontend directory should exist"
    assert os.path.exists("tests"), "Tests directory should exist"
    
    # Check that key files exist
    assert os.path.exists("backend/src/main.py"), "Main application file should exist"
    assert os.path.exists("backend/app/mcp_server.py"), "MCP server should exist"
    assert os.path.exists("backend/app/openrouter_agent.py"), "OpenRouter agent should exist"
    assert os.path.exists("docker-compose.yml"), "Docker Compose file should exist"
    assert os.path.exists("docker-compose.neon.yml"), "NeonDB Docker Compose file should exist"


def test_backend_modules_exist():
    """Test that backend modules exist."""
    backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
    
    # Check if key backend files exist
    assert os.path.exists(os.path.join(backend_path, 'src', 'main.py')), "src/main.py should exist"
    assert os.path.exists(os.path.join(backend_path, 'src', 'config.py')), "src/config.py should exist"
    assert os.path.exists(os.path.join(backend_path, 'src', 'database.py')), "src/database.py should exist"
    assert os.path.exists(os.path.join(backend_path, 'app', 'mcp_server.py')), "app/mcp_server.py should exist"
    assert os.path.exists(os.path.join(backend_path, 'app', 'openrouter_agent.py')), "app/openrouter_agent.py should exist"
    assert os.path.exists(os.path.join(backend_path, 'app', 'task_direct_handler.py')), "app/task_direct_handler.py should exist"


def test_test_suite_exists():
    """Test that the test suite files exist."""
    tests_path = os.path.join(os.path.dirname(__file__))
    
    # Check if test files exist
    test_files = [
        'test_api_endpoints.py',
        'test_mcp_functions.py', 
        'test_api_routes.py',
        'test_middleware.py',
        'test_auth.py',
        'test_ai_agent.py',
        'test_task_handler.py',
        'test_config.py',
        'test_app.py',
        'test_environment.py'
    ]
    
    for test_file in test_files:
        assert os.path.exists(os.path.join(tests_path, test_file)), f"Test file {test_file} should exist"


def test_docker_files_exist():
    """Test that Docker configuration files exist."""
    assert os.path.exists("docker-compose.yml"), "Docker Compose file should exist"
    assert os.path.exists("docker-compose.neon.yml"), "NeonDB Docker Compose file should exist"


if __name__ == "__main__":
    pytest.main([__file__])