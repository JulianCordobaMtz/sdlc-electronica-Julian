from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.reading import SensorReadingIn, SensorReadingUpdate

class ReadingService:
    def __init__(self, repo):
        self.repo = repo

    def registrar_lectura(self, db: Session, sensor_id: str, reading_in: SensorReadingIn):
        return self.repo.create(db, sensor_id, reading_in.model_dump())

    def obtener_lectura(self, db: Session, reading_id: int):
        db_reading = self.repo.get_by_id(db, reading_id)
        if not db_reading or not db_reading.is_active:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        return db_reading

    def listar_lecturas(self, db: Session, sensor_id: str, limit: int, offset: int, from_date, to_date):
        if from_date and to_date and from_date > to_date:
            raise HTTPException(status_code=400, detail="La fecha 'from' no puede ser mayor a 'to'")
        return self.repo.get_by_sensor(db, sensor_id, limit, offset, from_date, to_date)

    def actualizar_lectura(self, db: Session, reading_id: int, reading_update: SensorReadingUpdate):
        db_reading = self.obtener_lectura(db, reading_id) # Reutilizamos la lógica del 404
        update_data = reading_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")
        return self.repo.update(db, db_reading, update_data)

    def eliminar_lectura(self, db: Session, reading_id: int):
        db_reading = self.obtener_lectura(db, reading_id) # Verifica que exista (404)
        if not db_reading.is_active:
            raise HTTPException(status_code=409, detail="La lectura ya estaba eliminada")
        self.repo.delete(db, db_reading)