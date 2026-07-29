from fastapi import FastAPI
from pydantic import BaseModel, Field

# AHORA IMPORTAMOS "Session" DIRECTAMENTE DE SQLALCHEMY
from sqlalchemy.orm import Session 

from app.db import Base, engine
from app.models import ReadingModel 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="0.1.0")

class SensorReadingIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"

class SensorReadingOut(SensorReadingIn):
    id: int

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/readings", response_model=SensorReadingOut, status_code=201)
def create_reading(reading: SensorReadingIn) -> SensorReadingOut:
    # USAMOS EXACTAMENTE LA SINTAXIS DEL QUICK START DE SQLALCHEMY 2.0
    with Session(engine) as session:
        db_reading = ReadingModel(**reading.model_dump())
        
        session.add(db_reading)
        session.commit()
        session.refresh(db_reading)
        
        return db_reading