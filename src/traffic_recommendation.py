
def get_traffic_recommendation(
    traffic_level,
    hour=None,
    road_type="Main Road"
):

    traffic_level = traffic_level.lower()

    if "low" in traffic_level:

        recommendation = {
            "title": "Smooth Traffic",
            "message": "Traffic is currently low. It is a good time to travel.",
            "suggestions": [
                "You can proceed with your journey.",
                "Maintain a safe driving speed.",
                "Follow traffic rules."
            ],
            "status": "green"
        }

    elif "moderate" in traffic_level:

        recommendation = {
            "title": "Moderate Traffic",
            "message": "Traffic is moderately busy. Allow some extra travel time.",
            "suggestions": [
                "Drive carefully and maintain a safe distance.",
                "Avoid unnecessary lane changes.",
                "Consider an alternative route if available."
            ],
            "status": "yellow"
        }

    else:

        recommendation = {
            "title": "Heavy Traffic",
            "message": "Heavy traffic is expected. Consider delaying your journey.",
            "suggestions": [
                "Check alternative routes.",
                "Avoid peak traffic hours if possible.",
                "Allow additional travel time.",
                "Follow traffic signals and drive patiently."
            ],
            "status": "red"
        }

    if hour is not None:

        if 8 <= hour <= 10 or 17 <= hour <= 20:
            recommendation["peak_hour_notice"] = (
                "This time falls within a typical peak-hour window."
            )
        else:
            recommendation["peak_hour_notice"] = (
                "This is outside the configured peak-hour window."
            )

    recommendation["road_type"] = road_type

    return recommendation


if __name__ == "__main__":

    result = get_traffic_recommendation(
        traffic_level="Moderate Traffic",
        hour=18,
        road_type="Main Road"
    )

    print("\n========== SMARTFLOW AI ==========")
    print("TRAFFIC RECOMMENDATIONS")
    print("==================================")

    for key, value in result.items():
        print(f"\n{key}: {value}")

    print("\nRecommendation generated successfully!")
