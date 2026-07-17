from typing import Protocol #Importa la herramienta Protocol para crear contratos

# I - PRINCIPIO DE SEGREGACIÓN DE INTERFACES (ISP)

# EL EJEMPLO MALO
class FatDeviceInterface: #Crea una interfaz gigante (gorda) que obliga a todo
    def read(self) -> float:
        pass
    def write(self, data: float) -> None:
        pass
    def calibrate(self) -> None:
        pass
    def reset(self) -> None:
        pass

class SimpleTemperatureSensorMal(FatDeviceInterface): #El sensor simple hereda el molde gigante
    def read(self) -> float: #Esta sí la usa
        return 25.5
    
    def write(self, data: float) -> None: #Obligado a tener una función que no usa
        raise Exception("Un sensor de temperatura no puede escribir datos")

# EL EJEMPLO BUENO
# Dividimos el molde gigante en módulos chiquitos y específicos 
class Readable: #Molde solo para leer
    def read(self) -> float:
        pass

class Writable: #Molde solo para escribir
    def write(self, data: float) -> None:
        pass

class Calibratable: #Molde solo para calibrar
    def calibrate(self) -> None:
        pass

class SimpleTemperatureSensor(Readable): #El sensor simple solo hereda lo que de verdad necesita
    def read(self) -> float: #Cumple su contrato sin tener funciones basura
        return 25.5

# D - PRINCIPIO DE INVERSIÓN DE DEPENDENCIAS (DIP)

class SensorReading: #Clase auxiliar rápida para representar la lectura
    def __init__(self, sensor_id: str, value: float) -> None:
        self.sensor_id = sensor_id
        self.value = value

# EL EJEMPLO MALO
class PostgreSQLRepositoryMal: #Crea una base de datos específica
    def save(self, reading: SensorReading) -> None:
        pass #Finge guardar en la base de datos real

class DataProcessorMal: #Crea el procesador
    def __init__(self) -> None:
        self._repo = PostgreSQLRepositoryMal() #ROMPE LA REGLA: Está soldado directamente a la base de datos específica

# EL EJEMPLO BUENO (Basado en la imagen del profesor)

class DataRepository(Protocol): #Crea el contrato estándar (el conector)
    def save(self, reading: SensorReading) -> None: ... #Exige que el módulo que le conecten tenga el pin "save"
    def get_latest(self, sensor_id: str) -> SensorReading | None: ... #Exige que tenga el pin "get_latest"

class DataProcessor: #Crea el procesador bien diseñado
    def __init__(self, repository: DataRepository) -> None: #Pide que le inyecten CUALQUIER módulo que cumpla el contrato
        self._repo = repository # Inyección de dependencias

    def process(self, reading: SensorReading) -> None: #Función para usar el repositorio
        # Aquí podría haber lógica de validación
        self._repo.save(reading) #Usa el módulo inyectado sin saber qué es por debajo

class InMemoryRepository: #Crea una base de datos de mentiras (en memoria RAM)
    def __init__(self) -> None:
        self.storage = [] #Usa una simple lista para guardar datos
        
    def save(self, reading: SensorReading) -> None: #Cumple con el pin "save" del contrato
        self.storage.append(reading)
        
    def get_latest(self, sensor_id: str) -> SensorReading | None: #Cumple con el pin "get_latest" del contrato
        if not self.storage:
            return None
        return self.storage[-1]