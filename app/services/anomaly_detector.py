# app/services/anomaly_detector.py
from abc import ABC, abstractmethod

from app.repositories.alert_repository import AlertRepository


# =====================================================================
# INTERFAZ / ABSTRACCIÓN DE LA ESTRATEGIA (Principio DIP / ISP)
# =====================================================================
class AlertNotificationStrategy(ABC):
    """Interfaz abstracta que define el contrato para cualquier estrategia
    de notificación de anomalías en el sistema SensorHub.
    """
    @abstractmethod
    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        """Envía una alerta cuando un sensor supera su umbral físico."""
        pass


# =====================================================================
# IMPLEMENTACIONES CONCRETAS DE ESTRATEGIAS (Abierto a Extensión - OCP)
# =====================================================================
class ConsoleAlertStrategy(AlertNotificationStrategy):
    """Estrategia concreta que emite las alertas directamente a la consola
    del servidor de producción de forma formateada.
    """
    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        print(
            f"[ALERTA CRÍTICA] Sensor '{sensor_id}' superó el umbral seguro. "
            f"Lectura actual: {value} | Umbral máximo permitido: {threshold}"
        )


class InMemoryAlertStorageStrategy(AlertNotificationStrategy):
    """Estrategia concreta que guarda un historial de las alertas generadas
    en memoria para propósitos de pruebas o consultas rápidas.
    """
    def __init__(self) -> None:
        self.alerts: list[dict[str, float | str]] = []

    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        self.alerts.append({
            "sensor_id": sensor_id,
            "value": value,
            "threshold": threshold
        })


# =====================================================================
#   EL DETECTOR DE ANOMALÍAS (Contexto del Patrón Strategy)
# =====================================================================
class AnomalyDetector:
    """Clase responsable de evaluar las lecturas de los sensores.
    Depende de la abstracción de estrategia inyectada en su constructor.
    """
    def __init__(self, strategy: AlertNotificationStrategy) -> None:
        # Inyección de dependencias estricta (DIP)
        self.strategy = strategy

    def evaluate(self, sensor_id: str, value: float, threshold: float) -> None:
        """Evalúa si el valor recibido supera el umbral límite.
        Si hay una anomalía, delega la alerta a la estrategia activa.
        """
        # Regla de negocio: si el valor es estrictamente mayor que el umbral 
        if value > threshold:
            self.strategy.notify(sensor_id, value, threshold)

class DatabaseAlertStrategy(AlertNotificationStrategy):
    """Estrategia concreta que persiste las alertas directamente en la base de datos."""
    def __init__(self, alert_repo: AlertRepository) -> None:
        self.alert_repo = alert_repo

    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        from app.models.alert import AlertModel
        alert = AlertModel(
            sensor_id=sensor_id,
            value=value,
            threshold=threshold,
            status="open"
        )
        self.alert_repo.create(alert)
