from pydantic import BaseModel
from typing import Optional

class PayrollInput(BaseModel):
    employee_id: int
    month: int
    year: int
    ctc: float
    basic: float
    da: float

class PayrollResponse(BaseModel):
    employee_id: int
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
    is_fifty_rule_violated: bool
    was_adjusted: bool
    status: str

    class Config:
        from_attributes = True