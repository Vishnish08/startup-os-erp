from sqlmodel import Session, select
from app.models.events import Event
from app.models.task import Task
from app.models.employee import Employee
from app.models.payroll import Payroll
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

def store_event(event_type: str, payload: dict, session: Session):
    event = Event(
        event_type=event_type,
        payload=json.dumps(payload),
        status="processed",
        triggered_at=datetime.utcnow(),
        processed_at=datetime.utcnow()
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

def get_employee_performance_trend(employee_id: int, session: Session):
    tasks = session.exec(
        select(Task).where(Task.assigned_to == employee_id)
    ).all()
    
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == "completed")
    overdue = sum(1 for t in tasks if t.is_overdue)
    
    payrolls = session.exec(
        select(Payroll).where(Payroll.employee_id == employee_id)
    ).all()
    
    avg_net_salary = sum(p.net_salary for p in payrolls) / len(payrolls) if payrolls else 0
    
    return {
        "employee_id": employee_id,
        "total_tasks": total,
        "completed_tasks": completed,
        "overdue_tasks": overdue,
        "completion_rate": round(completed / total * 100, 2) if total > 0 else 0,
        "average_net_salary": round(avg_net_salary, 2),
        "payroll_cycles": len(payrolls)
    }

def get_past_delays(session: Session):
    overdue_tasks = session.exec(
        select(Task).where(Task.is_overdue == True)
    ).all()
    
    return {
        "total_overdue_ever": len(overdue_tasks),
        "overdue_tasks": [
            {
                "task_id": t.id,
                "title": t.title,
                "due_date": str(t.due_date),
                "assigned_to": t.assigned_to
            }
            for t in overdue_tasks[:10]
        ]
    }

def get_system_memory(session: Session):
    events = session.exec(select(Event)).all()
    employees = session.exec(select(Employee)).all()
    
    return {
        "total_events_logged": len(events),
        "recent_events": [
            {
                "type": e.event_type,
                "triggered_at": str(e.triggered_at)
            }
            for e in events[-10:]
        ],
        "employee_trends": [
            get_employee_performance_trend(e.id, session)
            for e in employees[:5]
        ],
        "past_delays": get_past_delays(session)
    }