import os
import subprocess
from datetime import date, datetime
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from core.logging import logger
from database import SessionLocal
from models import Client, Lead, Payment, SalePaymentRecord
from Project.lead_scoring.predict import score_lead as ml_score_lead
from utils.response import error_response, success_response

load_dotenv()

app = FastAPI()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error", exc_info=exc)
    return JSONResponse(status_code=500, content=error_response("Internal server error"))


def get_db():
    """Read-only DB session dependency (API layer never writes)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: str = Header(...)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


class LeadRequest(BaseModel):
    name: str | None = None
    source: str | None = None
    course_service: str | None = None
    gender: str | None = None
    location: str | None = None
    created_at: str | None = None
    contacted_at: str | None = None
    referral_id: int | None = None
    notes: str | None = None
    phone: str | None = None
    stage: str | None = None


@app.get("/")
def root():
    return success_response(message="MetroBlue API running")


@app.get("/api/health")
def health():
    return success_response(data={"status": "ok"})


@app.get("/api/config")
def frontend_config():
    """Frontend-safe settings. Use env-injected key value only."""
    return success_response(
        data={
            "api_url": os.getenv("PUBLIC_API_URL", "http://127.0.0.1:8000"),
            "api_key_header": "X-API-KEY",
            "requires_api_key": True,
        }
    )


@app.get("/api/stats")
def stats(api_key: str = Depends(verify_api_key), db: Session = Depends(get_db)):
    lead_count = db.query(Lead).count()
    client_count = db.query(Client).count()
    return success_response(
        data={
            "leads": lead_count,
            "clients": client_count,
            "last_updated": datetime.utcnow().isoformat(),
        },
        message="Stats fetched successfully",
    )


@app.post("/api/leads/score")
def score_lead(lead: LeadRequest, api_key: str = Depends(verify_api_key)):
    payload = lead.model_dump()
    result = ml_score_lead(payload)
    return success_response(data=result, message="Lead scored successfully")


@app.get("/api/leads/scores")
def score_all_leads(
    limit: int = Query(200, ge=1, le=5000),
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    leads = db.query(Lead).limit(limit).all()
    results: list[dict[str, Any]] = []

    for lead in leads:
        payload = {
            "name": lead.name,
            "source": lead.source,
            "course_service": lead.course_service,
            "gender": lead.gender,
            "location": lead.location,
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
            "contacted_at": lead.contacted_at.isoformat() if lead.contacted_at else None,
            "referral_id": lead.referral_id,
            "notes": lead.notes,
            "phone": lead.phone,
            "stage": lead.stage,
        }
        scored = ml_score_lead(payload)
        results.append(
            {
                "lead_id": lead.id,
                "name": lead.name,
                "stage": lead.stage,
                "score": scored["score"],
                "label": scored["label"],
            }
        )

    return success_response(data={"results": results}, message="Batch scoring completed")


@app.get("/api/revenue/forecast")
def revenue_forecast(
    months: int = Query(6, ge=1, le=24),
    history_months: int = Query(6, ge=1, le=36),
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(func.date_format(Payment.paid_at, "%Y-%m").label("month"), func.sum(Payment.amount).label("revenue"))
        .filter(Payment.paid_at.isnot(None))
        .group_by(func.date_format(Payment.paid_at, "%Y-%m"))
        .order_by(func.date_format(Payment.paid_at, "%Y-%m"))
        .all()
    )

    history = [{"month": month, "revenue": float(revenue or 0)} for month, revenue in rows]
    history = history[-history_months:]
    base = history[-1]["revenue"] if history else 0.0
    trend = (base * 0.03) if base else 1000.0

    forecast = []
    for i in range(1, months + 1):
        predicted = base + (trend * i)
        forecast.append(
            {
                "month": f"F+{i}",
                "predicted_revenue": round(predicted, 2),
                "lower_bound": round(predicted * 0.9, 2),
                "upper_bound": round(predicted * 1.1, 2),
            }
        )

    return success_response(
        data={"history": history, "forecast": forecast},
        message=f"{months}-month forecast generated",
    )


@app.get("/api/revenue/overdue")
def overdue_revenue(api_key: str = Depends(verify_api_key), db: Session = Depends(get_db)):
    today = date.today()
    records = (
        db.query(SalePaymentRecord, Client)
        .outerjoin(Client, SalePaymentRecord.client_id == Client.id)
        .filter(SalePaymentRecord.due_date.isnot(None))
        .all()
    )

    data = []
    for record, client in records:
        amount_due = float(record.amount_due or 0) - float(record.amount_paid or 0)
        days_overdue = (today - record.due_date).days if record.due_date else 0
        if days_overdue > 0 and amount_due > 0:
            data.append(
                {
                    "client": client.name if client else f"Client #{record.client_id}",
                    "amount_due": round(amount_due, 2),
                    "days_overdue": days_overdue,
                }
            )

    return success_response(data=data, message="Overdue revenue fetched")


@app.get("/api/clients/risk")
def client_risk(api_key: str = Depends(verify_api_key), db: Session = Depends(get_db)):
    overdue_payload = overdue_revenue(api_key=api_key, db=db)["data"]

    output = []
    for item in overdue_payload:
        days = item["days_overdue"]
        if days >= 45:
            level, reason = "High", "Payment overdue by 45+ days"
        elif days >= 20:
            level, reason = "Medium", "Payment overdue by 20+ days"
        else:
            level, reason = "Low", "Recent overdue payment"

        output.append({"client": item["client"], "risk_level": level, "reason": reason})

    return success_response(data=output, message="Client risk analysis completed")


@app.post("/api/models/retrain")
def retrain_models(api_key: str = Depends(verify_api_key)):
    logger.info("Retrain started in background")
    subprocess.Popen(["python3", "retrain.py"])
    return success_response(message="Retrain process started in background")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
