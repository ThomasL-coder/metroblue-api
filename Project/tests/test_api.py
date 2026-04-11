from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "API Running"


def test_score_lead_api():
    payload = {
        "source": "Google",
        "course_service": "IELTS",
        "gender": "Female",
        "location": "Darwin",
    }

    response = client.post("/api/leads/score", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "score" in data
    assert "label" in data


def test_score_lead_api_empty():
    response = client.post("/api/leads/score", json={})
    assert response.status_code == 200

    data = response.json()
    assert "score" in data
    assert "label" in data


def test_revenue_forecast_api():
    response = client.get("/api/revenue/forecast?months=3")
    assert response.status_code == 200

    data = response.json()
    assert "forecast" in data
    assert len(data["forecast"]) == 3
