from fastapi import APIRouter, Depends
from sqlmodel import Session, select # type: ignore
from app.database import get_session
from app.models.task import Task
from app.models.payroll import Payroll
from app.models.employee import Employee
from app.config import settings
from datetime import datetime
from groq import Groq # type: ignore

router = APIRouter()
client = Groq(api_key=settings.GROQ_API_KEY)

@router.get("/daily-brief")
def get_daily_brief(session: Session = Depends(get_session)):
    now = datetime.utcnow()

    tasks = session.exec(select(Task)).all()
    overdue_tasks = [t for t in tasks if t.is_overdue or (t.due_date and t.due_date < now and t.status != "completed")]
    completed_tasks = [t for t in tasks if t.status == "completed"]
    task_completion_rate = len(completed_tasks) / len(tasks) * 100 if tasks else 0

    payrolls = session.exec(select(Payroll)).all()
    violations = [p for p in payrolls if p.is_fifty_rule_violated]
    total_payroll = sum(p.net_salary for p in payrolls)

    employees = session.exec(select(Employee)).all()
    high_risk = [e for e in employees if e.workload_score > 8 or e.overtime_hours > 40]

    data_summary = f"""
    Company Status Report - {now.strftime('%Y-%m-%d')}
    
    TASKS:
    - Total tasks: {len(tasks)}
    - Overdue tasks: {len(overdue_tasks)}
    - Completed tasks: {len(completed_tasks)}
    - Completion rate: {task_completion_rate:.1f}%
    
    PAYROLL:
    - Total employees on payroll: {len(payrolls)}
    - 50% rule violations: {len(violations)}
    - Total payroll this cycle: ₹{total_payroll:,.2f}
    
    ATTRITION RISK:
    - High risk employees: {len(high_risk)}
    - Total employees: {len(employees)}
    """

    chat = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an AI business advisor for a startup. Given company data, provide a concise daily brief with top 3 priorities the founder should focus on today. Be specific and actionable."
            },
            {
                "role": "user",
                "content": data_summary
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    ai_insights = chat.choices[0].message.content

    return {
        "date": now.strftime("%Y-%m-%d"),
        "summary": {
            "overdue_tasks": len(overdue_tasks),
            "task_completion_rate": round(task_completion_rate, 2),
            "payroll_violations": len(violations),
            "total_payroll": round(total_payroll, 2),
            "high_risk_employees": len(high_risk)
        },
        "ai_insights": ai_insights,
        "raw_overdue_tasks": [{"id": t.id, "title": t.title, "due_date": str(t.due_date)} for t in overdue_tasks[:5]],
        "high_risk_employees": [{"id": e.id, "name": e.name, "workload": e.workload_score} for e in high_risk]
    }