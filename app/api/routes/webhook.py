from fastapi import APIRouter, BackgroundTasks, Request
from app.services.event_service import process_event
import json

router = APIRouter()

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.json()
    except:
        body = {}
    
    # Return HTTP 200 immediately (< 2 seconds requirement)
    background_tasks.add_task(process_event, body)
    
    return {"status": "received", "message": "Processing in background"}

@router.get("/whatsapp")
def verify_webhook(hub_mode: str = None, hub_challenge: str = None, hub_verify_token: str = None):
    # WhatsApp webhook verification
    if hub_verify_token == "startupos_verify_token":
        return int(hub_challenge) if hub_challenge else "verified"
    return {"status": "verification_failed"}