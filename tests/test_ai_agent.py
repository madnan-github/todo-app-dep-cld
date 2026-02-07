import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add backend to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.openrouter_agent import process_user_message, process_user_message_sync


def test_process_user_message_function_exists():
    """Test that the process_user_message function exists."""
    assert callable(process_user_message)


def test_process_user_message_sync_function_exists():
    """Test that the process_user_message_sync function exists."""
    assert callable(process_user_message_sync)


def test_process_user_message_parameters():
    """Test that process_user_message accepts the correct parameters."""
    # This test will check if the function signature is correct
    import inspect
    sig = inspect.signature(process_user_message)
    params = list(sig.parameters.keys())
    
    # The function should accept user_id, conversation_id, and message
    expected_params = ["user_id", "conversation_id", "message"]
    for param in expected_params:
        assert param in params


def test_process_user_message_sync_parameters():
    """Test that process_user_message_sync accepts the correct parameters."""
    import inspect
    sig = inspect.signature(process_user_message_sync)
    params = list(sig.parameters.keys())
    
    # The function should accept user_id, conversation_id, and message
    expected_params = ["user_id", "conversation_id", "message"]
    for param in expected_params:
        assert param in params


def test_process_user_message_fallback_behavior():
    """Test the fallback behavior of process_user_message."""
    # Mock the external dependencies to force fallback behavior
    with patch('app.openrouter_agent.asyncio.wait_for') as mock_wait_for:
        # Simulate a timeout to trigger fallback
        mock_wait_for.side_effect = TimeoutError()
        
        # Also mock the handle_task_command function that's used in fallback
        with patch('app.openrouter_agent.handle_task_command') as mock_handle_task:
            mock_handle_task.return_value = {
                "response": "Fallback response",
                "tool_calls": [],
                "conversation_id": 1
            }
            
            result = process_user_message("user123", 1, "test message")
            
            # Verify fallback was called
            mock_handle_task.assert_called_once_with("user123", "test message")


def test_process_user_message_exception_handling():
    """Test exception handling in process_user_message."""
    # Mock the external dependencies to force exception handling
    with patch('app.openrouter_agent.asyncio.wait_for') as mock_wait_for:
        # Simulate an exception to trigger fallback
        mock_wait_for.side_effect = Exception("Test exception")
        
        # Also mock the handle_task_command function that's used in fallback
        with patch('app.openrouter_agent.handle_task_command') as mock_handle_task:
            mock_handle_task.return_value = {
                "response": "Fallback response",
                "tool_calls": [],
                "conversation_id": 1
            }
            
            result = process_user_message("user123", 1, "test message")
            
            # Verify fallback was called
            mock_handle_task.assert_called_once_with("user123", "test message")


def test_process_user_message_sync_exception_handling():
    """Test exception handling in process_user_message_sync."""
    # Mock the external dependencies to force exception handling
    with patch('app.openrouter_agent.Runner.run_sync') as mock_run_sync:
        # Simulate an exception
        mock_run_sync.side_effect = Exception("Test exception")
        
        result = process_user_message_sync("user123", 1, "test message")
        
        # Verify the function returns a proper response even with exception
        assert "response" in result
        assert "tool_calls" in result
        assert "conversation_id" in result


if __name__ == "__main__":
    pytest.main([__file__])