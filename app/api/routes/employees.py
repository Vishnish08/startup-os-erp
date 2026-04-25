from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.employee import Employee
from datetime import datetime

router = APIRouter()

@router.post("/create")
def create_employee(
    name: str,
    email: str,
    department: str,
    designation: str,
    ctc: float,
    basic: float,
    da: float,
    session: Session = Depends(get_session)
):
    employee = Employee(
        name=name,
        email=email,
        department=department,
        designation=designation,
        ctc=ctc,
        basic=basic,
        da=da,
        date_of_joining=datetime.utcnow()
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

@router.get("/all")
def get_all_employees(session: Session = Depends(get_session)):
    return session.exec(select(Employee)).all()