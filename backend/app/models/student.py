"""
Student model - Student-specific profile and tracking data
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric
import uuid
from app.core.database import Base
from app.models.user import User


class Student(Base):
    """
    Student profile model
    
    Extends User with student-specific information.
    Uses one-to-one relationship with User.
    """
    __tablename__ = "students"
    
    # Primary key (references User)
    id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    # Academic information
    graduation_year = Column(Integer, nullable=True, index=True)  # Can be set later during profile completion
    major = Column(String(100), nullable=True, index=True)
    secondary_major = Column(String(100), nullable=True)
    
    # Career interests (JSONB for flexible structure)
    career_interests = Column(JSONB, nullable=False, default=list)
    target_companies = Column(JSONB, nullable=True)
    target_roles = Column(JSONB, nullable=True)
    target_industries = Column(JSONB, nullable=True)
    
    # Location
    current_location = Column(String(100), nullable=True)
    preferred_locations = Column(JSONB, nullable=True)
    
    # Personal information
    bio = Column(Text, nullable=True)
    hobbies = Column(JSONB, nullable=True)
    interests = Column(JSONB, nullable=True)
    interesting_facts = Column(JSONB, nullable=True)
    
    # External links
    linkedin_url = Column(String(255), nullable=True)
    resume_url = Column(String(255), nullable=True)
    
    # Internal metrics (not public)
    reputation_score = Column(Numeric(5, 2), nullable=False, default=0.0, index=True)
    total_requests = Column(Integer, nullable=False, default=0)
    successful_introductions = Column(Integer, nullable=False, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", backref="student_profile")
    
    # Indexes for JSONB fields (GIN indexes for efficient querying)
    __table_args__ = (
        Index('idx_student_career_interests', 'career_interests', postgresql_using='gin'),
        Index('idx_student_hobbies', 'hobbies', postgresql_using='gin'),
        Index('idx_student_interests', 'interests', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<Student(id={self.id}, graduation_year={self.graduation_year}, major={self.major})>"


