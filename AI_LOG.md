## Semana 1 · Entrada 1

**Prompt usado:** "proponme otras 5 funciones puras sobre reading con type hints, observa las que he agregado y anota pequeños comentarios arriba de cada una para saber lo que hacen, que sean similares a las que propuse originalmente"

**Qué produjo la IA:** Copilot generó un bloque con 5 funciones lógicas y matemáticas, respetando correctamente los tipos de datos y la estructura propuesta

**Mi decisión:** Acepté 2 de las 5 funciones propuestas, debido a que de las otras 3, no conocía del todo su funcionamiento o aplicación y creo que no iba a terminar de comprender en caso de que tuviera que explicar el verdadero funcionamiento de la misma función.
Estas fueron las rechazadas:
# Calcula el promedio entre dos lecturas del mismo sensor/tipo (pura)
def average_readings(a: Reading, b: Reading) -> Reading:
    if a.sensor_id != b.sensor_id or a.sensor_type != b.sensor_type:
        # Si difieren, devuelve la primera sin modificar (no muta nada)
        return a
    avg = (a.value + b.value) / 2.0
    return Reading(sensor_id=a.sensor_id, value=avg, sensor_type=a.sensor_type)

# Limitar el valor de la lectura a un rango específico
def clamp_reading(r: Reading, min_v: float, max_v: float) -> Reading:
    clamped = max(min_v, min(max_v, r.value))
    return Reading(sensor_id=r.sensor_id, value=clamped, sensor_type=r.sensor_type)

De la primera, no termino de comprender como calcula el promedio, de la segunda si comprendo lo que se muestra, pero preferí poner otra opción con otra mejor aplicación.