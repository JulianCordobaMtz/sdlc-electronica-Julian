#IMPORTACIONES
import pytest
from solid_srp_ocp_lsp import (
    SensorReader, DataLogger, 
    SensorReading, AnomalyDetector, ConsoleAlert, FileAlert,
    BaseSensor, TemperatureSensor, HumiditySensor, process_sensor
)

# ==================== TESTS PARA SRP ====================

class TestSRP: #Agrupa las pruebas del principio de responsabilidad única
    
    def test_sensor_reader_reads_value(self):
        sensor = SensorReader() #Crea el objeto lector de sensor
        value = sensor.read() #Ejecuta la lectura del hardware simulado
        
        assert isinstance(value, float), "El sensor debe devolver un float" #Comprueba que la salida sea un número decimal
        assert value == 25.5, "El sensor debe leer el valor correcto" #Verifica que el valor sea exactamente el esperado
    
    def test_data_logger_persists_data(self):
        logger = DataLogger() #Crea el objeto guardador de datos
        test_data = 42.0 #Prepara un dato de prueba
        result = logger.persist(test_data) #Intenta guardar el dato en la memoria
        
        assert isinstance(result, str), "Persist debe devolver un string" #Verifica que el reporte entregado sea texto
        assert "42.0" in result, "El resultado debe contener el valor guardado" #Busca que el número esté dentro del mensaje
        assert "guardado en memoria" in result, "El resultado debe indicar que se guardó" #Confirma que el mensaje sea el correcto


# ==================== TESTS PARA OCP ====================

class TestOCP: #Agrupa las pruebas del principio abierto/cerrado
    
    def test_anomaly_detector_with_console_alert(self):
        alert = ConsoleAlert() #Crea el módulo de alarma para la consola
        detector = AnomalyDetector(alert, threshold=50.0) #Configura el detector con un límite de 50
        
        reading = SensorReading(sensor_id="TEMP_01", value=55.0) #Simula una lectura alta que supera el límite
        result = detector.check(reading) #Ejecuta la revisión del sistema
        
        assert result is not None, "Debe detectar la anomalía" #Comprueba que el sistema no se haya quedado callado
        assert "Consola:" in result, "La alerta debe ser de tipo consola" #Verifica que se usara el módulo correcto
        assert "TEMP_01" in result, "La alerta debe contener el ID del sensor" #Confirma que el reporte incluya el nombre del sensor
    
    def test_anomaly_detector_silencioso(self):
        alert = ConsoleAlert() #Crea el módulo de alarma para la consola
        detector = AnomalyDetector(alert, threshold=80.0) #Configura el detector con un límite alto de 80
        
        reading = SensorReading(sensor_id="TEMP_01", value=60.0) #Simula una lectura normal que no supera el límite
        result = detector.check(reading) #Ejecuta la revisión del sistema
        
        assert result is None, "El detector debe quedarse en silencio si no hay anomalía" #Comprueba que no se dispare ninguna falsa alarma


# ==================== TESTS PARA LSP ====================

class TestLSP: #Agrupa las pruebas del principio de sustitución de Liskov
    
    def test_temperature_sensor_returns_float(self):
        temp_sensor = TemperatureSensor() #Crea el sensor de temperatura hijo
        result = process_sensor(temp_sensor) #Lo conecta a la función de procesamiento general
        
        assert isinstance(result, str), "process_sensor debe devolver un string" #Verifica que la función general responda con texto
        assert "25.50" in result, "El resultado debe contener el valor del sensor" #Busca el dato numérico formateado en el mensaje
        assert "Procesando valor:" in result, "El resultado debe tener el formato correcto" #Confirma la estructura del reporte
    
    def test_humidity_sensor_returns_float(self):
        humidity_sensor = HumiditySensor() #Crea el sensor de humedad hijo para sustituir al anterior
        result = process_sensor(humidity_sensor) #Lo conecta a la MISMA función general de procesamiento
        
        assert isinstance(result, str), "process_sensor debe devolver un string" #Verifica que la función trabaje igual con el nuevo sensor
        assert "60.00" in result, "El resultado debe contener el valor del sensor" #Busca el nuevo dato numérico dentro del texto
        assert "Procesando valor:" in result, "El resultado debe tener el formato correcto" #Valida que el comportamiento no se haya roto