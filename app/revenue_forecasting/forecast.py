from __future__ import annotations
from app.revenue_forecasting.predict import forecast_revenue

def get_forecast(months: int = 3) -> list:
    """
    Returns predicted revenue for the next N months.
    Each item has a month and predicted_revenue value.
    """
    return forecast_revenue(months=months)

if __name__ == "__main__":
    results = get_forecast(months=3)
    for item in results:
        print(f"{item['month']}: ₦{item['predicted_revenue']:,}")