class SensorNotFoundError(Exception):
    # Excepción lanzada cuando un sensor no existe en el sistema.
    pass

class SensorRegistry:
    # Registro en memoria para administrar los sensores de utilidad pública.
    def __init__(self):
        self._sensors = {}

    def get(self, sensor_id):
        # Valida y recupera un sensor específico mediante su ID.
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"El sensor '{sensor_id}' no está registrado.")
        
        return self._sensors[sensor_id]