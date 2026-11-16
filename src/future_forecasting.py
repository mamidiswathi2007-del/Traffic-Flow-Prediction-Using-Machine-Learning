from datetime import datetime, timedelta

from src.prediction import predict_traffic


def forecast_traffic(
    hour,
    day_of_week,
    is_weekend,
    weather,
    temperature_c,
    rainfall_mm,
    road_type,
    month,
    day
):

    current_date = datetime(2026, month, day, hour)

    forecast_hours = [1, 3, 6]

    results = []

    for future_hour in forecast_hours:

        future_date = current_date + timedelta(hours=future_hour)

        future_prediction = predict_traffic(
            hour=future_date.hour,
            day_of_week=future_date.weekday(),
            is_weekend=1 if future_date.weekday() >= 5 else 0,
            weather=weather,
            temperature_c=temperature_c,
            rainfall_mm=rainfall_mm,
            road_type=road_type,
            month=future_date.month,
            day=future_date.day
        )

        results.append({
            "time": future_date.strftime("%I:%M %p"),
            "hours_ahead": future_hour,
            "predicted_traffic": future_prediction["predicted_traffic"],
            "traffic_level": future_prediction["traffic_level"],
            "traffic_color": future_prediction["traffic_color"]
        })

    return results