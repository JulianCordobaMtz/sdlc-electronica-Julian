from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.sensor import SensorIn, SensorUpdate

class SensorService:
    def __init__(self, repo):
        self.repo = repo

    def crear_sensor(self, db: Session, sensor_in: SensorIn):
        # Evitar duplicados (Error 409 Conflict)
        existente = self.repo.get_by_id(db, sensor_in.sensor_id)
        if existente:
            raise HTTPException(status_code=409, detail="El sensor_id ya está registrado")
        return self.repo.create(db, sensor_in.model_dump())

    def obtener_sensor(self, db: Session, sensor_id: str):
        db_sensor = self.repo.get_by_id(db, sensor_id)
        if not db_sensor or not db_sensor.is_active:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return db_sensor

    def listar_sensores(self, db: Session, limit: int, offset: int):
        return self.repo.get_all(db, limit, offset)

    def actualizar_sensor(self, db: Session, sensor_id: str, sensor_update: SensorUpdate):
        db_sensor = self.obtener_sensor(db, sensor_id)
        update_data = sensor_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")
        return self.repo.update(db, db_sensor, update_data)

    def eliminar_sensor(self, db: Session, sensor_id: str):
        db_sensor = self.obtener_sensor(db, sensor_id)
        self.repo.delete(db, db_sensor)