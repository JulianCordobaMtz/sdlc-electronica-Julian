class AlertManager:
    def __init__(self) -> None:
        self.ultima_alerta = ""

    def enviar_alerta(self, sensor_id: str, motivo: str) -> bool:
        """
        Simula el envío de una alerta y guarda el registro.
        """
        self.ultima_alerta = f"ALERTA: Sensor {sensor_id} - {motivo}"
        print(self.ultima_alerta)
        return True