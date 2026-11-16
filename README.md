# 🚦 SmartFlow AI – Intelligent Traffic Flow Prediction

### AI-Powered Traffic Prediction and Smart Route Planning System

SmartFlow AI is a machine learning-based web application designed to predict traffic conditions, analyze traffic patterns, forecast future traffic flow, and support smarter route planning.

The project aims to help users understand traffic conditions and make better travel decisions using data-driven predictions.

## ✨ Key Features

- **Traffic Prediction:** Predicts traffic levels using machine learning.
- **Future Forecasting:** Forecasts future traffic conditions.
- **Smart Route Planner:** Helps users explore route options and estimated travel distances.
- **Traffic Analytics:** Visualizes traffic patterns and insights.
- **AI Chatbot:** Provides an interactive interface for traffic-related queries.
- **User Authentication:** Supports user registration and login.

## 🧠 Machine Learning

The project uses machine learning techniques to analyze traffic data and generate predictions.

**Model:** XGBoost

**Best Model Performance:**
- R² Score: 0.8528

## 🛠️ Technologies Used

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend | Flask |
| Frontend | HTML, CSS |
| Machine Learning | Scikit-learn, XGBoost |
| Data Processing | Pandas, NumPy |
| Database | SQLite |
| Development Tool | Visual Studio Code |

## 📂 Project Structure

```text
SmartFlow-AI/
│
├── data/
│   └── processed/
│
├── database/
│
├── models/
│
├── notebooks/
│
├── src/
│   ├── prediction.py
│   ├── future_forecasting.py
│   └── route_optimizer.py
│
├── static/
│
├── templates/
│
├── tests/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd SmartFlow-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

```text
http://127.0.0.1:5001
```

## 🎯 Project Objective

The main objective of SmartFlow AI is to use Artificial Intelligence and Machine Learning to improve traffic analysis, predict traffic conditions, and support intelligent route