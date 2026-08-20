from time import perf_counter
from typing import Any
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.db import get_db
from app.logging_config import configure_logging
from app.observability import metrics
from app.routers import (
    alert,
    reading,
    sensor_router,
)

app = FastAPI(title="SensorHub API", version="0.1.0")
logger = configure_logging()


def _error_content(
    request: Request,
    error_type: str,
    message: str,
    detail: Any,
) -> dict[str, Any]:
    return {
        "error": {
            "type": error_type,
            "message": message,
            "request_id": getattr(request.state, "request_id", None),
        },
        "detail": detail,
    }


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    error: StarletteHTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=error.status_code,
        content=_error_content(request, "http_error", str(error.detail), error.detail),
        headers=error.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    error: RequestValidationError,
) -> JSONResponse:
    detail = jsonable_encoder(error.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=_error_content(
            request,
            "validation_error",
            "La solicitud contiene datos inválidos",
            detail,
        ),
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request,
    error: Exception,
) -> JSONResponse:
    logger.error(
        "Error inesperado al procesar la solicitud",
        extra={
            "event": "unhandled_exception",
            "request_id": getattr(request.state, "request_id", None),
            "method": request.method,
            "path": request.url.path,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        exc_info=(type(error), error, error.__traceback__),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_error_content(
            request,
            "internal_error",
            "Ocurrió un error interno",
            "Error interno del servidor",
        ),
    )


@app.middleware("http")
async def collect_http_metrics(request: Request, call_next):
    started_at = perf_counter()
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.request_id = request_id
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
    duration_seconds = perf_counter() - started_at
    metrics.observe(
        request.method,
        path,
        response.status_code,
        duration_seconds,
    )
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "Solicitud HTTP procesada",
        extra={
            "event": "http_request",
            "request_id": request_id,
            "method": request.method,
            "path": path,
            "status_code": response.status_code,
            "duration_ms": round(duration_seconds * 1000, 3),
        },
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
