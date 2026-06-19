Fuel Route API

Overview

This Django REST API calculates a driving route between two US locations, estimates fuel costs, and suggests fuel stops using the provided fuel price dataset.

Features

- Route calculation between two US cities
- Fuel cost estimation
- Fuel stop suggestions
- Route geometry output
- Uses provided fuel price CSV dataset

Tech Stack

- Django
- Django REST Framework
- OpenRouteService API
- Pandas

Installation

git clone <repository-url>
cd fuel-route-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver

API Endpoint

GET /api/route/?start=Dallas&end=New+York

Example Response
{
  "start": "Dallas",
  "end": "New York",
  "distance_miles": 1553.83,
  "total_cost": 520.56,
  "fuel_stops": [...],
  "route": "encoded_polyline"
}

Returns:

- Start location
- End location
- Distance in miles
- Estimated fuel cost
- Fuel stops
- Route geometry