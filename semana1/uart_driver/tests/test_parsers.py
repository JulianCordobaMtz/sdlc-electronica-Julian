import sys
from pathlib import Path
import pytest

# Asegurarnos de que el módulo 'parsers.py' en la carpeta padre sea importable.
# Añadimos el directorio padre (uart_driver) al inicio de sys.path para que
# pytest pueda encontrar el módulo sin instalarlo como paquete.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from parsers import ModbusParser, NMEAParser

# PRUEBAS PARA EL MÓDULO DE DECODIFICADORES
def test_modbus_parser_trama_valida():
    """
    Prueba 1: ModbusParser debe reconocer una trama RTU mínima válida
    y devolver un diccionario con los campos esperados.
    - Construimos: [slave_addr, func_code, data..., crc_lo, crc_hi]
    - No verificamos CRC real (el parser actual no lo calcula), solo estructura.
    """
    parser = ModbusParser()  # Instancia el parser específico de Modbus
    raw = bytes([0x01, 0x03, 0x02, 0xAA, 0x00, 0x00])  # Trama Modbus de ejemplo

    assert parser.can_parse(raw) is True  # Debe reconocer el formato Modbus válido
    parsed = parser.parse(raw)  # Decodifica la trama en un diccionario
    assert parsed['slave_address'] == 0x01  # Dirección de esclavo esperada
    assert parsed['function_code'] == 0x03  # Código de función esperado
    assert parsed['data'] == '02aa'  # Verificar que los bytes de datos queden en hex
    assert parsed['crc'] == '0000'  # El CRC se reporta como hex string
    assert parsed['length'] == len(raw)  # Longitud total de la trama debe coincidir


def test_modbus_parser_trama_invalida():
    """
    Prueba 2: Trama con dirección fuera de rango debe ser rechazada.
    Además probamos una trama demasiado corta.
    """
    parser = ModbusParser()  # Instanciamos el parser para probar el rechazo de entradas invalidas

    # Dirección fuera de rango (250 > 247)
    bad_addr = bytes([250, 0x03, 0x00, 0x00])
    assert parser.can_parse(bad_addr) is False  # No debe aceptar direcciones inválidas

    # Trama demasiado corta
    too_short = bytes([0x01])
    assert parser.can_parse(too_short) is False  # El parser exige al menos dirección+función+CRC


def test_nmea_parser_sentencia_valida():
    """
    Prueba 3: NMEAParser debe reconocer una sentencia que empieza con '$'
    y termina en CRLF o LF, y separar los campos por comas.
    """
    parser = NMEAParser()  # Instancia el parser de sentencias NMEA
    raw = b"$GPRMC,123,456*1A\r\n"  # Sentencia NMEA de ejemplo con terminación CRLF

    assert parser.can_parse(raw) is True  # Debe detectar el inicio y fin correctos
    parsed = parser.parse(raw)  # Decodifica en tipo, campos y raw text
    assert parsed['type'] == 'GPRMC'  # El tipo debe leerse correctamente
    assert parsed['fields'][0] == '123'  # El primer campo debe conservarse
    assert parsed['raw'].startswith('GPRMC')  # Se elimina el '$' inicial en raw
    assert parsed['valid'] is True  # El parser considera válida la sentencia


def test_nmea_parser_sentencia_invalida():
    """
    Prueba 4: Cadenas que no comienzan con '$' o no terminan con salto de línea
    deben ser rechazadas por can_parse.
    """
    parser = NMEAParser()  # Instancia el parser NMEA para el caso inválido
    raw = b"RANDOM,NOFORMAT\n"  # Cadena que no comienza con '$'
    assert parser.can_parse(raw) is False  # Debe rechazarla porque no es NMEA válida
