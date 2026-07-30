from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.reading import ReadingModel

class ReadingRepository:
    def create(self, db: Session, sensor_id: str, data: dict) -> ReadingModel:
        db_reading = ReadingModel(sensor_id=sensor_id, **data)
        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)
        return db_reading

    def get_by_id(self, db: Session, reading_id: int) -> ReadingModel | None:
        return db.get(ReadingModel, reading_id)

    def get_by_sensor(self, db: Session, sensor_id: str, limit: int, offset: int, from_date, to_date):
        stmt = select(ReadingModel).where(
            ReadingModel.sensor_id == sensor_id,
            ReadingModel.is_active == True
        )
        if from_date:
            stmt = stmt.where(ReadingModel.timestamp >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.timestamp <= to_date)
            
        stmt = stmt.offset(offset).limit(limit)
        return db.scalars(stmt).all()

    def update(self, db: Session, db_reading: ReadingModel, data: dict) -> ReadingModel:
        for key, value in data.items():
            setattr(db_reading, key, value)
        db.commit()
        db.refresh(db_reading)
        return db_reading

    def delete(self, db: Session, db_reading: ReadingModel):
        db_reading.is_active = False # Borrado lógico (soft delete)
        db.commit()