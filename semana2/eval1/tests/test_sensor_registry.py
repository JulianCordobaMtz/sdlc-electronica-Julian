import pytest
# Intentamos importar la clase y el error, aunque aún no existan
from sensor_registry import SensorRegistry, SensorNotFoundError

def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")