from fastapi import FastAPI

from app.db import Base, engine
from app.routers import (  # IMPORTANTE: importar el nuevo router
    reading_router,
    sensor_router,
)

# Si es necesario, esta línea asegura que SQLAlchemy cree las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="0.1.0")
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

# Registramos ambas rutas
app.include_router(sensor_router.router)
app.include_router(reading_router.router)
#Prueba para verificar que el despliegue en Render funciona correctamente