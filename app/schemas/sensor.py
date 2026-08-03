
from pydantic import BaseModel, Field


class SensorIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    name: str = Field(..., examples=["Sensor de caldera"])
    type: str = Field(..., examples=["temperatura"])
    location: str | None = None
    alert_threshold: float | None = None

class SensorUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    location: str | None = None
    alert_threshold: float | None = None

class SensorOut(SensorIn):
    is_active: bool