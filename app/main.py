from fastapi import FastAPI

from app.routers import (
    alert,
    reading,
    sensor_router,
)

app = FastAPI(title="SensorHub API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Registramos las rutas
app.include_router(sensor_router.router)
app.include_router(reading.router)
app.include_router(alert.router)
