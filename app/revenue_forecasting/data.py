from __future__ import annotations
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db import get_engine

PAYMENTS_QUERY = """
SELECT amount, date, payment_type, category, client_id, purpose
FROM payments
"""
INSTALLMENTS_QUERY = """
SELECT amount, date_paid, due_date, installment_number
FROM sales_payment_installments
"""
RECORDS_QUERY = """
SELECT total_amount, balance, due_date, client_id
FROM sales_payment_records
"""

RECURRING_CATEGORIES = ["Retainer", "Subscription"]


def sample_revenue_data():
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=12, freq="MS")
    today = pd.Timestamp.today().normalize()
    payments = pd.DataFrame({
        "date": dates,
        "amount": [12000, 15000, 14500, 16000, 17250, 18000, 19400, 21000, 20500, 22300, 24000, 25000],
        "payment_type": ["Bank", "Cash", "Bank", "Mobile Payment", "Bank", "Cash", "Bank", "Bank", "Mobile Payment", "Bank", "Cash", "Bank"],
        "category": ["Retainer", "Project Fee", "Retainer", "Subscription", "Project Fee", "Retainer", "Subscription", "Project Fee", "Retainer", "Retainer", "Project Fee", "Subscription"],
        "client_id": range(1, 13),
        "purpose": "Sample"
    })
    installments = pd.DataFrame({
        "amount": [3000, 3200, 2800, 4000, 3500, 2900, 3000, 3200, 2800],
        "date_paid": [
            today - pd.Timedelta(days=30),
            today - pd.Timedelta(days=60),
            today - pd.Timedelta(days=10),
            today - pd.Timedelta(days=5),
            today - pd.Timedelta(days=20),
            today - pd.Timedelta(days=45),
            None, None, None
        ],
        "due_date": [
            today - pd.Timedelta(days=35),
            today - pd.Timedelta(days=55),
            today - pd.Timedelta(days=15),
            today - pd.Timedelta(days=20),
            today - pd.Timedelta(days=25),
            today - pd.Timedelta(days=30),
            today + pd.offsets.MonthBegin(1),
            today + pd.offsets.MonthBegin(2),
            today + pd.offsets.MonthBegin(3),
        ],
        "installment_number": range(1, 10),
    })
    records = pd.DataFrame({
        "total_amount": [9000],
        "balance": [4500],
        "due_date": [today + pd.offsets.MonthBegin(1)],
        "client_id": [99],
    })
    return payments, installments, records


def fetch_revenue_tables():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            payments = pd.read_sql(text(PAYMENTS_QUERY), conn)
            installments = pd.read_sql(text(INSTALLMENTS_QUERY), conn)
            records = pd.read_sql(text(RECORDS_QUERY), conn)
        if payments.empty:
            return sample_revenue_data()
        return payments, installments, records
    except SQLAlchemyError:
        return sample_revenue_data()