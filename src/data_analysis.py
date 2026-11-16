import pandas as pd
import os

# Dataset path
DATA_PATH = "data/traffic_data.csv"

# Check dataset
if not os.path.exists(DATA_PATH):
    print("Dataset not found!")
    exit()

# Load dataset
df = pd.read_csv(DATA_PATH)

print("\n========== SMARTFLOW AI ==========")

# Dataset shape
print("\n1. Dataset Shape:")
print(df.shape)

# Column names
print("\n2. Dataset Columns:")
print(df.columns.tolist())

# First five records
print("\n3. First Five Records:")
print(df.head())

# Dataset information
print("\n4. Dataset Information:")
print(df.info())

# Missing values
print("\n5. Missing Values:")
print(df.isnull().sum())

# Statistical analysis
print("\n6. Statistical Analysis:")
print(df.describe())

# Traffic information
print("\n7. Average Traffic Flow:")
print(df["traffic_flow"].mean())

print("\n8. Maximum Traffic Flow:")
print(df["traffic_flow"].max())

print("\n9. Minimum Traffic Flow:")
print(df["traffic_flow"].min())

print("\nDataset Analysis Completed!")