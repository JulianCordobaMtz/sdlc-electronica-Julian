# IMPORTACIONES
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol

# ESTRUCTURAS BASE

class SensorType(Enum): # Catálogo estricto para evitar mezclar datos por accidente (mejor que usar números)
    TEMPERATURE = auto()
    HUMIDITY = auto()

@dataclass(frozen=True) # frozen=True actúa como memoria ROM: hace que la lectura sea inmutable
class Reading:
    sensor_id: str
    value: float
    sensor_type: SensorType

class Transport(Protocol):
    def send(self, payload: bytes) -> None: ... # Los '...' indican que es un contrato (interfaz), aquí no va el código real

# FUNCIONES PURAS SOBRE READING

# Función 1: Aplicar offset de calibración (Suma)
def apply_calibration_offset(r: Reading, offset: float) -> Reading:
    return Reading( # Al ser función pura, creamos un objeto 100% nuevo en lugar de alterar el original
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

# Función 4: Calcula la diferencia (delta) entre dos lecturas (nuevo - antiguo)
def delta_between_readings(old: Reading, new: Reading) -> float:
    if old.sensor_id != new.sensor_id or old.sensor_type != new.sensor_type: # Blindaje: evita comparar datos que no coinciden  
        return float('nan') # 'Not a Number': devuelve un estado de error matemático seguro si no coinciden
    return new.value - old.value

# Función 5: Redondea el valor de la lectura a 'ndigits' decimales
def round_reading(r: Reading, ndigits: int = 2) -> Reading:
    rounded = round(r.value, ndigits)
    return Reading(sensor_id=r.sensor_id, value=rounded, sensor_type=r.sensor_type)