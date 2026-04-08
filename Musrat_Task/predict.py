import joblib
from preprocess import transform_single_lead


MODEL_PATH = "models/lead_model.pkl"
COLUMNS_PATH = "models/training_columns.pkl"


def score_to_label(score: float) -> str:
    if score < 0.30:
        return "Cold"
    if score < 0.60:
        return "Warm"
    return "Hot"


def score_lead(lead_dict: dict) -> dict:
    model = joblib.load(MODEL_PATH)
    training_columns = joblib.load(COLUMNS_PATH)

    X = transform_single_lead(lead_dict, training_columns)

    if hasattr(model, "predict_proba"):
        score = float(model.predict_proba(X)[0][1])
    else:
        score = float(model.predict(X)[0])

    label = score_to_label(score)

    top_factors = []
    if lead_dict.get("referral_id"):
        top_factors.append("has_referral")
    if lead_dict.get("notes"):
        top_factors.append("has_notes")
    if lead_dict.get("phone"):
        top_factors.append("has_phone")

    return {
        "score": round(score, 2),
        "label": label,
        "top_factors": top_factors[:3]
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
        "phone": "0400000000"
    }

    result = score_lead(sample_lead)
    print(result)