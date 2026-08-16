from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_reading_service
from app.schemas.reading import SensorReadingIn, SensorReadingOut, SensorReadingUpdate
from app.services.reading_service import ReadingService

router = APIRouter()


# 1. CREATE (Registro de Lectura)
@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=SensorReadingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(
    sensor_id: str,
    reading: SensorReadingIn,
    service: ReadingService = Depends(get_reading_service),
):
    """Registrar una lectura para un sensor y evaluar automáticamente anomalías."""
    try:
        return service.registrar_lectura(sensor_id, reading)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# 2. READ (Lista con paginación y filtros por rango de fechas)
@router.get("/sensors/{sensor_id}/readings", response_model=list[SensorReadingOut])
def list_readings(
    sensor_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: datetime | None = Query(None, alias="from"),
    to_date: datetime | None = Query(None, alias="to"),
    service: ReadingService = Depends(get_reading_service),
):
    """Listar lecturas de un sensor con filtros opcionales de fecha."""
    try:
        return service.listar_lecturas(sensor_id, limit, offset, from_date, to_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# 3. READ (Lectura individual por ID)
@router.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(
    reading_id: int,
    service: ReadingService = Depends(get_reading_service),
):
    """Obtener una lectura específica por su ID."""
    try:
        return service.obtener_lectura(reading_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# 4. UPDATE (Actualización parcial de lectura)
@router.patch("/readings/{reading_id}", response_model=SensorReadingOut)
def update_reading(
    reading_id: int,
    reading_update: SensorReadingUpdate,
    service: ReadingService = Depends(get_reading_service),
):
    """Actualizar una lectura existente (actualización parcial)."""
    try:
        return service.actualizar_lectura(reading_id, reading_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# 5. DELETE (Soft delete de lectura)
@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(
    reading_id: int,
    service: ReadingService = Depends(get_reading_service),
):
    """Eliminar (soft delete) una lectura."""
    try:
        service.eliminar_lectura(reading_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e