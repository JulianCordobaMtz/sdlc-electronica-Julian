import os
from datetime import datetime
from sensor_reading import SensorReading
from alert_manager import AlertManager, ConsoleStrategy, FileStrategy

def test_console_strategy_output(capsys):
    """Prueba que ConsoleStrategy imprima la alerta en la salida estándar"""
    # Arrange
    lectura = SensorReading(
        sensor_id="BODEGA-01", 
        temperatura=36.0, 
        humedad=50.0, 
        timestamp=datetime.now()
    )
    estrategia = ConsoleStrategy()
    manager = AlertManager(estrategia)
    
    # Act
    manager.enviar_alerta(lectura, "TEMPERATURA")
    
    # Assert
    captured = capsys.readouterr()
    assert "ALERTA" in captured.out
    assert "BODEGA-01" in captured.out
    assert "TEMPERATURA" in captured.out

def test_file_strategy_output(tmp_path):
    """Prueba que FileStrategy escriba la alerta en un archivo de texto"""
    # Arrange
    # tmp_path es una herramienta de pytest que crea una carpeta temporal segura
    archivo_prueba = tmp_path / "alertas_test.log"
    lectura = SensorReading(
        sensor_id="BODEGA-01", 
        temperatura=25.0, 
        humedad=85.0, 
        timestamp=datetime.now()
    )
    estrategia = FileStrategy(filepath=str(archivo_prueba))
    manager = AlertManager(estrategia)
    
    # Act
    manager.enviar_alerta(lectura, "HUMEDAD")
    
    # Assert
    assert archivo_prueba.exists()
    contenido = archivo_prueba.read_text()
    assert "ALERTA" in contenido
    assert "BODEGA-01" in contenido
    assert "HUMEDAD" in contenido