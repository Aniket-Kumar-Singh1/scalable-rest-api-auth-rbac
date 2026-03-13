from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, examples=["Complete project report"])
    description: Optional[str] = Field(default=None, examples=["Write the final report for Q4."])
    status: Optional[str] = Field(
        default="pending",
        pattern="^(pending|in_progress|completed)$",
        examples=["pending"],
    )

class TaskUpdate(BaseModel):
    """Schema for updating an existing task (all fields optional)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    status: Optional[str] = Field(
        default=None,
        pattern="^(pending|in_progress|completed)$",
    )

class TaskResponse(BaseModel):
    """Public task representation."""
    id: int
    title: str
    description: Optional[str]
    status: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
