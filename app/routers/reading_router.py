from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import engine
from app.schemas.reading import SensorReadingIn, SensorReadingOut
from app.services.reading_service import ReadingService
from app.repositories.reading_repo import ReadingRepository 

# Fabricamos el router
router = APIRouter()
# Instanciamos el servicio
service = ReadingService(repo=ReadingRepository())

# Función para inyectar la sesión de la BD en cada petición
def get_db():
    with Session(engine) as session:
        yield session

@router.post("/readings", response_model=SensorReadingOut, status_code=201)
def create_reading(reading: SensorReadingIn, db: Session = Depends(get_db)):
    # El router NO sabe de bases de datos, solo le pasa la tarea al servicio
    return service.registrar_lectura(db, reading)