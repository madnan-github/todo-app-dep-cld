import pytest
import sys
import os
# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp_server import add_task, list_tasks, complete_task, delete_task, update_task


def test_add_task_contract():
    """Test the add_task MCP tool contract"""
    # Test basic functionality
    result = add_task("test_user_123", "Test task title", "Test description")

    # Verify the contract: {"task_id": int, "status": "created", "title": str}
    assert "task_id" in result
    assert isinstance(result["task_id"], int)
    assert result["status"] == "created"
    assert "title" in result
    assert result["title"] == "Test task title"


def test_list_tasks_contract():
    """Test the list_tasks MCP tool contract"""
    # Test basic functionality
    tasks = list_tasks("test_user_123", "all")

    # Verify the contract: [{"id": int, "title": str, "completed": bool}]
    if tasks:  # If there are tasks returned
        for task in tasks:
            assert "id" in task
            assert isinstance(task["id"], int)
            assert "title" in task
            assert isinstance(task["title"], str)
            assert "completed" in task
            assert isinstance(task["completed"], bool)


def test_complete_task_contract():
    """Test the complete_task MCP tool contract"""
    # Test basic functionality (using mock task ID)
    result = complete_task("test_user_123", 1)

    # Verify the contract: {"task_id": int, "status": "completed", "title": str}
    assert "task_id" in result
    assert isinstance(result["task_id"], int)
    assert result["status"] == "completed"
    assert "title" in result
    assert isinstance(result["title"], str)


def test_delete_task_contract():
    """Test the delete_task MCP tool contract"""
    # Test basic functionality (using mock task ID)
    result = delete_task("test_user_123", 1)

    # Verify the contract: {"task_id": int, "status": "deleted", "title": str}
    assert "task_id" in result
    assert isinstance(result["task_id"], int)
    assert result["status"] == "deleted"
    assert "title" in result
    assert isinstance(result["title"], str)


def test_update_task_contract():
    """Test the update_task MCP tool contract"""
    # Test basic functionality (using mock task ID)
    result = update_task("test_user_123", 1, "Updated title", "Updated description")

    # Verify the contract: {"task_id": int, "status": "updated", "title": str}
    assert "task_id" in result
    assert isinstance(result["task_id"], int)
    assert result["status"] == "updated"
    assert "title" in result
    assert isinstance(result["title"], str)
    assert result["title"] == "Updated title"


if __name__ == "__main__":
    pytest.main()