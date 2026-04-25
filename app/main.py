from fastapi import FastAPI, Depends, BackgroundTasks
from sqlmodel import Session # type: ignore
from app.database import create_db_and_tables, get_session
from app.api.routes import tasks, projects, payroll, ingest, founder, webhook, intelligence
from app.services.action_service import run_autonomous_checks

app = FastAPI(
    title="Startup OS - Intelligence ERP",
    description="Company Operating System for 10-person startups",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(payroll.router, prefix="/payroll", tags=["Payroll"])
app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(founder.router, prefix="/founder", tags=["Founder"])
app.include_router(webhook.router, prefix="/webhook", tags=["WhatsApp"])
app.include_router(intelligence.router, tags=["Intelligence"])

@app.get("/")
def root():
    return {
        "system": "Startup OS",
        "status": "running",
        "message": "What should the founder focus on today?"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/actions/execute")
def execute_actions(background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    background_tasks.add_task(run_autonomous_checks, session)
    return {"status": "actions triggered", "message": "Autonomous checks running in background"}

@app.get("/memory")
def get_memory(session: Session = Depends(get_session)):
    from app.services.memory_service import get_system_memory
    return get_system_memory(session)