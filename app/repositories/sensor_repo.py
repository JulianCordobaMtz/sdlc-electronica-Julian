from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sensor import SensorModel

class SensorRepository:
    def create(self, db: Session, data: dict) -> SensorModel:
        db_sensor = SensorModel(**data)
        db.add(db_sensor)
        db.commit()
        db.refresh(db_sensor)
        return db_sensor

    def get_by_id(self, db: Session, sensor_id: str) -> SensorModel | None:
        return db.get(SensorModel, sensor_id)

    def get_all(self, db: Session, limit: int, offset: int):
        # Filtramos para devolver solo los sensores activos
        stmt = select(SensorModel).where(SensorModel.is_active == True).offset(offset).limit(limit)
        return db.scalars(stmt).all()

    def update(self, db: Session, db_sensor: SensorModel, data: dict) -> SensorModel:
        for key, value in data.items():
            setattr(db_sensor, key, value)
        db.commit()
        db.refresh(db_sensor)
        return db_sensor

    def delete(self, db: Session, db_sensor: SensorModel):
        db_sensor.is_active = False # Borrado lógico según la rúbrica
        db.commit()