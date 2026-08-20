from time import perf_counter

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import get_db
from app.observability import metrics
from app.routers import (
    alert,
    reading,
    sensor_router,
)

app = FastAPI(title="SensorHub API", version="0.1.0")


@app.middleware("http")
async def collect_http_metrics(request: Request, call_next):
    started_at = perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        metrics.observe(
            request.method,
            request.url.path,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            perf_counter() - started_at,
        )
        raise

    route = request.scope.get("route")
    path = getattr(route, "path", request.url.path)
    metrics.observe(
        request.method,
        path,
        response.status_code,
        perf_counter() - started_at,
    )
    return response


@app.get("/health")
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos no disponible",
        ) from error
    return {"status": "ok", "database": "reachable"}


@app.get("/metrics", include_in_schema=False)
def get_metrics() -> Response:
    return Response(
        content=metrics.render(),
        media_type="text/plain; version=0.0.4",
    )


# Registramos las rutas
app.include_router(sensor_router.router)
app.include_router(reading.router)
app.include_router(alert.router)
