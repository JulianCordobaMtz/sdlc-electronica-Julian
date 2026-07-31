from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.db import engine
from app.schemas.sensor import SensorIn, SensorOut, SensorUpdate
from app.services.sensor_service import SensorService
from app.repositories.sensor_repo import SensorRepository 

# Agregamos la etiqueta "Sensors" para agruparlo bonito en Swagger
router = APIRouter(tags=["Sensors"])
service = SensorService(repo=SensorRepository())

def get_db():
    with Session(engine) as session:
        yield session

@router.post("/sensors", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(sensor: SensorIn, db: Session = Depends(get_db)):
    return service.crear_sensor(db, sensor)

@router.get("/sensors", response_model=List[SensorOut])
def list_sensors(
    limit: int = Query(50, ge=1, le=100), 
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return service.listar_sensores(db, limit, offset)

@router.get("/sensors/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: str, db: Session = Depends(get_db)):
    return service.obtener_sensor(db, sensor_id)

@router.patch("/sensors/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: str, sensor_update: SensorUpdate, db: Session = Depends(get_db)):
    return service.actualizar_sensor(db, sensor_id, sensor_update)

@router.delete("/sensors/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: str, db: Session = Depends(get_db)):
    service.eliminar_sensor(db, sensor_id)
    return None