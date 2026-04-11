
import joblib
import os
import pandas as pd

MODEL_PATH = os.path.join("models", "pipeline.pkl")


def score_to_label(score: float) -> str:
    if score < 0.30:
        return "Cold"
    elif score < 0.60:
        return "Warm"
    return "Hot"


# Lazy load model (important)
_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def score_lead(lead_dict: dict) -> dict:
    model = get_model()

    df = pd.DataFrame([lead_dict])

    # prediction
    score = float(model.predict_proba(df)[0][1])
    label = score_to_label(score)

    return {
        "score": round(score, 2),
        "label": label,
        "top_factors": []  # simplified for now
    }
