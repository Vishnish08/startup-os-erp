from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session   # type: ignore
from app.database import get_session
from app.config import settings
import google.generativeai as genai    # type: ignore
import json
import re
import os
import shutil

router = APIRouter()

genai.configure(api_key=settings.GEMINI_API_KEY)

def mask_sensitive(text: str) -> str:
    text = re.sub(r'\b\d{4}\s?\d{4}\s?\d{4}\b', 'XXXX-XXXX-XXXX', text)
    text = re.sub(r'\b[A-Z]{5}\d{4}[A-Z]\b', 'XXXXX0000X', text)
    return text

@router.post("/employee-doc")
async def ingest_employee_doc(
    employee_id: int,
    doc_type: str,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{employee_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        with open(file_path, "rb") as f:
            image_data = f.read()

        prompt = """Extract information from this document and return ONLY a JSON object with these fields:
        {
            "name": "full name",
            "date_of_birth": "DOB if found",
            "id_number": "ID number",
            "address": "address if found",
            "confidence": 0.0 to 1.0
        }
        Return ONLY the JSON, no other text."""

        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])

        raw_text = response.text.strip()
        clean_text = raw_text.replace("```json", "").replace("```", "").strip()
        extracted = json.loads(clean_text)
        confidence = extracted.get("confidence", 0)

        if confidence < 0.8:
            return {
                "status": "rejected",
                "reason": f"Confidence too low: {confidence}",
                "confidence": confidence
            }

        masked = mask_sensitive(json.dumps(extracted))

        from app.models.document import Document
        doc = Document(
            employee_id=employee_id,
            doc_type=doc_type,
            raw_file_path=file_path,
            extracted_data=json.dumps(extracted),
            masked_data=masked,
            confidence_score=confidence,
            is_verified=True
        )
        session.add(doc)
        session.commit()

        return {
            "status": "success",
            "confidence": confidence,
            "masked_data": json.loads(masked),
            "message": "Document processed successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }