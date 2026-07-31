import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import Base
from app.routers import reading_router, sensor_router

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
app.dependency_overrides[reading_router.get_db] = override_get_db
app.dependency_overrides[sensor_router.get_db] = override_get_db

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
    response_post = client.post("/sensors", json={
        "sensor_id": "TEMP-01",
        "name": "Sensor de caldera",
        "type": "temperatura",
        "location": "Sotano"
    })
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
    client.post("/sensors", json={"sensor_id": "TEMP-02", "name": "Sensor 2", "type": "temperatura"})
    
    # Registramos su lectura
    response = client.post("/sensors/TEMP-02/readings", json={
        "value": 25.5,
        "unit": "C"
    })
    assert response.status_code == 201
    assert response.json()["value"] == 25.5

def test_validacion_fisica_cero_absoluto_devuelve_422():
    # Creamos el sensor
    client.post("/sensors", json={"sensor_id": "TEMP-03", "name": "Sensor 3", "type": "temperatura"})
    
    # Intentamos registrar una temperatura imposible en el universo
    response = client.post("/sensors/TEMP-03/readings", json={
        "value": -300,  # Falla la validación Pydantic
        "unit": "C"
    })
    assert response.status_code == 422
    # Validamos que Pydantic nos devuelva el error en el campo 'value'
    assert response.json()["detail"][0]["loc"] == ["body", "value"] 

    # ================= TESTS PARA COMPLETAR COBERTURA =================

def test_operaciones_completas_sensores():
    # 1. Crear
    client.post("/sensors", json={"sensor_id": "SENS-04", "name": "S4", "type": "humedad"})
    
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
    client.post("/sensors", json={"sensor_id": "SENS-05", "name": "S5", "type": "temperatura"})
    
    # 2. Crear lectura
    res_create = client.post("/sensors/SENS-05/readings", json={"value": 20.0, "unit": "C"})
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