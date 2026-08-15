from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class AlertModel(Base):
    __tablename__ = 'alert'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Cambiado 'sensor.sensor_id' por 'sensores.sensor_id' para que coincida con tu commit estable
    sensor_id: Mapped[str] = mapped_column(String, ForeignKey('sensors.sensor_id'), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, default="open", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )