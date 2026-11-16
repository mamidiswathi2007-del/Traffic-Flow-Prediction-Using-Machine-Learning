
import os
import joblib
import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR, "data", "processed", "cleaned_traffic_data.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "best_model.pkl"
)


def evaluate_model():

    print("\n========== SMARTFLOW AI ==========")
    print("MODEL EVALUATION")
    print("==================================")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Traffic dataset not found!")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained model not found! Train the model first.")

    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["traffic_flow", "timestamp"])
    y = df["traffic_flow"]

    split_index = int(len(df) * 0.8)

    X_test = X.iloc[split_index:]
    y_test = y.iloc[split_index:]

    model = joblib.load(MODEL_PATH)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print("\nEvaluation Results")
    print("-------------------")
    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2 Score:", round(r2, 4))

    print("\nModel evaluation completed successfully!")


if __name__ == "__main__":
    evaluate_model()
