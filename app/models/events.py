from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str
    payload: Optional[str] = None
    status: str = "pending"
    triggered_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None