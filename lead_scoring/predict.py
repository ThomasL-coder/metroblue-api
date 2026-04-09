from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np

from .preprocess import transform_single_lead

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PACKAGE_ROOT / "models" / "lead_model.pkl"
METADATA_PATH = PACKAGE_ROOT / "models" / "model_metadata.json"



def score_to_label(score: float) -> str:
    if score < 0.30:
        return "Cold"
    if score < 0.60:
        return "Warm"
    return "Hot"



def load_assets():
    model = joblib.load(MODEL_PATH)
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    return model, metadata



def derive_top_factors(model, X_row, feature_names: list[str]) -> list[str]:
    classifier = model.named_steps.get("classifier")
    if classifier is None or not hasattr(classifier, "feature_importances_"):
        return []

    preprocessor = model.named_steps["preprocessor"]
    transformed = preprocessor.transform(X_row)
    if transformed.ndim == 1:
        transformed = transformed.reshape(1, -1)

    lead_vector = np.abs(np.asarray(transformed)[0])
    contributions = classifier.feature_importances_ * lead_vector

    ranked = sorted(
        [(feature_names[i], float(contributions[i])) for i in range(len(feature_names))],
        key=lambda x: x[1],
        reverse=True,
    )
    return [name for name, value in ranked if value > 0][:3]



def score_lead(lead_dict: dict) -> dict:
    model, metadata = load_assets()
    X_row = transform_single_lead(lead_dict, top_locations=metadata.get("top_locations"))

    if hasattr(model, "predict_proba"):
        score = float(model.predict_proba(X_row)[0][1])
    else:
        score = float(model.predict(X_row)[0])

    label = score_to_label(score)
    top_factors = derive_top_factors(model, X_row, metadata.get("feature_names", []))

    return {
        "score": round(score, 4),
        "label": label,
        "top_factors": top_factors,
    }


if __name__ == "__main__":
    sample_lead = {
        "name": "John Doe",
        "source": "Facebook",
        "course_service": "IELTS",
        "gender": "Male",
        "location": "Darwin",
        "created_at": "2026-03-20",
        "contacted_at": "2026-03-21",
        "referral_id": 2,
        "notes": "Interested in weekend batch",
        "phone": "0400000000",
    }
    print(score_lead(sample_lead))
