from app.schemas.reading import SensorReadingIn, SensorReadingUpdate

# Importamos el detector y la estrategia de consola por defecto
from app.services.anomaly_detector import AnomalyDetector, ConsoleAlertStrategy


class ReadingService:
    def __init__(self, repo, detector: AnomalyDetector = None):
        # El servicio recibe el repositorio inyectado
        self.repo = repo
        # Si no se pasa un detector, creamos uno por defecto con alertas a consola
        self.detector = detector or AnomalyDetector(ConsoleAlertStrategy())

    def registrar_lectura(
        self, sensor_id: str, reading_in: SensorReadingIn
    ):
        # 1. Guardamos la lectura en la base de datos
        db_reading = self.repo.create(sensor_id, reading_in.model_dump())

        # 2. Obtenemos el sensor asociado directamente desde la lectura
        # (relación ORM). Usamos getattr por seguridad para que los
        # repositorios de prueba (fakes) no truenen.
        sensor = getattr(db_reading, "sensor", None)

        # 3. Si el sensor existe y tiene un umbral configurado, evaluamos la anomalía
        if (
            sensor
            and hasattr(sensor, "alert_threshold")
            and sensor.alert_threshold is not None
        ):
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