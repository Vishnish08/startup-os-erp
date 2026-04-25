from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskCreate(BaseModel):
    milestone_id: int
    assigned_to: int
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    dependencies: Optional[List[int]] = None

class TaskUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    blocked_reason: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    milestone_id: int
    assigned_to: int
    title: str
    status: str
    priority: str
    is_overdue: bool
    due_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True