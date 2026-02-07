import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add backend to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.task_direct_handler import handle_task_command


def test_handle_task_command_function_exists():
    """Test that the handle_task_command function exists."""
    assert callable(handle_task_command)


def test_handle_task_command_add_task():
    """Test handling of add task commands."""
    result = handle_task_command("user123", "add buy groceries")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert isinstance(result["tool_calls"], list)


def test_handle_task_command_list_tasks():
    """Test handling of list tasks commands."""
    result = handle_task_command("user123", "show my tasks")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert isinstance(result["tool_calls"], list)


def test_handle_task_command_complete_task():
    """Test handling of complete task commands."""
    result = handle_task_command("user123", "complete task 1")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert isinstance(result["tool_calls"], list)


def test_handle_task_command_delete_task():
    """Test handling of delete task commands."""
    result = handle_task_command("user123", "delete task 1")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert isinstance(result["tool_calls"], list)


def test_handle_task_command_update_task():
    """Test handling of update task commands."""
    result = handle_task_command("user123", "update task 1 title to new title")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert isinstance(result["tool_calls"], list)


def test_handle_task_command_unrecognized():
    """Test handling of unrecognized commands."""
    result = handle_task_command("user123", "random unrecognized command")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert isinstance(result["tool_calls"], list)


def test_handle_task_command_empty_message():
    """Test handling of empty messages."""
    result = handle_task_command("user123", "")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert isinstance(result["tool_calls"], list)


def test_handle_task_command_case_insensitive():
    """Test that command recognition is case insensitive."""
    result_upper = handle_task_command("user123", "ADD Buy Groceries")
    result_lower = handle_task_command("user123", "add buy groceries")
    
    # Both should have similar structure
    assert "response" in result_upper
    assert "response" in result_lower
    assert "tool_calls" in result_upper
    assert "tool_calls" in result_lower


def test_handle_task_command_with_numbers():
    """Test handling of commands with numbers."""
    result = handle_task_command("user123", "mark task 123 as complete")
    
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert isinstance(result["tool_calls"], list)


def test_handle_task_command_return_structure():
    """Test that the function returns the expected structure."""
    result = handle_task_command("user123", "show tasks")
    
    # Verify the structure of the response
    assert isinstance(result, dict)
    assert "response" in result
    assert "tool_calls" in result
    assert "conversation_id" in result
    assert isinstance(result["response"], str)
    assert isinstance(result["tool_calls"], list)
    assert isinstance(result["conversation_id"], int)


if __name__ == "__main__":
    pytest.main([__file__])