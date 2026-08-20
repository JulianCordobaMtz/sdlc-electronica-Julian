from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.db import get_db
from app.main import app

client = TestClient(app)


def test_health_confirms_database_connection() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "reachable"}


def test_health_returns_503_when_database_is_unavailable() -> None:
    class UnavailableSession:
        def execute(self, statement):
            raise OperationalError("SELECT 1", {}, Exception("offline"))

    def override_unavailable_db():
        yield UnavailableSession()

    app.dependency_overrides[get_db] = override_unavailable_db
    try:
        response = client.get("/health")
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 503
    assert response.json()["detail"] == "Base de datos no disponible"
    assert response.json()["error"]["type"] == "http_error"
    assert response.json()["error"]["request_id"]


def test_metrics_exposes_request_count_and_duration() -> None:
    client.get("/health")

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "# TYPE sensorhub_http_requests_total counter" in response.text
    assert 'method="GET",path="/health",status="200"' in response.text
    assert "sensorhub_http_request_duration_seconds_count" in response.text
