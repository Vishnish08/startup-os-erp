from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

EVENTS = [
    "TASK_OVERDUE",
    "PAYROLL_PROCESSED", 
    "HIGH_ATTRITION_ALERT"
]

async def process_event(payload: dict):
    try:
        event_type = payload.get("event_type", "UNKNOWN")
        logger.info(f"Processing event: {event_type} at {datetime.utcnow()}")

        if event_type == "TASK_OVERDUE":
            await handle_task_overdue(payload)
        elif event_type == "PAYROLL_PROCESSED":
            await handle_payroll_processed(payload)
        elif event_type == "HIGH_ATTRITION_ALERT":
            await handle_attrition_alert(payload)
        else:
            await handle_whatsapp_message(payload)

    except Exception as e:
        logger.error(f"Event processing error: {str(e)}")

async def handle_task_overdue(payload: dict):
    task_id = payload.get("task_id")
    assigned_to = payload.get("assigned_to")
    logger.warning(f"TASK_OVERDUE: Task {task_id} assigned to employee {assigned_to}")
    # In production: send WhatsApp message via Twilio/Meta API
    print(f"📱 WhatsApp Alert: Task {task_id} is overdue! Employee {assigned_to} notified.")

async def handle_payroll_processed(payload: dict):
    employee_id = payload.get("employee_id")
    amount = payload.get("net_salary")
    logger.info(f"PAYROLL_PROCESSED: Employee {employee_id} paid ₹{amount}")
    print(f"📱 WhatsApp Alert: Payroll processed for employee {employee_id}. Net salary: ₹{amount}")

async def handle_attrition_alert(payload: dict):
    employee_id = payload.get("employee_id")
    risk_score = payload.get("risk_score")
    logger.warning(f"HIGH_ATTRITION_ALERT: Employee {employee_id} risk score {risk_score}")
    print(f"📱 WhatsApp Alert: Employee {employee_id} has high attrition risk ({risk_score})")

async def handle_whatsapp_message(payload: dict):
    message = payload.get("message", "")
    sender = payload.get("from", "unknown")
    logger.info(f"WhatsApp message from {sender}: {message}")
    print(f"📱 WhatsApp message received from {sender}: {message}")

def trigger_event(event_type: str, payload: dict):
    if event_type not in EVENTS:
        logger.warning(f"Unknown event type: {event_type}")
        return False
    
    full_payload = {
        "event_type": event_type,
        "triggered_at": datetime.utcnow().isoformat(),
        **payload
    }
    print(f"🔔 Event triggered: {event_type} | Payload: {json.dumps(full_payload)}")
    return True