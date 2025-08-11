from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Worklet(Base):
    __tablename__ = "worklets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    difficulty_level = Column(String, default="Beginner")
    category = Column(String, nullable=True)
    requirements = Column(Text, nullable=True)
    learning_outcomes = Column(Text, nullable=True)
    estimated_duration = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    creator = relationship("User", back_populates="worklets")
