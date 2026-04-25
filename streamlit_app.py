import streamlit as st  # type: ignore
import warnings
warnings.filterwarnings("ignore")

API_BASE = "https://timocratic-nocuous-denzel.ngrok-free.dev"

# Session with ngrok header to bypass browser warning
session = __import__('requests').Session()
session.headers.update({"ngrok-skip-browser-warning": "true"})

st.set_page_config(
    page_title="Startup OS — Intelligence ERP",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Startup OS — Intelligence ERP")
st.caption("CR Cognitech Assignment · Vishakha Bhavsar")

tabs = st.tabs(["📊 Overview", "✅ Tasks", "💰 Payroll", "🧠 Intelligence", "📋 Founder Brief"])


# ─────────────────────────────────────────
# TAB 1: OVERVIEW
# ─────────────────────────────────────────
with tabs[0]:
    st.header("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    try:
        projects_res = session.get(f"{API_BASE}/projects/all").json()
        tasks_res = session.get(f"{API_BASE}/tasks/all").json()

        total_projects = len(projects_res) if isinstance(projects_res, list) else 0
        total_tasks = len(tasks_res) if isinstance(tasks_res, list) else 0
        overdue = sum(1 for t in (tasks_res if isinstance(tasks_res, list) else []) if t.get("is_overdue"))
        completed = sum(1 for t in (tasks_res if isinstance(tasks_res, list) else []) if t.get("status") == "completed")

        col1.metric("Total Projects", total_projects)
        col2.metric("Total Tasks", total_tasks)
        col3.metric("Overdue Tasks", overdue, delta=f"-{overdue}" if overdue else "0", delta_color="inverse")
        col4.metric("Completed Tasks", completed)

    except Exception as e:
        st.warning(f"Could not reach API: {e}")
        col1.metric("Total Projects", "—")
        col2.metric("Total Tasks", "—")
        col3.metric("Overdue Tasks", "—")
        col4.metric("Completed Tasks", "—")

    st.divider()
    st.subheader("API Health")
    try:
        health = session.get(f"{API_BASE}/health").json()
        if health.get("status") == "healthy":
            st.success("✅ API is online and healthy!")
        else:
            st.warning("⚠️ API returned unexpected response")
    except:
        st.error("❌ API is offline. Make sure Docker is running.")


# ─────────────────────────────────────────
# TAB 2: TASKS
# ─────────────────────────────────────────
with tabs[1]:
    st.header("Task Management")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("All Tasks")
        try:
            tasks = session.get(f"{API_BASE}/tasks/all").json()
            if isinstance(tasks, list) and tasks:
                for task in tasks:
                    status_icon = "✅" if task.get("status") == "completed" else "⏳" if not task.get("is_overdue") else "🔴"
                    with st.expander(f"{status_icon} {task.get('title', 'Untitled')} — {task.get('status', 'unknown').upper()}"):
                        st.write(f"**Milestone ID:** {task.get('milestone_id', '—')}")
                        st.write(f"**Assigned To:** {task.get('assigned_to', '—')}")
                        st.write(f"**Due Date:** {task.get('due_date', '—')}")
                        st.write(f"**Priority:** {task.get('priority', '—')}")
                        st.write(f"**Overdue:** {'Yes 🔴' if task.get('is_overdue') else 'No ✅'}")
            else:
                st.info("No tasks found.")
        except Exception as e:
            st.error(f"Error loading tasks: {e}")

    with col2:
        st.subheader("Create Task")
        with st.form("create_task"):
            title = st.text_input("Title", placeholder="e.g. Build login page")
            milestone_id = st.number_input("Milestone ID", min_value=1, value=4)
            assigned_to = st.number_input("Assigned To (Employee ID)", min_value=1, value=1)
            priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
            due_date = st.date_input("Due Date")
            submitted = st.form_submit_button("Create Task")

            if submitted:
                try:
                    payload = {
                        "title": title,
                        "milestone_id": milestone_id,
                        "assigned_to": assigned_to,
                        "priority": priority,
                        "due_date": str(due_date),
                    }
                    res = session.post(f"{API_BASE}/tasks/create", json=payload)
                    if res.status_code in (200, 201):
                        st.success("✅ Task created!")
                        st.rerun()
                    else:
                        st.error(f"Failed: {res.text}")
                except Exception as e:
                    st.error(f"Error: {e}")


# ─────────────────────────────────────────
# TAB 3: PAYROLL
# ─────────────────────────────────────────
with tabs[2]:
    st.header("Payroll Engine")
    st.caption("50% salary rule · PF deduction · TDS calculation")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Run Payroll Calculation")
        with st.form("payroll_form"):
            emp_id = st.number_input("Employee ID", min_value=1, value=1)
            month = st.number_input("Month", min_value=1, max_value=12, value=4)
            year = st.number_input("Year", min_value=2020, max_value=2030, value=2026)
            ctc = st.number_input("CTC (₹/year)", min_value=0.0, value=1200000.0, step=10000.0)
            basic = st.number_input("Basic (₹/year)", min_value=0.0, value=500000.0, step=10000.0)
            da = st.number_input("DA (₹/year)", min_value=0.0, value=50000.0, step=1000.0)
            calc = st.form_submit_button("Calculate Payroll")

            if calc:
                try:
                    payload = {
                        "employee_id": emp_id,
                        "month": month,
                        "year": year,
                        "ctc": ctc,
                        "basic": basic,
                        "da": da
                    }
                    res = session.post(f"{API_BASE}/payroll/validate", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state["payroll_result"] = data
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col2:
        st.subheader("Result")
        if "payroll_result" in st.session_state:
            d = st.session_state["payroll_result"]
            st.metric("Gross Salary", f"₹{d.get('gross_salary', 0):,.0f}")
            st.metric("PF (Employee)", f"₹{d.get('pf_employee', 0):,.0f}")
            st.metric("TDS", f"₹{d.get('tds', 0):,.0f}")
            st.metric("Net Salary", f"₹{d.get('net_salary', 0):,.0f}", delta="Take home")
            st.metric("50% Rule", "✅ Passed" if not d.get("is_fifty_rule_violated") else "❌ Violated")
        else:
            st.info("Run a payroll calculation to see results here.")


# ─────────────────────────────────────────
# TAB 4: INTELLIGENCE
# ─────────────────────────────────────────
with tabs[3]:
    st.header("AI Intelligence Layer")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Attrition Risk (XGBoost)")
        with st.form("attrition_form"):
            emp_id = st.text_input("Employee ID", value="EMP001")
            tenure = st.slider("Tenure (months)", 1, 120, 24)
            performance = st.slider("Performance Score", 1.0, 5.0, 3.5, 0.1)
            salary_ratio = st.slider("Salary Ratio (vs market)", 0.6, 1.4, 1.0, 0.05)
            absences = st.number_input("Absences (last 90 days)", 0, 30, 2)
            promotions = st.number_input("Promotions", 0, 10, 1)
            overtime = st.slider("Overtime Hours/week", 0.0, 40.0, 5.0)
            team_size = st.number_input("Team Size", 1, 50, 8)
            predict = st.form_submit_button("Predict Attrition Risk")

            if predict:
                try:
                    payload = {
                        "employee_id": emp_id,
                        "tenure_months": tenure,
                        "performance_score": performance,
                        "salary_ratio": salary_ratio,
                        "absences_last_90d": absences,
                        "promotions": promotions,
                        "overtime_hours": overtime,
                        "team_size": team_size
                    }
                    res = session.post(f"{API_BASE}/intelligence/attrition", json=payload)
                    if res.status_code == 200:
                        st.session_state["attrition_result"] = res.json()
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

        if "attrition_result" in st.session_state:
            r = st.session_state["attrition_result"]
            risk = r.get("risk_level", "—")
            color = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(risk, "⚪")
            st.metric("Risk Score", f"{r.get('risk_score', 0):.1%}")
            st.markdown(f"**Risk Level:** {color} {risk}")
            st.markdown(f"**Top Factors:** {', '.join(r.get('top_factors', []))}")
            st.info(f"💡 {r.get('recommendation', '')}")

    with col2:
        st.subheader("📈 Project Risk")
        with st.form("project_risk_form"):
            proj_id = st.text_input("Project ID", value="PROJ001")
            proj_name = st.text_input("Project Name", value="Alpha Launch")
            overdue_tasks = st.number_input("Overdue Tasks", 0, 50, 2)
            completion = st.slider("Completion %", 0.0, 100.0, 45.0)
            days_left = st.number_input("Days Remaining", 0, 365, 14)
            proj_team = st.number_input("Team Size", 1, 50, 4)
            blockers = st.number_input("Open Blockers", 0, 20, 1)
            predict_proj = st.form_submit_button("Predict Project Risk")

            if predict_proj:
                try:
                    payload = {
                        "project_id": proj_id,
                        "project_name": proj_name,
                        "overdue_tasks": overdue_tasks,
                        "completion_pct": completion,
                        "days_remaining": days_left,
                        "team_size": proj_team,
                        "open_blockers": blockers
                    }
                    res = session.post(f"{API_BASE}/intelligence/project-risk", json=payload)
                    if res.status_code == 200:
                        st.session_state["project_risk_result"] = res.json()
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

        if "project_risk_result" in st.session_state:
            r = st.session_state["project_risk_result"]
            risk = r.get("risk_level", "—")
            color = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(risk, "⚪")
            st.metric("Risk Score", f"{r.get('risk_score', 0)}/100")
            st.markdown(f"**Risk Level:** {color} {risk}")
            st.markdown(f"**Reasons:** {', '.join(r.get('reasons', []))}")
            st.info(f"💡 {r.get('recommendation', '')}")


# ─────────────────────────────────────────
# TAB 5: FOUNDER BRIEF
# ─────────────────────────────────────────
with tabs[4]:
    st.header("📋 Founder Daily Brief")
    st.caption("AI-generated daily summary powered by Groq")

    if st.button("🔄 Generate Today's Brief", type="primary"):
        with st.spinner("Asking Groq AI to generate your brief..."):
            try:
                res = session.get(f"{API_BASE}/founder/daily-brief")
                if res.status_code == 200:
                    data = res.json()
                    st.session_state["founder_brief"] = data
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    if "founder_brief" in st.session_state:
        brief = st.session_state["founder_brief"]
        st.markdown("---")
        if isinstance(brief, dict):
            if "ai_insights" in brief:
                st.markdown(f"### 📅 {brief.get('date', '')}")
                summary = brief.get("summary", {})
                col1, col2, col3 = st.columns(3)
                col1.metric("Overdue Tasks", summary.get("overdue_tasks", 0))
                col2.metric("Payroll Violations", summary.get("payroll_violations", 0))
                col3.metric("High Risk Employees", summary.get("high_risk_employees", 0))
                st.markdown("---")
                st.markdown(brief["ai_insights"])
            elif "brief" in brief:
                st.markdown(brief["brief"])
            else:
                st.json(brief)
        else:
            st.markdown(str(brief))