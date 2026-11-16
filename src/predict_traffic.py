
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import pandas as pd

from config import MODEL_PATH



def predict_traffic(
    hour,
    day_of_week,
    temperature,
    rainfall,
    road_type,
):
    """Predict vehicle count using the trained ML model."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. Run src/train_model.py first."
        )

    model = joblib.load(MODEL_PATH)

    input_data = pd.DataFrame(
        [
            {
                "hour": hour,
                "day_of_week": day_of_week,
                "temperature": temperature,
                "rainfall": rainfall,
                "road_type": road_type,
            }
        ]
    )

    predicted_count = model.predict(input_data)[0]
    predicted_count = max(0, round(float(predicted_count)))

    # Demonstration thresholds; calibrate using real traffic data.
    if predicted_count < 600:
        traffic_level = "Low"
    elif predicted_count < 1000:
        traffic_level = "Moderate"
    else:
        traffic_level = "High"

    return {
        "predicted_vehicle_count": predicted_count,
        "traffic_level": traffic_level,
    }


if __name__ == "__main__":
    result = predict_traffic(
        hour=18,
        day_of_week=2,
        temperature=29,
        rainfall=0,
        road_type="Main Road",
    )

    print("\nSMARTFLOW AI - TRAFFIC PREDICTION")
    print("-" * 40)
    print(f"Predicted Vehicle Count: {result['predicted_vehicle_count']}")
    print(f"Traffic Level: {result['traffic_level']}")
