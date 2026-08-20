import math
import unicodedata


def _normalize_sensor_type(sensor_type: str) -> str:
    normalized = unicodedata.normalize("NFKD", sensor_type.strip().lower())
    return "".join(
        character for character in normalized if not unicodedata.combining(character)
    )


def validate_physical_reading(sensor_type: str, value: float, unit: str) -> None:
    """Valida una lectura usando reglas físicas del tipo de sensor."""
    if not math.isfinite(value):
        raise ValueError("El valor de la lectura debe ser un número finito")

    normalized_type = _normalize_sensor_type(sensor_type)

    if normalized_type in {"temperatura", "temperature"}:
        minimum_by_unit = {"C": -273.15, "F": -459.67, "K": 0.0}
        if unit not in minimum_by_unit:
            raise ValueError("Temperatura solo admite las unidades C, F o K")
        if value < minimum_by_unit[unit]:
            raise ValueError(f"Temperatura por debajo del cero absoluto en {unit}")
        return

    if normalized_type in {"humedad", "humidity"}:
        if unit != "%":
            raise ValueError("Humedad solo admite la unidad %")
        if not 0 <= value <= 100:
            raise ValueError("La humedad debe estar entre 0 y 100 %")
        return

    if normalized_type in {"presion", "pressure"}:
        if unit not in {"Pa", "kPa", "bar"}:
            raise ValueError("Presión solo admite las unidades Pa, kPa o bar")
        if value < 0:
            raise ValueError("La presión no puede ser negativa")
        return

    raise ValueError(f"Tipo de sensor no soportado: {sensor_type}")
