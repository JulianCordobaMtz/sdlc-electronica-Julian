from abc import ABC, abstractmethod
from sensor_reading import SensorReading

class AlertStrategy(ABC):
    """Clase base abstracta para las estrategias de alerta."""
    @abstractmethod
    def enviar(self, lectura: SensorReading, motivo: str) -> None:
        pass

class ConsoleStrategy(AlertStrategy):
    """Estrategia para imprimir la alerta en la terminal."""
    def enviar(self, lectura: SensorReading, motivo: str) -> None:
        mensaje = f"ALERTA: Sensor {lectura.sensor_id} - {motivo}"
        print(mensaje)

class FileStrategy(AlertStrategy):
    """Estrategia para guardar la alerta en un archivo de texto."""
    def __init__(self, filepath: str = "alertas.log"):
        self.filepath = filepath

    def enviar(self, lectura: SensorReading, motivo: str) -> None:
        mensaje = f"ALERTA: Sensor {lectura.sensor_id} - {motivo}\n"
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(mensaje)

class AlertManager:
    """Gestor de alertas que delega el envío a una estrategia específica."""
    def __init__(self, estrategia: AlertStrategy) -> None:
        self.estrategia = estrategia

    def enviar_alerta(self, lectura: SensorReading, motivo: str) -> bool:
        self.estrategia.enviar(lectura, motivo)
        return True