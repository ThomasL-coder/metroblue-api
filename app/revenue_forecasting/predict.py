from __future__ import annotations
import joblib
import pandas as pd
from app.revenue_forecasting.train import train_revenue_model, MODEL_PATH


def load_artifacts():
    if not MODEL_PATH.exists():
        train_revenue_model()
    return joblib.load(MODEL_PATH)


def forecast_revenue(months: int = 3):
    """
    Forecast monthly revenue for the next N months.
    Applies reliability factor to make predictions more realistic.
    """
    months = max(1, min(int(months), 24))
    artifacts = load_artifacts()
    model = artifacts["model"]
    history = pd.DataFrame(artifacts["history"])
    reliability_factor = artifacts.get("reliability_factor", 1.0)

    last_idx = int(history["month_index"].max()) if not history.empty else 0
    last_month = (
        pd.to_datetime(history["month"].max())
        if not history.empty
        else pd.Timestamp.today().to_period("M").to_timestamp()
    )

    future = []
    for i in range(1, months + 1):
        idx = last_idx + i
        month = (last_month + pd.offsets.MonthBegin(i)).to_period("M").to_timestamp()
        raw_pred = float(model.predict([[idx]])[0])
        raw_pred = max(0.0, raw_pred)
        adjusted_pred = round(raw_pred * reliability_factor, 2)
        future.append({
            "month": month.strftime("%Y-%m"),
            "predicted_revenue": adjusted_pred,
        })
    return future