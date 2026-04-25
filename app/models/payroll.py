from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Payroll(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    month: int
    year: int
    ctc: float
    basic: float
    da: float
    pf_employee: float
    pf_employer: float
    tds: float
    gross_salary: float
    net_salary: float
    is_fifty_rule_violated: bool = False
    was_adjusted: bool = False
    status: str = "pending"
    processed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)