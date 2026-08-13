# tests/test_conversions.py
import math

import pytest
from pytest import approx

from semana5.conversions import (
	celsius_to_fahrenheit,
	celsius_to_kelvin,
	fahrenheit_to_celsius,
	kelvin_to_celsius,
)

# =====================================================================
# PRUEBAS ORIGINALES DE COPILOT (Casos de uso estándar)
# =====================================================================

def test_celsius_to_fahrenheit_happy() -> None:
	assert celsius_to_fahrenheit(0.0) == approx(32.0)
	assert celsius_to_fahrenheit(100.0) == approx(212.0)


def test_celsius_to_fahrenheit_below_absolute_zero() -> None:
	with pytest.raises(ValueError) as exc:
		celsius_to_fahrenheit(-274.0)
	assert "por debajo del cero absoluto" in str(exc.value)


def test_fahrenheit_to_celsius_happy() -> None:
	assert fahrenheit_to_celsius(32.0) == approx(0.0)
	assert fahrenheit_to_celsius(-40.0) == approx(-40.0)


def test_fahrenheit_to_celsius_below_absolute_zero() -> None:
	with pytest.raises(ValueError) as exc:
		fahrenheit_to_celsius(-500.0)
	assert "por debajo del cero absoluto" in str(exc.value)


def test_celsius_to_kelvin_happy() -> None:
	assert celsius_to_kelvin(0.0) == approx(273.15)
	assert celsius_to_kelvin(-273.15) == approx(0.0)


def test_celsius_to_kelvin_below_absolute_zero() -> None:
	with pytest.raises(ValueError) as exc:
		celsius_to_kelvin(-274.0)
	assert "por debajo del cero absoluto" in str(exc.value)


def test_kelvin_to_celsius_happy() -> None:
	assert kelvin_to_celsius(273.15) == approx(0.0)
	assert kelvin_to_celsius(0.0) == approx(-273.15)


def test_kelvin_to_celsius_below_absolute_zero() -> None:
	with pytest.raises(ValueError) as exc:
		kelvin_to_celsius(-1.0)
	assert "por debajo del cero absoluto" in str(exc.value)


# =====================================================================
# NUEVAS PRUEBAS DE AUDITORÍA (Casos extremos y límites físicos)
# =====================================================================

def test_precision_limite_infinitesimal_cero_absoluto():
    """Test 1: Verifica que el cero absoluto exacto sea aceptado, pero
    rechaza inmediatamente cualquier valor infinitesimalmente menor.
    """
    # Límite exacto de Celsius (-273.15) debe ser procesado sin lanzar excepción
    assert celsius_to_fahrenheit(-273.15) == (-273.15 * 9.0 / 5.0) + 32.0
    
    # Un valor infinitesimalmente menor (-273.15001) debe disparar ValueError
    with pytest.raises(ValueError, match="por debajo del cero absoluto"):
        celsius_to_fahrenheit(-273.15001)

    # Límite exacto de Fahrenheit (-459.67) debe ser aceptado
    assert fahrenheit_to_celsius(-459.67) == (-459.67 - 32.0) * 5.0 / 9.0
    
    # Un valor infinitesimalmente menor (-459.67001) debe fallar
    with pytest.raises(ValueError, match="por debajo del cero absoluto"):
        fahrenheit_to_celsius(-459.67001)


def test_conversions_nan_handling():
    """Test 2: Documenta el comportamiento de las funciones ante un valor NaN.

    Debido a que Python evalúa (NaN < Límite) como False, la función no lanza
    ValueError por default, sino que propaga el NaN aritméticamente.
    """
    nan_val = float("nan")

    # Verificamos que no lanza ValueError, sino que retorna NaN por propagación
    assert math.isnan(celsius_to_fahrenheit(nan_val))
    assert math.isnan(fahrenheit_to_celsius(nan_val))
    assert math.isnan(celsius_to_kelvin(nan_val))
    assert math.isnan(kelvin_to_celsius(nan_val))


def test_conversions_infinity_handling():
    """Test 3: Evalúa el comportamiento ante infinitos de punto flotante.

    Un infinito positivo es aritméticamente válido, pero un infinito negativo
    está físicamente por debajo del cero absoluto y debe ser bloqueado con
    ValueError.
    """
    pos_inf = float("inf")
    neg_inf = float("-inf")

    # Caso feliz extremo (Infinito positivo se propaga)
    assert celsius_to_fahrenheit(pos_inf) == pos_inf
    assert celsius_to_kelvin(pos_inf) == pos_inf

    # Caso de error extremo (Infinito negativo dispara ValueError)
    with pytest.raises(ValueError, match="por debajo del cero absoluto"):
        celsius_to_fahrenheit(neg_inf)

    with pytest.raises(ValueError, match="por debajo del cero absoluto"):
        fahrenheit_to_celsius(neg_inf)


def test_dynamic_type_evasion_at_runtime():
    """Test 4: Simula la evasión del tipado estático en tiempo de ejecución.

    Verifica que la lógica física del intérprete lance un TypeError de forma
    nativa si se le intentan inyectar tipos de datos no matemáticos
    incompatibles con la conversión.
    """
    with pytest.raises(TypeError):
        # Evasión dinámica de tipo string para simular un sensor enviando texto
        celsius_to_fahrenheit("temperatura_critica")  # type: ignore

    with pytest.raises(TypeError):
        # Evasión dinámica pasándole una estructura compleja
        kelvin_to_celsius({"valor": 300.0})  # type: ignore


def test_precision_round_trip_conversions():
    """Test 5: Comprueba la consistencia matemática de 'viaje redondo' (round-trip)
    entre las diferentes escalas físicas, asegurando que no haya deriva numérica
    por redondeo binario de punto flotante usando pytest.approx.
    """
    temp_original = 23.53  # Valor típico de lectura de sensor en SensorHub
    
    # Viaje redondo: Celsius -> Kelvin -> Celsius
    temp_k = celsius_to_kelvin(temp_original)
    temp_c_devuelta = kelvin_to_celsius(temp_k)
    assert temp_c_devuelta == approx(temp_original)

    # Viaje redondo: Celsius -> Fahrenheit -> Celsius
    temp_f = celsius_to_fahrenheit(temp_original)
    temp_c_f_devuelta = fahrenheit_to_celsius(temp_f)
    assert temp_c_f_devuelta == approx(temp_original)
