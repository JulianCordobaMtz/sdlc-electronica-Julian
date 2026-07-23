from datetime import datetime
from sensor_reading import SensorReading
from anomaly_detector import AnomalyDetector

def test_detector_acepta_umbrales():
    # Comprobamos que podemos inyectar los límites al crearlo
    detector = AnomalyDetector(umbral_temperatura=35.0, umbral_humedad=80.0)
    assert detector.umbral_temperatura == 35.0
    assert detector.umbral_humedad == 80.0

def test_detector_ignora_lectura_normal():
    detector = AnomalyDetector(umbral_temperatura=35.0, umbral_humedad=80.0)
    lectura_normal = SensorReading(sensor_id="T1", temperatura=25.0, humedad=50.0, timestamp=datetime.now())
    
    es_anomalia = detector.evaluar(lectura_normal)
    assert es_anomalia is False

def test_detector_identifica_alta_temperatura():
    detector = AnomalyDetector(umbral_temperatura=35.0, umbral_humedad=80.0)
    lectura_caliente = SensorReading(sensor_id="T2", temperatura=36.0, humedad=50.0, timestamp=datetime.now())
    
    es_anomalia = detector.evaluar(lectura_caliente)
    assert es_anomalia is True

def test_detector_identifica_alta_humedad():
    detector = AnomalyDetector(umbral_temperatura=35.0, umbral_humedad=80.0)
    lectura_humeda = SensorReading(sensor_id="T3", temperatura=25.0, humedad=85.0, timestamp=datetime.now())
    
    es_anomalia = detector.evaluar(lectura_humeda)
    assert es_anomalia is True