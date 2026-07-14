# IMPORTACION
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol
import math

# ESTRUCTURAS BASE

class SensorType(Enum): 
    TEMPERATURE = auto()
    HUMIDITY = auto()

@dataclass(frozen=True)
class Reading:
    sensor_id: str
    value: float
    sensor_type: SensorType

class Transport(Protocol):
    def send(self, payload: bytes) -> None: ...

# --- 2. FUNCIONES PURAS SOBRE READING ---

# Función 1: Aplicar offset de calibración (Suma)
def apply_calibration_offset(r: Reading, offset: float) -> Reading:
    return Reading(
        sensor_id=r.sensor_id,
        value=r.value + offset,
        sensor_type=r.sensor_type
    )

# Función 2: Aplicar ganancia (Multiplicación - útil para escalar voltajes)
def apply_gain(r: Reading, multiplier: float) -> Reading:
    return Reading(
        sensor_id=r.sensor_id,
        value=r.value * multiplier,
        sensor_type=r.sensor_type
    )

# Función 3: Conversión de unidades (Celsius a Fahrenheit)
def celsius_to_fahrenheit(r: Reading) -> Reading:
    if r.sensor_type != SensorType.TEMPERATURE:
        return r  # Si no es temperatura, devuelve el dato intacto
    
    new_value = (r.value * 9/5) + 32
    return Reading(
        sensor_id=r.sensor_id,
        value=new_value,
        sensor_type=r.sensor_type
    )

# Función 4: Evaluación de umbral lógico (Detector de alarma)
def is_alarm_triggered(r: Reading, threshold: float) -> bool:
    return r.value > threshold

# Función 5: Serialización de la lectura a bytes (Preparación para el Protocol)
def serialize_for_transport(r: Reading) -> bytes:
    # Empaqueta los datos en un string y los convierte a bytes puros
    payload_str = f"{r.sensor_id}|{r.sensor_type.name}|{r.value:.2f}"
    return payload_str.encode('utf-8')

# --- OTRAS 5 FUNCIONES PURAS SOBRE READING (SUGERIDAS) ---

# Limita el valor de la lectura a un rango [min_v, max_v]
def clamp_reading(r: Reading, min_v: float, max_v: float) -> Reading:
    clamped = max(min_v, min(max_v, r.value))
    return Reading(sensor_id=r.sensor_id, value=clamped, sensor_type=r.sensor_type)

# Redondea el valor de la lectura a 'ndigits' decimales
def round_reading(r: Reading, ndigits: int = 2) -> Reading:
    rounded = round(r.value, ndigits)
    return Reading(sensor_id=r.sensor_id, value=rounded, sensor_type=r.sensor_type)

# Calcula el promedio entre dos lecturas del mismo sensor/tipo (pura)
def average_readings(a: Reading, b: Reading) -> Reading:
    if a.sensor_id != b.sensor_id or a.sensor_type != b.sensor_type:
        # Si difieren, devuelve la primera sin modificar (no muta nada)
        return a
    avg = (a.value + b.value) / 2.0
    return Reading(sensor_id=a.sensor_id, value=avg, sensor_type=a.sensor_type)

# Calcula la diferencia (delta) entre dos lecturas (nuevo - antiguo)
def delta_between_readings(old: Reading, new: Reading) -> float:
    if old.sensor_id != new.sensor_id or old.sensor_type != new.sensor_type:
        return float('nan')
    return new.value - old.value

# Normaliza el valor de la lectura al rango [0.0, 1.0] según min/max
def normalize_reading(r: Reading, min_v: float, max_v: float) -> Reading:
    if math.isnan(r.value) or max_v == min_v:
        return Reading(sensor_id=r.sensor_id, value=float('nan'), sensor_type=r.sensor_type)
    clipped = max(min_v, min(max_v, r.value))
    normalized = (clipped - min_v) / (max_v - min_v)
    return Reading(sensor_id=r.sensor_id, value=normalized, sensor_type=r.sensor_type)