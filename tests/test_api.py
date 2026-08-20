from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models.reading import ReadingModel

# 1. Configurar una base de datos SQLite EN MEMORIA (se borra al terminar)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# 2. Inyección de dependencias: Le decimos a FastAPI que use la DB de prueba
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# 3. Este "fixture" recrea las tablas limpias antes de cada test
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ================= TESTS DE SENSORES =================


def test_crear_y_obtener_sensor():
    # POST: Crear un sensor
    response_post = client.post(
        "/sensors",
        json={
            "sensor_id": "TEMP-01",
            "name": "Sensor de caldera",
            "type": "temperatura",
            "location": "Sotano",
        },
    )
    assert response_post.status_code == 201
    assert response_post.json()["sensor_id"] == "TEMP-01"

    # GET: Verificar que se guardó
    response_get = client.get("/sensors/TEMP-01")
    assert response_get.status_code == 200
    assert response_get.json()["name"] == "Sensor de caldera"


def test_sensor_no_encontrado_devuelve_404():
    response = client.get("/sensors/ID-FALSO")
    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor no encontrado"


def test_sensor_duplicado_devuelve_409():
    payload = {
        "sensor_id": "TEMP-DUP",
        "name": "Sensor duplicado",
        "type": "temperatura",
    }
    first_response = client.post("/sensors", json=payload)
    duplicate_response = client.post("/sensors", json=payload)

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert "Ya existe un sensor" in duplicate_response.json()["detail"]


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 0},
        {"limit": 101},
        {"offset": -1},
    ],
)
def test_paginacion_de_sensores_rechaza_limites_invalidos(params):
    response = client.get("/sensors", params=params)

    assert response.status_code == 422


# ================= TESTS DE LECTURAS =================


def test_crear_lectura_exitosa():
    # Primero creamos el sensor padre
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-02", "name": "Sensor 2", "type": "temperatura"},
    )

    # Registramos su lectura
    response = client.post(
        "/sensors/TEMP-02/readings", json={"value": 25.5, "unit": "C"}
    )
    assert response.status_code == 201
    assert response.json()["value"] == 25.5


def test_validacion_fisica_cero_absoluto_devuelve_400():
    # Creamos el sensor
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-03", "name": "Sensor 3", "type": "temperatura"},
    )

    # Intentamos registrar una temperatura imposible en el universo
    response = client.post(
        "/sensors/TEMP-03/readings",
        json={
            "value": -300,  # Falla la validación Pydantic
            "unit": "C",
        },
    )
    assert response.status_code == 400
    assert "cero absoluto" in response.json()["detail"]


def test_rechaza_lectura_de_sensor_inexistente():
    response = client.post(
        "/sensors/NO-EXISTE/readings", json={"value": 20.0, "unit": "C"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Sensor no encontrado"


def test_rechaza_lectura_de_sensor_inactivo():
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-OFF", "name": "Off", "type": "temperatura"},
    )
    client.delete("/sensors/TEMP-OFF")

    response = client.post(
        "/sensors/TEMP-OFF/readings", json={"value": 20.0, "unit": "C"}
    )

    assert response.status_code == 400
    assert "sensor inactivo" in response.json()["detail"]


def test_valida_humedad_segun_tipo_de_sensor():
    client.post(
        "/sensors",
        json={"sensor_id": "HUM-01", "name": "Humedad", "type": "humedad"},
    )

    valid_response = client.post(
        "/sensors/HUM-01/readings", json={"value": 60.0, "unit": "%"}
    )
    invalid_response = client.post(
        "/sensors/HUM-01/readings", json={"value": 120.0, "unit": "%"}
    )

    assert valid_response.status_code == 201
    assert invalid_response.status_code == 400

    # ================= TESTS PARA COMPLETAR COBERTURA =================


def test_operaciones_completas_sensores():
    # 1. Crear
    client.post(
        "/sensors", json={"sensor_id": "SENS-04", "name": "S4", "type": "humedad"}
    )

    # 2. Listar
    response_list = client.get("/sensors")
    assert len(response_list.json()) > 0

    # 3. Actualizar (PATCH)
    response_patch = client.patch("/sensors/SENS-04", json={"name": "S4 Actualizado"})
    assert response_patch.status_code == 200
    assert response_patch.json()["name"] == "S4 Actualizado"

    # 4. Eliminar (DELETE)
    response_delete = client.delete("/sensors/SENS-04")
    assert response_delete.status_code == 204


def test_operaciones_completas_lecturas():
    # 1. Crear sensor padre
    client.post(
        "/sensors", json={"sensor_id": "SENS-05", "name": "S5", "type": "temperatura"}
    )

    # 2. Crear lectura
    res_create = client.post(
        "/sensors/SENS-05/readings", json={"value": 20.0, "unit": "C"}
    )
    reading_id = res_create.json()["id"]

    # 3. Listar lecturas del sensor
    res_list = client.get("/sensors/SENS-05/readings")
    assert res_list.status_code == 200

    # 4. Obtener lectura individual
    res_get = client.get(f"/readings/{reading_id}")
    assert res_get.status_code == 200

    # 5. Actualizar lectura
    res_patch = client.patch(f"/readings/{reading_id}", json={"value": 22.5})
    assert res_patch.status_code == 200

    # 6. Eliminar lectura
    res_del = client.delete(f"/readings/{reading_id}")
    assert res_del.status_code == 204


def test_estadisticas_por_sensor_ignoran_lecturas_eliminadas():
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-STATS", "name": "Stats", "type": "temperatura"},
    )
    reading_ids = []
    for value in (10.0, 20.0, 30.0, 100.0):
        response = client.post(
            "/sensors/TEMP-STATS/readings", json={"value": value, "unit": "C"}
        )
        reading_ids.append(response.json()["id"])

    client.delete(f"/readings/{reading_ids[-1]}")

    response = client.get("/sensors/TEMP-STATS/statistics")

    assert response.status_code == 200
    assert response.json() == {
        "sensor_id": "TEMP-STATS",
        "from_date": None,
        "to_date": None,
        "count": 3,
        "minimum": 10.0,
        "maximum": 30.0,
        "average": 20.0,
    }


