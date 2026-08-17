from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class AlertModel(Base):
    __tablename__ = 'alert'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # La clave foránea debe coincidir con el nombre real de la tabla de sensores.
    sensor_id: Mapped[str] = mapped_column(
        String, ForeignKey('sensors.sensor_id'), nullable=False
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, default="open", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
