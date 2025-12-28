"""Task management routes."""
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.auth import get_user_id_from_token
from src.database import get_session
from src.models import User, Task, Tag, TaskTag
from src.schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    TagCreate, TagResponse
)

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.get("", response_model=TaskListResponse)
async def get_tasks(
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
    # Filtering
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    tag_id: Optional[int] = Query(None),
    # Search
    search: Optional[str] = Query(None),
    # Sorting
    sort_by: str = Query("created_at", enum=["created_at", "updated_at", "title", "priority"]),
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
        query = query.where(Task.priority == priority)
        count_query = count_query.where(Task.priority == priority)

    if tag_id is not None:
        query = query.join(TaskTag).where(TaskTag.tag_id == tag_id)
        count_query = count_query.join(TaskTag).where(TaskTag.tag_id == tag_id)

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

    # Execute queries
    result = await session.execute(query)
    tasks = result.scalars().unique().all()

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
    """Create a new task."""
    # Create task
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
    )
    session.add(task)
    await session.flush()  # Get the task ID

    # Add tags if provided
    if task_data.tag_ids:
        for tag_id in task_data.tag_ids:
            # Verify tag belongs to user
            tag_result = await session.execute(
                select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
            )
            tag = tag_result.scalar_one_or_none()
            if tag:
                task_tag = TaskTag(task_id=task.id, tag_id=tag_id)
                session.add(task_tag)

    await session.commit()
    await session.refresh(task)

    return TaskResponse.model_validate(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_user_id_from_token),
    session: AsyncSession = Depends(get_session),
):
    """Get a specific task."""
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

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
    """Update a task."""
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await session.commit()
    await session.refresh(task)

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
    await session.commit()
    await session.refresh(task)

    return TaskResponse.model_validate(task)
