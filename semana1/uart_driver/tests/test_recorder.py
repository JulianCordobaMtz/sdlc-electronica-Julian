import sys
import json
from pathlib import Path
import pytest

# Forzar la inclusión de la carpeta 'uart_driver' en el PATH del sistema
# Esto permite importar el módulo `recorder.py` para las pruebas
directorio_actual = Path(__file__).resolve().parent
directorio_padre = directorio_actual.parent
sys.path.insert(0, str(directorio_padre))

from recorder import DataRecorder

# PRUEBAS PARA EL MÓDULO DE RECORDER
def test_datarecorder_crea_directorio(tmp_path):
    """Prueba 1: Verifica que al instanciar DataRecorder, 
    cree la carpeta de destino automáticamente si esta no existe.
    Nota: 'tmp_path' es inyectado por pytest para usar una ruta temporal segura."""
    # Preparación: usar un subdirectorio dentro de tmp_path
    target_dir = tmp_path / "logs"
    recorder = DataRecorder(str(target_dir))

    # Validaciones: directorio creado y propiedad interna apuntando a Path
    assert target_dir.exists()
    assert target_dir.is_dir()
    assert recorder.log_directory == target_dir


def test_datarecorder_guarda_nuevo_archivo(tmp_path):
    """Prueba 2: Verifica que el método record() cree el archivo JSON
    y escriba el diccionario correctamente cuando el archivo es nuevo."""
    # Preparación: crear recorder apuntando al tmp_path
    recorder = DataRecorder(str(tmp_path))
    payload = {'slave_address': 1, 'function_code': 3, 'data': '0102'}

    # Acción: escribir el primer registro
    recorder.record(payload, filename='test_log.json')

    # Verificación: el archivo existe y contiene una lista con el payload
    file_path = tmp_path / 'test_log.json'
    assert file_path.exists()

    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)

    assert isinstance(content, list)
    assert content == [payload]


def test_datarecorder_anexa_datos_existentes(tmp_path):
    """Prueba 3: Verifica que si el archivo JSON ya tiene información,
    el método record() no la sobreescriba, sino que agregue el nuevo dato."""
    # Preparación: crear un archivo existente con registros previos
    file_path = tmp_path / 'test_log.json'
    existing = [{'slave_address': 1, 'function_code': 3, 'data': '0102'}]
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f)

    # Acción: instanciar recorder y anexar un nuevo registro
    recorder = DataRecorder(str(tmp_path))
    next_record = {'slave_address': 2, 'function_code': 4, 'data': 'ff00'}
    recorder.record(next_record, filename='test_log.json')

    # Verificación: el archivo ahora contiene ambos registros en orden
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)

    assert content == existing + [next_record]