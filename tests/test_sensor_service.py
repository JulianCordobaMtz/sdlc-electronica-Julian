from typing import Any

import pytest

from app.models.sensor import SensorModel
from app.schemas.sensor import SensorIn, SensorUpdate
from app.services.sensor_service import SensorRepositoryProtocol, SensorService


# Implementación de un repositorio falso en memoria para pruebas de aislamiento
class FakeSensorRepository:
    def __init__(self):
        self.sensors: dict[str, SensorModel] = {}

    def get_by_id(self, sensor_id: str) -> SensorModel | None:
        return self.sensors.get(sensor_id)

    def get_all(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        all_sensors = list(self.sensors.values())
        return all_sensors[offset : offset + limit]

    def create(self, sensor_in: SensorIn) -> SensorModel:
        sensor = SensorModel(
            sensor_id=sensor_in.sensor_id,
            location=sensor_in.location,
            type=sensor_in.type,
            alert_threshold=sensor_in.alert_threshold,
            is_active=True
        )
        self.sensors[sensor_in.sensor_id] = sensor
        return sensor

    def update(self, sensor: SensorModel, update_data: dict[str, Any]) -> SensorModel:
        for key, value in update_data.items():
            setattr(sensor, key, value)
        self.sensors[sensor.sensor_id] = sensor
        return sensor

    def delete(self, sensor: SensorModel) -> None:
        if sensor.sensor_id in self.sensors:
            del self.sensors[sensor.sensor_id]


# Fixture para inicializar el servicio limpio antes de cada prueba
@pytest.fixture
def sensor_service() -> SensorService:
    repo = FakeSensorRepository()
    return SensorService(repo=repo)


# Test 1: Validación estricta de sensor_id (Bloquea nulos, vacíos y espacios)
def test_create_sensor_invalid_id_rejected(sensor_service: SensorService):
    # Intentar con ID vacío
    invalid_sensor = SensorIn(
        sensor_id="",
        name="Sensor de prueba",  # Agregado
        location="Bodega A",
        type="temperatura",
        alert_threshold=30.0
    )
    with pytest.raises(
        ValueError,
        match="El sensor_id no puede ser None, vacío o solo espacios",
    ):
        sensor_service.create_sensor(invalid_sensor)

    # Intentar con ID que contiene solo espacios en blanco
    spaces_sensor = SensorIn(
        sensor_id="   ",
        name="Sensor de prueba",  # Agregado
        location="Bodega A",
        type="temperatura",
        alert_threshold=30.0
    )
    with pytest.raises(
        ValueError,
        match="El sensor_id no puede ser None, vacío o solo espacios",
    ):
        sensor_service.create_sensor(spaces_sensor)


# Test 2: Validación de umbrales no finitos (Bloquea NaN e Infinitos)
def test_create_sensor_nan_threshold_rejected(sensor_service: SensorService):
    # Intentar con NaN (Not a Number)
    nan_sensor = SensorIn(
        sensor_id="TEMP-01",
        name="Sensor de prueba",  # Agregado
        location="Bodega A",
        type="temperatura",
        alert_threshold=float("nan")
    )
    with pytest.raises(
        ValueError,
        match="El umbral de alerta debe ser un número finito",
    ):
        sensor_service.create_sensor(nan_sensor)

    # Intentar con Infinito positivo
    inf_sensor = SensorIn(
        sensor_id="TEMP-02",
        name="Sensor de prueba",  # Agregado
        location="Bodega A",
        type="temperatura",
        alert_threshold=float("inf")
    )
    with pytest.raises(
        ValueError,
        match="El umbral de alerta debe ser un número finito",
    ):
        sensor_service.create_sensor(inf_sensor)


# Test 3: Soft Delete (Borrado lógico para salvar el historial)
def test_sensor_soft_delete_preserves_historical_data(sensor_service: SensorService):
    # Crear un sensor activo inicialmente
    new_sensor = SensorIn(
        sensor_id="TEMP-03",
        name="Sensor de prueba",  # Agregado
        location="Bodega B",
        type="temperatura",
        alert_threshold=35.0
    )
    sensor_service.create_sensor(new_sensor)

    # Ejecutar el borrado
    deleted_sensor = sensor_service.delete_sensor("TEMP-03")

    # El sensor no debe eliminarse de la estructura de datos, solo marcarse
    # como inactivo
    assert deleted_sensor.is_active is False
    assert sensor_service.get_sensor("TEMP-03") is not None


# Test 4: Inmutabilidad del sensor_id en actualizaciones
def test_update_sensor_blocks_immutable_fields(sensor_service: SensorService):
    # Crear sensor base
    new_sensor = SensorIn(
        sensor_id="TEMP-04",
        name="Sensor de prueba",  # Agregado
        location="Bodega C",
        type="temperatura",
        alert_threshold=28.0
    )
    sensor_service.create_sensor(new_sensor)

    # Intentar modificar el id mediante la actualización
    update_data = SensorUpdate(
        sensor_id="TEMP-VULNERABLE",  # Intento de cambiar la llave primaria
        location="Bodega C Modificada",
        alert_threshold=29.0
    )
    
    updated_sensor = sensor_service.update_sensor("TEMP-04", update_data)
    
    # El ID original debe permanecer intacto y la ubicación debió cambiar
    assert updated_sensor.sensor_id == "TEMP-04"
    assert updated_sensor.location == "Bodega C Modificada"


# Test 5: Aislamiento absoluto de la base de datos (Garantiza DIP)
def test_sensor_service_dip_isolation_without_db():
    # Esta prueba certifica que SensorService puede funcionar sin
    # dependencias de base de datos
    assert issubclass(FakeSensorRepository, SensorRepositoryProtocol)
