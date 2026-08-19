import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

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
