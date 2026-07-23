import sys
from pathlib import Path
import pytest

# Forzar la inclusión de la carpeta 'uart_driver' en el PATH del sistema
# Esto permite importar módulos locales (ej. device.py) directamente
directorio_actual = Path(__file__).resolve().parent
directorio_padre = directorio_actual.parent
sys.path.insert(0, str(directorio_padre))

from device import UARTDevice  # Clase bajo prueba
from config import UartConfig    # Configuración inyectada en el dispositivo
from parsers import MessageParser  # Interfaz para crear mocks de parsers

# MÓDULO DE PRUEBAS (MOCK)
class DummyParser(MessageParser):
    """Mock de parser para pruebas.
    - `can_parse` devuelve True solo para la secuencia exacta b'HOLA'.
    - `parse` devuelve un diccionario fijo que las pruebas esperan.
    Esto permite verificar que `UARTDevice` delega correctamente en el parser."""
    def can_parse(self, raw_data: bytes) -> bool:
        # Simula reconocimiento de trama: True únicamente para b'HOLA'
        return raw_data == b"HOLA"

    def parse(self, raw_data: bytes) -> dict:
        # Devuelve un resultado conocido para aserciones en tests
        return {"mensaje": "saludo_recibido"}

# PRUEBAS PARA EL MÓDULO DE DEVICE
def test_device_inicializacion():
    """Prueba 1: Verifica que el controlador central guarde bien 
    su configuración (UartConfig) y sus decodificadores al arrancar,
    y que su estado inicial de conexión sea False."""
    # Preparación: crear configuración y dispositivo con parser mock
    cfg = UartConfig()
    device = UARTDevice(config=cfg, parsers=[DummyParser()])

    # Verificaciones: las dependencias deben haberse guardado correctamente
    assert device.config == cfg
    assert len(device.parsers) == 1
    assert isinstance(device.parsers[0], DummyParser)
    # Estado inicial de conexión (antes de connect) debe ser False
    assert device._is_connected is False


def test_device_conexion():
    """Prueba 2: Verifica que al llamar a connect(), el estado 
    interno _is_connected cambie a True sin lanzar errores."""
    # Preparación y acción: conectar el dispositivo
    cfg = UartConfig()
    device = UARTDevice(config=cfg, parsers=[DummyParser()])

    device.connect()  # Cambia el estado interno a conectado
    assert device._is_connected is True

def test_device_error_si_lee_sin_conectar():
    """
    Prueba 3: Verifica el seguro de hardware que le pusimos. 
    Si se llama a receive_data() ANTES de connect(), 
    debe lanzar un RuntimeError.
    """
    # Sin conectar, receive_data debe fallar con RuntimeError (seguridad)
    cfg = UartConfig()
    device = UARTDevice(config=cfg, parsers=[DummyParser()])

    with pytest.raises(RuntimeError):
        device.receive_data(b"HOLA")


def test_device_decodificacion_exitosa():
    """Prueba 4: Verifica que si inyectamos el DummyParser, conectamos 
    el puerto y le mandamos los bytes b'HOLA', el controlador orqueste 
    todo correctamente y nos devuelva el diccionario esperado."""
    # Conectar y pasar una trama que el DummyParser reconoce
    cfg = UartConfig()
    device = UARTDevice(config=cfg, parsers=[DummyParser()])
    device.connect()

    resultado = device.receive_data(b"HOLA")
    # Debe devolver exactamente el diccionario que el parser mock retorna
    assert resultado == {"mensaje": "saludo_recibido"}

def test_device_decodificacion_fallida():
    """Prueba 5: Verifica que si inyectamos el DummyParser, conectamos
    el puerto y le mandamos datos basura (ej. b'BASURA'), el controlador 
    lance un ValueError porque ningún parser lo reconoce."""
    # Conectar y pasar una trama no reconocida: esperamo ValueError
    cfg = UartConfig()
    device = UARTDevice(config=cfg, parsers=[DummyParser()])
    device.connect()

    with pytest.raises(ValueError):
        device.receive_data(b"BASURA")