
import os
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    session
)

from src.prediction import predict_traffic
from src.future_forecasting import forecast_traffic
from src.route_optimizer import get_routes

# Authentication
from auth import auth_bp, login_required, init_db


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_traffic_data.csv"
)

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

app.secret_key = "SmartFlow_AI_Traffic_Project_2026"


# ==========================================
# AUTHENTICATION INITIALIZATION
# ==========================================

app.register_blueprint(auth_bp)

with app.app_context():
    init_db()


# ==========================================
# FORM DATA
# ==========================================

def get_form_data():

    return {
        "hour": int(request.form["hour"]),

        "day_of_week": int(
            request.form["day_of_week"]
        ),

        "is_weekend": int(
            request.form["is_weekend"]
        ),

        "weather": request.form["weather"],

        "temperature_c": float(
            request.form["temperature"]
        ),

        "rainfall_mm": float(
            request.form["rainfall"]
        ),

        "road_type": request.form["road_type"],

        "month": int(request.form["month"]),

        "day": int(request.form["day"])
    }


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():

    try:

        df = pd.read_csv(DATASET_PATH)

        total_records = len(df)

        average_traffic = round(
            df["traffic_flow"].mean(), 2
        )

        maximum_traffic = round(
            df["traffic_flow"].max(), 2
        )

        minimum_traffic = round(
            df["traffic_flow"].min(), 2
        )

        low = int(
            (df["traffic_flow"] < 40).sum()
        )

        moderate = int(
            (
                (df["traffic_flow"] >= 40) &
                (df["traffic_flow"] < 80)
            ).sum()
        )

        heavy = int(
            (df["traffic_flow"] >= 80).sum()
        )

        latest_prediction = session.get(
            "latest_prediction"
        )

        return render_template(
            "dashboard.html",
            total_records=total_records,
            average_traffic=average_traffic,
            maximum_traffic=maximum_traffic,
            minimum_traffic=minimum_traffic,
            low=low,
            moderate=moderate,
            heavy=heavy,
            latest_prediction=latest_prediction
        )

    except Exception as error:

        return f"Dashboard Error: {error}", 500


# ==========================================
# TRAFFIC PREDICTION
# ==========================================

@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():

    if request.method == "GET":

        return render_template("prediction.html")

    try:

        data = get_form_data()

        result = predict_traffic(**data)

        session["latest_prediction"] = {
            "predicted_vehicle_count":
                result["predicted_vehicle_count"],

            "predicted_traffic":
                result["predicted_traffic"],

            "traffic_level":
                result["traffic_level"],

            "traffic_color":
                result["traffic_color"],

            "weather":
                data["weather"],

            "road_type":
                data["road_type"],

            "hour":
                data["hour"]
        }

        session.modified = True

        return render_template(
            "prediction.html",
            result=result,
            data=data
        )

    except (ValueError, KeyError):

        return render_template(
            "prediction.html",
            error="Please enter valid traffic details."
        )

    except Exception as error:

        return render_template(
            "prediction.html",
            error=f"Prediction Error: {error}"
        )


# ==========================================
# FUTURE TRAFFIC FORECAST
# ==========================================

@app.route("/forecast", methods=["GET", "POST"])
@login_required
def forecast():

    if request.method == "GET":

        return render_template("future_forecast.html")

    try:

        data = get_form_data()

        forecasts = forecast_traffic(**data)

        return render_template(
            "future_forecast.html",
            forecasts=forecasts
        )

    except (ValueError, KeyError):

        return render_template(
            "future_forecast.html",
            error="Please enter valid traffic details."
        )

    except Exception as error:

        return render_template(
            "future_forecast.html",
            error=f"Forecast Error: {error}"
        )


# ==========================================
# ROUTE PLANNER
# ==========================================

@app.route("/route-planner", methods=["GET", "POST"])
@login_required
def route_planner():

    if request.method == "GET":

        return render_template("route_planner.html")

    try:

        start_location = request.form.get(
            "start_location", ""
        ).strip()

        end_location = request.form.get(
            "end_location", ""
        ).strip()

        if not start_location or not end_location:

            return render_template(
                "route_planner.html",
                error="Please enter both starting location and destination."
            )

        if start_location.lower() == end_location.lower():

            return render_template(
                "route_planner.html",
                error="Starting location and destination cannot be the same."
            )

        result = get_routes(
            start_location,
            end_location
        )

        if not result or not result.get("routes"):

            return render_template(
                "route_planner.html",
                error="No routes found. Try different locations."
            )

        return render_template(
            "route_planner.html",
            routes=result["routes"],
            best_route=result["best_route"],
            start_location=start_location,
            end_location=end_location
        )

    except Exception as error:

        return render_template(
            "route_planner.html",
            error=f"Route Planning Error: {error}"
        )


# ==========================================
# TRAFFIC MAP
# ==========================================

@app.route("/traffic-map")
@login_required
def traffic_map():

    return render_template("traffic_map.html")


# ==========================================
# AI CHATBOT
# ==========================================

@app.route("/chatbot")
@login_required
def chatbot():

    return render_template("chatbot.html")


# ==========================================
# ANALYTICS
# ==========================================

@app.route("/analytics")
@login_required
def analytics():

    try:

        df = pd.read_csv(DATASET_PATH)

        total_records = len(df)

        average_traffic = round(
            df["traffic_flow"].mean(), 2
        )

        maximum_traffic = round(
            df["traffic_flow"].max(), 2
        )

        minimum_traffic = round(
            df["traffic_flow"].min(), 2
        )

        low = int(
            (df["traffic_flow"] < 40).sum()
        )

        moderate = int(
            (
                (df["traffic_flow"] >= 40) &
                (df["traffic_flow"] < 80)
            ).sum()
        )

        heavy = int(
            (df["traffic_flow"] >= 80).sum()
        )

        return render_template(
            "analytics.html",
            total_records=total_records,
            average_traffic=average_traffic,
            maximum_traffic=maximum_traffic,
            minimum_traffic=minimum_traffic,
            low=low,
            moderate=moderate,
            heavy=heavy
        )

    except Exception as error:

        return f"Analytics Error: {error}", 500


# ==========================================
# ABOUT PAGE
# ==========================================

@app.route("/about")
@login_required
def about():

    return render_template("about.html")


# ==========================================
# 404 ERROR HANDLER
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return """
    <h1>404 - Page Not Found</h1>
    <p>The requested page does not exist.</p>
    <a href="/">Go to Home Page</a>
    """, 404


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    print("\n======================================")
    print("           SMARTFLOW AI")
    print("   AI-POWERED TRAFFIC PREDICTION")
    print("======================================")

    print("Home          : http://127.0.0.1:5001/")
    print("Login         : http://127.0.0.1:5001/login")
    print("Register      : http://127.0.0.1:5001/register")
    print("Dashboard     : http://127.0.0.1:5001/dashboard")
    print("Prediction    : http://127.0.0.1:5001/predict")
    print("Forecast      : http://127.0.0.1:5001/forecast")
    print("Route Planner : http://127.0.0.1:5001/route-planner")
    print("Traffic Map   : http://127.0.0.1:5001/traffic-map")
    print("Chatbot       : http://127.0.0.1:5001/chatbot")
    print("Analytics     : http://127.0.0.1:5001/analytics")
    print("About         : http://127.0.0.1:5001/about")

    print("======================================\n")

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )