from pydantic import BaseModel, Field
from typing import Optional

class SensorIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    name: str = Field(..., examples=["Sensor de caldera"])
    type: str = Field(..., examples=["temperatura"])
    location: Optional[str] = None
    alert_threshold: Optional[float] = None

class SensorUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    alert_threshold: Optional[float] = None

class SensorOut(SensorIn):
    is_active: bool