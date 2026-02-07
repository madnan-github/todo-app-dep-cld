import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add backend to path to import modules
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from app.task_direct_handler import handle_task_command


def test_handle_task_command_add_task():
    """Test adding a task via direct handler."""
    with patch('app.task_direct_handler.mcp_add_task') as mock_add_task:
        mock_add_task.return_value = {
            "task_id": 1,
            "status": "created",
            "title": "Buy groceries",
            "description": None
        }
        
        result = handle_task_command("user123", "add buy groceries")
        
        assert "response" in result
        assert "tool_calls" in result
        assert "conversation_id" in result
        assert "buy groceries" in result["response"].lower()
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "add_task"


def test_handle_task_command_list_tasks():
    """Test listing tasks via direct handler."""
    with patch('app.task_direct_handler.mcp_list_tasks') as mock_list_tasks:
        mock_list_tasks.return_value = [
            {"id": 1, "title": "Buy groceries", "completed": False},
            {"id": 2, "title": "Walk the dog", "completed": True}
        ]
        
        result = handle_task_command("user123", "show my tasks")
        
        assert "response" in result
        assert "tool_calls" in result
        assert "conversation_id" in result
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "list_tasks"


def test_handle_task_command_complete_task():
    """Test completing a task via direct handler."""
    with patch('app.task_direct_handler.mcp_complete_task') as mock_complete_task:
        mock_complete_task.return_value = {
            "task_id": 1,
            "status": "completed",
            "title": "Buy groceries"
        }
        
        result = handle_task_command("user123", "complete task 1")
        
        assert "response" in result
        assert "tool_calls" in result
        assert "conversation_id" in result
        assert "1" in result["response"]  # Task ID should be in response
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "complete_task"


def test_handle_task_command_delete_task():
    """Test deleting a task via direct handler."""
    with patch('app.task_direct_handler.mcp_delete_task') as mock_delete_task:
        mock_delete_task.return_value = {
            "task_id": 1,
            "status": "deleted",
            "title": "Buy groceries"
        }
        
        result = handle_task_command("user123", "delete task 1")
        
        assert "response" in result
        assert "tool_calls" in result
        assert "conversation_id" in result
        assert "1" in result["response"]  # Task ID should be in response
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "delete_task"


def test_handle_task_command_update_task():
    """Test updating a task via direct handler."""
    with patch('app.task_direct_handler.mcp_update_task') as mock_update_task:
        mock_update_task.return_value = {
            "task_id": 1,
            "status": "updated",
            "title": "Buy weekly groceries"
        }
        
        result = handle_task_command("user123", "update task 1 title to buy weekly groceries")
        
        assert "response" in result
        assert "tool_calls" in result
        assert "conversation_id" in result
        assert "1" in result["response"]  # Task ID should be in response
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "update_task"


def test_handle_task_command_no_task_id():
    """Test commands without task ID."""
    result = handle_task_command("user123", "complete task")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert "specify which task" in result["response"].lower()


def test_handle_task_command_unrecognized():
    """Test unrecognized commands."""
    result = handle_task_command("user123", "random unrecognized command")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert "can help you manage" in result["response"].lower()


def test_handle_task_command_case_insensitive():
    """Test that commands are case insensitive."""
    with patch('app.task_direct_handler.mcp_add_task') as mock_add_task:
        mock_add_task.return_value = {
            "task_id": 1,
            "status": "created",
            "title": "BUY GROCERIES",
            "description": None
        }
        
        result = handle_task_command("user123", "ADD BUY GROCERIES")
        
        assert "response" in result
        assert "buy groceries" in result["response"].lower()


def test_handle_task_command_with_description():
    """Test adding task with description."""
    with patch('app.task_direct_handler.mcp_add_task') as mock_add_task:
        mock_add_task.return_value = {
            "task_id": 1,
            "status": "created",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }
        
        result = handle_task_command("user123", "add buy groceries with description milk, eggs, bread")
        
        assert "response" in result
        assert "buy groceries" in result["response"].lower()
        assert "milk, eggs, bread" in result["response"].lower()


def test_handle_task_command_list_completed_tasks():
    """Test listing completed tasks."""
    with patch('app.task_direct_handler.mcp_list_tasks') as mock_list_tasks:
        mock_list_tasks.return_value = [
            {"id": 1, "title": "Buy groceries", "completed": True}
        ]
        
        result = handle_task_command("user123", "show my completed tasks")
        
        assert "response" in result
        assert "tool_calls" in result
        assert len(result["tool_calls"]) == 1
        # Verify that the status parameter was passed correctly
        mock_list_tasks.assert_called_once_with("user123", "completed")


if __name__ == "__main__":
    pytest.main([__file__])