from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: Optional[str] = None
    department: str
    designation: str
    date_of_joining: datetime
    ctc: float
    basic: float
    da: float
    is_active: bool = True
    overtime_hours: float = 0.0
    tasks_completed: int = 0
    tasks_total: int = 0
    workload_score: float = 0.0
    salary_growth_percent: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)