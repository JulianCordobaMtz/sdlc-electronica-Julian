class SensorNotFoundError(Exception):
    pass

class SensorRegistry:
    def __init__(self):
        self.sensors = {}

    def get(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorNotFoundError(f"Sensor {sensor_id} no encontrado")
        return self.sensors[sensor_id]