from sensor_reading import SensorReading


class AnomalyDetector:
    """Detecta anomalías en las lecturas de los sensores basándose en umbrales."""
    
    def __init__(self, umbral_temperatura: float, umbral_humedad: float) -> None:
        """Inicializa el detector inyectando los umbrales límite."""
        self.umbral_temperatura = umbral_temperatura
        self.umbral_humedad = umbral_humedad

    def evaluar(self, lectura: SensorReading) -> bool:
        """
        Evalúa si una lectura supera los umbrales configurados.
        Retorna True si hay anomalía, False si es normal.
        """
        return (lectura.temperatura > self.umbral_temperatura or 
                lectura.humedad > self.umbral_humedad)