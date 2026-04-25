from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Milestone(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    name: str
    description: Optional[str] = None
    status: str = "pending"
    due_date: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)