from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.project import Project
from app.models.milestone import Milestone
from app.services.task_service import get_project_health
from datetime import datetime

router = APIRouter()

@router.post("/create")
def create_project(name: str, description: str, start_date: datetime, end_date: datetime, session: Session = Depends(get_session)):
    project = Project(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.get("/health/{project_id}")
def project_health(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return get_project_health(project_id, session)

@router.get("/all")
def get_all_projects(session: Session = Depends(get_session)):
    projects = session.exec(select(Project)).all()
    return projects

@router.post("/{project_id}/milestone")
def create_milestone(project_id: int, name: str, due_date: datetime, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    milestone = Milestone(
        project_id=project_id,
        name=name,
        due_date=due_date
    )
    session.add(milestone)
    session.commit()
    session.refresh(milestone)
    return milestone