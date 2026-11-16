import pandas as pd
import os

# Dataset location
DATA_PATH = "data/traffic_data.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("SMARTFLOW AI - DATA PREPROCESSING")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Remove duplicate records
df = df.drop_duplicates()

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Handle missing values
for column in df.select_dtypes(include="number").columns:
    df[column] = df[column].fillna(df[column].median())

for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].fillna(df[column].mode()[0])

# Create additional time features
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day

# Save processed dataset
os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    "data/processed/cleaned_traffic_data.csv",
    index=False
)

print("\nPreprocessing Completed Successfully!")
print("\nFinal Dataset Shape:", df.shape)

print("\nNew Dataset Columns:")
print(df.columns.tolist())

print("\nCleaned dataset saved successfully!")