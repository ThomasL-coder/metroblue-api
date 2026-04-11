import os

import joblib
import pandas as pd

MODEL_DIR = os.getenv("MODEL_DIR", "Project/models")
MODEL_PATH = os.path.join(MODEL_DIR, "pipeline.pkl")


def score_to_label(score: float) -> str:
    if score < 0.30:
        return "Cold"
    if score < 0.60:
        return "Warm"
    return "Hot"


_model = None


def get_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    return _model


def _heuristic_score(lead_dict: dict) -> float:
    source = (lead_dict.get("source") or "").strip().lower()
    stage = (lead_dict.get("stage") or "").strip().lower()

    score = 0.35
    if source in {"google", "referral", "linkedin"}:
        score += 0.2
    if stage in {"qualified", "warm", "hot", "paid"}:
        score += 0.25
    if lead_dict.get("phone"):
        score += 0.1
    if lead_dict.get("location"):
        score += 0.05

    return max(0.01, min(0.99, score))


def score_lead(lead_dict: dict) -> dict:
    model = get_model()

    if model is None:
        score = _heuristic_score(lead_dict)
    else:
        df = pd.DataFrame([lead_dict])
        score = float(model.predict_proba(df)[0][1])

    label = score_to_label(score)
    return {"score": round(score, 2), "label": label, "top_factors": []}
