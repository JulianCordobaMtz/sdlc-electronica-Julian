from datetime import datetime

from pydantic import BaseModel, field_validator


class SensorReadingIn(BaseModel):
    value: float
    unit: str = "C"

    @field_validator('unit')
    @classmethod
    def validar_unidad(cls, v):
        if v not in ["C", "F"]:
            raise ValueError("Unidad desconocida. Solo se permite 'C' o 'F'")
        return v

    @field_validator('value')
    @classmethod
    def validar_cero_absoluto(cls, v, info):
        unidad = info.data.get('unit', 'C')
        if unidad == "C" and v < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto (-273.15 C)")
        elif unidad == "F" and v < -459.67:
            raise ValueError("Temperatura por debajo del cero absoluto (-459.67 F)")
        return v

# Schema para el PATCH (todo opcional)
class SensorReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None

class SensorReadingOut(SensorReadingIn):
    id: int
    sensor_id: str
    timestamp: datetime
    is_active: bool