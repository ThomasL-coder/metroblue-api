from lead_scoring.predict import score_lead


def test_hot_lead():
    lead = {
        "source": "Google",
        "course_service": "IELTS",
        "gender": "Female",
        "location": "Darwin"
    }

    result = score_lead(lead)

    assert isinstance(result, dict)
    assert "score" in result
    assert "label" in result
    assert result["label"] in ["Cold", "Warm", "Hot"]


def test_cold_lead():
    lead = {}

    result = score_lead(lead)

    assert isinstance(result, dict)
    assert "score" in result
    assert "label" in result
    assert result["label"] in ["Cold", "Warm", "Hot"]


def test_missing_fields():
    lead = {
        "source": None,
        "course_service": None,
        "gender": None,
        "location": None
    }

    result = score_lead(lead)

    assert isinstance(result, dict)
    assert "score" in result
    assert "label" in result
    assert result["label"] in ["Cold", "Warm", "Hot"]
