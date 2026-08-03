from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor import SensorModel
from app.schemas.sensor import SensorIn, SensorUpdate


class SensorRepository:
    # ¡ESTE ES EL MÉTODO QUE FALTABA Y CAUSABA EL ERROR!
    # Ahora el repositorio sí acepta la base de datos (db) que le manda el router
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sensor_id: str) -> SensorModel | None:
        # Sintaxis estricta de SQLAlchemy 2.0
        stmt = select(SensorModel).where(SensorModel.sensor_id == sensor_id)
        return self.db.scalars(stmt).first()

    def get_all(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        stmt = select(SensorModel).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def create(self, sensor_in: SensorIn) -> SensorModel:
        nuevo_sensor = SensorModel(**sensor_in.model_dump())
        self.db.add(nuevo_sensor)
        self.db.commit()
        self.db.refresh(nuevo_sensor)
        return nuevo_sensor

    def update(self, sensor: SensorModel, sensor_update: SensorUpdate) -> SensorModel:
        update_data = sensor_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(sensor, key, value)
        self.db.commit()
        self.db.refresh(sensor)
        return sensor

    def delete(self, sensor: SensorModel) -> None:
        self.db.delete(sensor)
        self.db.commit()