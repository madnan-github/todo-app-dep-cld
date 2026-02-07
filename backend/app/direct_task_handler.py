"""
Direct Task Handler for AI DevOps Tools Integration
Provides direct implementation of task operations without AI service dependency
"""
from typing import Dict, Any, List, Optional
from .mcp_server import add_task as mcp_add_task, list_tasks as mcp_list_tasks, complete_task as mcp_complete_task, delete_task as mcp_delete_task, update_task as mcp_update_task


def handle_task_command(user_id: str, message: str) -> Dict[str, Any]:
    """
    Directly handle task-related commands without AI service
    """
    message_lower = message.lower().strip()

    # Parse the command
    if any(word in message_lower for word in ["add ", "create ", "new task", "make task"]):
        # Extract task title and description if possible
        parts = message.split(" ", 2)
        if len(parts) >= 2:
            title = parts[1] if len(parts) == 2 else " ".join(parts[1:])
            description = None

            # Check if there's a description after certain keywords
            if " with description " in message:
                title_part, desc_part = message.split(" with description ", 1)
                title = title_part.replace("add ", "").replace("create ", "").replace("new ", "").strip()
                description = desc_part.strip()

            result = mcp_add_task(user_id, title, description)
            return {
                "response": result.get("status") == "created" and f"✓ Added task: '{title}' {f'with description: {description}' if description else ''}" or "Failed to add task",
                "tool_calls": [{"tool_name": "add_task", "result": result}]
            }

    elif any(word in message_lower for word in ["show ", "list ", "display ", "my tasks", "tasks"]):
        status = "all"
        if "completed" in message_lower:
            status = "completed"
        elif "pending" in message_lower or "incomplete" in message_lower:
            status = "pending"

        tasks = mcp_list_tasks(user_id, status)
        if tasks:
            task_list = "\n".join([f"{i+1}. {task['title']} - {'completed' if task['completed'] else 'pending'}" for i, task in enumerate(tasks)])
            response = f"Your tasks:\n{task_list}"
        else:
            response = "No tasks found."

        return {
            "response": response,
            "tool_calls": [{"tool_name": "list_tasks", "result": tasks}]
        }

    elif any("complete" in word or "done" in word for word in message_lower.split()) or "finish" in message_lower:
        # Try to extract task ID from the message
        import re
        task_ids = re.findall(r'\d+', message)
        if task_ids:
            task_id = int(task_ids[0])
            result = mcp_complete_task(user_id, task_id)
            status = result.get("status", "error")
            if status == "completed":
                return {
                    "response": f"✓ Task {task_id} marked as completed",
                    "tool_calls": [{"tool_name": "complete_task", "result": result}]
                }
            else:
                return {
                    "response": f"Could not find task {task_id} to complete",
                    "tool_calls": [{"tool_name": "complete_task", "result": result}]
                }
        else:
            return {
                "response": "Please specify which task to complete by number (e.g., 'complete task 1')",
                "tool_calls": []
            }

    elif any(word in message_lower for word in ["delete ", "remove ", "cancel "]):
        # Try to extract task ID from the message
        import re
        task_ids = re.findall(r'\d+', message)
        if task_ids:
            task_id = int(task_ids[0])
            result = mcp_delete_task(user_id, task_id)
            status = result.get("status", "error")
            if status == "deleted":
                return {
                    "response": f"✓ Task {task_id} deleted",
                    "tool_calls": [{"tool_name": "delete_task", "result": result}]
                }
            else:
                return {
                    "response": f"Could not find task {task_id} to delete",
                    "tool_calls": [{"tool_name": "delete_task", "result": result}]
                }
        else:
            return {
                "response": "Please specify which task to delete by number (e.g., 'delete task 1')",
                "tool_calls": []
            }

    elif any(word in message_lower for word in ["update ", "change ", "modify ", "edit "]):
        # Try to extract task ID and new details
        import re
        task_ids = re.findall(r'\d+', message)
        if task_ids:
            task_id = int(task_ids[0])

            # Extract title and description if mentioned
            title = None
            description = None

            if "title to " in message_lower:
                title_start = message_lower.find("title to ") + len("title to ")
                title_end = message_lower.find(" ", title_start)
                if title_end == -1:  # If it's at the end
                    title_end = len(message_lower)
                title = message_lower[title_start:title_end].strip().strip('"\'')

            if "description to " in message_lower:
                desc_start = message_lower.find("description to ") + len("description to ")
                description = message_lower[desc_start:].strip().strip('"\'')

            result = mcp_update_task(user_id, task_id, title, description)
            status = result.get("status", "error")
            if status == "updated":
                updates = []
                if title: updates.append(f"title to '{title}'")
                if description: updates.append(f"description to '{description}'")
                return {
                    "response": f"✓ Task {task_id} updated: {', '.join(updates)}",
                    "tool_calls": [{"tool_name": "update_task", "result": result}]
                }
            else:
                return {
                    "response": f"Could not find task {task_id} to update",
                    "tool_calls": [{"tool_name": "update_task", "result": result}]
                }
        else:
            return {
                "response": "Please specify which task to update by number (e.g., 'update task 1 title to new title')",
                "tool_calls": []
            }

    # Default response for unrecognized commands
    return {
        "response": f"I can help you manage your tasks. You can ask me to: add, list, complete, delete, or update tasks. For example: 'add Buy groceries' or 'show my tasks'",
        "tool_calls": []
    }