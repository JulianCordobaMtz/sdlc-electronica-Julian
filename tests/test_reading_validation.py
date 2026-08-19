import pytest

from app.domain.reading_validation import validate_physical_reading


@pytest.mark.parametrize(
    ("sensor_type", "value", "unit"),
    [
        ("temperatura", -273.15, "C"),
        ("temperature", 32.0, "F"),
        ("humedad", 50.0, "%"),
        ("presión", 101.325, "kPa"),
    ],
)
def test_accepts_valid_physical_readings(sensor_type, value, unit):
    validate_physical_reading(sensor_type, value, unit)


@pytest.mark.parametrize(
    ("sensor_type", "value", "unit", "message"),
    [
        ("temperatura", -274.0, "C", "cero absoluto"),
        ("humedad", 101.0, "%", "entre 0 y 100"),
        ("presión", -1.0, "Pa", "no puede ser negativa"),
        ("humedad", 50.0, "C", "solo admite la unidad %"),
    ],
)
def test_rejects_impossible_physical_readings(sensor_type, value, unit, message):
    with pytest.raises(ValueError, match=message):
        validate_physical_reading(sensor_type, value, unit)
