from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db import engine
from app.repositories.reading_repo import ReadingRepository
from app.schemas.reading import SensorReadingIn, SensorReadingOut, SensorReadingUpdate
from app.services.reading_service import ReadingService

router = APIRouter()
service = ReadingService(repo=ReadingRepository())

def get_db():
    with Session(engine) as session:
        yield session

# 1. CREATE
@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=SensorReadingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(
    sensor_id: str, 
    reading: SensorReadingIn, 
    db: Session = Depends(get_db)
):
    return service.registrar_lectura(db, sensor_id, reading)

# 2. READ (Lista con paginación y filtros)
@router.get("/sensors/{sensor_id}/readings", response_model=list[SensorReadingOut])
def list_readings(
    sensor_id: str, 
    limit: int = Query(50, ge=1, le=100), 
    offset: int = Query(0, ge=0),
    from_date: datetime | None = Query(None, alias="from"),
    to_date: datetime | None = Query(None, alias="to"),
    db: Session = Depends(get_db)
):
    return service.listar_lecturas(db, sensor_id, limit, offset, from_date, to_date)

# 3. READ (Individual)
@router.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    return service.obtener_lectura(db, reading_id)

# 4. UPDATE
@router.patch("/readings/{reading_id}", response_model=SensorReadingOut)
def update_reading(
    reading_id: int, 
    reading_update: SensorReadingUpdate, 
    db: Session = Depends(get_db)
):
    return service.actualizar_lectura(db, reading_id, reading_update)

# 5. DELETE
@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(reading_id: int, db: Session = Depends(get_db)):
    service.eliminar_lectura(db, reading_id)
