from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.attrition_service import predict_attrition, predict_project_risk

router = APIRouter()


class EmployeeInput(BaseModel):
    employee_id: Optional[str] = "unknown"
    tenure_months: float = 12
    performance_score: float = 3.0
    salary_ratio: float = 1.0
    absences_last_90d: int = 2
    promotions: int = 0
    overtime_hours: float = 5.0
    team_size: int = 8


class ProjectInput(BaseModel):
    project_id: Optional[str] = "unknown"
    project_name: Optional[str] = "Unnamed Project"
    overdue_tasks: int = 0
    completion_pct: float = 50.0
    days_remaining: int = 30
    team_size: int = 5
    open_blockers: int = 0


@router.post("/intelligence/attrition")
async def attrition_risk(employee: EmployeeInput):
    result = predict_attrition(employee.dict())
    return {
        "employee_id": employee.employee_id,
        **result,
        "recommendation": _attrition_recommendation(result["risk_level"])
    }


@router.post("/intelligence/project-risk")
async def project_risk(project: ProjectInput):
    result = predict_project_risk(project.dict())
    return {
        "project_id": project.project_id,
        "project_name": project.project_name,
        **result,
        "recommendation": _project_recommendation(result["risk_level"])
    }


@router.get("/intelligence/health")
async def intelligence_health():
    return {"status": "ok", "models": ["xgboost_attrition", "rule_based_project_risk"]}


def _attrition_recommendation(risk_level: str) -> str:
    return {
        "HIGH": "Immediate 1:1 with manager. Review compensation and workload.",
        "MEDIUM": "Schedule check-in. Consider growth opportunities or workload adjustment.",
        "LOW": "Employee appears stable. Continue regular engagement."
    }[risk_level]


def _project_recommendation(risk_level: str) -> str:
    return {
        "HIGH": "Escalate to founder. Reassign resources or revise scope immediately.",
        "MEDIUM": "Review blockers in next standup. Consider timeline adjustment.",
        "LOW": "Project on track. Maintain current velocity."
    }[risk_level]