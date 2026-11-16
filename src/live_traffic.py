
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.prediction import predict_traffic


def get_live_traffic_estimate(
    weather="Clear",
    temperature_c=30.0,
    rainfall_mm=0.0,
    road_type="Main Road"
):
    """
    Generate a current-time traffic estimate using
    the trained ML model.

    Note: This is an ML-based estimate, not a
    real-time traffic sensor reading.
    """

    now = datetime.now()

    hour = now.hour
    day_of_week = now.weekday()
    is_weekend = 1 if day_of_week >= 5 else 0

    result = predict_traffic(
        hour=hour,
        day_of_week=day_of_week,
        is_weekend=is_weekend,
        weather=weather,
        temperature_c=temperature_c,
        rainfall_mm=rainfall_mm,
        road_type=road_type,
        month=now.month,
        day=now.day
    )

    return {
        "location_type": road_type,
        "current_time": now.strftime("%I:%M %p"),
        "weather": weather,
        "temperature_c": temperature_c,
        "rainfall_mm": rainfall_mm,
        "predicted_traffic": result["predicted_traffic"],
        "traffic_level": result["traffic_level"],
        "traffic_color": result["traffic_color"],
        "source": "Machine Learning Prediction"
    }


if __name__ == "__main__":

    try:
        result = get_live_traffic_estimate()

        print("\n========== SMARTFLOW AI ==========")
        print("CURRENT-TIME TRAFFIC ESTIMATE")
        print("==================================")

        for key, value in result.items():
            print(f"{key}: {value}")

        print("\nTraffic estimation completed!")

    except Exception as error:
        print("Traffic Estimation Error:", error)
