
import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


print("\n========== SMARTFLOW AI ==========")
print("MACHINE LEARNING MODEL TRAINING")
print("==================================")

# 1. Load Dataset
df = pd.read_csv("data/processed/cleaned_traffic_data.csv")

print("\nDataset Loaded Successfully!")
print("Dataset Shape:", df.shape)

# 2. Separate Input and Output
X = df.drop(columns=["traffic_flow", "timestamp"])
y = df["traffic_flow"]

# 3. Identify Numerical and Categorical Columns
numerical_features = X.select_dtypes(include=["number"]).columns.tolist()
categorical_features = X.select_dtypes(include=["object", "str"]).columns.tolist()

# 4. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numerical_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# 5. Split Data Chronologically
split_index = int(len(X) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining Records:", len(X_train))
print("Testing Records:", len(X_test))

# 6. Create Models
models = {
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),

    "XGBoost": XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        objective="reg:squarederror",
        random_state=42
    )
}

os.makedirs("models", exist_ok=True)

results = {}
trained_models = {}

# 7. Train and Evaluate Models
for name, model in models.items():

    print(f"\nTraining {name} Model...")

    pipeline = Pipeline([
        ("preprocessing", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    results[name] = {
        "MAE": mae,
        "RMSE": rmse,
        "R2 Score": r2
    }

    trained_models[name] = pipeline

    print(f"{name} Training Completed!")
    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2 Score:", round(r2, 4))

    joblib.dump(pipeline, f"models/{name.lower().replace(' ', '_')}.pkl")

# 8. Select Best Model
best_model_name = min(results, key=lambda name: results[name]["RMSE"])

best_model = trained_models[best_model_name]

joblib.dump(best_model, "models/best_model.pkl")

# 9. Save Evaluation Results
results_df = pd.DataFrame(results).T
results_df.to_csv("models/model_results.csv")

print("\n==================================")
print("MODEL COMPARISON")
print("==================================")

print(results_df)

print("\nBEST MODEL:", best_model_name)
print("Best model saved successfully!")

print("\nMACHINE LEARNING TRAINING COMPLETED!")

