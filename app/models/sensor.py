from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.reading import ReadingModel


class SensorModel(Base):
    __tablename__ = "sensors"

    # Usaremos un string como ID principal (ej. "TEMP-01")
    sensor_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)  # ej. "temperatura"
    location: Mapped[str] = mapped_column(String, nullable=True)
    alert_threshold: Mapped[float] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relación inversa hacia las lecturas del sensor
    readings: Mapped[list["ReadingModel"]] = relationship(
        back_populates="sensor", cascade="all, delete-orphan"
    )
