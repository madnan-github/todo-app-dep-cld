import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_read_main():
    """Test the main endpoint"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo AI Chatbot API"}

def test_health_check():
    """Test the health check endpoint"""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

if __name__ == "__main__":
    pytest.main()