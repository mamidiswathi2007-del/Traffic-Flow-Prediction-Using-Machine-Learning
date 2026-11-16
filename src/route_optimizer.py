import requests

HEADERS = {
    "User-Agent": "SmartFlowAI/1.0 (student project)"
}


# STEP 1: FIND LOCATION COORDINATES
def get_coordinates(location):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": location,
        "format": "json",
        "limit": 1
    }

    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError(f"Location not found: {location}")

    latitude = float(data[0]["lat"])
    longitude = float(data[0]["lon"])

    return longitude, latitude


# STEP 2: FIND ALTERNATIVE ROUTES
def get_routes(start_location, end_location):

    start_lon, start_lat = get_coordinates(start_location)

    end_lon, end_lat = get_coordinates(end_location)

    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
    )

    params = {
        "alternatives": "true",
        "overview": "false",
        "steps": "false"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        raise ValueError("No driving routes found.")

    routes = []

    for index, route in enumerate(data["routes"], start=1):

        distance_km = round(route["distance"] / 1000, 2)

        duration_minutes = round(route["duration"] / 60)

        routes.append({
            "route_number": index,
            "distance": distance_km,
            "duration": duration_minutes
        })

    # Shortest-distance route suggestion
    best_route = min(routes, key=lambda route: route["distance"])

    return {
        "routes": routes,
        "best_route": best_route
    }


# STEP 3: TEST THE ROUTE PLANNER
if __name__ == "__main__":

    try:

        result = get_routes(
            "Miyapur, Hyderabad",
            "HITEC City, Hyderabad"
        )

        print("\n========== SMARTFLOW AI ==========")
        print("SMART ROUTE PLANNER")
        print("==================================")

        for route in result["routes"]:

            print(f"\nRoute {route['route_number']}")

            print("Distance:", route["distance"], "KM")

            print("Estimated Time:", route["duration"], "Minutes")

        print("\nBEST ROUTE:")

        print("Distance:", result["best_route"]["distance"], "KM")

        print("Estimated Time:", result["best_route"]["duration"], "Minutes")

        print("\nROUTE PLANNING COMPLETED!")

    except Exception as error:

        print("\nRoute Planning Error:", error)