def test_estadisticas_sin_lecturas_devuelven_404():
    response = client.get("/sensors/SIN-LECTURAS/statistics")

    assert response.status_code == 404


def test_consulta_de_lecturas_requiere_sensor_existente():
    response = client.get("/sensors/NO-EXISTE/readings")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor no encontrado"


def test_consulta_de_lecturas_rechaza_periodo_invertido():
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-DATE", "name": "Fechas", "type": "temperatura"},
    )

    response = client.get(
        "/sensors/TEMP-DATE/readings",
        params={"from": "2026-08-19T12:00:00", "to": "2026-08-18T12:00:00"},
    )

    assert response.status_code == 400
    assert "no puede ser mayor" in response.json()["detail"]


def test_consulta_de_lecturas_filtra_fechas_y_pagina_resultados():
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-FILTER", "name": "Filtro", "type": "temperatura"},
    )
    for value in (10.0, 20.0, 30.0):
        client.post(
            "/sensors/TEMP-FILTER/readings",
            json={"value": value, "unit": "C"},
        )

    with TestingSessionLocal() as db:
        readings = list(
            db.scalars(
                select(ReadingModel)
                .where(ReadingModel.sensor_id == "TEMP-FILTER")
                .order_by(ReadingModel.id)
            )
        )
        readings[0].timestamp = datetime.fromisoformat("2026-08-17T12:00:00")
        readings[1].timestamp = datetime.fromisoformat("2026-08-18T12:00:00")
        readings[2].timestamp = datetime.fromisoformat("2026-08-19T12:00:00")
        db.commit()

    response = client.get(
        "/sensors/TEMP-FILTER/readings",
        params={
            "from": "2026-08-18T00:00:00",
            "to": "2026-08-19T23:59:59",
            "limit": 1,
            "offset": 1,
        },
    )

    assert response.status_code == 200
    assert [reading["value"] for reading in response.json()] == [30.0]


def _crear_alerta_de_prueba(sensor_id: str = "TEMP-ALERT") -> int:
    client.post(
        "/sensors",
        json={
            "sensor_id": sensor_id,
            "name": "Sensor de alertas",
            "type": "temperatura",
            "alert_threshold": 30.0,
        },
    )
    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={"value": 31.0, "unit": "C"},
    )
    assert response.status_code == 201

    alerts = client.get("/alerts", params={"status": "open"})
    assert alerts.status_code == 200
    return alerts.json()[0]["id"]


def test_alerta_sigue_flujo_open_acknowledged_resolved():
    alert_id = _crear_alerta_de_prueba()

    acknowledged = client.patch(f"/alerts/{alert_id}", json={"status": "acknowledged"})
    resolved = client.patch(f"/alerts/{alert_id}", json={"status": "resolved"})

    assert acknowledged.status_code == 200
    assert acknowledged.json()["status"] == "acknowledged"
    assert resolved.status_code == 200
    assert resolved.json()["status"] == "resolved"


def test_alerta_rechaza_salto_directo_a_resolved():
    alert_id = _crear_alerta_de_prueba("TEMP-SKIP")

    response = client.patch(f"/alerts/{alert_id}", json={"status": "resolved"})

    assert response.status_code == 409
    assert "open -> resolved" in response.json()["detail"]


def test_alerta_rechaza_estado_desconocido():
    alert_id = _crear_alerta_de_prueba("TEMP-UNKNOWN")

    response = client.patch(f"/alerts/{alert_id}", json={"status": "closed"})

    assert response.status_code == 422


def test_alerta_inexistente_devuelve_404():
    response = client.patch("/alerts/999", json={"status": "acknowledged"})

    assert response.status_code == 404
