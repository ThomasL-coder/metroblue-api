from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline

from .db_extract import extract_lead_data
from .preprocess import build_preprocessor, build_training_frame

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PACKAGE_ROOT / "models"
MODEL_PATH = MODELS_DIR / "lead_model.pkl"
METADATA_PATH = MODELS_DIR / "model_metadata.json"
IMPORTANCE_CHART_PATH = MODELS_DIR / "feature_importance.png"



def evaluate_model(name: str, model: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict:
    class_counts = y.value_counts()
    min_class_count = class_counts.min()

    if min_class_count < 2:
        model.fit(X, y)
        y_pred = model.predict(X)
    else:
        n_splits = min(5, int(min_class_count))
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        y_pred = cross_val_predict(model, X, y, cv=cv)

    return {
        "model_name": name,
        "accuracy": round(accuracy_score(y, y_pred), 4),
        "precision": round(precision_score(y, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y, y_pred, zero_division=0), 4),
        "f1_score": round(f1_score(y, y_pred, zero_division=0), 4),
        "confusion_matrix": confusion_matrix(y, y_pred).tolist(),
    }



def get_feature_names(fitted_pipeline: Pipeline) -> list[str]:
    preprocessor = fitted_pipeline.named_steps["preprocessor"]
    return list(preprocessor.get_feature_names_out())



def save_feature_importance(fitted_pipeline: Pipeline):
    classifier = fitted_pipeline.named_steps["classifier"]
    if not hasattr(classifier, "feature_importances_"):
        return

    feature_names = get_feature_names(fitted_pipeline)
    importances = pd.Series(classifier.feature_importances_, index=feature_names)
    top_features = importances.sort_values(ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    top_features.sort_values().plot(kind="barh")
    plt.title("Top 10 Feature Importances")
    plt.tight_layout()
    plt.savefig(IMPORTANCE_CHART_PATH)
    plt.close()



def build_candidate_pipelines() -> tuple[Pipeline, GridSearchCV]:
    logistic = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "classifier",
                LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
            ),
        ]
    )

    rf_pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "classifier",
                RandomForestClassifier(class_weight="balanced", random_state=42),
            ),
        ]
    )
    rf_grid = GridSearchCV(
        estimator=rf_pipeline,
        param_grid={
            "classifier__n_estimators": [100, 200, 400],
            "classifier__max_depth": [5, 10, None],
        },
        scoring="f1",
        cv=3,
        n_jobs=-1,
        refit=True,
    )
    return logistic, rf_grid



def main() -> dict:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    df = extract_lead_data()
    X, y, metadata = build_training_frame(df)

    logistic, rf_grid = build_candidate_pipelines()

    logistic_metrics = evaluate_model("Logistic Regression", logistic, X, y)
    rf_grid.fit(X, y)
    tuned_rf = rf_grid.best_estimator_
    rf_metrics = evaluate_model("Random Forest (GridSearchCV)", tuned_rf, X, y)

    if rf_metrics["f1_score"] >= logistic_metrics["f1_score"]:
        best_model = tuned_rf
        best_model_name = "Random Forest"
        best_params = rf_grid.best_params_
    else:
        best_model = logistic.fit(X, y)
        best_model_name = "Logistic Regression"
        best_params = {}

    if best_model_name == "Random Forest":
        best_model.fit(X, y)
        save_feature_importance(best_model)

    joblib.dump(best_model, MODEL_PATH)

    output_metadata = {
        "best_model_name": best_model_name,
        "best_params": best_params,
        "metrics": {
            "logistic_regression": logistic_metrics,
            "random_forest": rf_metrics,
        },
        "feature_names": get_feature_names(best_model),
        "top_locations": metadata["top_locations"],
        "training_rows": int(len(df)),
        "positive_rate": round(float(y.mean()), 4),
    }
    METADATA_PATH.write_text(json.dumps(output_metadata, indent=2), encoding="utf-8")

    print(json.dumps(output_metadata, indent=2))
    return output_metadata


if __name__ == "__main__":
    main()
