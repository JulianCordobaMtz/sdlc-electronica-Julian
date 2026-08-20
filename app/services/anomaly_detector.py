# app/services/anomaly_detector.py
from abc import ABC, abstractmethod
from enum import StrEnum

from app.repositories.alert_repository import AlertRepository


# =====================================================================
# INTERFAZ / ABSTRACCIÓN DE LA ESTRATEGIA (Principio DIP / ISP)
# =====================================================================
class AlertNotificationStrategy(ABC):
    """Interfaz abstracta que define el contrato para cualquier estrategia
    de notificación de anomalías en el sistema SensorHub.
    """

    @abstractmethod
    def notify(
        self,
        sensor_id: str,
        value: float,
        threshold: float,
        severity: "AnomalySeverity",
    ) -> None:
        """Envía una alerta cuando un sensor supera su umbral físico."""
        pass


class AnomalySeverity(StrEnum):
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


# =====================================================================
# IMPLEMENTACIONES CONCRETAS DE ESTRATEGIAS (Abierto a Extensión - OCP)
# =====================================================================
class ConsoleAlertStrategy(AlertNotificationStrategy):
    """Estrategia concreta que emite las alertas directamente a la consola
    del servidor de producción de forma formateada.
    """

    def notify(
        self,
        sensor_id: str,
        value: float,
        threshold: float,
        severity: AnomalySeverity,
    ) -> None:
        print(
            f"[{severity}] Sensor '{sensor_id}' superó el umbral seguro. "
            f"Lectura actual: {value} | Umbral máximo permitido: {threshold}"
        )


class InMemoryAlertStorageStrategy(AlertNotificationStrategy):
    """Estrategia concreta que guarda un historial de las alertas generadas
    en memoria para propósitos de pruebas o consultas rápidas.
    """

    def __init__(self) -> None:
        self.alerts: list[dict[str, float | str]] = []

    def notify(
        self,
        sensor_id: str,
        value: float,
        threshold: float,
        severity: AnomalySeverity,
    ) -> None:
        self.alerts.append(
            {
                "sensor_id": sensor_id,
                "value": value,
                "threshold": threshold,
                "severity": severity,
            }
        )


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

    def evaluate(
        self, sensor_id: str, value: float, threshold: float
    ) -> AnomalySeverity | None:
        """Evalúa si el valor recibido supera el umbral límite.
        Si hay una anomalía, delega la alerta a la estrategia activa.
        """
        if value <= threshold:
            return None

        critical_margin = max(abs(threshold) * 0.20, 1.0)
        severity = (
            AnomalySeverity.CRITICAL
            if value >= threshold + critical_margin
            else AnomalySeverity.WARNING
        )
        self.strategy.notify(sensor_id, value, threshold, severity)
        return severity


class DatabaseAlertStrategy(AlertNotificationStrategy):
    """Estrategia concreta que persiste las alertas directamente en la base de datos."""

    def __init__(self, alert_repo: AlertRepository) -> None:
        self.alert_repo = alert_repo

    def notify(
        self,
        sensor_id: str,
        value: float,
        threshold: float,
        severity: AnomalySeverity,
    ) -> None:
        from app.models.alert import AlertModel

        alert = AlertModel(
            sensor_id=sensor_id,
            value=value,
            threshold=threshold,
            status="open",
            severity=severity,
        )
        self.alert_repo.create(alert)
