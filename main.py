from fastapi import FastAPI
from database import engine
from models import Base
from database import SessionLocal
from models import Lead
from fastapi import FastAPI, Header, HTTPException, Depends
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import Depends 
from fastapi import Header, HTTPException
app = FastAPI()

# CREATE TABLES
Base.metadata.create_all(bind=engine)

load_dotenv()
API_KEY = os.getenv("API_KEY")

class LeadRequest(BaseModel):
    name: str
    source: str
    course_service: str

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
@app.post("/api/leads/score")
def score_lead(
    lead: LeadRequest,
    api_key: str = Depends(verify_api_key)
):
    
    # FAKE ML LOGIC (for now)
    if lead.source.lower() == "google":
        score = 0.8
        label = "Hot"
    else:
        score = 0.4
        label = "Cold"

    return {
        "score": score,
        "label": label
    }



@app.get("/")
def root():
    return {"message": "Intern C API running "}

@app.get("/api/health")
def health():
    return {"status": "ok"}

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

    return {"message": "Data inserted "}

@app.get("/api/stats")
def stats(api_key: str = Depends(verify_api_key)):
    db = SessionLocal()

    lead_count = db.query(Lead).count()

    db.close()

    return {"leads": lead_count}

@app.get("/api/revenue/forecast")
def revenue_forecast(api_key: str = Depends(verify_api_key)):
    
    # FAKE forecast data
    return [
        {"month": "2026-04", "predicted_revenue": 50000},
        {"month": "2026-05", "predicted_revenue": 62000},
        {"month": "2026-06", "predicted_revenue": 71000}
    ]

@app.get("/api/revenue/overdue")
def overdue_revenue(api_key: str = Depends(verify_api_key)):

    # FAKE overdue data
    return [
        {"client": "ABC Corp", "amount_due": 12000, "days_overdue": 15},
        {"client": "XYZ Ltd", "amount_due": 8500, "days_overdue": 30}
    ]

@app.get("/api/clients/risk")
def client_risk(api_key: str = Depends(verify_api_key)):

    # FAKE risk data
    return [
        {"client": "ABC Corp", "risk_level": "High", "reason": "Overdue payments"},
        {"client": "XYZ Ltd", "risk_level": "Medium", "reason": "Low engagement"}
    ]

@app.post("/api/models/retrain")
def retrain_models(api_key: str = Depends(verify_api_key)):

    # FAKE retrain result
    return {
        "message": "Models retrained successfully",
        "lead_model_accuracy": 0.87,
        "revenue_model_accuracy": 0.82
    }
