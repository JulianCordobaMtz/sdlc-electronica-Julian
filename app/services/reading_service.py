
from app.schemas.reading import SensorReadingIn, SensorReadingUpdate


class ReadingService:
    def __init__(self, repo):
        self.repo = repo

    def registrar_lectura(
        self, sensor_id: str, reading_in: SensorReadingIn
    ):
        return self.repo.create(sensor_id, reading_in.model_dump())

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

    def actualizar_lectura(
        self, reading_id: int, reading_update: SensorReadingUpdate
    ):
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