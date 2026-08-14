from typing import Protocol
import math
from app.schemas.sensor import SensorIn, SensorUpdate

class SensorRepositoryProtocol(Protocol):
    def get_by_id(self, sensor_id: str) -> SensorModel | None: ...
    def create(self, sensor_in: SensorIn) -> SensorModel: ...
    def update(self, sensor: SensorModel, sensor_update: SensorUpdate) -> SensorModel: ...
    def delete(self, sensor: SensorModel) -> None: ...

class SensorService:
    def __init__(self, repo: SensorRepositoryProtocol):
        self.repo = repo

    def create_sensor(self, sensor_in: SensorIn):
        # Validación de sensor_id
        sensor_id = sensor_in.sensor_id
        if not sensor_id or not sensor_id.strip():
            raise ValueError("El sensor_id no puede ser None, vacío o solo espacios")
        
        # Validación de umbral de alerta
        if hasattr(sensor_in, 'alert_threshold') and not math.isfinite(sensor_in.alert_threshold):
            raise ValueError("El umbral de alerta debe ser un número finito")
        
        # Crear sensor
        return self.repo.create(sensor_in)

    def get_sensors(self, limit: int = 50, offset: int = 0):
        return self.repo.get_all(limit=limit, offset=offset)

    def get_sensor(self, sensor_id: str):
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        return sensor

    def update_sensor(self, sensor_id: str, sensor_update: SensorUpdate):
        # Validación de umbral de alerta
        if hasattr(sensor_update, 'alert_threshold') and not math.isfinite(sensor_update.alert_threshold):
            raise ValueError("El umbral de alerta debe ser un número finito")
        
        # Filtrar campo inmutable (sensor_id)
        update_data = sensor_update.dict(exclude={'sensor_id'})
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        return self.repo.update(sensor, update_data)

    def delete_sensor(self, sensor_id: str):
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        # Borrado lógico
        sensor.is_active = False
        return self.repo.update(sensor, {})
