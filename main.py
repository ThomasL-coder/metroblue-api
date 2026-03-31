from fastapi import FastAPI, Header, HTTPException, Depends, Request, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from database import engine, SessionLocal
from models import Base, Lead
from core.logging import logger
from utils.response import success_response, error_response
import subprocess
from datetime import datetime

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content=error_response("Internal server error")
    )

Base.metadata.create_all(bind=engine)

load_dotenv()
API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

class LeadRequest(BaseModel):
    name: str
    source: str
    course_service: str


@app.get("/")
def root():
    return success_response(message="Intern C API running")


@app.get("/api/health")
def health():
    return success_response(data={"status": "ok"})


@app.get("/api/seed")
def seed():
    db = SessionLocal()

    new_lead = Lead(
        name="Alice",
        source="Google",
        course_service="AI"
    )

    db.add(new_lead)
    db.commit()
    db.close()

    logger.info("Seed data inserted")

    return success_response(message="Data inserted")


@app.get("/api/stats")
def stats(api_key: str = Depends(verify_api_key)):
    db = SessionLocal()

    lead_count = db.query(Lead).count()
    db.close()

    logger.info("Fetched stats")

    return success_response(
    data={
        "leads": lead_count,
        "last_updated": datetime.utcnow().isoformat()
    },
    message="Stats fetched successfully"
)


@app.post("/api/leads/score")
def score_lead(
    lead: LeadRequest,
    api_key: str = Depends(verify_api_key)
):
    logger.info(f"Scoring lead: {lead.name}")

    if lead.source.lower() == "google":
        score = 0.8
        label = "Hot"
    else:
        score = 0.4
        label = "Cold"

    return success_response(
        data={"score": score, "label": label},
        message="Lead scored successfully"
    )


@app.get("/api/leads/scores")
def score_all_leads(api_key: str = Depends(verify_api_key)):
    db = SessionLocal()

    leads = db.query(Lead).all()
    results = []

    for lead in leads:
        score = 0.5  # replace with real logic 

        results.append({
            "lead_id": lead.id,
            "score": score
        })

    db.close()

    logger.info("Batch scoring completed")

    return success_response(
        data={"results": results},
        message="Batch scoring completed"
    )

@app.get("/api/revenue/forecast")
def revenue_forecast(
    months: int = Query(3, ge=1, le=12),
    api_key: str = Depends(verify_api_key)
):
    forecast = []

    for i in range(months):
        forecast.append({
            "month": f"Month {i+1}",
            "predicted_revenue": 50000 + i * 10000
        })

    logger.info(f"{months}-month forecast generated")

    return success_response(
        data={"forecast": forecast},
        message=f"{months}-month forecast generated"
    )


@app.get("/api/revenue/overdue")
def overdue_revenue(api_key: str = Depends(verify_api_key)):

    data = [
        {"client": "ABC Corp", "amount_due": 12000, "days_overdue": 15},
        {"client": "XYZ Ltd", "amount_due": 8500, "days_overdue": 30}
    ]

    logger.info("Fetched overdue revenue")

    return success_response(
        data=data,
        message="Overdue revenue fetched"
    )


@app.get("/api/clients/risk")
def client_risk(api_key: str = Depends(verify_api_key)):

    data = [
        {"client": "ABC Corp", "risk_level": "High", "reason": "Overdue payments"},
        {"client": "XYZ Ltd", "risk_level": "Medium", "reason": "Low engagement"}
    ]

    logger.info("Client risk analysis completed")

    return success_response(
        data=data,
        message="Client risk analysis completed"
    )


@app.post("/api/models/retrain")
def retrain_models(api_key: str = Depends(verify_api_key)):

    logger.info("Retrain started in background")

    script_path = os.path.join(os.getcwd(), "retrain.py")

    subprocess.Popen(["python3", script_path])

    return success_response(
        message="Retrain process started in background"
    )