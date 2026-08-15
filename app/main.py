from fastapi import FastAPI
from app.db import Base, engine

# === SOLUCIÓN DE CLAVE FORÁNEA: IMPORTACIÓN EXPLÍCITA DE TODOS LOS MODELOS ===
# Esto obliga a SQLAlchemy a cargar las tres tablas en memoria antes de crearlas
from app.models.sensor import SensorModel
from app.models.reading import ReadingModel
from app.models.alert import AlertModel 

from app.routers import (  
    reading,
    sensor_router,
    alert,  
)

# Ahora sí, SQLAlchemy conoce todas las relaciones y creará la base de datos sin errores
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="0.1.0")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

# Registramos las rutas
app.include_router(sensor_router.router)
app.include_router(reading.router)
app.include_router(alert.router)