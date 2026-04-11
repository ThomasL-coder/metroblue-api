from lead_scoring.predict import score_lead


def test_hot_lead():
    lead = {
        "source": "Facebook",
        "course_service": "IELTS",
        "gender": "Male",
        "location": "Darwin"
    }

    result = score_lead(lead)

    assert "score" in result
    assert "label" in result


def test_cold_lead():
    lead = {}

    result = score_lead(lead)

    assert "score" in result
    assert result["label"] in ["Cold", "Warm", "Hot"]


def test_missing_fields():
    lead = {
        "source": None,
        "course_service": None
    }

    result = score_lead(lead)

    assert isinstance(result, dict)
