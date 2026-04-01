from app.revenue_forecasting.predict import forecast_revenue
from app.revenue_forecasting.overdue import get_overdue_installments

def test_forecast_returns_correct_number_of_months():
    result = forecast_revenue(months=3)
    assert len(result) == 3

def test_forecast_has_correct_keys():
    result = forecast_revenue(months=1)
    assert "month" in result[0]
    assert "predicted_revenue" in result[0]

def test_forecast_revenue_is_positive():
    result = forecast_revenue(months=3)
    for item in result:
        assert item["predicted_revenue"] >= 0

def test_overdue_returns_list():
    result = get_overdue_installments()
    assert isinstance(result, list)

def test_overdue_items_have_correct_keys():
    result = get_overdue_installments()
    if result:
        assert "installment_number" in result[0]
        assert "amount" in result[0]
        assert "days_overdue" in result[0]