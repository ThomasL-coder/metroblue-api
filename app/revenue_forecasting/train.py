from __future__ import annotations
import json
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from app.config import settings
from app.revenue_forecasting.data import fetch_revenue_tables, RECURRING_CATEGORIES

MODEL_PATH = settings.model_dir / "revenue_model.joblib"


def build_monthly_revenue(payments: pd.DataFrame) -> pd.DataFrame:
    """Aggregate all payments into monthly totals."""
    payments = payments.copy()
    payments["date"] = pd.to_datetime(payments["date"], errors="coerce")
    payments = payments.dropna(subset=["date"])
    payments["month"] = payments["date"].dt.to_period("M").dt.to_timestamp()
    monthly = payments.groupby("month", as_index=False)["amount"].sum().sort_values("month")
    monthly["month_index"] = range(len(monthly))
    return monthly


def calculate_reliability_factor(installments: pd.DataFrame) -> float:
    """
    Calculate what percentage of past installments were paid on time.
    Returns a number between 0 and 1.
    Used to adjust forecast to be more realistic.
    """
    if installments.empty:
        return 1.0
    installments = installments.copy()
    installments["date_paid"] = pd.to_datetime(installments["date_paid"], errors="coerce")
    installments["due_date"] = pd.to_datetime(installments["due_date"], errors="coerce")
    paid = installments[installments["date_paid"].notna()].copy()
    if paid.empty:
        return 1.0
    paid["days_delay"] = (paid["date_paid"] - paid["due_date"]).dt.days
    on_time = (paid["days_delay"] <= 0).sum()
    return round(float(on_time / len(paid)), 4)


def build_category_forecasts(payments: pd.DataFrame) -> dict:
    """
    Split payments into recurring and one-time categories
    and build separate monthly totals for each.
    """
    payments = payments.copy()
    payments["date"] = pd.to_datetime(payments["date"], errors="coerce")
    payments = payments.dropna(subset=["date"])
    payments["month"] = payments["date"].dt.to_period("M").dt.to_timestamp()

    recurring = payments[payments["category"].isin(RECURRING_CATEGORIES)]
    one_time = payments[~payments["category"].isin(RECURRING_CATEGORIES)]

    def monthly_series(df):
        if df.empty:
            return []
        series = df.groupby("month", as_index=False)["amount"].sum().sort_values("month")
        return series.to_dict(orient="records")

    return {
        "recurring": monthly_series(recurring),
        "one_time": monthly_series(one_time),
    }


def train_revenue_model() -> dict:
    payments, installments, records = fetch_revenue_tables()
    monthly = build_monthly_revenue(payments)

    if len(monthly) < 2:
        monthly = pd.DataFrame({
            "month": [pd.Timestamp.today().to_period("M").to_timestamp()],
            "amount": [0.0],
            "month_index": [0]
        })

    X = monthly[["month_index"]]
    y = monthly["amount"]
    model = LinearRegression()
    model.fit(X, y)

    reliability_factor = calculate_reliability_factor(installments)

    installment_future = 0.0
    if not installments.empty:
        installments["due_date"] = pd.to_datetime(installments["due_date"], errors="coerce")
        future_installments = installments[
            installments["due_date"] >= pd.Timestamp.today().normalize()
        ]
        installment_future = float(future_installments["amount"].fillna(0).sum())

    category_forecasts = build_category_forecasts(payments)

    payload = {
        "model": model,
        "history": monthly.to_dict(orient="records"),
        "training_rows": int(len(monthly)),
        "installment_future_total": installment_future,
        "reliability_factor": reliability_factor,
        "category_forecasts": category_forecasts,
        "model_name": "linear_regression_monthly_revenue_v2",
    }
    joblib.dump(payload, MODEL_PATH)
    return payload


if __name__ == "__main__":
    result = train_revenue_model()
    print(json.dumps({
        "saved_to": str(MODEL_PATH),
        "model_name": result["model_name"],
        "training_rows": result["training_rows"],
        "reliability_factor": result["reliability_factor"],
        "installment_future_total": result["installment_future_total"],
    }, indent=2))