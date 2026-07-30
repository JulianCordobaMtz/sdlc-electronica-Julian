from datetime import datetime
from sqlalchemy import String, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class ReadingModel(Base):
    __tablename__ = "readings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(String)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)
    # Agregamos fecha para los filtros y estado para el borrado lógico
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)