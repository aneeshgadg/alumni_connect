"""
Database models package

Import all models here so Alembic can detect them for migrations.
"""

from app.models.user import User, UserRole, UserStatus
from app.models.student import Student
from app.models.alumni import Alumni, AvailabilityStatus
from app.models.email_verification import EmailVerificationToken

__all__ = [
    "User",
    "UserRole",
    "UserStatus",
    "Student",
    "Alumni",
    "AvailabilityStatus",
    "EmailVerificationToken",
]
