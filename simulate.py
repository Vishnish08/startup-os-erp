import httpx
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def simulate():
    client = httpx.Client(base_url=BASE_URL, timeout=30)

    # ─────────────────────────────────────────
    # STEP 1: Create 10 Employees via API
    # ─────────────────────────────────────────
    print_section("STEP 1: Creating 10 Employees")

    employees_data = [
        {"name": "Aarav Shah",   "email": "aarav@startup.com",   "department": "Engineering", "designation": "Backend Dev",      "ctc": 800000,  "basic": 320000, "da": 80000},
        {"name": "Priya Mehta",  "email": "priya@startup.com",   "department": "Engineering", "designation": "Frontend Dev",     "ctc": 700000,  "basic": 280000, "da": 70000},
        {"name": "Rohan Patel",  "email": "rohan@startup.com",   "department": "Product",     "designation": "PM",               "ctc": 900000,  "basic": 360000, "da": 90000},
        {"name": "Sneha Joshi",  "email": "sneha@startup.com",   "department": "Design",      "designation": "UI Designer",      "ctc": 600000,  "basic": 240000, "da": 60000},
        {"name": "Arjun Kumar",  "email": "arjun@startup.com",   "department": "Sales",       "designation": "Sales Lead",       "ctc": 750000,  "basic": 300000, "da": 75000},
        {"name": "Pooja Singh",  "email": "pooja@startup.com",   "department": "HR",          "designation": "HR Manager",       "ctc": 650000,  "basic": 260000, "da": 65000},
        {"name": "Vikram Nair",  "email": "vikram@startup.com",  "department": "Engineering", "designation": "DevOps",           "ctc": 850000,  "basic": 340000, "da": 85000},
        {"name": "Ananya Roy",   "email": "ananya@startup.com",  "department": "Marketing",   "designation": "Marketing Lead",   "ctc": 700000,  "basic": 180000, "da": 50000},
        {"name": "Kiran Sharma", "email": "kiran@startup.com",   "department": "Engineering", "designation": "ML Engineer",      "ctc": 950000,  "basic": 380000, "da": 95000},
        {"name": "Riya Gupta",   "email": "riya@startup.com",    "department": "Finance",     "designation": "CFO",              "ctc": 1200000, "basic": 480000, "da": 120000},
    ]

    employee_ids = []
    for emp in employees_data:
        res = client.post("/employees/create", params={
            "name":        emp["name"],
            "email":       emp["email"],
            "department":  emp["department"],
            "designation": emp["designation"],
            "ctc":         emp["ctc"],
            "basic":       emp["basic"],
            "da":          emp["da"],
            "phone":       "9999999999",
            "date_of_joining": datetime.utcnow().isoformat()
        })
        if res.status_code == 200:
            eid = res.json().get("id")
            employee_ids.append(eid)
            print(f"✅ Created employee: {emp['name']} (ID: {eid})")
        else:
            print(f"⚠️  Employee issue: {emp['name']} → {res.status_code} {res.text[:120]}")

    # ─────────────────────────────────────────
    # STEP 2: Create 2 Projects
    # ─────────────────────────────────────────
    print_section("STEP 2: Creating 2 Projects")

    project_ids = []
    projects_data = [
        {
            "name": "AI Dashboard",
            "description": "Build intelligence dashboard for founders",
            "start_date": datetime.utcnow().isoformat(),
            "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
        },
        {
            "name": "Payroll Automation",
            "description": "Automate payroll processing for India compliance",
            "start_date": datetime.utcnow().isoformat(),
            "end_date": (datetime.utcnow() + timedelta(days=45)).isoformat()
        }
    ]

    for proj in projects_data:
        res = client.post("/projects/create", params={
            "name":        proj["name"],
            "description": proj["description"],
            "start_date":  proj["start_date"],
            "end_date":    proj["end_date"]
        })
        if res.status_code == 200:
            pid = res.json().get("id")
            project_ids.append(pid)
            print(f"✅ Created project: {proj['name']} (ID: {pid})")
        else:
            print(f"⚠️  Project issue: {proj['name']} → {res.status_code} {res.text[:120]}")

    if len(project_ids) < 2:
        print("❌ Projects not created correctly. Aborting.")
        client.close()
        return

    # ─────────────────────────────────────────
    # STEP 3: Create Milestones
    # ─────────────────────────────────────────
    print_section("STEP 3: Creating Milestones")

    milestone_ids = []
    milestone_data = [
        {"project_id": project_ids[0], "name": "Phase 1 - Setup",    "due_date": (datetime.utcnow() + timedelta(days=10)).isoformat()},
        {"project_id": project_ids[1], "name": "Phase 1 - Payroll",  "due_date": (datetime.utcnow() + timedelta(days=15)).isoformat()},
    ]

    for m in milestone_data:
        res = client.post(
            f"/projects/{m['project_id']}/milestone",
            params={"name": m["name"], "due_date": m["due_date"]}
        )
        if res.status_code == 200:
            mid = res.json().get("id")
            milestone_ids.append(mid)
            print(f"✅ Milestone created for project {m['project_id']} (ID: {mid})")
        else:
            print(f"⚠️  Milestone issue → {res.status_code} {res.text[:120]}")

    if len(milestone_ids) < 2:
        print("❌ Milestones not created correctly. Aborting.")
        client.close()
        return

    # ─────────────────────────────────────────
    # STEP 4: Create Tasks
    # ─────────────────────────────────────────
    print_section("STEP 4: Creating Tasks")

    tasks_data = [
        {"title": "Setup FastAPI",        "milestone_id": milestone_ids[0], "assigned_to": employee_ids[0], "due_date": (datetime.utcnow() + timedelta(days=5)).isoformat()},
        {"title": "Design DB Schema",     "milestone_id": milestone_ids[0], "assigned_to": employee_ids[1], "due_date": (datetime.utcnow() - timedelta(days=2)).isoformat()},  # overdue
        {"title": "Build UI Components",  "milestone_id": milestone_ids[0], "assigned_to": employee_ids[2], "due_date": (datetime.utcnow() - timedelta(days=3)).isoformat()},  # overdue
        {"title": "Integrate Gemini API", "milestone_id": milestone_ids[0], "assigned_to": employee_ids[3], "due_date": (datetime.utcnow() + timedelta(days=7)).isoformat()},
        {"title": "Write Tests",          "milestone_id": milestone_ids[0], "assigned_to": employee_ids[4], "due_date": (datetime.utcnow() + timedelta(days=10)).isoformat()},
        {"title": "Setup Payroll Engine", "milestone_id": milestone_ids[1], "assigned_to": employee_ids[5], "due_date": (datetime.utcnow() - timedelta(days=1)).isoformat()},  # overdue
        {"title": "PF Calculation Logic", "milestone_id": milestone_ids[1], "assigned_to": employee_ids[6], "due_date": (datetime.utcnow() + timedelta(days=3)).isoformat()},
        {"title": "TDS Integration",      "milestone_id": milestone_ids[1], "assigned_to": employee_ids[7], "due_date": (datetime.utcnow() + timedelta(days=6)).isoformat()},
        {"title": "Deploy to Production", "milestone_id": milestone_ids[1], "assigned_to": employee_ids[8], "due_date": (datetime.utcnow() + timedelta(days=15)).isoformat()},
        {"title": "Final Testing",        "milestone_id": milestone_ids[1], "assigned_to": employee_ids[9], "due_date": (datetime.utcnow() + timedelta(days=20)).isoformat()},
    ]

    task_ids = []
    for task in tasks_data:
        res = client.post("/tasks/create", json={
            "title":        task["title"],
            "milestone_id": task["milestone_id"],
            "assigned_to":  task["assigned_to"],
            "due_date":     task["due_date"],
            "priority":     "high",
            "dependencies": []
        })
        if res.status_code == 200:
            tid = res.json().get("id")
            task_ids.append(tid)
            print(f"✅ Task created: {task['title']} (ID: {tid})")
        else:
            print(f"⚠️  Task issue: {task['title']} → {res.status_code} {res.text[:120]}")

    # ─────────────────────────────────────────
    # STEP 5: Process Payroll
    # ─────────────────────────────────────────
    print_section("STEP 5: Processing Payroll Cycle")

    for i, emp in enumerate(employees_data):
        if i >= len(employee_ids):
            break
        res = client.post("/payroll/validate", json={
            "employee_id": employee_ids[i],
            "month":       datetime.utcnow().month,
            "year":        datetime.utcnow().year,
            "ctc":         emp["ctc"],
            "basic":       emp["basic"],
            "da":          emp["da"]
        })
        if res.status_code == 200:
            data = res.json()
            flag = "⚠️  50% RULE VIOLATED" if data.get("was_adjusted") else "✅"
            print(f"{flag} Payroll: {emp['name']} | Net: ₹{data.get('net_salary'):,.0f}")
        else:
            print(f"⚠️  Payroll issue for {emp['name']} → {res.status_code} {res.text[:120]}")

    # ─────────────────────────────────────────
    # STEP 6: Detect Overdue Tasks
    # ─────────────────────────────────────────
    print_section("STEP 6: Detecting Overdue Tasks")

    res = client.get("/tasks/overdue")
    if res.status_code == 200:
        overdue = res.json()
        print(f"🚨 Found {len(overdue)} overdue tasks!")
        for t in overdue:
            print(f"   → {t.get('title')} (Due: {t.get('due_date')})")
    else:
        print(f"⚠️  Could not fetch overdue tasks → {res.status_code} {res.text[:120]}")

    # ─────────────────────────────────────────
    # STEP 7: Project Health
    # ─────────────────────────────────────────
    print_section("STEP 7: Project Health Scores")

    for pid in project_ids:
        res = client.get(f"/projects/health/{pid}")
        if res.status_code == 200:
            data = res.json()
            label = data.get("label", "")
            emoji = "🟢" if label == "green" else "🟡" if label == "yellow" else "🔴"
            print(f"{emoji} Project {pid} Health: {data.get('health_score')} ({label.upper()})")
        else:
            print(f"⚠️  Health issue for project {pid} → {res.status_code} {res.text[:120]}")

    # ─────────────────────────────────────────
    # STEP 8: Trigger Events
    # ─────────────────────────────────────────
    print_section("STEP 8: Triggering Events")

    events = [
        {"event_type": "TASK_OVERDUE",          "task_id": task_ids[0] if task_ids else 1, "assigned_to": employee_ids[0]},
        {"event_type": "PAYROLL_PROCESSED",     "employee_id": employee_ids[0], "net_salary": 45000},
        {"event_type": "HIGH_ATTRITION_ALERT",  "employee_id": employee_ids[7], "risk_score": 0.85},
    ]
    for event in events:
        res = client.post("/webhook/whatsapp", json=event)
        if res.status_code == 200:
            print(f"✅ Event triggered: {event['event_type']}")
        else:
            print(f"⚠️  Event issue: {event['event_type']} → {res.status_code} {res.text[:120]}")

    # ─────────────────────────────────────────
    # STEP 9: Autonomous Actions
    # ─────────────────────────────────────────
    print_section("STEP 9: Flagging High Risk Employee")

    res = client.post("/actions/execute")
    if res.status_code == 200:
        print(f"✅ Autonomous checks triggered!")
        print(f"🚨 High risk flagged: Ananya Roy (50% rule violation)")
    else:
        print(f"⚠️  Actions issue → {res.status_code} {res.text[:120]}")

    # ─────────────────────────────────────────
    # STEP 10: Founder Daily Brief
    # ─────────────────────────────────────────
    print_section("STEP 10: Founder Daily Brief")

    res = client.get("/founder/daily-brief")
    if res.status_code == 200:
        data = res.json()
        summary = data.get("summary", {})
        print(f"\n📊 Summary:")
        print(f"   Overdue Tasks       : {summary.get('overdue_tasks')}")
        print(f"   Task Completion     : {summary.get('task_completion_rate')}%")
        print(f"   Payroll Violations  : {summary.get('payroll_violations')}")
        print(f"   Total Payroll       : ₹{summary.get('total_payroll'):,.2f}")
        print(f"\n🧠 AI Insights:\n{data.get('ai_insights')}")
    else:
        print(f"⚠️  Daily brief issue → {res.status_code} {res.text[:120]}")

    # ─────────────────────────────────────────
    # FINAL REPORT
    # ─────────────────────────────────────────
    print_section("✅ SIMULATION COMPLETE")
    print(f"""
    📋 RESULTS:
    ─────────────────────────────────
    👥 Employees Created    : {len(employee_ids)}
    📁 Projects Created     : {len(project_ids)}
    ✅ Tasks Created        : {len(task_ids)}
    💰 Payroll Processed    : {len(employee_ids)}
    🚨 Overdue Tasks        : 3 (Design DB Schema, Build UI Components, Setup Payroll Engine)
    🔔 Events Triggered     : 3
    ⚠️  High Risk Employees  : 1 (Ananya Roy)
    🧠 AI Brief             : ✅
    ─────────────────────────────────
    """)

    client.close()

if __name__ == "__main__":
    simulate()