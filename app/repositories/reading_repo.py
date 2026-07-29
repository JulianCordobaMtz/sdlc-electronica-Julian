from sqlalchemy.orm import Session
from app.models.reading import ReadingModel
from app.schemas.reading import SensorReadingIn

class ReadingRepository:
    def create(self, db: Session, reading_in: SensorReadingIn) -> ReadingModel:
        # Traduce el schema validado al modelo de la BD
        db_reading = ReadingModel(**reading_in.model_dump())
        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)
        return db_reading