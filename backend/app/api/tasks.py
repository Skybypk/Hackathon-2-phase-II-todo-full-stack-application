from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select, update
from typing import List
from uuid import UUID
from app.database.engine import engine
from app.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskRead])
def get_tasks(current_user_id: str = Depends(get_current_user)):
    """Get all tasks for the current user."""
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == UUID(current_user_id))
        tasks = session.exec(statement).all()
        return tasks


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, current_user_id: str = Depends(get_current_user)):
    """Create a new task for the current user."""
    with Session(engine) as session:
        # Verify user exists
        user = session.get(User, current_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db_task = Task.model_validate(task)
        db_task.user_id = UUID(current_user_id)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: UUID, current_user_id: str = Depends(get_current_user)):
    """Get a specific task by ID."""
    with Session(engine) as session:
        task = session.get(Task, task_id)

        # Check if task exists and belongs to current user
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if str(task.user_id) != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this task")

        return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: UUID, task_update: TaskUpdate, current_user_id: str = Depends(get_current_user)):
    """Update a specific task."""
    with Session(engine) as session:
        task = session.get(Task, task_id)

        # Check if task exists and belongs to current user
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if str(task.user_id) != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        # Update task fields
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update timestamps
        from datetime import datetime
        task.updated_at = datetime.now()  # Update to current time

        # Handle completion timestamp
        if hasattr(task_update, 'completed') and task_update.completed is not None:
            if task_update.completed and not task.completed_at:
                task.completed_at = task.updated_at
            elif not task_update.completed:
                task.completed_at = None

        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@router.patch("/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(task_id: UUID, completed: bool, current_user_id: str = Depends(get_current_user)):
    """Toggle task completion status."""
    with Session(engine) as session:
        task = session.get(Task, task_id)

        # Check if task exists and belongs to current user
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if str(task.user_id) != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        # Update completion status
        task.completed = completed
        from datetime import datetime
        task.updated_at = datetime.now()  # Update to current time

        # Set completion timestamp
        if completed:
            task.completed_at = task.updated_at
        else:
            task.completed_at = None

        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, current_user_id: str = Depends(get_current_user)):
    """Delete a specific task."""
    with Session(engine) as session:
        task = session.get(Task, task_id)

        # Check if task exists and belongs to current user
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if str(task.user_id) != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this task")

        session.delete(task)
        session.commit()
        return