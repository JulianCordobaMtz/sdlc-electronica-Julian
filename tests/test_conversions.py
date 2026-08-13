import pytest

from pytest import approx

from semana5.conversions import (
	celsius_to_fahrenheit,
	fahrenheit_to_celsius,
	celsius_to_kelvin,
	kelvin_to_celsius,
)


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
