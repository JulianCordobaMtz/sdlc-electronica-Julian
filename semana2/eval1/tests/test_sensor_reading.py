import pytest
from datetime import datetime
from sensor_reading import SensorReading

def test_sensor_reading_creacion():
    # Dado que tenemos datos de un sensor
    fecha_actual = datetime.now()
    
    # Cuando creamos una lectura
    lectura = SensorReading(sensor_id="TEMP-01", temperatura=36.5, humedad=82.0, timestamp=fecha_actual)
    
    # Entonces los datos se guardan correctamente
    assert lectura.sensor_id == "TEMP-01"
    assert lectura.temperatura == 36.5
    assert lectura.humedad == 82.0
    assert lectura.timestamp == fecha_actual

def test_sensor_reading_es_inmutable():
    lectura = SensorReading(sensor_id="TEMP-01", temperatura=36.5, humedad=82.0, timestamp=datetime.now())
    
    # Comprobamos que intentar cambiar la temperatura lanza un error
    with pytest.raises(Exception):
        lectura.temperatura = 99.9