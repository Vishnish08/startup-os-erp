from sqlmodel import Session, select
from app.models.task import Task
from app.models.employee import Employee
from app.services.event_service import trigger_event
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def execute_action(action_type: str, payload: dict, session: Session):
    if action_type == "reassign_overloaded":
        return reassign_overloaded_employee(payload, session)
    elif action_type == "escalate_overdue":
        return escalate_overdue_tasks(payload, session)
    elif action_type == "send_reminder":
        return send_whatsapp_reminder(payload)
    else:
        return {"status": "error", "message": f"Unknown action: {action_type}"}

def reassign_overloaded_employee(payload: dict, session: Session):
    employee_id = payload.get("employee_id")
    employee = session.get(Employee, employee_id)
    
    if not employee:
        return {"status": "error", "message": "Employee not found"}
    
    # Find overdue tasks for this employee
    tasks = session.exec(
        select(Task).where(
            Task.assigned_to == employee_id,
            Task.status != "completed"
        )
    ).all()
    
    if len(tasks) > 2:
        trigger_event("TASK_OVERDUE", {
            "employee_id": employee_id,
            "task_count": len(tasks)
        })
        return {
            "status": "success",
            "action": "reassignment_suggested",
            "employee_id": employee_id,
            "overdue_task_count": len(tasks),
            "message": f"Employee {employee.name} has {len(tasks)} pending tasks. Reassignment recommended."
        }
    
    return {"status": "ok", "message": "Workload is manageable"}

def escalate_overdue_tasks(payload: dict, session: Session):
    now = datetime.utcnow()
    two_days_ago = now - timedelta(days=2)
    
    tasks = session.exec(select(Task)).all()
    escalated = []
    
    for task in tasks:
        if (task.due_date and 
            task.due_date < two_days_ago and 
            task.status != "completed"):
            
            task.status = "blocked"
            task.blocked_reason = "Escalated due to overdue > 2 days"
            session.add(task)
            escalated.append(task.id)
            
            trigger_event("TASK_OVERDUE", {
                "task_id": task.id,
                "assigned_to": task.assigned_to,
                "days_overdue": (now - task.due_date).days
            })
    
    session.commit()
    return {
        "status": "success",
        "escalated_tasks": escalated,
        "count": len(escalated)
    }

def send_whatsapp_reminder(payload: dict):
    employee_id = payload.get("employee_id")
    message = payload.get("message", "You have pending tasks!")
    
    # Mock WhatsApp send (in production use Twilio/Meta API)
    print(f"📱 Sending WhatsApp to employee {employee_id}: {message}")
    
    return {
        "status": "success",
        "message": f"Reminder sent to employee {employee_id}",
        "content": message
    }

def run_autonomous_checks(session: Session):
    results = []
    
    # Check 1: Escalate tasks overdue > 2 days
    escalation_result = escalate_overdue_tasks({}, session)
    results.append({"check": "escalation", "result": escalation_result})
    
    # Check 2: Find overloaded employees
    employees = session.exec(select(Employee)).all()
    for emp in employees:
        tasks = session.exec(
            select(Task).where(
                Task.assigned_to == emp.id,
                Task.status != "completed"
            )
        ).all()
        if len(tasks) > 5:
            emp.workload_score = min(10.0, len(tasks) * 1.5)
            session.add(emp)
            results.append({
                "check": "workload",
                "employee_id": emp.id,
                "task_count": len(tasks),
                "workload_score": emp.workload_score
            })
    
    session.commit()
    return results