from fastapi import FastAPI
from database import engine
from models import Base
from database import SessionLocal
from models import Lead
from fastapi import FastAPI, Header, HTTPException, Depends
import os
from dotenv import load_dotenv

from fastapi import Header, HTTPException
app = FastAPI()

# CREATE TABLES
Base.metadata.create_all(bind=engine)

load_dotenv()
API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

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