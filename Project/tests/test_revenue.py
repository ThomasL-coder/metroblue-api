from revenue_forecasting.forecast import forecast_revenue


def test_forecast_default():
    result = forecast_revenue()

    assert isinstance(result, dict)
    assert "forecast" in result
    assert len(result["forecast"]) == 3


def test_forecast_custom_months():
    result = forecast_revenue(5)

    assert isinstance(result, dict)
    assert "forecast" in result
    assert len(result["forecast"]) == 5


def test_forecast_row_shape():
    result = forecast_revenue(2)

    first = result["forecast"][0]
    assert "month" in first
    assert "revenue" in first or "predicted_revenue" in first
