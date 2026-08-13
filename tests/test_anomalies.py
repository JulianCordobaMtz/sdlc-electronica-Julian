# tests/test_anomalies.py

# NOTA: Importamos clases que AÚN NO EXISTEN.
# Tu suite de pytest va a fallar al correr 
from app.services.anomaly_detector import (
    AlertNotificationStrategy,
    AnomalyDetector,
)


# 1. Creamos un mock/doble de prueba para verificar que la alerta se notifica
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