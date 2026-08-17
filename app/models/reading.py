from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.sensor import SensorModel

class ReadingModel(Base):
    __tablename__ = "readings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(
        String, ForeignKey("sensors.sensor_id"), index=True
    )
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relación inversa hacia el sensor
    sensor: Mapped["SensorModel"] = relationship(back_populates="readings")