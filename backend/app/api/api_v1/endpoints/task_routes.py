"""
Task API routes — full CRUD, all require JWT authentication.
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a task owned by the authenticated user."""
    return task_service.create_task(payload, current_user, db)


@router.get(
    "",
    response_model=List[TaskResponse],
    summary="List tasks",
)
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve tasks:
    - Regular users see only their own tasks.
    - Admins see all tasks.
    """
    return task_service.get_tasks(current_user, db)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve a single task. Users can only view their own; admins can view any."""
    return task_service.get_task_by_id(task_id, current_user, db)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a task. Users can only update their own; admins can update any."""
    return task_service.update_task(task_id, payload, current_user, db)


@router.delete(
    "/{task_id}",
    summary="Delete a task",
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a task. Users can only delete their own; admins can delete any."""
    return task_service.delete_task(task_id, current_user, db)
