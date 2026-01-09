"""
User model - Base entity for authentication and identity
"""

from sqlalchemy import Column, String, Enum, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration"""
    STUDENT = "student"
    ALUMNI = "alumni"


class UserStatus(str, enum.Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class User(Base):
    """
    Base User model for authentication and identity
    
    This is the parent table for both Student and Alumni.
    Uses single-table inheritance pattern with a role discriminator.
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Multi-tenant isolation
    university_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # User type and status
    role = Column(Enum(UserRole), nullable=False, index=True)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    
    # Email verification
    email_verified = Column(Boolean, nullable=False, default=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships (will be defined in child models)
    # student_profile = relationship("Student", back_populates="user", uselist=False)
    # alumni_profile = relationship("Alumni", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

