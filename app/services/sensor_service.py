from typing import Protocol, Any
import math
from app.schemas.sensor import SensorIn, SensorUpdate
from app.models.sensor import SensorModel

class SensorRepositoryProtocol(Protocol):
    def get_by_id(self, sensor_id: str) -> SensorModel | None: ...
    def get_all(self, limit: int = 50, offset: int = 0) -> list[SensorModel]: ...
    def create(self, sensor_in: SensorIn) -> SensorModel: ...
    def update(self, sensor: SensorModel, update_data: dict[str, Any]) -> SensorModel: ...
    def delete(self, sensor: SensorModel) -> None: ...

class SensorService:
    def __init__(self, repo: SensorRepositoryProtocol):
        self.repo = repo

    def create_sensor(self, sensor_in: SensorIn) -> SensorModel:
        sensor_id = sensor_in.sensor_id
        if not sensor_id or not sensor_id.strip():
            raise ValueError("El sensor_id no puede ser None, vacío o solo espacios")
        
        threshold = getattr(sensor_in, "alert_threshold", None)
        if threshold is not None and not math.isfinite(threshold):
            raise ValueError("El umbral de alerta debe ser un número finito")
        
        return self.repo.create(sensor_in)

    def get_sensors(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        return self.repo.get_all(limit=limit, offset=offset)

    def get_sensor(self, sensor_id: str) -> SensorModel:
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        return sensor

    def update_sensor(self, sensor_id: str, sensor_update: SensorUpdate) -> SensorModel:
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")

        threshold = getattr(sensor_update, "alert_threshold", None)
        if threshold is not None and not math.isfinite(threshold):
            raise ValueError("El umbral de alerta debe ser un número finito")
        
        update_data = sensor_update.model_dump(exclude_unset=True, exclude={'sensor_id'})
        
        return self.repo.update(sensor, update_data)

    def delete_sensor(self, sensor_id: str) -> SensorModel:
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        
        sensor.is_active = False
        return self.repo.update(sensor, {"is_active": False})
