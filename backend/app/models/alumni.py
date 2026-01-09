"""
Alumni model - Alumni-specific profile and availability data
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Index, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric
import uuid
import enum
from app.core.database import Base
from app.models.user import User


class AvailabilityStatus(str, enum.Enum):
    """Alumni availability status"""
    OPEN = "open"
    LIMITED = "limited"
    CLOSED = "closed"


class Alumni(Base):
    """
    Alumni profile model
    
    Extends User with alumni-specific information.
    Uses one-to-one relationship with User.
    """
    __tablename__ = "alumni"
    
    # Primary key (references User)
    id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    # Academic information
    graduation_year = Column(Integer, nullable=False)
    degree = Column(String(100), nullable=True)
    major = Column(String(100), nullable=True)
    
    # Professional information
    current_role = Column(String(100), nullable=True)  # Can be set later during profile completion
    current_company = Column(String(100), nullable=True, index=True)  # Can be set later
    industry = Column(String(100), nullable=True, index=True)  # Can be set later
    location = Column(String(100), nullable=True, index=True)
    years_experience = Column(Integer, nullable=True)
    
    # Career history
    previous_companies = Column(JSONB, nullable=True)
    
    # Personal information
    bio = Column(Text, nullable=True)
    hobbies = Column(JSONB, nullable=True)
    interests = Column(JSONB, nullable=True)
    interesting_facts = Column(JSONB, nullable=True)
    
    # External links
    linkedin_url = Column(String(255), nullable=True)
    
    # Availability and preferences
    availability_status = Column(Enum(AvailabilityStatus), nullable=False, default=AvailabilityStatus.OPEN, index=True)
    request_preferences = Column(JSONB, nullable=True)
    max_requests_per_month = Column(Integer, nullable=False, default=5)
    current_month_requests = Column(Integer, nullable=False, default=0)
    
    # Internal metrics (not public)
    helpfulness_score = Column(Numeric(5, 2), nullable=False, default=0.0, index=True)
    total_introductions = Column(Integer, nullable=False, default=0)
    response_rate = Column(Numeric(5, 2), nullable=False, default=0.0)
    avg_response_time_hours = Column(Numeric(8, 2), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", backref="alumni_profile")
    
    # Indexes for JSONB fields and composite indexes
    __table_args__ = (
        Index('idx_alumni_career', 'industry', 'current_role'),
        Index('idx_alumni_hobbies', 'hobbies', postgresql_using='gin'),
        Index('idx_alumni_interests', 'interests', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<Alumni(id={self.id}, current_role={self.current_role}, company={self.current_company})>"


