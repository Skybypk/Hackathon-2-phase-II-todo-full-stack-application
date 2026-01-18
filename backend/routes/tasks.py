from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
try:
    from ..models import Task as TaskModel
    from ..schemas.task import TaskCreate, TaskUpdate, TaskComplete, Task
    from ..db import get_session
    from ..auth import get_current_user
except ImportError:
    from models import Task as TaskModel
    from schemas.task import TaskCreate, TaskUpdate, TaskComplete, Task
    from db import get_session
    from auth import get_current_user
from datetime import datetime
import uuid

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/tasks", response_model=List[Task])
def get_tasks(
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user"""
    # Convert current_user to UUID if needed
    try:
        user_uuid = uuid.UUID(current_user)
    except ValueError:
        # If current_user is already a UUID object, use it directly
        user_uuid = current_user

    tasks = session.exec(
        select(TaskModel).where(TaskModel.user_id == user_uuid)
    ).all()
    return tasks


@router.post("/tasks", response_model=Task)
def create_task(
    task_create: TaskCreate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user"""
    # Convert current_user to UUID if needed
    try:
        user_uuid = uuid.UUID(current_user)
    except ValueError:
        # If current_user is already a UUID object, use it directly
        user_uuid = current_user

    task = TaskModel(
        user_id=user_uuid,
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID for the current user"""
    # Convert task_id and current_user to UUIDs if needed
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    try:
        user_uuid = uuid.UUID(current_user)
    except ValueError:
        # If current_user is already a UUID object, use it directly
        user_uuid = current_user

    task = session.get(TaskModel, task_uuid)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return task


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task by ID for the current user"""
    # Convert task_id and current_user to UUIDs if needed
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    try:
        user_uuid = uuid.UUID(current_user)
    except ValueError:
        # If current_user is already a UUID object, use it directly
        user_uuid = current_user

    task = session.get(TaskModel, task_uuid)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update task fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task by ID for the current user"""
    # Convert task_id and current_user to UUIDs if needed
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    try:
        user_uuid = uuid.UUID(current_user)
    except ValueError:
        # If current_user is already a UUID object, use it directly
        user_uuid = current_user

    task = session.get(TaskModel, task_uuid)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(
    task_id: str,
    task_complete: TaskComplete,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update the completion status of a specific task by ID for the current user"""
    # Convert task_id and current_user to UUIDs if needed
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    try:
        user_uuid = uuid.UUID(current_user)
    except ValueError:
        # If current_user is already a UUID object, use it directly
        user_uuid = current_user

    task = session.get(TaskModel, task_uuid)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    task.completed = task_complete.completed
    task.updated_at = datetime.utcnow()

    # Set completed_at based on completion status
    if task.completed and task.completed_at is None:
        task.completed_at = datetime.utcnow()
    elif not task.completed:
        task.completed_at = None

    session.add(task)
    session.commit()
    session.refresh(task)
    return task