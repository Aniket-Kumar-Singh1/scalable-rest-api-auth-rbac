"""
Task CRUD API endpoints.

All routes require authentication (Bearer token).
Regular users operate on their own tasks; admins can manage all tasks.
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_current_admin
from app.db.database import get_db
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ── Create ────────────────────────────────────────────────────────────────


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new task owned by the authenticated user."""
    return task_service.create_task(payload, current_user, db)


# ── Read ──────────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="List tasks",
)
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all tasks visible to the current user.
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
    """Retrieve a single task by its ID (ownership enforced)."""
    return task_service.get_task_by_id(task_id, current_user, db)


# ── Update ────────────────────────────────────────────────────────────────


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
    """Update a task by ID (ownership enforced)."""
    return task_service.update_task(task_id, payload, current_user, db)


# ── Delete ────────────────────────────────────────────────────────────────


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a task",
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a task by ID (ownership enforced)."""
    return task_service.delete_task(task_id, current_user, db)


# ── Admin-only ────────────────────────────────────────────────────────────


@router.get(
    "/admin/all",
    response_model=List[TaskResponse],
    summary="[Admin] List all tasks",
)
def admin_list_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Admin-only: return every task in the system."""
    return task_service.get_tasks(current_user, db)
