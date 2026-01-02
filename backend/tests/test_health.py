"""Test health check endpoint."""
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test that health check endpoint returns healthy status."""
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.0.0"
    assert data["service"] == "todo-api"
