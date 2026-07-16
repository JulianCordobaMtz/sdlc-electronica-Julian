# PRINCIPIO DE RESPONSABILIDAD ÚNICA (SRP)

# EL EJEMPLO MALO
class SensorSystemMal: #Crea la clase
    def read_sensor(self) -> float: #Define al sensor como objeto y coloca el tipo de dato que devuelve
        return 25.5 #Dato simulado

    def save_to_file(self, data: float) -> str: #Crea el objeto de guardar archivo
        return f"Dato {data} guardado en memoria." #Finge guardar en un archivo y devuelve un mensaje


# EL EJEMPLO BUENO
class SensorReader: #Crea la clase de lectura de sensores
    def read(self) -> float:
        return 25.5

class DataLogger: #Crea la clase de guardado de datos
    def persist(self, data: float) -> str:
        return f"Dato {data} guardado en memoria."
    

# PRINCIPIO DE ABIERTO/CERRADO (OCP)
class SensorReading: #Clase para representar la lectura de un sensor
    def __init__(self, sensor_id: str, value: float) -> None:
        self.sensor_id = sensor_id
        self.value = value

# EL EJEMPLO MALO
class AnomalyDetectorMal: #Crea el detector de anomalías mal diseñado
    def check(self, reading: SensorReading, alert_type: str) -> str: #Recibe la lectura y obliga a pedir el tipo de alerta
        if reading.value > 50.0: #
            if alert_type == "console": #Si es consola, entra aquí. Si mañana piden alerta por SMS, hay que modificar este código
                return f"Imprimiendo en consola: Anomalía en {reading.sensor_id}" #Devuelve el mensaje de consola
            elif alert_type == "file": #ROMPE LA REGLA (Cerrado a modificaciones): Nos obliga a seguir agregando "elifs" aquí adentro
                return f"Guardando en archivo: Anomalía en {reading.sensor_id}" #Devuelve el mensaje de archivo

# EL EJEMPLO BUENO 

class AlertStrategy: #Crea el molde base para las alarmas
    # Molde base sencillo. Solo define el nombre de la función vacía (pass).
    def send(self, message: str) -> str: #Establece que todas las alarmas deben tener esta función
        pass

class ConsoleAlert(AlertStrategy): #Crea la alarma de consola basada en el molde
    def send(self, message: str) -> str: #Implementa la función obligatoria
        return f"Consola: {message}" #Devuelve el mensaje formateado para consola

class FileAlert(AlertStrategy): #Crea la alarma de archivo basada en el molde
    def send(self, message: str) -> str:
        return f"Archivo log: {message}" #Devuelve el mensaje formateado para archivo

class AnomalyDetector: #Crea el detector principal
    def __init__(self, alert: AlertStrategy, threshold: float) -> None: #Pide que le inyecten una alarma y el límite
        self._alert = alert #Guarda la alarma de forma privada
        self._threshold = threshold #Guarda el límite de forma privada

    def check(self, reading: SensorReading) -> str | None: #Revisa la lectura del sensor
        if reading.value > self._threshold: #Compara la lectura con el límite establecido
            return self._alert.send(f"Anomalía en {reading.sensor_id}") #Si se pasa, dispara la alarma inyectada
        return None #Si todo está normal, no devuelve nada


# PRINCIPIO DE SUSTITUCIÓN DE LISKOV (LSP)
# EL EJEMPLO MALO
class SensorMalo: #Crea la clase base del sensor malo
    def read(self) -> float: #Promete devolver un dato numérico (float)
        return 20.5

class BrokenHumiditySensor(SensorMalo): #Crea un sensor hijo basado en el malo
    def read(self) -> str: #ROMPE LA REGLA: Prometió float pero devuelve un texto (str)
        return "Humedad: 45%" #Si otra función intenta hacer operaciones con esto, habrá error

# EL EJEMPLO BUENO

class BaseSensor: #Crea el molde base para los sensores buenos
    # Molde base sencillo.
    def read(self) -> float: #Establece el contrato estricto: todos deben devolver float
        pass

class TemperatureSensor(BaseSensor): #Crea el sensor de temperatura hijo
    def read(self) -> float: #Respeta el contrato devolviendo un float
        return 25.5 

class HumiditySensor(BaseSensor): #Crea el sensor de humedad hijo
    def read(self) -> float: #Respeta el contrato devolviendo un float
        return 60.0 

def process_sensor(sensor: BaseSensor) -> str: #Función que acepta cualquier sensor hijo del molde base
    valor = sensor.read() #Lee el valor con la seguridad de que SIEMPRE será un número
    return f"Procesando valor: {valor:.2f}" #Formatea el número a dos decimales y lo devuelve