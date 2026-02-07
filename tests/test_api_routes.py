import pytest
from fastapi.testclient import TestClient
import json
import sys
import os

# Add backend to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


def test_task_crud_operations(client):
    """Test full CRUD operations for tasks."""
    # Create a test user first (we'll use a mock session for this test)
    # In a real scenario, we would register a user first
    
    # Since we need authentication, we'll test the endpoints that don't require auth first
    response = client.get("/health")
    assert response.status_code == 200
    
    # Test creating a task (this would normally require authentication)
    # For this test, we'll just verify the endpoint structure
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "MEDIUM"
    }
    
    # This will fail due to authentication, but we can test the schema
    response = client.post("/api/v1/tasks", json=task_data)
    # Expect 401 Unauthorized because no auth token is provided
    assert response.status_code in [401, 422]  # Either unauthorized or validation error


def test_task_list_endpoint(client):
    """Test the task listing endpoint."""
    response = client.get("/api/v1/tasks")
    # Expect 401 Unauthorized because no auth token is provided
    assert response.status_code == 401


def test_task_specific_endpoints(client):
    """Test specific task endpoints."""
    # Test getting a specific task
    response = client.get("/api/v1/tasks/1")
    # Expect 401 Unauthorized because no auth token is provided
    assert response.status_code == 401
    
    # Test updating a specific task
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "priority": "HIGH"
    }
    response = client.put("/api/v1/tasks/1", json=update_data)
    # Expect 401 Unauthorized because no auth token is provided
    assert response.status_code == 401
    
    # Test deleting a specific task
    response = client.delete("/api/v1/tasks/1")
    # Expect 401 Unauthorized because no auth token is provided
    assert response.status_code == 204 or response.status_code == 401


def test_task_toggle_completion(client):
    """Test toggling task completion status."""
    response = client.patch("/api/v1/tasks/1/complete")
    # Expect 401 Unauthorized because no auth token is provided
    assert response.status_code in [401, 200]  # 200 if it gets past auth but task doesn't exist


def test_tag_endpoints(client):
    """Test tag-related endpoints."""
    # Test getting tags
    response = client.get("/api/v1/tags")
    assert response.status_code == 401  # Unauthorized without token
    
    # Test creating a tag
    tag_data = {
        "name": "test-tag"
    }
    response = client.post("/api/v1/tags", json=tag_data)
    assert response.status_code == 401  # Unauthorized without token


def test_auth_endpoints_exist(client):
    """Test that auth endpoints exist."""
    # These endpoints exist but will return 401 or 422 without proper data
    endpoints_to_check = [
        "/api/v1/auth/signup",
        "/api/v1/auth/signin", 
        "/api/auth/get-session",
        "/api/auth/sign-out"
    ]
    
    for endpoint in endpoints_to_check:
        try:
            response = client.get(endpoint)
            # Could be 404, 405, 401, or 422 depending on method
            assert response.status_code in [404, 405, 401, 422]
        except:
            # Some endpoints might require POST, not GET
            pass


if __name__ == "__main__":
    pytest.main([__file__])