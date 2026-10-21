from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_metrics_endpoint_returns_200():
    # The /metrics endpoint must be reachable and return HTTP 200
    response = client.get("/metrics")
    assert response.status_code == 200