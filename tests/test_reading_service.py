from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.schemas.reading import SensorReadingIn
from app.services.anomaly_detector import AnomalyDetector
from app.services.reading_service import ReadingService


# 1. Actualizamos el repositorio Fake para que exija 'sensor_id' y
# los datos en formato diccionario, igual que tu repo real de hoy.
class FakeReadingRepository:
    def create(self, sensor_id: str, data: dict):
        class FakeReading:
            def __init__(self, sensor_id, data):
                self.id = 1
                self.sensor_id = sensor_id
                self.value = data["value"]
                self.unit = data.get("unit", "C")

        return FakeReading(sensor_id, data)

    def get_statistics(self, sensor_id, from_date, to_date):
        return 3, 10.0, 30.0, 20.0


class FakeSensorRepository:
    def __init__(self, sensor=None):
        self.sensor = sensor or SimpleNamespace(
            sensor_id="TEMP-FAKE",
            type="temperatura",
            is_active=True,
            alert_threshold=30.0,
        )

    def get_by_id(self, sensor_id):
        return self.sensor


def test_registrar_lectura_con_fake_repo():
    fake_repo = FakeReadingRepository()
    detector = Mock(spec=AnomalyDetector)
    servicio = ReadingService(
        repo=fake_repo,
        detector=detector,
        sensor_repo=FakeSensorRepository(),
    )

    lectura_in = SensorReadingIn(value=25.5, unit="C")

    resultado = servicio.registrar_lectura("TEMP-FAKE", lectura_in)

    assert resultado.value == 25.5
    assert resultado.sensor_id == "TEMP-FAKE"


def test_obtener_estadisticas_con_fake_repo():
    servicio = ReadingService(
        repo=FakeReadingRepository(),
        detector=Mock(spec=AnomalyDetector),
        sensor_repo=FakeSensorRepository(),
    )

    stats = servicio.obtener_estadisticas("TEMP-FAKE", None, None)

    assert stats.count == 3
    assert stats.minimum == 10.0
    assert stats.maximum == 30.0
    assert stats.average == 20.0


def test_obtener_estadisticas_rechaza_periodo_invertido():
    servicio = ReadingService(
        repo=FakeReadingRepository(),
        detector=Mock(spec=AnomalyDetector),
        sensor_repo=FakeSensorRepository(),
    )

    with pytest.raises(ValueError, match="no puede ser mayor"):
        servicio.obtener_estadisticas(
            "TEMP-FAKE",
            datetime.fromisoformat("2026-08-18T12:00:00"),
            datetime.fromisoformat("2026-08-17T12:00:00"),
        )
