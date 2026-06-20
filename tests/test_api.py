import sys

sys.path.append(".")

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_categories():

    response = client.get("/categories")

    assert response.status_code == 200

    categories = response.json()

    assert isinstance(categories, list)
    assert len(categories) > 0


def test_regions():

    response = client.get("/regions")

    assert response.status_code == 200

    regions = response.json()

    assert isinstance(regions, list)
    assert len(regions) > 0


def test_summary():

    response = client.get("/summary")

    assert response.status_code == 200

    summary = response.json()

    assert "top_category" in summary
    assert "top_region" in summary
    assert "average_forecast_revenue" in summary


def test_forecast():

    response = client.get("/forecast")

    assert response.status_code == 200

    forecast = response.json()

    assert isinstance(forecast, list)
    assert len(forecast) > 0

    first_record = forecast[0]

    assert "forecast_date" in first_record
    assert "category" in first_record
    assert "region" in first_record
    assert "predicted_revenue" in first_record