import os
import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from db_extract import extract_lead_data
from preprocess import build_features


MODELS_DIR = "models"
MODEL_PATH = os.path.join(MODELS_DIR, "lead_model.pkl")
COLUMNS_PATH = os.path.join(MODELS_DIR, "training_columns.pkl")
IMPORTANCE_CHART_PATH = os.path.join(MODELS_DIR, "feature_importance.png")


def evaluate_model(name, model, X, y):
    class_counts = y.value_counts()
    min_class_count = class_counts.min()

    print(f"\n{name} class counts: {class_counts.to_dict()}")

    if min_class_count < 2:
        print(f"Skipping cross-validation for {name} because one class has fewer than 2 samples.")

        model.fit(X, y)
        y_pred = model.predict(X)

        metrics = {
            "model_name": name,
            "accuracy": round(accuracy_score(y, y_pred), 4),
            "precision": round(precision_score(y, y_pred, zero_division=0), 4),
            "recall": round(recall_score(y, y_pred, zero_division=0), 4),
            "f1_score": round(f1_score(y, y_pred, zero_division=0), 4),
            "confusion_matrix": confusion_matrix(y, y_pred).tolist(),
        }
        return metrics

    n_splits = min(5, min_class_count)
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    y_pred = cross_val_predict(model, X, y, cv=cv)

    metrics = {
        "model_name": name,
        "accuracy": round(accuracy_score(y, y_pred), 4),
        "precision": round(precision_score(y, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y, y_pred, zero_division=0), 4),
        "f1_score": round(f1_score(y, y_pred, zero_division=0), 4),
        "confusion_matrix": confusion_matrix(y, y_pred).tolist(),
    }
    return metrics


def save_feature_importance(model, X: pd.DataFrame):
    if not hasattr(model, "feature_importances_"):
        return

    importances = pd.Series(model.feature_importances_, index=X.columns)
    top_features = importances.sort_values(ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    top_features.plot(kind="barh")
    plt.title("Top 10 Feature Importances")
    plt.tight_layout()
    plt.savefig(IMPORTANCE_CHART_PATH)
    plt.close()


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    df = extract_lead_data()
    X, y, _ = build_features(df)

    logistic = LogisticRegression(max_iter=1000, class_weight="balanced")
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    )

    logistic_metrics = evaluate_model("Logistic Regression", logistic, X, y)
    rf_metrics = evaluate_model("Random Forest", rf, X, y)

    print("Logistic Regression Metrics:")
    print(logistic_metrics)
    print("\nRandom Forest Metrics:")
    print(rf_metrics)

    # Pick best model by F1
    best_model = rf if rf_metrics["f1_score"] >= logistic_metrics["f1_score"] else logistic
    best_model_name = "Random Forest" if best_model == rf else "Logistic Regression"

    best_model.fit(X, y)

    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(list(X.columns), COLUMNS_PATH)

    if best_model_name == "Random Forest":
        save_feature_importance(best_model, X)

    print(f"\nSaved best model: {best_model_name}")
    print(f"Model path: {MODEL_PATH}")
    print(f"Columns path: {COLUMNS_PATH}")


if __name__ == "__main__":
    main()