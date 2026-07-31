from fastapi import FastAPI
from app.db import Base, engine
from app.routers import reading_router, sensor_router  # IMPORTANTE: importar el nuevo router

# Si es necesario, esta línea asegura que SQLAlchemy cree las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="0.1.0")

# Registramos ambas rutas
app.include_router(sensor_router.router)
app.include_router(reading_router.router)