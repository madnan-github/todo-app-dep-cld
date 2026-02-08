"""Task management routes."""
import json
import os
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from src.auth import get_user_id_from_token
from src.database import get_session
from src.models import User, Task, Tag, TaskTag, TaskEvent, RecurrencePatternEnum
from src.schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    TagCreate, TagResponse
)

# Import Dapr client
from src.dapr_client import DaprClient

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


async def get_or_create_tag(
    session: AsyncSession,
    user_id: str,
    tag_name: str
) -> Tag:
    """Get existing tag or create new one (upsert by name)."""
    # Check if tag already exists (case-insensitive)
    result = await session.execute(
        select(Tag).where(Tag.user_id == user_id, Tag.name == tag_name.lower().strip())
    )
    existing_tag = result.scalar_one_or_none()
    if existing_tag:
        return existing_tag

    # Create new tag
    tag = Tag(
        user_id=user_id,
        name=tag_name.lower().strip(),
    )
    session.add(tag)
    await session.flush()
    return tag


async def update_task_tags(
    session: AsyncSession,
    task_id: int,
    user_id: str,
    tag_ids: Optional[List[int]]
) -> None:
    """Update task-tag associations: delete old, create new."""
    # Delete all existing tag associations for this task
    await session.execute(
        delete(TaskTag).where(TaskTag.task_id == task_id)
    )

    if not tag_ids:
        return

    # Create new tag associations
    for tag_id in tag_ids:
        # Verify tag belongs to user
        tag_result = await session.execute(
            select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
        )
        tag = tag_result.scalar_one_or_none()
        if tag:
            task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
            session.add(task_tag)


# Global Dapr client instance
dapr_client = DaprClient(dapr_http_port=os.getenv("DAPR_HTTP_PORT", 3500))

