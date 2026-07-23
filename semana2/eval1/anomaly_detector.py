from sensor_reading import SensorReading

class AnomalyDetector:
    def __init__(self, umbral_temperatura: float, umbral_humedad: float) -> None:
        """
        Inicializa el detector inyectando los umbrales límite.
        """
        self.umbral_temperatura = umbral_temperatura
        self.umbral_humedad = umbral_humedad

    def evaluar(self, lectura: SensorReading) -> bool:
        """
        Evalúa si una lectura supera los umbrales configurados.
        Retorna True si hay anomalía, False si es normal.
        """
        if lectura.temperatura > self.umbral_temperatura:
            return True
            
        if lectura.humedad > self.umbral_humedad:
            return True
            
        return False