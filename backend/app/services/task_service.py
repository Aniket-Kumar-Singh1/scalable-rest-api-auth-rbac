"""
Task service — logic for task CRUD operations.
Enforces ownership rules for regular users; admins can access all tasks.
"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.utils.logger import get_logger

logger = get_logger("task_service")


def create_task(payload: TaskCreate, current_user: User, db: Session) -> TaskResponse:
    """Create a new task owned by the current user."""
    new_task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status or "pending",
        user_id=current_user.id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info("Task created: id=%d by user=%d", new_task.id, current_user.id)
    return TaskResponse.model_validate(new_task)


def get_tasks(current_user: User, db: Session) -> List[TaskResponse]:
    """
    Return tasks visible to the current user.
    - Regular users see only their own tasks.
    - Admins see all tasks.
    """
    if current_user.role == "admin":
        tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    else:
        tasks = (
            db.query(Task)
            .filter(Task.user_id == current_user.id)
            .order_by(Task.created_at.desc())
            .all()
        )

    return [TaskResponse.model_validate(t) for t in tasks]


def get_task_by_id(task_id: int, current_user: User, db: Session) -> TaskResponse:
    """
    Retrieve a single task by ID.
    - Regular users can only view their own tasks.
    - Admins can view any task.
    Raises:
        HTTPException 404 if task not found.
        HTTPException 403 if user lacks permission.
    """
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    if current_user.role != "admin" and task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this task.",
        )

    return TaskResponse.model_validate(task)


def update_task(
    task_id: int,
    payload: TaskUpdate,
    current_user: User,
    db: Session,
) -> TaskResponse:
    """
    Update a task by ID.
    - Regular users can only update their own tasks.
    - Admins can update any task.
    Raises:
        HTTPException 404 if task not found.
        HTTPException 403 if user lacks permission.
    """
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    if current_user.role != "admin" and task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task.",
        )

    # Apply only provided fields
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    logger.info("Task updated: id=%d by user=%d", task.id, current_user.id)
    return TaskResponse.model_validate(task)


def delete_task(task_id: int, current_user: User, db: Session) -> dict:
    """
    Delete a task by ID.
    - Regular users can only delete their own tasks.
    - Admins can delete any task.
    Raises:
        HTTPException 404 if task not found.
        HTTPException 403 if user lacks permission.
    """
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    if current_user.role != "admin" and task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this task.",
        )

    db.delete(task)
    db.commit()

    logger.info("Task deleted: id=%d by user=%d", task_id, current_user.id)
    return {"detail": "Task deleted successfully."}
