import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError("Trained model not found!")

model = joblib.load(MODEL_PATH)


def predict_traffic(
    hour,
    day_of_week,
    is_weekend,
    weather,
    temperature_c,
    rainfall_mm,
    road_type,
    month=11,
    day=2
):

    input_data = pd.DataFrame([{
        "hour": int(hour),
        "day_of_week": int(day_of_week),
        "is_weekend": int(is_weekend),
        "weather": weather,
        "temperature_c": float(temperature_c),
        "rainfall_mm": float(rainfall_mm),
        "road_type": road_type,
        "month": int(month),
        "day": int(day)
    }])

    prediction = float(model.predict(input_data)[0])
    prediction = max(0, prediction)

    if prediction < 40:
        traffic_level = "Low"
        traffic_color = "green"

    elif prediction < 80:
        traffic_level = "Moderate"
        traffic_color = "yellow"

    else:
        traffic_level = "High"
        traffic_color = "red"

    return {
        "predicted_traffic": round(prediction, 2),
        "predicted_vehicle_count": round(prediction, 2),
        "traffic_level": traffic_level,
        "traffic_color": traffic_color
    }