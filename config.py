
from pathlib import Path

# Main project directory
BASE_DIR = Path(__file__).resolve().parent

# Project folders
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODEL_DIR = BASE_DIR / "models"

TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Dataset and model paths
DATASET_PATH = RAW_DATA_DIR / "traffic_data.csv"
MODEL_PATH = MODEL_DIR / "traffic_model.pkl"

# Website settings
APP_NAME = "SmartFlow AI"
APP_DESCRIPTION = "Traffic Flow Prediction & Intelligent Travel Assistant"

# Default prediction settings
DEFAULT_CONGESTION_THRESHOLD = 70

# Create required folders automatically
for folder in [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODEL_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

