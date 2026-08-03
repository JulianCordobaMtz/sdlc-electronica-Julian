class SensorService:
    def __init__(self, repo):
        # El servicio no crea el repositorio.
        # Recibe el repositorio ya inyectado por el router.
        self.repo = repo

    def create_sensor(self, sensor_in):
        # 1. Buscamos si el sensor ya existe en la base de datos
        sensor_existente = self.repo.get_by_id(sensor_in.sensor_id)
        
        # 2. Regla de negocio: Si existe, lanzamos excepción nativa de Python
        if sensor_existente:
            raise ValueError("El sensor_id ya está registrado")
        
        # 3. Si no existe, creamos el sensor
        return self.repo.create(sensor_in)

    def get_sensors(self, limit: int = 50, offset: int = 0):
        # Listar todos los sensores con soporte de paginación
        return self.repo.get_all(limit=limit, offset=offset)

    def get_sensor(self, sensor_id: str):
        # Buscar un sensor específico
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        return sensor

    def update_sensor(self, sensor_id: str, sensor_update):
        # Actualizar un sensor existente
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        return self.repo.update(sensor, sensor_update)

    def delete_sensor(self, sensor_id: str):
        # Eliminar un sensor existente
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        self.repo.delete(sensor)
        return None