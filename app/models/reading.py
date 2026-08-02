from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ReadingModel(Base):
    __tablename__ = "readings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Se agregó index=True para acelerar las búsquedas por sensor
    sensor_id: Mapped[str] = mapped_column(String, index=True)
    
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)
    
    # Se corrigió a timezone.utc usando una función lambda
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)