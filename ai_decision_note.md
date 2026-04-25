# AI Decision Note — Startup OS

## Groq API (LLaMA 3.3 70B) — Founder Daily Brief
Chosen for fastest LLM inference (500+ tokens/sec). Free tier. Used to convert raw company data into actionable founder insights daily.

## Gemini Vision API — Document Ingestion
Chosen for native multimodal capability. Reads Aadhaar/PAN images directly without separate OCR. More accurate than Tesseract on real documents.

## XGBoost — Attrition Prediction
Chosen over neural networks because HR data is tabular and small. XGBoost outperforms on structured data, trains in under 1 second, and provides native feature importance for explainability.

## Rule Engine — Project Risk
Chosen over ML because project risk has clear thresholds (overdue tasks, completion %, blockers). Fully explainable, no training data needed.

## FastAPI BackgroundTasks — Event System
Chosen over Celery because event volume for 10 people doesn't need Redis/RabbitMQ. Zero extra infrastructure.

## Total Cost: $0/month
All tools used are on free tier.