from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: Priority
    due_date: datetime
    status: Status = Status.PENDING

    @validator('title')
    def title_min_length(cls, v):
        if len(v) < 3:
            raise ValueError('Title must be at least 3 characters long')
        return v

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    priority: Priority = None
    due_date: datetime = None
    status: Status = None

class TaskResponse(BaseModel):
    _id: str
    title: str
    description: str
    priority: Priority
    due_date: datetime 
    status: Status
