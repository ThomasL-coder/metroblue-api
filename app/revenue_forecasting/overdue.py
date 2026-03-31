from __future__ import annotations
import pandas as pd
from app.revenue_forecasting.data import fetch_revenue_tables

def get_overdue_installments() -> list:
    """
    Returns a list of installments that are past their due date
    and have not been paid yet.
    """
    _, installments, _ = fetch_revenue_tables()

    if installments.empty:
        return []

    installments = installments.copy()
    installments["date_paid"] = pd.to_datetime(installments["date_paid"], errors="coerce")
    installments["due_date"] = pd.to_datetime(installments["due_date"], errors="coerce")

    today = pd.Timestamp.today().normalize()

    # Overdue = not paid AND due date has already passed
    overdue = installments[
        (installments["date_paid"].isna()) &
        (installments["due_date"] < today)
    ].copy()

    overdue["days_overdue"] = (today - overdue["due_date"]).dt.days

    result = []
    for _, row in overdue.iterrows():
        result.append({
            "installment_number": int(row["installment_number"]),
            "amount": float(row["amount"]),
            "due_date": row["due_date"].strftime("%Y-%m-%d"),
            "days_overdue": int(row["days_overdue"]),
        })

    return sorted(result, key=lambda x: x["days_overdue"], reverse=True)

if __name__ == "__main__":
    overdue = get_overdue_installments()
    if not overdue:
        print("No overdue installments.")
    for item in overdue:
        print(f"Installment #{item['installment_number']} — ₦{item['amount']:,} — {item['days_overdue']} days overdue")