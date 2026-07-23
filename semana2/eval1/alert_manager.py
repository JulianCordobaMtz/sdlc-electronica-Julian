from sensor_reading import SensorReading

class AlertManager:
    def generar_alerta(self, lectura: SensorReading, tipo_anomalia: str) -> str:
        """
        Genera un mensaje de alerta estandarizado basado en una lectura anómala.
        """
        timestamp_str = lectura.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        # Seleccionamos el valor correcto dependiendo del tipo de anomalía
        if tipo_anomalia == "TEMPERATURA":
            valor = lectura.temperatura
        else:
            valor = lectura.humedad
            
        mensaje = (
            f"*** ALERTA {tipo_anomalia} ***\n"
            f"Sensor: {lectura.sensor_id}\n"
            f"Valor registrado: {valor}\n"
            f"Fecha/Hora: {timestamp_str}\n"
            f"***************************"
        )
        return mensaje