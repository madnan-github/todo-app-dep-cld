import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

# Add backend to path to import modules
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from app.openrouter_agent import process_user_message, process_user_message_sync
from app.task_direct_handler import handle_task_command


@pytest.mark.asyncio
async def test_process_user_message_success():
    """Test successful processing of user message with AI agent."""
    with patch('app.openrouter_agent.Runner') as mock_runner:
        # Mock the runner result
        mock_result = MagicMock()
        mock_result.final_output = "Task added successfully"
        mock_result.steps = []
        
        mock_runner.run = AsyncMock(return_value=mock_result)
        
        result = await process_user_message("user123", 1, "add buy groceries")
        
        assert "response" in result
        assert "tool_calls" in result
        assert "conversation_id" in result
        assert result["response"] == "Task added successfully"


@pytest.mark.asyncio
async def test_process_user_message_timeout():
    """Test fallback when AI agent times out."""
    with patch('app.openrouter_agent.asyncio.wait_for') as mock_wait_for:
        # Simulate a timeout
        mock_wait_for.side_effect = asyncio.TimeoutError()
        
        # Mock the direct handler
        with patch('app.openrouter_agent.handle_task_command') as mock_handler:
            expected_result = {
                "response": "Fallback response",
                "tool_calls": [],
                "conversation_id": 1
            }
            mock_handler.return_value = expected_result
            
            result = await process_user_message("user123", 1, "add buy groceries")
            
            # Verify fallback was called
            mock_handler.assert_called_once_with("user123", "add buy groceries")
            assert result == expected_result


@pytest.mark.asyncio
async def test_process_user_message_exception():
    """Test fallback when AI agent throws exception."""
    with patch('app.openrouter_agent.Runner') as mock_runner:
        # Simulate an exception
        mock_runner.run = AsyncMock(side_effect=Exception("API Error"))
        
        # Mock the direct handler
        with patch('app.openrouter_agent.handle_task_command') as mock_handler:
            expected_result = {
                "response": "Fallback response",
                "tool_calls": [],
                "conversation_id": 1
            }
            mock_handler.return_value = expected_result
            
            result = await process_user_message("user123", 1, "add buy groceries")
            
            # Verify fallback was called
            mock_handler.assert_called_once_with("user123", "add buy groceries")
            assert result == expected_result


def test_process_user_message_sync_success():
    """Test successful synchronous processing of user message."""
    with patch('app.openrouter_agent.Runner') as mock_runner:
        # Mock the runner result
        mock_result = MagicMock()
        mock_result.final_output = "Task added successfully"
        mock_result.steps = []
        
        mock_runner.run_sync = MagicMock(return_value=mock_result)
        
        result = process_user_message_sync("user123", 1, "add buy groceries")
        
        assert "response" in result
        assert "tool_calls" in result
        assert "conversation_id" in result
        assert result["response"] == "Task added successfully"


def test_process_user_message_sync_exception():
    """Test exception handling in synchronous processing."""
    with patch('app.openrouter_agent.Runner') as mock_runner:
        # Simulate an exception
        mock_runner.run_sync = MagicMock(side_effect=Exception("Sync Error"))
        
        # Also mock the fallback handler to avoid database operations
        with patch('app.openrouter_agent.handle_task_command') as mock_handler:
            expected_result = {
                "response": "Fallback response",
                "tool_calls": [],
                "conversation_id": 1
            }
            mock_handler.return_value = expected_result
            
            result = process_user_message_sync("user123", 1, "add buy groceries")
            
            # Verify fallback was called
            mock_handler.assert_called_once_with("user123", "add buy groceries")
            assert result == expected_result


@pytest.mark.asyncio
async def test_process_user_message_with_tool_calls():
    """Test processing message that results in tool calls."""
    with patch('app.openrouter_agent.Runner') as mock_runner:
        # Mock the runner result with tool calls
        mock_step = MagicMock()
        mock_tool_call = MagicMock()
        mock_tool_call.function_name = "add_task"
        mock_tool_call.result = "Task created"
        mock_step.tool_calls = [mock_tool_call]
        
        mock_result = MagicMock()
        mock_result.final_output = "I've added your task"
        mock_result.steps = [mock_step]
        
        mock_runner.run = AsyncMock(return_value=mock_result)
        
        result = await process_user_message("user123", 1, "add buy groceries")
        
        assert result["response"] == "I've added your task"
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "add_task"
        assert result["tool_calls"][0]["result"] == "Task created"


def test_process_user_message_sync_with_tool_calls():
    """Test synchronous processing with tool calls."""
    with patch('app.openrouter_agent.Runner') as mock_runner:
        # Mock the runner result with tool calls
        mock_step = MagicMock()
        mock_tool_call = MagicMock()
        mock_tool_call.function_name = "list_tasks"
        mock_tool_call.result = "Here are your tasks"
        mock_step.tool_calls = [mock_tool_call]
        
        mock_result = MagicMock()
        mock_result.final_output = "Here are your tasks"
        mock_result.steps = [mock_step]
        
        mock_runner.run_sync = MagicMock(return_value=mock_result)
        
        result = process_user_message_sync("user123", 1, "show my tasks")
        
        assert result["response"] == "Here are your tasks"
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "list_tasks"


if __name__ == "__main__":
    import asyncio
    pytest.main([__file__])