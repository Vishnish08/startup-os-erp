from sqlmodel import Session, select
from app.models.task import Task
from app.schemas.task_schema import TaskCreate
from datetime import datetime
from typing import List, Optional
import json

def detect_circular_dependency(task_id: int, dependencies: List[int], session: Session) -> bool:
    visited = set()
    
    def dfs(current_id):
        if current_id in visited:
            return True
        visited.add(current_id)
        task = session.get(Task, current_id)
        if task and task.dependencies:
            deps = json.loads(task.dependencies)
            for dep in deps:
                if dfs(dep):
                    return True
        visited.remove(current_id)
        return False
    
    for dep_id in dependencies:
        if dep_id == task_id:
            return True
        if dfs(dep_id):
            return True
    return False

def create_task(task_data: TaskCreate, session: Session):
    dependencies = task_data.dependencies or []
    
    if dependencies:
        has_circular = detect_circular_dependency(0, dependencies, session)
        if has_circular:
            raise ValueError("Circular dependency detected")
    
    task = Task(
        milestone_id=task_data.milestone_id,
        assigned_to=task_data.assigned_to,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        dependencies=json.dumps(dependencies) if dependencies else None
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_overdue_tasks(session: Session):
    now = datetime.utcnow()
    tasks = session.exec(select(Task)).all()
    overdue = []
    for task in tasks:
        if task.due_date and task.due_date < now and task.status != "completed":
            task.is_overdue = True
            task.status = "overdue"
            session.add(task)
            overdue.append(task)
    session.commit()
    return overdue

def get_project_health(project_id: int, session: Session):
    from app.models.milestone import Milestone
    milestones = session.exec(
        select(Milestone).where(Milestone.project_id == project_id)
    ).all()
    
    if not milestones:
        return {"health_score": 0, "label": "red", "message": "No milestones found"}
    
    total_tasks = 0
    completed_tasks = 0
    on_time_milestones = 0
    
    for milestone in milestones:
        tasks = session.exec(
            select(Task).where(Task.milestone_id == milestone.id)
        ).all()
        total_tasks += len(tasks)
        completed_tasks += sum(1 for t in tasks if t.status == "completed")
        
        now = datetime.utcnow()
        if milestone.status == "completed" and milestone.completed_at:
            if milestone.completed_at <= milestone.due_date:
                on_time_milestones += 1
    
    task_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    milestone_percent = (on_time_milestones / len(milestones) * 100) if milestones else 0
    health_score = (task_percent * 0.5) + (milestone_percent * 0.5)
    
    if health_score > 80:
        label = "green"
    elif health_score >= 50:
        label = "yellow"
    else:
        label = "red"
    
    return {
        "project_id": project_id,
        "health_score": round(health_score, 2),
        "label": label,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "on_time_milestones": on_time_milestones,
        "total_milestones": len(milestones)
    }