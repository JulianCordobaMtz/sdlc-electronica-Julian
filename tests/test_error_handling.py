import json
import logging

from fastapi.testclient import TestClient

from app.db import get_db
from app.logging_config import JsonFormatter
from app.main import app
from app.routers.sensor_router import get_sensor_service

client = TestClient(app, raise_server_exceptions=False)


def test_http_error_has_consistent_structure_and_request_id() -> None:
    class MissingSensorService:
        def get_sensor(self, sensor_id: str):
            raise ValueError("Sensor no encontrado")

    app.dependency_overrides[get_sensor_service] = lambda: MissingSensorService()
    try:
        response = client.get(
            "/sensors/NO-EXISTE",
            headers={"X-Request-ID": "test-request-123"},
        )
    finally:
        app.dependency_overrides.pop(get_sensor_service, None)

    assert response.status_code == 404
    assert response.headers["X-Request-ID"] == "test-request-123"
    assert response.json() == {
        "error": {
            "type": "http_error",
            "message": "Sensor no encontrado",
            "request_id": "test-request-123",
        },
        "detail": "Sensor no encontrado",
    }


def test_validation_error_has_consistent_structure() -> None:
    response = client.get("/sensors", params={"limit": 0})

    assert response.status_code == 422
    assert response.json()["error"]["type"] == "validation_error"
    assert response.json()["error"]["request_id"]
    assert isinstance(response.json()["detail"], list)


def test_unexpected_error_is_hidden_from_client() -> None:
    def unavailable_dependency():
        raise RuntimeError("contraseña-secreta-no-debe-salir")
        yield

    app.dependency_overrides[get_db] = unavailable_dependency
    try:
        response = client.get("/health")
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 500
    assert response.json()["error"]["type"] == "internal_error"
    assert "contraseña-secreta" not in response.text


def test_json_formatter_produces_machine_readable_log() -> None:
    record = logging.LogRecord(
        name="sensorhub",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Solicitud procesada",
        args=(),
        exc_info=None,
    )
    record.event = "http_request"
    record.request_id = "request-456"
    record.status_code = 200

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["message"] == "Solicitud procesada"
    assert payload["event"] == "http_request"
    assert payload["request_id"] == "request-456"
    assert payload["status_code"] == 200
