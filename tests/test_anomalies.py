from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base
from app.models.alert import AlertModel
from app.models.sensor import SensorModel
from app.repositories.alert_repository import AlertRepository
from app.services.anomaly_detector import (
    AlertNotificationStrategy,
    AnomalyDetector,
    AnomalySeverity,
    DatabaseAlertStrategy,
)

# =====================================================================
# 1. PRUEBAS UNITARIAS EN AISLAMIENTO (Sin Base de Datos)
# =====================================================================


class SpyAlertStrategy(AlertNotificationStrategy):
    """Estrategia espía para verificar en los tests si se disparó la notificación."""

    def __init__(self):
        self.alerts_sent: list[str] = []

    def notify(
        self,
        sensor_id: str,
        value: float,
        threshold: float,
        severity: AnomalySeverity,
    ) -> None:
        self.alerts_sent.append(
            f"{severity}: {sensor_id} superó {threshold} con {value}"
        )


def _create_parent_sensor(db: Session) -> None:
    db.add(
        SensorModel(
            sensor_id="TEMP-01",
            name="Sensor Temperatura",
            type="temperatura",
            location="Bodega",
            alert_threshold=35.0,
        )
    )
    db.commit()


def test_no_anomaly_when_below_threshold():
    """Prueba que no se genere alerta si la lectura está en el rango seguro."""
    spy = SpyAlertStrategy()
    detector = AnomalyDetector(strategy=spy)

    # Supongamos un sensor con umbral de 35.0 °C
    detector.evaluate(sensor_id="TEMP-01", value=23.5, threshold=35.0)

    assert len(spy.alerts_sent) == 0


def test_anomaly_triggers_notification_when_exceeding_threshold():
    """Prueba que se dispare la estrategia si la lectura supera el umbral."""
    spy = SpyAlertStrategy()
    detector = AnomalyDetector(strategy=spy)

    # 36.0 °C supera el umbral de 35.0 °C
    severity = detector.evaluate(sensor_id="TEMP-01", value=36.0, threshold=35.0)

    assert len(spy.alerts_sent) == 1
    assert severity == AnomalySeverity.WARNING
    assert "WARNING: TEMP-01 superó 35.0 con 36.0" in spy.alerts_sent


def test_anomaly_is_critical_when_value_exceeds_margin():
    spy = SpyAlertStrategy()
    detector = AnomalyDetector(strategy=spy)

    severity = detector.evaluate(sensor_id="TEMP-01", value=42.0, threshold=35.0)

    assert severity == AnomalySeverity.CRITICAL
    assert spy.alerts_sent == ["CRITICAL: TEMP-01 superó 35.0 con 42.0"]


# =====================================================================
# 2. PRUEBAS DE INTEGRACIÓN (Con Base de Datos SQLite Aislada)
# =====================================================================


def test_database_alert_strategy_persists_alert_in_db():
    """Verifica que DatabaseAlertStrategy guarde la alerta en SQLite."""
    engine = create_engine("sqlite:///:memory:")
    try:
        Base.metadata.create_all(bind=engine)
        testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = testing_session()
        try:
            _create_parent_sensor(db)
            alert_repo = AlertRepository(db)
            detector = AnomalyDetector(DatabaseAlertStrategy(alert_repo))
            detector.evaluate(sensor_id="TEMP-01", value=36.0, threshold=35.0)

            alerts = alert_repo.get_all()
            assert len(alerts) == 1
            assert isinstance(alerts[0], AlertModel)
            assert alerts[0].sensor_id == "TEMP-01"
            assert alerts[0].value == 36.0
            assert alerts[0].threshold == 35.0
            assert alerts[0].severity == "WARNING"
            assert alerts[0].status == "open"
        finally:
            db.close()
    finally:
        engine.dispose()


def test_database_alert_strategy_no_alert_below_threshold():
    """Verifica que no se guarde una alerta por debajo del umbral."""
    engine = create_engine("sqlite:///:memory:")
    try:
        Base.metadata.create_all(bind=engine)
        testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = testing_session()
        try:
            _create_parent_sensor(db)
            alert_repo = AlertRepository(db)
            detector = AnomalyDetector(DatabaseAlertStrategy(alert_repo))
            detector.evaluate(sensor_id="TEMP-01", value=23.5, threshold=35.0)

            alerts = alert_repo.get_all()
            assert len(alerts) == 0
        finally:
            db.close()
    finally:
        engine.dispose()
