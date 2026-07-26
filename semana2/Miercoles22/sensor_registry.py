class SensorNotFoundError(Exception):
    pass

class SensorRegistry:
    def __init__(self):
        self._sensors = {}

    def _validar_existencia(self, sensor_id):
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"Sensor {sensor_id} no encontrado")

    def get(self, sensor_id):
        self._validar_existencia(sensor_id)
        return self._sensors[sensor_id]