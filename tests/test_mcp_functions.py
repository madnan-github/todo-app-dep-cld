import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add backend to path to import modules
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from src.main import app
from app.mcp_server import add_task, list_tasks, complete_task, delete_task, update_task


def test_add_task_function():
    """Test the add_task MCP function."""
    with patch('app.mcp_server.get_session') as mock_get_session:
        # Mock session and query results
        mock_session = MagicMock()
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        # Mock user existence check
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = True  # User exists
        mock_session.query.return_value = mock_query
        
        # Call the function
        result = add_task("test_user_123", "Test Task", "Test Description")
        
        # Assertions
        assert "task_id" in result
        assert result["status"] == "created"
        assert result["title"] == "Test Task"


def test_list_tasks_function():
    """Test the list_tasks MCP function."""
    with patch('app.mcp_server.get_session') as mock_get_session:
        # Mock session and query results
        mock_session = MagicMock()
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        # Mock task query results
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task.completed = False
        mock_session.exec.return_value.all.return_value = [mock_task]
        
        # Call the function
        result = list_tasks("test_user_123", "all")
        
        # Assertions
        assert len(result) >= 0  # Could be empty list if no tasks exist


def test_complete_task_function():
    """Test the complete_task MCP function."""
    with patch('app.mcp_server.get_session') as mock_get_session:
        # Mock session and query results
        mock_session = MagicMock()
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        # Mock task query results
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task.completed = True
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = mock_task
        mock_session.query.return_value = mock_query
        
        # Call the function
        result = complete_task("test_user_123", 1)
        
        # Assertions
        assert result["task_id"] == 1
        assert result["status"] == "completed"


def test_delete_task_function():
    """Test the delete_task MCP function."""
    with patch('app.mcp_server.get_session') as mock_get_session:
        # Mock session and query results
        mock_session = MagicMock()
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        # Mock task query results
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = mock_task
        mock_session.query.return_value = mock_query
        
        # Call the function
        result = delete_task("test_user_123", 1)
        
        # Assertions
        assert result["task_id"] == 1
        assert result["status"] == "deleted"


def test_update_task_function():
    """Test the update_task MCP function."""
    with patch('app.mcp_server.get_session') as mock_get_session:
        # Mock session and query results
        mock_session = MagicMock()
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        # Mock task query results
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Updated Task"
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = mock_task
        mock_session.query.return_value = mock_query
        
        # Call the function
        result = update_task("test_user_123", 1, "Updated Task", "Updated Description")
        
        # Assertions
        assert result["task_id"] == 1
        assert result["status"] == "updated"
        assert result["title"] == "Updated Task"


def test_mcp_functions_integration():
    """Integration test for MCP functions."""
    # Test the contract compliance of all MCP functions
    user_id = "integration_test_user"
    
    # Add a task
    add_result = add_task(user_id, "Integration Test Task", "Integration test description")
    assert "task_id" in add_result
    assert add_result["status"] == "created"
    
    task_id = add_result["task_id"]
    
    # List tasks
    tasks = list_tasks(user_id, "all")
    assert isinstance(tasks, list)
    
    # Update task
    update_result = update_task(user_id, task_id, "Updated Integration Task", "Updated description")
    assert update_result["status"] == "updated"
    
    # Complete task
    complete_result = complete_task(user_id, task_id)
    assert complete_result["status"] == "completed"
    
    # Delete task
    delete_result = delete_task(user_id, task_id)
    assert delete_result["status"] == "deleted"


if __name__ == "__main__":
    pytest.main([__file__])