## Semana 1 · Entrada 1

**Prompt usado:** "proponme otras 5 funciones puras sobre reading con type hints, observa las que he agregado y anota pequeños comentarios arriba de cada una para saber lo que hacen, que sean similares a las que propuse originalmente"

**Qué produjo la IA:** Copilot generó un bloque con 5 funciones lógicas y matemáticas, respetando correctamente los tipos de datos y la estructura propuesta

**Mi decisión:** Acepté 2 de las 5 funciones propuestas, debido a que de las otras 3, no conocía del todo su funcionamiento o aplicación y creo que no iba a terminar de comprender en caso de que tuviera que explicar el verdadero funcionamiento de la misma función.
Estas fueron las rechazadas:
# Calcula el promedio entre dos lecturas del mismo sensor/tipo (pura)
```python
def average_readings(a: Reading, b: Reading) -> Reading:
    if a.sensor_id != b.sensor_id or a.sensor_type != b.sensor_type:
        # Si difieren, devuelve la primera sin modificar (no muta nada)
        return a
    avg = (a.value + b.value) / 2.0
    return Reading(sensor_id=a.sensor_id, value=avg, sensor_type=a.sensor_type)
```
# Limitar el valor de la lectura a un rango específico
```python
def clamp_reading(r: Reading, min_v: float, max_v: float) -> Reading:
    clamped = max(min_v, min(max_v, r.value))
    return Reading(sensor_id=r.sensor_id, value=clamped, sensor_type=r.sensor_type)
```
## Semana 1· Entrada 2

**Prompt usado:** "quiero que construyas 4 test fsm del fsm demo que se construyó dentro de la carpeta de martes14, estado inicial, transición RED→GREEN, ciclo completo que vuelve a RED, y conteo de ciclos."

**Qué produjo la IA:** Copilot generó un código con los 4 tests, sin embargo, los produjo con unnitest, que vienen siendo una librería más antigua, siendo más compleja a mi parecer y no corresponde a lo que estoy viendo.
```python
import unittest
from fsm_demo import TrafficLightFSM, TrafficLightState
```

**Mi decisión:** Rechazé el trabajo realizado por la IA, le solicité de nuevo la creación de los 4 tests pero haciendo uso de pytest, ya que esa fue la instrucción original.

## Semana 1· Entrada 3

**Prompt usado:** "Vuelve a construir el código pero esta vez usando pytest y generando los 4 tests"

**Qué produjo la IA:** Copilot generó de nuevo los 4 tests, esta vez usando pytest

**Mi decisión:** Acepté el trabajo generado por la IA, aunque va a estar sujeta a cambios dependiendo el análisis que se le de al tema con respecto a las FSM.