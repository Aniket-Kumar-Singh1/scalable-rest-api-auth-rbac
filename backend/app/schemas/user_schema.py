from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """Schema for user registration."""
    name: str = Field(..., min_length=1, max_length=100, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=6, max_length=128, examples=["strongPass123"])
    role: Optional[str] = Field(default="user", pattern="^(user|admin)$", examples=["user"])
    
class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["strongPass123"])

class UserResponse(BaseModel):
    """Public user representation (never exposes password_hash)."""
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode

class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    """Decoded JWT payload subset."""
    user_id: Optional[int] = None
    role: Optional[str] = None