import math
from datetime import datetime

from pydantic import BaseModel, field_validator


class SensorReadingIn(BaseModel):
    value: float
    unit: str = "C"

    @field_validator("unit")
    @classmethod
    def validar_unidad(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("La unidad no puede estar vacía")
        return value.strip()

    @field_validator("value")
    @classmethod
    def validar_numero_finito(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("El valor debe ser un número finito")
        return value


# Schema para el PATCH (todo opcional)
class SensorReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None


class SensorReadingOut(SensorReadingIn):
    id: int
    sensor_id: str
    timestamp: datetime
    is_active: bool


class ReadingStatsOut(BaseModel):
    sensor_id: str
    from_date: datetime | None
    to_date: datetime | None
    count: int
    minimum: float
    maximum: float
    average: float
