"""
Authentication schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserRegister(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be between 8 and 128 characters",
    )
    role: UserRole
    university_id: str  # UUID as string


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class TokenRefresh(BaseModel):
    """Schema for token refresh"""
    refresh_token: str


class UserResponse(BaseModel):
    """Schema for user response"""
    id: str
    email: str
    role: str
    email_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
