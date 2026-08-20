from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.alert import AlertStatus


class AlertBase(BaseModel):
    sensor_id: str
    value: float
    threshold: float
    severity: str = "WARNING"
    status: str = "open"


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    status: AlertStatus = Field(..., examples=["acknowledged", "resolved"])


class AlertOut(AlertBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
