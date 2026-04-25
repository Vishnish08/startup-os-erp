from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    doc_type: str
    raw_file_path: str
    extracted_data: Optional[str] = None
    masked_data: Optional[str] = None
    confidence_score: float = 0.0
    is_verified: bool = False
    rejection_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)