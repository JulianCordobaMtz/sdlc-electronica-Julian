from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SensorReading:
    """Representa una lectura inmutable de los datos de un sensor."""
    sensor_id: str
    temperatura: float
    humedad: float
    timestamp: datetime