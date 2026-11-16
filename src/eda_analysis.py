import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_traffic_data.csv")

# Create graph folder
os.makedirs("static/graphs", exist_ok=True)

sns.set_theme(style="whitegrid")

# 1. Traffic by Hour
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x="hour", y="traffic_flow", errorbar=None)
plt.title("Traffic Flow by Hour")
plt.xlabel("Hour")
plt.ylabel("Traffic Flow")
plt.savefig("static/graphs/traffic_by_hour.png")
plt.close()

# 2. Traffic by Weather
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="weather", y="traffic_flow", errorbar=None)
plt.title("Traffic Flow by Weather")
plt.xticks(rotation=30)
plt.savefig("static/graphs/traffic_by_weather.png")
plt.close()

# 3. Traffic by Road Type
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="road_type", y="traffic_flow", errorbar=None)
plt.title("Traffic Flow by Road Type")
plt.xticks(rotation=30)
plt.savefig("static/graphs/traffic_by_road.png")
plt.close()

# 4. Weekday vs Weekend
df["day_category"] = df["is_weekend"].map({
    0: "Weekday",
    1: "Weekend"
})

plt.figure(figsize=(7, 5))
sns.barplot(data=df, x="day_category", y="traffic_flow", errorbar=None)
plt.title("Weekday vs Weekend Traffic")
plt.savefig("static/graphs/weekday_weekend.png")
plt.close()

# 5. Temperature vs Traffic
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="temperature_c", y="traffic_flow")
plt.title("Temperature vs Traffic")
plt.savefig("static/graphs/temperature_traffic.png")
plt.close()

# 6. Rainfall vs Traffic
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="rainfall_mm", y="traffic_flow")
plt.title("Rainfall vs Traffic")
plt.savefig("static/graphs/rainfall_traffic.png")
plt.close()

# 7. Correlation Heatmap
plt.figure(figsize=(9, 6))
sns.heatmap(
    df.select_dtypes(include="number").corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Traffic Data Correlation")
plt.savefig("static/graphs/correlation_heatmap.png")
plt.close()

print("EDA COMPLETED SUCCESSFULLY!")
print("7 Graphs Generated Successfully!")