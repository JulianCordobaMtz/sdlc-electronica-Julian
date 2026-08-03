from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reading import ReadingModel


class ReadingRepository:
    def __init__(self, db: Session):
        # El repositorio recibe la sesión por inyección y la mantiene en su instancia.
        # Esta capa es la única que toca la base de datos.
        self.db = db

    def create(self, sensor_id: str, data: dict) -> ReadingModel:
        db_reading = ReadingModel(sensor_id=sensor_id, **data)
        self.db.add(db_reading)
        self.db.commit()
        self.db.refresh(db_reading)
        return db_reading

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return self.db.get(ReadingModel, reading_id)

    def get_by_sensor(
        self, sensor_id: str, limit: int, offset: int, from_date, to_date
    ):
        stmt = select(ReadingModel).where(
            ReadingModel.sensor_id == sensor_id,
            ReadingModel.is_active
        )
        if from_date:
            stmt = stmt.where(ReadingModel.timestamp >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.timestamp <= to_date)
            
        stmt = stmt.offset(offset).limit(limit)
        return self.db.scalars(stmt).all()

    def update(self, db_reading: ReadingModel, data: dict) -> ReadingModel:
        for key, value in data.items():
            setattr(db_reading, key, value)
        self.db.commit()
        self.db.refresh(db_reading)
        return db_reading

    def delete(self, db_reading: ReadingModel):
        db_reading.is_active = False  # Borrado lógico (soft delete)
        self.db.commit()