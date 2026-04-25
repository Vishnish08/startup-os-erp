from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from app.database import get_session
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import create_task, get_overdue_tasks, get_project_health
from app.models.task import Task
from typing import List

router = APIRouter()

@router.post("/create", response_model=TaskResponse)
def create_new_task(task: TaskCreate, session: Session = Depends(get_session)):
    try:
        return create_task(task, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/overdue", response_model=List[TaskResponse])
def get_all_overdue_tasks(session: Session = Depends(get_session)):
    return get_overdue_tasks(session)

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, update: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/all")
def get_all_tasks(session: Session = Depends(get_session)):
    from sqlmodel import select
    tasks = session.exec(select(Task)).all()
    return tasks