def forecast_revenue(months=3):
    data = []

    for i in range(1, months + 1):
        data.append({
            "month": f"Month {i}",
            "revenue": 50000 + i * 2000
        })

    return {
        "forecast": data
    }
