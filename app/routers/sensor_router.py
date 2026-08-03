from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor import SensorIn, SensorOut, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])

def get_sensor_service(db: Session = Depends(get_db)) -> SensorService:
    repo = SensorRepository(db)
    return SensorService(repo)

@router.post("/", response_model=SensorOut, status_code=201)
def create_sensor(
    sensor_in: SensorIn,
    service: SensorService = Depends(get_sensor_service),
):
    try:
        return service.create_sensor(sensor_in)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

@router.get("/", response_model=list[SensorOut], status_code=200)
def list_sensors(
    limit: int = 50,
    offset: int = 0,
    service: SensorService = Depends(get_sensor_service),
):
    return service.get_sensors(limit=limit, offset=offset)

@router.get("/{sensor_id}", response_model=SensorOut, status_code=200)
def get_sensor(
    sensor_id: str, service: SensorService = Depends(get_sensor_service)
):
    try:
        return service.get_sensor(sensor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

@router.patch("/{sensor_id}", response_model=SensorOut, status_code=200)
def update_sensor(
    sensor_id: str,
    sensor_update: SensorUpdate,
    service: SensorService = Depends(get_sensor_service),
):
    try:
        return service.update_sensor(sensor_id, sensor_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

@router.delete("/{sensor_id}", status_code=204)
def delete_sensor(
    sensor_id: str, service: SensorService = Depends(get_sensor_service)
):
    try:
        service.delete_sensor(sensor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e