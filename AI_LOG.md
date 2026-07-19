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

## Semana 1· Entrada 4
**Prompt usado:** "Necesito que generes 2 tests por cada principio de S, O y L, del archivo solid_srp_ocp_lsp.py dentro de carpeta Miercoles 15, por lo que serán 6 tests al final, uno por cada ejemplo, lo harás con pytest"

**Qué produjo la IA:** Copilot generó de nuevo los tests, 2 por cada principio, para validar que el diseño de los 6 casos, agrupandolos en 3 clases distintas, inyectando valores simulados de sensores.

**Mi decisión:** Acepté el trabajo que hizo, dado que si cumplia con lo solicitado y sirvió para comprobar los 3 primeros principios de la arquitectura SOLID. Aunque tuve que comentar el código debido a que no todo lo lograba comprender.

## Semana 1· Entrada 6
**Prompt usado:** "Quiero que construyas un código donde se incluyan los 2 últimos principios de SOLID, los cuales vienen siendo el principio de segregación de interfaces y el principio de sustitución de LISKOV, quiero que la estructura sea que por cada principio sea uno bueno y otro malo, estructurado hacia el ámbito de sensores como los demás trabajos"

**Qué produjo la IA:** Copilot generó el código con los últimos 2 principios, con los comentarios respectivos para comprender mejor las intenciones de cada sección, de todas formas se hizo un análisis completo.

**Mi decisión:** Acepté el código generado, se aplicó un estudio aparte además de lo que vienen siendo estos 2 conceptos y se buscaron más ejemplos para compararlos para ver si lo que se había integrado era lo correcto.

**Semana 1· Entrada 7**
**Prompt usado:** "Tengo estas clases vacías en Python para decodificar protocolos seriales. Basándote en los docstrings, sugiéreme el código para reemplazar los pass con la lógica necesaria para validar y leer los bytes crudos."

**Qué produjo la IA:** Copilot generó la lógica interna de las clases reemplazando los pass, implementando el código necesario para validar y decodificar los bytes crudos en base a las instrucciones de los docstrings.

**Mi decisión:** Acepté el uso de este código debido a que coincidía con el uso de los principios SRP e inmutabilidad que se pidieron.

**Semana 1· Entrada 8**
**Prompt usado:** "Analiza las clases vacías en este archivo(device.py) cumpliendo el principio DIP, básate en los docstrings para sugerir el código que reemplace los pass para desarrollar un microncontrolador central, reemplaza el código y aplica los cambios, además de documentarlo con comentarios."

**Qué produjo la IA:** Copilot generó el código para el microcontrolador central respetando el principio de Inversión de Dependencias (DIP). Sustituyó los pass con la lógica correspondiente y agregó comentarios documentando el desarrollo. Pero con 2 errores, el primero debido a que tuvo una inscosistencia en las clases de connect, ya que especificaba la impresión de un puerto serial, sin embargo, en el apartado de configuración, nunca se asignó la creación de un puerto, ya que no venía en la tabla compartida de información, así que se le solicitó que lo cambiara apegado al config. El segundo error fue que puso en mayúsculas UARTConfig, siendo que estaba escrito UartConfig.

**Mi decisión:** Se modificó este código solicitandole que eliminara esto, además de manualmente editar el texto de UARTConfig a UartConfig.

**Semana 1 · Entrada 9**
Prompt usado: "Analiza las clases vacías en este archivo recorder.py, básate en los docstrings para sugerir el código que reemplace los pass para desarrollar el modulo de memoria, recuerda revisar el nombre de los archivos para las importaciones correctas y comentalo respectivamente, incluye los cambios en el archivo"

**Qué produjo la IA:** Copilot generó el código para el módulo de memoria en recorder.py guiándose por los docstrings proporcionados. Manejó correctamente las importaciones de los archivos y agregó los comentarios respectivos a las funciones.

**Mi decisión:** Se conservó el genero proporcionado, ya que coincide con lo solicitado, mantiene los principios SRP y se enlaza correctamente.

**Semana 1 · Entrada 10**
**Prompt usado:** "Revisa este archivo, aquí quiero construir el punto de prueba con pytest para el modulo de decodificadores que se construyo en el archivo parsers.py, siguiendo los docstrings para su construcción y comentalo respectivamente. Incluye los cambios en el archivo"

**Qué produjo la IA:** Copilot generó los tests unitarios utilizando pytest para el módulo de decodificadores, estructurando las pruebas a partir de los docstrings y documentando cada bloque.

**Mi decisión:** El código fue puesto a prueba con pytest y las respuestas fueron exitosas, se comprobó su correcto funcionamiento.

**Semana 1 · Entrada 11**
**Prompt usado:** "Revisa este archivo, aquí quiero construir el punto de prueba con pytest para el modulo de configuración, que se construyó en el archivo config.py, siguiendo los docstrings para su construcción y comentalo respectivamente. Incluye los cambios en el archivo"

**Qué produjo la IA:** Copilot generó las pruebas correspondientes con pytest para validar el módulo de configuración, incorporando los comentarios solicitados de acuerdo con los docstrings.

**Mi decisión:** El código generado pasó exitosamente las pruebas, por lo tanto, revisando su estructura se concluyó que era apto.

**Semana 1 · Entrada 12**
**Prompt usado:** "Revisa este archivo, aquí quiero construir el punto de prueba con pytest para el modulo de device, que se construyó en el archivo device.py, siguiendo los docstrings para su construcción y comentalo respectivamente. Incluye los cambios en el archivo."

**Qué produjo la IA:** Copilot generó el bloque de pruebas con pytest para auditar el funcionamiento del controlador central device.py, siguiendo las instrucciones de los docstrings e incluyendo la documentación necesaria.

**Mi decisión:** El código generado fue puesto a prueba con pytest y los resultados fueron positivos, por lo que se leyeron los comentarios generados y fue aceptado para el trabajo.

**Semana 1 · Entrada 13**
**Prompt usado:** "revisa este archivo, aquí quiero construir el punto de prueba con pytest para el modulo de memoria, que se construyó en el archivo recorder.py, siguiendo los docstrings para su construcción y comentalo respectivamente. Incluye los cambios en el archivo."

**Qué produjo la IA:** Copilot generó los escenarios de prueba con pytest para el módulo de almacenamiento recorder.py, reemplazando los esqueletos vacíos con la lógica de validación correspondiente y sus respectivos comentarios.

**Mi decisión:** Se le aplicaron las pruebas dentro de pytest junto con la lectura de su código y resultaron las respuestas positivas,por lo que se procede a almacenar el código generado.

**Semana 1 · Entrada 14**
**Prompt usado:** "Genera un código con pytest para generar 2 pruebas por cada uno de los 2 principios ISP y DIP, sigue la estructura trabajada con anterioridad, comenta las lineas para mejorar la comprensión."

**Qué produjo la IA:** Copilot generó el código de prueba con los 4 tests en total, se hicieron las pruebas correspondientes en la terminal y resultaron positivas.

**Mi decisión:** Se le aplicaron las pruebas dentro de pytest junto con la lectura de su código, y se aceptó dentro de la prueba.