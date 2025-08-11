from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WorkletBase(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty_level: Optional[str] = "Beginner"
    category: Optional[str] = None
    requirements: Optional[str] = None
    learning_outcomes: Optional[str] = None
    estimated_duration: Optional[str] = None

class WorkletCreate(WorkletBase):
    pass

class WorkletUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: Optional[str] = None
    category: Optional[str] = None
    requirements: Optional[str] = None
    learning_outcomes: Optional[str] = None
    estimated_duration: Optional[str] = None

class WorkletOut(WorkletBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
