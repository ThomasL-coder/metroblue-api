
import os
import joblib

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

from lead_scoring.db_extract import extract_lead_data


MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "pipeline.pkl")


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = extract_lead_data()

    # target
    df["converted"] = df["stage"].fillna("").str.lower().eq("paid").astype(int)

    # simple features
    features = ["source", "course_service", "gender", "location"]
    X = df[features].fillna("Unknown")
    y = df["converted"]

    # preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), features)
        ]
    )

    # model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X, y)

    joblib.dump(pipeline, MODEL_PATH)

    print("Model trained and saved!")


if __name__ == "__main__":
    main()
