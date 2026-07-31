from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class SensorModel(Base):
    __tablename__ = "sensors"
    
    # Usaremos un string como ID principal (ej. "TEMP-01")
    sensor_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String) # ej. "temperatura"
    location: Mapped[str] = mapped_column(String, nullable=True)
    alert_threshold: Mapped[float] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)