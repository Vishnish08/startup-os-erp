from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.payroll_schema import PayrollInput, PayrollResponse
from app.services.payroll_service import validate_and_calculate_payroll

router = APIRouter()

@router.post("/validate", response_model=PayrollResponse)
def validate_payroll(data: PayrollInput, session: Session = Depends(get_session)):
    return validate_and_calculate_payroll(data, session)