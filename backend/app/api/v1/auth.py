"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import uuid

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_verification_token
)
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.models.email_verification import EmailVerificationToken
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    TokenRefresh,
    UserResponse
)
from app.services.email_service import email_service

# All auth endpoints will be under /api/v1/auth/*
router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login", auto_error=False)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    """
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active",
        )
    
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user (student or alumni)
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # For now, accept any university_id value without strict validation.
    # If the provided value is not a valid UUID, generate a new UUID so the insert succeeds.
    try:
        university_uuid = uuid.UUID(user_data.university_id)
    except (ValueError, TypeError):
        university_uuid = uuid.uuid4()
    
    # Create user
    user = User(
        id=uuid.uuid4(),
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role=user_data.role,
        university_id=university_uuid,
        status=UserStatus.ACTIVE,
        email_verified=False
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create Student or Alumni profile based on role
    # Profiles are created with minimal data - users complete them after email verification
    if user.role == UserRole.STUDENT:
        from app.models.student import Student
        student_profile = Student(
            id=user.id,
            graduation_year=None,  # Will be set when user completes profile
            career_interests=[]  # Required field, empty array initially
        )
        db.add(student_profile)
    elif user.role == UserRole.ALUMNI:
        from app.models.alumni import Alumni, AvailabilityStatus
        alumni_profile = Alumni(
            id=user.id,
            graduation_year=None,  # Will be set when user completes profile
            current_role=None,  # Will be set when user completes profile
            current_company=None,  # Will be set when user completes profile
            industry=None,  # Will be set when user completes profile
            availability_status=AvailabilityStatus.OPEN
        )
        db.add(alumni_profile)
    
    db.commit()
    
    # Generate email verification token
    verification_token = generate_verification_token()
    expires_at = datetime.utcnow() + timedelta(days=1)
    
    email_token = EmailVerificationToken(
        user_id=user.id,
        token=verification_token,
        token_type="email_verification",
        expires_at=expires_at
    )
    
    db.add(email_token)
    db.commit()
    
    # Send verification email
    email_service.send_verification_email(
        to_email=user.email,
        verification_token=verification_token,
        user_name=user.email.split("@")[0]
    )
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        role=user.role.value,
        email_verified=user.email_verified,
        created_at=user.created_at
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active"
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # Create tokens
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "email_verified": user.email_verified
        }
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    payload = decode_token(refresh_data.refresh_token)
    
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Create new tokens
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "email_verified": user.email_verified
        }
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information
    """
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        role=current_user.role.value,
        email_verified=current_user.email_verified,
        created_at=current_user.created_at
    )


@router.post("/verify-email")
async def verify_email(
    token: str = Query(..., description="Email verification token"),
    db: Session = Depends(get_db)
):
    """
    Verify user email using verification token
    Token should be passed as query parameter: ?token=xxx
    """
    email_token = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.token == token,
        EmailVerificationToken.token_type == "email_verification",
        EmailVerificationToken.used == False,
        EmailVerificationToken.expires_at > datetime.utcnow()
    ).first()
    
    if not email_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Mark email as verified
    user = db.query(User).filter(User.id == email_token.user_id).first()
    if user:
        user.email_verified = True
        user.email_verified_at = datetime.utcnow()
        email_token.used = True
        db.commit()
        
        return {"message": "Email verified successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
