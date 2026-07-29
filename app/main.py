from fastapi import FastAPI
from app.db import Base, engine
from app.routers import reading_router

# Creamos las tablas físicamente
Base.metadata.create_all(bind=engine)

# Encendemos la API
app = FastAPI(title="SensorHub API", version="0.1.0")

# Conectamos el router (la sub-placa) a nuestra app principal
app.include_router(reading_router.router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}