from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Session
from .database import get_session
from src.models import Message, Conversation, Task
try:
    from app.openrouter_agent import process_user_message
except ImportError:
    # Fallback if openrouter agent is not available
    async def process_user_message(user_id: str, conversation_id: int, message: str):
        from app.task_direct_handler import handle_task_command
        return handle_task_command(user_id, message)

from .mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list = []

@router.post("/api/{user_id}/chat")
async def chat(user_id: str, request: ChatRequest, background_tasks: BackgroundTasks):
    """
    Process a user message and return AI response with any tool execution results
    """
    # Create or get conversation
    conversation_id = request.conversation_id

    # If no conversation_id provided, create a new conversation
    if not conversation_id:
        conversation = Conversation(user_id=user_id)
        # In a real implementation, you'd save this to the database
        # For now, we'll simulate a new conversation ID
        conversation_id = int(str(uuid.uuid4().int)[:8])  # Simple ID generation
    else:
        # Verify conversation belongs to user
        # In a real implementation, you'd fetch from DB and verify ownership
        pass

    # Store user message in database
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="user",
        content=request.message
    )

    try:
        # Process message with AI agent
        result = await process_user_message(user_id, conversation_id, request.message)
    except Exception as e:
        print(f"Error processing chat message: {str(e)}")
        # Fallback to direct handler if there's an error
        from .task_direct_handler import handle_task_command
        result = handle_task_command(user_id, request.message)

    # Store AI response in database
    ai_message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="assistant",
        content=result.get("response", "")
    )

    # Update conversation timestamp
    # In a real implementation, you'd update the conversation in DB

    return ChatResponse(
        conversation_id=conversation_id,
        response=result.get("response", ""),
        tool_calls=result.get("tool_calls", [])
    )

# Additional endpoints for task management (if needed separately from AI)
@router.get("/api/{user_id}/tasks")
async def get_tasks(user_id: str, status: Optional[str] = "all"):
    """Get user's tasks"""
    tasks = list_tasks(user_id, status)
    return {"tasks": tasks}

@router.post("/api/{user_id}/tasks")
async def create_task(user_id: str, title: str, description: Optional[str] = None):
    """Create a new task"""
    task = add_task(user_id, title, description)
    return {"task": task}