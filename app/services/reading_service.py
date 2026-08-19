from datetime import datetime
from typing import Any, Protocol

from app.domain.reading_validation import validate_physical_reading
from app.schemas.reading import ReadingStatsOut, SensorReadingIn, SensorReadingUpdate
from app.services.anomaly_detector import AnomalyDetector


class SensorLookupRepository(Protocol):
    def create(self, sensor_id: str, data: dict[str, Any]) -> Any: ...
    def get_by_id(self, reading_id: int) -> Any: ...
    def get_by_sensor(
        self, sensor_id: str, limit: int, offset: int, from_date: Any, to_date: Any
    ) -> Any: ...
    def get_statistics(
        self,
        sensor_id: str,
        from_date: datetime | None,
        to_date: datetime | None,
    ) -> tuple[int, float | None, float | None, float | None]: ...
    def update(self, db_reading: Any, data: dict[str, Any]) -> Any: ...
    def delete(self, db_reading: Any) -> None: ...


class SensorStatusRepository(Protocol):
    def get_by_id(self, sensor_id: str) -> Any: ...


class ReadingService:
    def __init__(
        self,
        repo: SensorLookupRepository,
        detector: AnomalyDetector,
        sensor_repo: SensorStatusRepository,
    ) -> None:
        self.repo = repo
        self.detector = detector
        self.sensor_repo = sensor_repo

    def registrar_lectura(self, sensor_id: str, reading_in: SensorReadingIn):
        sensor = self.sensor_repo.get_by_id(sensor_id)
        if sensor is None:
            raise ValueError("Sensor no encontrado")
        if not sensor.is_active:
            raise ValueError("No se aceptan lecturas de un sensor inactivo")

        validate_physical_reading(sensor.type, reading_in.value, reading_in.unit)

        # 1. Guardamos la lectura después de validar el sensor y el valor físico.
        db_reading = self.repo.create(sensor_id, reading_in.model_dump())

        # 2. Si tiene umbral configurado, evaluamos la anomalía.
        if sensor.alert_threshold is not None:
            self.detector.evaluate(
                sensor_id=sensor_id,
                value=db_reading.value,
                threshold=sensor.alert_threshold,
            )

        return db_reading

    def obtener_lectura(self, reading_id: int):
        db_reading = self.repo.get_by_id(reading_id)
        if not db_reading or not db_reading.is_active:
            raise ValueError("Lectura no encontrada")
        return db_reading

    def listar_lecturas(
        self, sensor_id: str, limit: int, offset: int, from_date, to_date
    ):
        if from_date and to_date and from_date > to_date:
            raise ValueError("La fecha 'from' no puede ser mayor a 'to'")
        return self.repo.get_by_sensor(sensor_id, limit, offset, from_date, to_date)

    def obtener_estadisticas(
        self,
        sensor_id: str,
        from_date: datetime | None,
        to_date: datetime | None,
    ) -> ReadingStatsOut:
        if from_date and to_date and from_date > to_date:
            raise ValueError("La fecha 'from' no puede ser mayor a 'to'")

        count, minimum, maximum, average = self.repo.get_statistics(
            sensor_id, from_date, to_date
        )
        if count == 0 or minimum is None or maximum is None or average is None:
            raise LookupError("No hay lecturas para el sensor y periodo solicitados")

        return ReadingStatsOut(
            sensor_id=sensor_id,
            from_date=from_date,
            to_date=to_date,
            count=count,
            minimum=minimum,
            maximum=maximum,
            average=average,
        )

    def actualizar_lectura(self, reading_id: int, reading_update: SensorReadingUpdate):
        """Actualizar una lectura existente."""
        db_reading = self.obtener_lectura(reading_id)
        update_data = reading_update.model_dump(exclude_unset=True)

        if not update_data:
            return db_reading

        return self.repo.update(db_reading, update_data)

    def eliminar_lectura(self, reading_id: int):
        """Eliminar (soft delete) una lectura."""
        db_reading = self.obtener_lectura(reading_id)
        if not db_reading.is_active:
            raise ValueError("La lectura ya estaba eliminada")
        self.repo.delete(db_reading)
