from app.repositories.alert_repository import AlertRepository
from app.services.anomaly_detector import (
    AlertNotificationStrategy,
    AnomalyDetector,
    DatabaseAlertStrategy,
)

# =====================================================================
# 1. PRUEBAS UNITARIAS EN AISLAMIENTO (Sin Base de Datos)
# =====================================================================

class SpyAlertStrategy(AlertNotificationStrategy):
    """Estrategia espía para verificar en los tests si se disparó la notificación."""
    def __init__(self):
        self.alerts_sent: list[str] = []

    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        self.alerts_sent.append(f"ALERTA: {sensor_id} superó {threshold} con {value}")


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
    detector.evaluate(sensor_id="TEMP-01", value=36.0, threshold=35.0)
    
    assert len(spy.alerts_sent) == 1
    assert "ALERTA: TEMP-01 superó 35.0 con 36.0" in spy.alerts_sent


# =====================================================================
# 2. PRUEBAS DE INTEGRACIÓN (Con Base de Datos SQLite Aislada)
# =====================================================================

def test_database_alert_strategy_persists_alert_in_db():
    """Verifica que DatabaseAlertStrategy guarde la alerta en SQLite."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from app.db import Base
    
    # 1. Creamos base de datos en memoria para garantizar aislamiento total
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        alert_repo = AlertRepository(db)
        strategy = DatabaseAlertStrategy(alert_repo)
        detector = AnomalyDetector(strategy)
        
        # 2. Evaluamos un valor que supera el umbral
        detector.evaluate(sensor_id="TEMP-01", value=36.0, threshold=35.0)
        
        # 3. Verificamos utilizando accesos por índice  sobre la lista
        alerts = alert_repo.get_all()
        assert len(alerts) == 1
        assert alerts[0].sensor_id == "TEMP-01"  # <-- Corregido con 
        assert alerts[0].value == 36.0          # <-- Corregido con 
        assert alerts[0].threshold == 35.0      # <-- Corregido con 
        assert alerts[0].status == "open"        # <-- Corregido con 
    finally:
        db.close()


def test_database_alert_strategy_no_alert_below_threshold():
    """Verifica que no se guarde una alerta por debajo del umbral."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from app.db import Base
    
    # 1. Creamos la base de datos de pruebas limpia
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        alert_repo = AlertRepository(db)
        strategy = DatabaseAlertStrategy(alert_repo)
        detector = AnomalyDetector(strategy)
        
        # 2. Evaluamos un valor seguro
        detector.evaluate(sensor_id="TEMP-01", value=23.5, threshold=35.0)
        
        # 3. Verificamos que la tabla de alertas permanezca vacía
        alerts = alert_repo.get_all()
        assert len(alerts) == 0
    finally:
        db.close()
