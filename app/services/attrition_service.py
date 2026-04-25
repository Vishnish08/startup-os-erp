import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Train once on module load with synthetic data
def _train_model():
    np.random.seed(42)
    n = 200

    df = pd.DataFrame({
        "tenure_months": np.random.randint(1, 120, n),
        "performance_score": np.random.uniform(1, 5, n),
        "salary_ratio": np.random.uniform(0.6, 1.4, n),
        "absences_last_90d": np.random.randint(0, 15, n),
        "promotions": np.random.randint(0, 4, n),
        "overtime_hours": np.random.uniform(0, 40, n),
        "team_size": np.random.randint(2, 20, n),
    })

    # Synthetic label: high absence + low salary_ratio + low performance = likely to leave
    df["attrition"] = (
        (df["absences_last_90d"] > 8) |
        (df["salary_ratio"] < 0.8) |
        (df["performance_score"] < 2.0)
    ).astype(int)

    X = df.drop("attrition", axis=1)
    y = df["attrition"]

    model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1,
                          use_label_encoder=False, eval_metric="logloss")
    model.fit(X, y)
    return model

_model = _train_model()

FEATURES = ["tenure_months", "performance_score", "salary_ratio",
            "absences_last_90d", "promotions", "overtime_hours", "team_size"]

def predict_attrition(employee_data: dict) -> dict:
    """
    employee_data: dict with employee fields
    Returns: risk_score (0-1), risk_level, top_factors
    """
    row = {
        "tenure_months": employee_data.get("tenure_months", 12),
        "performance_score": employee_data.get("performance_score", 3.0),
        "salary_ratio": employee_data.get("salary_ratio", 1.0),
        "absences_last_90d": employee_data.get("absences_last_90d", 2),
        "promotions": employee_data.get("promotions", 0),
        "overtime_hours": employee_data.get("overtime_hours", 5),
        "team_size": employee_data.get("team_size", 8),
    }

    X = pd.DataFrame([row])
    prob = float(_model.predict_proba(X)[0][1])

    if prob >= 0.7:
        risk_level = "HIGH"
    elif prob >= 0.4:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Feature importances as top factors
    importances = _model.feature_importances_
    top_factors = sorted(
        zip(FEATURES, importances), key=lambda x: x[1], reverse=True
    )[:3]

    return {
        "risk_score": round(prob, 3),
        "risk_level": risk_level,
        "top_factors": [f for f, _ in top_factors]
    }


def predict_project_risk(project_data: dict) -> dict:
    """
    Simple rule-based project risk scorer.
    """
    score = 0
    reasons = []

    overdue_tasks = project_data.get("overdue_tasks", 0)
    completion_pct = project_data.get("completion_pct", 0)
    days_remaining = project_data.get("days_remaining", 30)
    team_size = project_data.get("team_size", 5)
    open_blockers = project_data.get("open_blockers", 0)

    if overdue_tasks > 3:
        score += 30
        reasons.append(f"{overdue_tasks} overdue tasks")
    if completion_pct < 30 and days_remaining < 14:
        score += 35
        reasons.append("Low completion with tight deadline")
    if open_blockers > 0:
        score += 20
        reasons.append(f"{open_blockers} open blockers")
    if team_size < 3:
        score += 15
        reasons.append("Understaffed team")

    score = min(score, 100)

    if score >= 60:
        risk_level = "HIGH"
    elif score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons if reasons else ["Project on track"]
    }