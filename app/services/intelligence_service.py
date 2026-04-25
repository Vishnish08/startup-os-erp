import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# ─────────────────────────────────────────
# Train a lightweight XGBoost model on synthetic data
# (In production, replace with real HR data)
# ─────────────────────────────────────────

MODEL_PATH = "models/attrition_model.pkl"

def _train_and_save_model():
    np.random.seed(42)
    n = 500

    X = np.column_stack([
        np.random.randint(1, 120, n),        # tenure_months
        np.random.uniform(1, 5, n),          # performance_score
        np.random.uniform(0.6, 1.4, n),      # salary_ratio
        np.random.randint(0, 30, n),         # absences_last_90d
        np.random.randint(0, 5, n),          # promotions
        np.random.uniform(0, 40, n),         # overtime_hours
        np.random.randint(1, 50, n),         # team_size
    ])

    # Synthetic label: high absence + low salary + low performance = attrition
    y = (
        (X[:, 3] > 10) &
        (X[:, 2] < 0.85) &
        (X[:, 1] < 3.0)
    ).astype(int)

    model = XGBClassifier(n_estimators=100, max_depth=4, random_state=42, eval_metric="logloss")
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model

def get_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return _train_and_save_model()


# ─────────────────────────────────────────
# Attrition prediction
# ─────────────────────────────────────────

FEATURE_NAMES = [
    "tenure_months", "performance_score", "salary_ratio",
    "absences_last_90d", "promotions", "overtime_hours", "team_size"
]

def predict_attrition(data: dict) -> dict:
    model = get_model()

    features = np.array([[
        data["tenure_months"],
        data["performance_score"],
        data["salary_ratio"],
        data["absences_last_90d"],
        data["promotions"],
        data["overtime_hours"],
        data["team_size"],
    ]])

    prob = model.predict_proba(features)[0][1]
    risk_score = round(prob, 4)

    if prob >= 0.65:
        risk_level = "HIGH"
    elif prob >= 0.35:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Top factors (simple rule-based explanation)
    top_factors = []
    if data["absences_last_90d"] > 10:
        top_factors.append("High absences")
    if data["salary_ratio"] < 0.85:
        top_factors.append("Below-market salary")
    if data["performance_score"] < 3.0:
        top_factors.append("Low performance score")
    if data["overtime_hours"] > 20:
        top_factors.append("Excessive overtime")
    if data["promotions"] == 0 and data["tenure_months"] > 24:
        top_factors.append("No promotions in 2+ years")
    if not top_factors:
        top_factors.append("No major risk signals")

    recommendations = {
        "HIGH": "Immediate 1:1 with manager. Review compensation. Consider retention bonus.",
        "MEDIUM": "Schedule check-in. Discuss growth path and workload.",
        "LOW": "Employee appears stable. Continue regular engagement."
    }

    return {
        "employee_id": data["employee_id"],
        "risk_score": risk_score,
        "risk_level": risk_level,
        "top_factors": top_factors,
        "recommendation": recommendations[risk_level]
    }


# ─────────────────────────────────────────
# Project risk (rule-based scoring)
# ─────────────────────────────────────────

def predict_project_risk(data: dict) -> dict:
    score = 0
    reasons = []

    if data["overdue_tasks"] > 3:
        score += 30
        reasons.append(f"{data['overdue_tasks']} overdue tasks")

    if data["completion_pct"] < 50 and data["days_remaining"] < 14:
        score += 35
        reasons.append("Less than 50% done with <14 days left")

    if data["open_blockers"] > 0:
        score += data["open_blockers"] * 10
        reasons.append(f"{data['open_blockers']} open blocker(s)")

    if data["team_size"] < 3:
        score += 10
        reasons.append("Small team size")

    score = min(score, 100)

    if score >= 60:
        risk_level = "HIGH"
        recommendation = "Escalate to founder. Daily standups. Reassign resources immediately."
    elif score >= 30:
        risk_level = "MEDIUM"
        recommendation = "Review blockers in next sprint. Consider scope reduction."
    else:
        risk_level = "LOW"
        recommendation = "Project on track. Maintain current velocity."

    if not reasons:
        reasons.append("No major risk signals detected")

    return {
        "project_id": data["project_id"],
        "project_name": data["project_name"],
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons,
        "recommendation": recommendation
    }