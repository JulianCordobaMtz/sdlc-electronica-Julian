import sys
import os
from pathlib import Path
import pytest

# Forzar la inclusión de la carpeta 'uart_driver' en el PATH del sistema
directorio_actual = Path(__file__).resolve().parent
directorio_padre = directorio_actual.parent
sys.path.insert(0, str(directorio_padre))

from config import UartConfig

# PRUEBAS PARA EL MÓDULO DE CONFIGURACIÓN
def test_uartconfig_valores_por_defecto():
    """Prueba 1: Verifica que al instanciar UartConfig sin parámetros,
    se asignen los valores por defecto correctos 
    (ej. baudrate=9600, parity='N', stop_bits=1, timeout=1.0)."""
    # Instanciación usando valores por defecto
    cfg = UartConfig()
    # Comprobamos cada atributo esperado por defecto
    assert cfg.baudrate == 9600  # baudrate por defecto
    assert cfg.parity == 'N'     # paridad por defecto
    assert cfg.stop_bits == 1    # stop bits por defecto
    assert cfg.timeout == 1.0    # timeout por defecto

def test_uartconfig_valores_personalizados():
    """Prueba 2: Verifica que al instanciar UartConfig pasándole valores
    específicos (ej. baudrate=115200, parity='E'), estos se guarden
    correctamente en el objeto."""
    # Crear una configuración personalizada y verificar los campos
    cfg = UartConfig(baudrate=115200, parity='E', stop_bits=2, timeout=0.5)
    assert cfg.baudrate == 115200
    assert cfg.parity == 'E'
    assert cfg.stop_bits == 2
    assert cfg.timeout == 0.5

def test_uartconfig_validacion_baudrate_invalido():
    """Prueba 3: Verifica el manejo de errores. Si se intenta crear 
    una configuración con un baudrate negativo o no estándar,
    debería lanzar una excepción (ValueError)."""
    # Baudrate 0 no es válido
    with pytest.raises(ValueError):
        UartConfig(baudrate=0, parity='N', stop_bits=1, timeout=1.0)

    # Baudrate negativo tampoco es válido
    with pytest.raises(ValueError):
        UartConfig(baudrate=-9600, parity='N', stop_bits=1, timeout=1.0)

    # También validar que stop_bits inválido lance error
    with pytest.raises(ValueError):
        UartConfig(baudrate=9600, parity='N', stop_bits=3, timeout=1.0)

    # Y paridad inválida debe lanzar ValueError
    with pytest.raises(ValueError):
        UartConfig(baudrate=9600, parity='X', stop_bits=1, timeout=1.0)