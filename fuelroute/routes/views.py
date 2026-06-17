from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd

import requests


@api_view(['GET', 'POST'])
def get_route(request):

    start = request.query_params.get("start")
    end = request.query_params.get("end")

    API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjQxNTEyZDNiZjdhYTQ4NDliNGI5YTI0ZjJmZTFiNTFmIiwiaCI6Im11cm11cjY0In0="

    headers = {
        "Authorization": API_KEY
    }

    start_res = requests.get(
        f"https://api.openrouteservice.org/geocode/search?text={start}&size=1",
        headers=headers
    ).json()

    end_res = requests.get(
        f"https://api.openrouteservice.org/geocode/search?text={end}&size=1",
        headers=headers
    ).json()

    start_coords = start_res["features"][0]["geometry"]["coordinates"]
    end_coords = end_res["features"][0]["geometry"]["coordinates"]

    route_res = requests.post(
        "https://api.openrouteservice.org/v2/directions/driving-car",
        headers={
            "Authorization": API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "coordinates": [
                start_coords,
                end_coords
            ]
        }
    ).json()

    distance_meters = route_res["routes"][0]["summary"]["distance"]
    distance_miles = distance_meters * 0.000621371

    try:
        df = pd.read_csv("fuel-prices-for-be-assessment.csv")

        stations = df[['City', 'State', 'Retail Price']].head(10)

        fuel_stops = []

        for _, row in stations.iterrows():
            fuel_stops.append({
                "city": row["City"],
                "state": row["State"],
                "price": float(row["Retail Price"])
            })

        average_price = sum(
            stop["price"] for stop in fuel_stops
        ) / len(fuel_stops)

        total_gallons = distance_miles / 10
        total_cost = total_gallons * average_price

        return Response({
            "start": start,
            "end": end,
            "distance_miles": round(distance_miles, 2),
            "total_cost": round(total_cost, 2),
            "fuel_stops": fuel_stops,
            "route":route_res["routes"][0]["geometry"]
        })

    except Exception as e:
        return Response({
            "error": str(e)
        })