async def publish_task_event(
    task_id: int,
    event_type: str,
    payload: dict
) -> None:
    """Publish a task event via Dapr pub/sub."""
    try:
        # Publish event to appropriate topic via Dapr
        await dapr_client.publish_event("kafka-pubsub", f"task-{event_type}", {
            "taskId": task_id,
            "eventType": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        # If Dapr is unavailable, log the error but don't fail the operation
        print(f"Warning: Failed to publish {event_type} event for task {task_id}: {e}")
        # Optionally, we could fall back to storing in the database
        # For now, we'll just log the failure


def calculate_next_occurrence(
    current_date: datetime,
    pattern: RecurrencePatternEnum,
    interval: int
) -> datetime:
    """Calculate the next occurrence date based on recurrence pattern."""
    if pattern == RecurrencePatternEnum.DAILY:
        return current_date + timedelta(days=interval)
    elif pattern == RecurrencePatternEnum.WEEKLY:
        return current_date + timedelta(weeks=interval)
    elif pattern == RecurrencePatternEnum.MONTHLY:
        # Add months by adjusting year and month
        year = current_date.year
        month = current_date.month + interval
        
        # Handle year overflow
        while month > 12:
            year += 1
            month -= 12
            
        # Handle day overflow (e.g., Jan 31 + 1 month -> Feb 28/29)
        day = min(current_date.day, 31)
        if month == 2:
            # February - check for leap year
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                max_day = 29
            else:
                max_day = 28
            day = min(day, max_day)
        elif month in [4, 6, 9, 11]:
            # Months with 30 days
            day = min(day, 30)
        
        return current_date.replace(year=year, month=month, day=day)
    elif pattern == RecurrencePatternEnum.YEARLY:
        return current_date.replace(year=current_date.year + interval)
    else:
        # Default to daily if pattern is invalid
        return current_date + timedelta(days=interval)


async def create_recurring_task_instance(
    session: AsyncSession,
    original_task: Task
) -> Optional[Task]:
    """Create the next instance of a recurring task."""
    if not original_task.is_recurring or not original_task.recurrence_pattern or not original_task.recurrence_interval:
        return None
    
    # Calculate next occurrence date
    next_date = calculate_next_occurrence(
        original_task.next_occurrence or datetime.utcnow(),
        original_task.recurrence_pattern,
        original_task.recurrence_interval
    )
    
    # Create new task instance
    new_task = Task(
        user_id=original_task.user_id,
        title=original_task.title,
        description=original_task.description,
        priority=original_task.priority,
        due_date=next_date,  # Set due date to next occurrence
        is_recurring=original_task.is_recurring,
        recurrence_pattern=original_task.recurrence_pattern,
        recurrence_interval=original_task.recurrence_interval,
        next_occurrence=calculate_next_occurrence(next_date, original_task.recurrence_pattern, original_task.recurrence_interval),
        parent_task_id=original_task.id  # Link to parent task
    )
    
    session.add(new_task)
    await session.flush()
    
    return new_task


@router.get("", response_model=TaskListResponse)
async def get_tasks(
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
    # Filtering
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    tag_id: Optional[int] = Query(None),
    # Advanced filtering
    due_date_from: Optional[datetime] = Query(None),
    due_date_to: Optional[datetime] = Query(None),
    is_recurring: Optional[bool] = Query(None),
    # Search
    search: Optional[str] = Query(None),
    # Sorting
    sort_by: str = Query("created_at", enum=["created_at", "updated_at", "title", "priority", "due_date"]),
    sort_order: str = Query("desc", enum=["asc", "desc"]),
    # Pagination
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    """Get user's tasks with filtering, search, sorting, and pagination."""
    # Build query
    query = select(Task).where(Task.user_id == user_id)
    count_query = select(func.count(Task.id)).where(Task.user_id == user_id)

    # Apply filters
    if completed is not None:
        query = query.where(Task.completed == completed)
        count_query = count_query.where(Task.completed == completed)

    if priority is not None:
        if "," in priority:
            priorities = [p.strip().upper() for p in priority.split(",")]
            query = query.where(Task.priority.in_(priorities))
            count_query = count_query.where(Task.priority.in_(priorities))
        else:
            query = query.where(Task.priority == priority.upper())
            count_query = count_query.where(Task.priority == priority.upper())

    if tag_id is not None:
        query = query.join(TaskTag).where(TaskTag.tag_id == tag_id)
        count_query = count_query.join(TaskTag).where(TaskTag.tag_id == tag_id)

    # Advanced filters
    if due_date_from is not None:
        query = query.where(Task.due_date >= due_date_from)
        count_query = count_query.where(Task.due_date >= due_date_from)
        
    if due_date_to is not None:
        query = query.where(Task.due_date <= due_date_to)
        count_query = count_query.where(Task.due_date <= due_date_to)
        
    if is_recurring is not None:
        query = query.where(Task.is_recurring == is_recurring)
        count_query = count_query.where(Task.is_recurring == is_recurring)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Task.title.ilike(search_term)) |
            (Task.description.ilike(search_term))
        )
        count_query = count_query.where(
            (Task.title.ilike(search_term)) |
            (Task.description.ilike(search_term))
        )

    # Apply sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    # Execute queries with eager tag loading (T124: JOIN query for tags)
    result = await session.execute(
        query.options(joinedload(Task.tags))
    )
    tasks = result.unique().scalars().all()

    count_result = await session.execute(count_query)
    total = count_result.scalar()

    return TaskListResponse(
        tasks=[TaskResponse.model_validate(task) for task in tasks],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Create a new task with optional tag associations."""
    # Verify user exists before creating task
    from src.models import User
    user_check = await session.execute(select(User).where(User.id == user_id))
    if not user_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session: User does not exist. Please sign out and sign in again.",
        )

    # Calculate next occurrence for recurring tasks
    next_occurrence = None
    if task_data.is_recurring and task_data.recurrence_pattern and task_data.recurrence_interval:
        next_occurrence = calculate_next_occurrence(
            datetime.utcnow(),
            task_data.recurrence_pattern,
            task_data.recurrence_interval
        )

    # Create task
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        # Advanced features
        due_date=task_data.due_date,
        is_recurring=task_data.is_recurring,
        recurrence_pattern=task_data.recurrence_pattern,
        recurrence_interval=task_data.recurrence_interval,
        next_occurrence=next_occurrence
    )
    session.add(task)
    try:
        await session.flush()  # Get the task ID
    except Exception as e:
        await session.rollback()
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session: User account not found. Please sign out and sign in again.",
            )
        raise

    # Add tags if provided (T120, T121: tag creation/upsert and junction creation)
    if task_data.tag_ids:
        await update_task_tags(session, task.id, user_id, task_data.tag_ids)

    # Publish task event via Dapr
    await publish_task_event(
        task.id,
        "create",
        {
            "task_id": task.id,
            "user_id": user_id,
            "title": task.title,
            "completed": task.completed,
            "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "is_recurring": task.is_recurring,
            "recurrence_pattern": task.recurrence_pattern.value if task.recurrence_pattern else None,
            "recurrence_interval": task.recurrence_interval,
            "next_occurrence": task.next_occurrence.isoformat() if task.next_occurrence else None
        }
    )

    await session.commit()

    # Reload task with tags eagerly loaded to avoid async context issues
    result = await session.execute(
        select(Task)
        .options(joinedload(Task.tags))
        .where(Task.id == task.id)
    )
    task = result.unique().scalar_one()

    return TaskResponse.model_validate(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Get a specific task with its tags."""
    result = await session.execute(
        select(Task)
        .options(joinedload(Task.tags))
        .where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.unique().scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Update a task with optional tag association updates."""
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update fields (T123: tag removal logic is handled via tag_ids update)
    update_data = task_data.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)

    for field, value in update_data.items():
        setattr(task, field, value)

    # Update tags if provided
    if tag_ids is not None:
        await update_task_tags(session, task_id, user_id, tag_ids)

    # Publish task event via Dapr
    await publish_task_event(
        task.id,
        "update",
        {
            "task_id": task.id,
            "user_id": user_id,
            "title": task.title,
            "completed": task.completed,
            "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "is_recurring": task.is_recurring,
            "recurrence_pattern": task.recurrence_pattern.value if task.recurrence_pattern else None,
            "recurrence_interval": task.recurrence_interval,
            "next_occurrence": task.next_occurrence.isoformat() if task.next_occurrence else None
        }
    )

    await session.commit()

    # Reload task with tags eagerly loaded to avoid async context issues
    result = await session.execute(
        select(Task)
        .options(joinedload(Task.tags))
        .where(Task.id == task_id)
    )
    task = result.unique().scalar_one()

    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Delete a task."""
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Publish task event via Dapr
    await publish_task_event(
        task.id,
        "delete",
        {
            "task_id": task.id,
            "user_id": user_id,
            "title": task.title
        }
    )

    await session.delete(task)
    await session.commit()


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    task_id: int,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Toggle task completion status."""
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.completed = not task.completed
    
    # If this is a recurring task, create the next instance when completed
    if task.is_recurring and task.recurrence_pattern and task.recurrence_interval:
        await create_recurring_task_instance(session, task)

    # Publish task event via Dapr
    await publish_task_event(
        task.id,
        "complete" if task.completed else "incomplete",
        {
            "task_id": task.id,
            "user_id": user_id,
            "completed": task.completed,
            "title": task.title
        }
    )

    await session.commit()

    # Reload task with tags eagerly loaded to avoid async context issues
    result = await session.execute(
        select(Task)
        .options(joinedload(Task.tags))
        .where(Task.id == task_id)
    )
    task = result.unique().scalar_one()

    return TaskResponse.model_validate(task)


@router.post("/{task_id}/remind", response_model=TaskResponse)
async def send_reminder(
    task_id: int,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Send a reminder for a task."""
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update reminder status
    task.reminder_sent = True
    
    # Publish task event via Dapr
    await publish_task_event(
        task.id,
        "reminder",
        {
            "task_id": task.id,
            "user_id": user_id,
            "title": task.title,
            "due_date": task.due_date.isoformat() if task.due_date else None
        }
    )

    await session.commit()

    # Reload task with tags eagerly loaded to avoid async context issues
    result = await session.execute(
        select(Task)
        .options(joinedload(Task.tags))
        .where(Task.id == task_id)
    )
    task = result.unique().scalar_one()

    return TaskResponse.model_validate(task)
