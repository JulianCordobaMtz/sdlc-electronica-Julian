"""Funciones de conversión de temperatura.

Requisitos:
- Tipado explícito (Python 3.12)
- Validación contra el cero absoluto
"""
from __future__ import annotations

from typing import Final

ABSOLUTE_ZERO_C_IN_C: Final[float] = -273.15
ABSOLUTE_ZERO_F_IN_F: Final[float] = -459.67
ABSOLUTE_ZERO_K_IN_K: Final[float] = 0.0



def celsius_to_fahrenheit(c: float) -> float:
	"""Convierte Celsius a Fahrenheit.

	Lanza ValueError si `c` está por debajo del cero absoluto (-273.15 °C).
	"""
	if c < ABSOLUTE_ZERO_C_IN_C:
		msg = (
			f"Temperatura en Celsius ({c}) por debajo del "
			f"cero absoluto ({ABSOLUTE_ZERO_C_IN_C} °C)"
		)
		raise ValueError(msg)
	return c * 9.0 / 5.0 + 32.0


def fahrenheit_to_celsius(f: float) -> float:
	"""Convierte Fahrenheit a Celsius.

	Lanza ValueError si `f` está por debajo del cero absoluto (-459.67 °F).
	"""
	if f < ABSOLUTE_ZERO_F_IN_F:
		msg = (
			f"Temperatura en Fahrenheit ({f}) por debajo del "
			f"cero absoluto ({ABSOLUTE_ZERO_F_IN_F} °F)"
		)
		raise ValueError(msg)
	return (f - 32.0) * 5.0 / 9.0


def celsius_to_kelvin(c: float) -> float:
	"""Convierte Celsius a Kelvin.

	Lanza ValueError si `c` está por debajo del cero absoluto (-273.15 °C).
	"""
	if c < ABSOLUTE_ZERO_C_IN_C:
		msg = (
			f"Temperatura en Celsius ({c}) por debajo del "
			f"cero absoluto ({ABSOLUTE_ZERO_C_IN_C} °C)"
		)
		raise ValueError(msg)
	return c + 273.15


def kelvin_to_celsius(k: float) -> float:
	"""Convierte Kelvin a Celsius.

	Lanza ValueError si `k` está por debajo de 0 K.
	"""
	if k < ABSOLUTE_ZERO_K_IN_K:
		msg = (
			f"Temperatura en Kelvin ({k}) por debajo del "
			f"cero absoluto ({ABSOLUTE_ZERO_K_IN_K} K)"
		)
		raise ValueError(msg)
	return k - 273.15


__all__ = [
	"celsius_to_fahrenheit",
	"fahrenheit_to_celsius",
	"celsius_to_kelvin",
	"kelvin_to_celsius",
]
