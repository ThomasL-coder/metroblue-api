
from fastapi import FastAPI
from pydantic import BaseModel

from lead_scoring import score_lead


app = FastAPI(title="Lead Scoring API")


class LeadInput(BaseModel):
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


@app.get("/")
def home():
    return {"message": "API Running"}


@app.post("/api/leads/score")
def score(payload: LeadInput):
    return score_lead(payload.model_dump())
