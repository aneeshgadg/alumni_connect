"""
Application configuration using Pydantic settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load .env file with interpolation disabled to avoid % character issues
load_dotenv(interpolate=False)


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    # Get DATABASE_URL directly from os.environ to avoid interpolation issues
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_URL_ASYNC: str = os.getenv("DATABASE_URL_ASYNC", "")  # Optional, for async operations
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Email (SMTP configuration)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""
    FRONTEND_URL: str = "http://localhost:3000"  # For email links
    
    # Supabase (optional - for Storage, Realtime, etc.)
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

