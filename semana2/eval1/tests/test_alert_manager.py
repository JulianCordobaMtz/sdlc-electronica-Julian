from datetime import datetime
from sensor_reading import SensorReading
from alert_manager import AlertManager

def test_generar_alerta_temperatura():
    manager = AlertManager()
    lectura = SensorReading(sensor_id="TEMP-99", temperatura=45.5, humedad=40.0, timestamp=datetime.now())
    
    mensaje = manager.generar_alerta(lectura, tipo_anomalia="TEMPERATURA")
    
    # Verificamos que el mensaje contenga los datos clave
    assert "ALERTA TEMPERATURA" in mensaje
    assert "TEMP-99" in mensaje
    assert "45.5" in mensaje

def test_generar_alerta_humedad():
    manager = AlertManager()
    lectura = SensorReading(sensor_id="HUM-88", temperatura=22.0, humedad=89.9, timestamp=datetime.now())
    
    mensaje = manager.generar_alerta(lectura, tipo_anomalia="HUMEDAD")
    
    # Verificamos que el mensaje contenga los datos clave
    assert "ALERTA HUMEDAD" in mensaje
    assert "HUM-88" in mensaje
    assert "89.9" in mensaje