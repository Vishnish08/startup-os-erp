# 🧠 Startup OS — Intelligence-First ERP

> "What should the founder focus on today?"

A Company Operating System built for 10-person startups that understands documents, tracks execution, ensures compliance, predicts risks, and communicates automatically.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (async) |
| Database | PostgreSQL + SQLModel |
| AI Vision | Google Gemini API |
| AI Text | Groq API (Llama3) |
| ML Model | XGBoost (Attrition Prediction) |
| Containers | Docker Compose |
| Dashboard | Streamlit |
| Live URL | ngrok |
| Version Control | GitHub |

---

## ⚡ Quick Start

### Prerequisites
- Docker Desktop installed
- Groq API key (console.groq.com)
- Gemini API key (aistudio.google.com)

### Run in 3 commands
```bash
git clone https://github.com/Vishnish08/startup-os-erp
cd startup-os-erp
cp .env.example .env
# Add your API keys to .env file
docker compose up --build
```

### Access Points
API Server    →  http://localhost:8000
API Docs      →  http://localhost:8000/docs
Dashboard     →  streamlit run streamlit_app.py

---

## 📦 System Architecture
                ┌─────────────────────────────┐
                │      FastAPI Backend          │
                │        Port 8000              │
                └──────────┬──────────────────┘
                           │
          ┌────────────────┼─────────────────┐
          ▼                ▼                  ▼
  ┌──────────────┐  ┌───────────┐  ┌──────────────────┐
  │  PostgreSQL  │  │ AI Layer  │  │Background Workers│
  │  (SQLModel)  │  │           │  │(BackgroundTasks) │
  └──────────────┘  │ • Gemini  │  └──────────────────┘
                    │ • Groq    │
                    │ • XGBoost │
                    └───────────┘
                           │
                ┌──────────▼──────────┐
                │   Event System       │
                │  WhatsApp Webhooks   │
                └─────────────────────┘
                
---

## 🔌 API Endpoints

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /tasks/create | Create task with circular dependency check |
| GET | /tasks/overdue | Get all overdue tasks |
| PATCH | /tasks/{id} | Update task status |
| GET | /tasks/all | List all tasks |

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /projects/create | Create new project |
| GET | /projects/health/{id} | Get project health score |
| POST | /projects/{id}/milestone | Add milestone to project |
| GET | /projects/all | List all projects |

### Payroll
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /payroll/validate | Calculate and validate payroll |

### Intelligence & AI
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /founder/daily-brief | AI-powered founder daily brief |
| POST | /ingest/employee-doc | Document OCR + extraction |
| POST | /webhook/whatsapp | WhatsApp event webhook |
| POST | /actions/execute | Autonomous action engine |
| GET | /memory | System memory and trends |
| GET | /health | System health check |

---

## 🧠 AI Features

### 1. Document Ingestion — Gemini Vision
- Accepts Aadhaar / PAN as image or PDF
- Extracts structured JSON with confidence score
- Auto-rejects if confidence < 80%
- Masks all sensitive data (Aadhaar, PAN numbers)
- Stores raw file, extracted data, and masked version

### 2. Founder Daily Brief — Groq + Llama3
- Combines tasks + payroll + attrition into one API call
- Returns top 3 actionable priorities for the founder
- Feels like a CEO dashboard in a single request
- Powered by Llama3-8b via Groq (ultra fast)

### 3. Attrition Prediction — XGBoost
- Features: overtime hours, workload score, task completion rate, salary growth
- Returns attrition risk score per employee
- Includes feature importance for explainability
- Automatically flags high-risk employees

### 4. Project Health Score
Health = (Tasks Done % × 0.5) + (On-Time Milestones % × 0.5)
🟢 Green  → score > 80
🟡 Yellow → score 50 to 80
🔴 Red    → score < 50

---

## 💰 Payroll Engine (India 2026)

| Rule | Logic |
|------|-------|
| 50% Rule | Basic + DA must be ≥ 50% of CTC. Auto-adjusts if violated |
| PF Calculation | 12% on min(Basic, ₹15,000) wage ceiling |
| TDS | New tax regime slab-based deduction |
| History | Full payroll history stored per employee |

---

## 🔔 Event System

```python
EVENTS = [
    "TASK_OVERDUE",
    "PAYROLL_PROCESSED",
    "HIGH_ATTRITION_ALERT"
]
```

- WhatsApp webhook responds in under 2 seconds (HTTP 200)
- All heavy processing runs in background workers
- Full event log stored in database
- Autonomous escalation if task overdue > 2 days

---

## ⚙️ Action Engine (Autonomous Layer)

System automatically:
- Escalates tasks overdue > 2 days
- Flags overloaded employees (> 5 pending tasks)
- Sends WhatsApp reminders
- Triggers HIGH_ATTRITION_ALERT for at-risk employees
- Suggests task reassignment when needed

---

## 🗄️ Database Schema
Employee     → core employee data + workload metrics
Document     → raw + extracted + masked versions
Project      → with health score tracking
Milestone    → linked to projects
Task         → with dependency graph + overdue detection
Payroll      → full calculation history
Event        → complete audit log

---

## 🎯 Final Simulation

Simulates a real 10-person startup:
- ✅ 10 employees across departments
- ✅ 2 projects with milestones and tasks
- ✅ 1 complete payroll cycle with PF + TDS
- ✅ Overdue task detection and escalation
- ✅ 2+ events triggered automatically
- ✅ 1 high-risk employee flagged
- ✅ AI daily brief with actionable insights

---

## 📁 Project Structure
startup-os-erp/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── tasks.py
│   │       ├── projects.py
│   │       ├── payroll.py
│   │       ├── ingest.py
│   │       ├── founder.py
│   │       ├── webhook.py
│   │       └── intelligence.py
│   ├── models/
│   │   ├── employee.py
│   │   ├── document.py
│   │   ├── project.py
│   │   ├── milestone.py
│   │   ├── task.py
│   │   ├── payroll.py
│   │   └── events.py
│   ├── services/
│   │   ├── task_service.py
│   │   ├── payroll_service.py
│   │   ├── event_service.py
│   │   ├── action_service.py
│   │   ├── attrition_service.py
│   │   └── memory_service.py
│   ├── schemas/
│   ├── workers/
│   ├── database.py
│   ├── config.py
│   └── main.py
├── streamlit_app.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── architecture_diagram.html
├── ai_decision_note.md
└── .env.example

---

## 🏆 Evaluation Coverage

| Category | Weight | Status |
|----------|--------|--------|
| System Design | 25% | ✅ Architecture diagram + clean structure |
| Backend Engineering | 25% | ✅ FastAPI + SQLModel + clean service layers |
| AI Integration | 25% | ✅ Gemini + Groq + XGBoost |
| Problem Solving | 15% | ✅ Edge cases + graceful fallbacks |
| Tool Usage | 10% | ✅ Docker + ngrok + Streamlit |

---

## 👩‍💻 Built By

**Vishakha Bhavsar**  
Applied AI / Backend Engineer  
Assignment — CR Cognitive Systems LLP  
Built with: FastAPI · PostgreSQL · Gemini · Groq · XGBoost · Docker
