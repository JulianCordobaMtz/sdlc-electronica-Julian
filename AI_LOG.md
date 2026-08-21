# Bitácora de uso de IA

> Registro de las interacciones con herramientas de inteligencia artificial durante el curso.
> Cada entrada documenta el prompt utilizado, la propuesta generada por la IA, la decisión tomada frente a esa propuesta y la justificación detrás de esa decisión.

---

## Semana 1

### Entrada 1 — Funciones puras adicionales sobre `Reading`

#### Objetivo

Ampliar el módulo de sensores con nuevas funciones puras que operaran sobre el objeto `Reading`, evaluando cuáles de ellas se comprendían lo suficiente como para incorporarlas al proyecto.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> proponme otras 5 funciones puras sobre reading con type hints, observa las que he agregado y anota pequeños comentarios arriba de cada una para saber lo que hacen, que sean similares a las que propuse originalmente

#### Propuesta de la IA

Copilot generó un bloque con 5 funciones puras lógicas y matemáticas relacionadas con `Reading`, respetando correctamente los tipos de datos y el estilo de las funciones ya existentes en el archivo.

#### Decisión y cambios realizados

Se aceptaron únicamente 2 de las 5 funciones propuestas. Las otras 3 se rechazaron, entre ellas:

- `average_readings`, que promedia dos lecturas del mismo sensor.
- `clamp_reading`, que limita el valor de una lectura a un rango específico.

#### Justificación

No se comprendía del todo el funcionamiento ni la aplicación real de esas 3 funciones, y de haberse incorporado no habría podido explicar con seguridad su comportamiento. Se priorizó conservar únicamente el código que se domina.

---

### Entrada 2 — Primer intento de pruebas para la FSM (rechazado por usar `unittest`)

#### Objetivo

Generar 4 pruebas para el FSM (máquina de estados finitos) construido en la carpeta `martes14`: estado inicial, transición RED→GREEN, ciclo completo de vuelta a RED y conteo de ciclos.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> quiero que construyas 4 test fsm del fsm demo que se construyó dentro de la carpeta de martes14, estado inicial, transición RED→GREEN, ciclo completo que vuelve a RED, y conteo de ciclos.

#### Propuesta de la IA

Copilot generó las 4 pruebas solicitadas, pero utilizando la librería `unittest` en lugar de `pytest`.

#### Decisión y cambios realizados

Se rechazó por completo la propuesta y se solicitó rehacer el ejercicio usando `pytest`.

#### Justificación

`unittest` es una librería más antigua y, en comparación con `pytest`, más compleja de leer; además no correspondía al framework que se estaba trabajando en el curso hasta ese momento.

---

### Entrada 3 — Reconstrucción de pruebas de la FSM con `pytest`

#### Objetivo

Reintentar la generación de las 4 pruebas del FSM, ahora utilizando `pytest`.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Vuelve a construir el código pero esta vez usando pytest y generando los 4 tests

#### Propuesta de la IA

Copilot generó nuevamente las 4 pruebas, esta vez con `pytest`.

#### Decisión y cambios realizados

Se aceptó el trabajo generado, dejando abierta la posibilidad de ajustarlo conforme avanzara el análisis del tema de las FSM.

#### Justificación

La propuesta cumplió con el requisito explícito de usar `pytest`, que era el framework correcto para el curso.

---

### Entrada 4 — Pruebas para SRP, OCP y LSP

#### Objetivo

Generar 2 pruebas por cada uno de los principios S, O y L de SOLID (6 en total) a partir del archivo `solid_srp_ocp_lsp.py`.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Necesito que generes 2 tests por cada principio de S, O y L, del archivo solid_srp_ocp_lsp.py dentro de carpeta Miercoles 15, por lo que serán 6 tests al final, uno por cada ejemplo, lo harás con pytest

#### Propuesta de la IA

Copilot generó los 6 tests, agrupados en 3 clases distintas (una por principio), inyectando valores simulados de sensores para validar cada diseño.

#### Decisión y cambios realizados

Se aceptó el trabajo, aunque fue necesario comentar manualmente varias líneas del código porque no todo se comprendía a primera vista.

#### Justificación

Los tests cumplían con lo solicitado y sirvieron para comprobar el comportamiento de los 3 primeros principios de la arquitectura SOLID.

---

### Entrada 5 — Pruebas para ISP y LSP (ejemplos buenos y malos)

#### Objetivo

Cubrir los 2 principios restantes de SOLID —segregación de interfaces (ISP) y sustitución de Liskov (LSP)— con un ejemplo "bueno" y uno "malo" por principio, en el contexto de sensores.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Quiero que construyas un código donde se incluyan los 2 últimos principios de SOLID, los cuales vienen siendo el principio de segregación de interfaces y el principio de sustitución de LISKOV, quiero que la estructura sea que por cada principio sea uno bueno y otro malo, estructurado hacia el ámbito de sensores como los demás trabajos

#### Propuesta de la IA

Copilot generó el código con los 2 principios restantes, incluyendo comentarios para comprender mejor la intención de cada sección.

#### Decisión y cambios realizados

Se aceptó el código generado.

#### Justificación

Se complementó con estudio adicional por fuera de la IA y con la búsqueda de más ejemplos externos, para comparar y confirmar que lo integrado era correcto.

---

### Entrada 6 — Decodificación de protocolos seriales

#### Objetivo

Reemplazar los `pass` de un conjunto de clases vacías para decodificar protocolos seriales, a partir de la información contenida en sus docstrings.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Tengo estas clases vacías en Python para decodificar protocolos seriales. Basándote en los docstrings, sugiéreme el código para reemplazar los pass con la lógica necesaria para validar y leer los bytes crudos.

#### Propuesta de la IA

Copilot generó la lógica interna de las clases, reemplazando los `pass` con el código necesario para validar y decodificar los bytes crudos, según lo indicado en los docstrings.

#### Decisión y cambios realizados

Se aceptó el código generado.

#### Justificación

Coincidía con el uso de los principios de responsabilidad única (SRP) e inmutabilidad que se pedían para ese ejercicio.

---

### Entrada 7 — Microcontrolador central (`device.py`) respetando DIP

#### Objetivo

Implementar el microcontrolador central en `device.py` respetando el principio de Inversión de Dependencias (DIP), a partir de sus docstrings.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Analiza las clases vacías en este archivo(device.py) cumpliendo el principio DIP, básate en los docstrings para sugerir el código que reemplace los pass para desarrollar un microncontrolador central, reemplaza el código y aplica los cambios, además de documentarlo con comentarios.

#### Propuesta de la IA

Copilot generó el código del microcontrolador central respetando DIP, sustituyó los `pass` con la lógica correspondiente y documentó el desarrollo con comentarios. La propuesta incluyó, sin embargo, 2 errores:

1. Una inconsistencia en la clase de conexión: imprimía un puerto serial que nunca llegaba a configurarse, ya que no existía en la tabla de configuración compartida.
2. El nombre `UARTConfig` en mayúsculas, cuando el nombre correcto en el proyecto era `UartConfig`.

#### Decisión y cambios realizados

Se solicitó a la IA corregir el primer error apegándose a la configuración real, y se corrigió manualmente el segundo (`UARTConfig` → `UartConfig`).

#### Justificación

Ambos errores generaban una inconsistencia entre lo documentado y lo realmente configurado en el proyecto, por lo que era necesario resolverlos antes de aceptar el código.

---

### Entrada 8 — Módulo de memoria (`recorder.py`)

#### Objetivo

Implementar el módulo de memoria en `recorder.py`, a partir de sus docstrings y respetando las importaciones correctas del proyecto.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Analiza las clases vacías en este archivo recorder.py, básate en los docstrings para sugerir el código que reemplace los pass para desarrollar el modulo de memoria, recuerda revisar el nombre de los archivos para las importaciones correctas y comentalo respectivamente, incluye los cambios en el archivo

#### Propuesta de la IA

Copilot generó el código del módulo de memoria guiándose por los docstrings, manejó correctamente las importaciones entre archivos y agregó los comentarios respectivos.

#### Decisión y cambios realizados

Se conservó el código generado sin modificaciones.

#### Justificación

Coincidía con lo solicitado, mantenía el principio de responsabilidad única y se enlazaba correctamente con el resto del proyecto.

---

### Entrada 9 — Pruebas para el módulo de decodificadores (`parsers.py`)

#### Objetivo

Construir pruebas con `pytest` para el módulo de decodificadores construido en `parsers.py`, siguiendo sus docstrings.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Revisa este archivo, aquí quiero construir el punto de prueba con pytest para el modulo de decodificadores que se construyo en el archivo parsers.py, siguiendo los docstrings para su construcción y comentalo respectivamente. Incluye los cambios en el archivo

#### Propuesta de la IA

Copilot generó los tests unitarios con `pytest`, estructurando las pruebas a partir de los docstrings y documentando cada bloque.

#### Decisión y cambios realizados

Se aceptó el código después de ejecutar las pruebas y comprobar que los resultados fueran exitosos.

#### Justificación

Las pruebas confirmaron el correcto funcionamiento del módulo de decodificadores.

---

### Entrada 10 — Pruebas para el módulo de configuración (`config.py`)

#### Objetivo

Construir pruebas con `pytest` para el módulo de configuración construido en `config.py`.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Revisa este archivo, aquí quiero construir el punto de prueba con pytest para el modulo de configuración, que se construyó en el archivo config.py, siguiendo los docstrings para su construcción y comentalo respectivamente. Incluye los cambios en el archivo

#### Propuesta de la IA

Copilot generó las pruebas correspondientes para validar el módulo de configuración, incorporando comentarios de acuerdo con los docstrings.

#### Decisión y cambios realizados

Se aceptó el código tras revisar su estructura y confirmar que las pruebas pasaban correctamente.

#### Justificación

El resultado positivo de las pruebas confirmó que la estructura propuesta era apta para el proyecto.

---

### Entrada 11 — Pruebas para el controlador central (`device.py`)

#### Objetivo

Construir pruebas con `pytest` para el controlador central desarrollado en `device.py`.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Revisa este archivo, aquí quiero construir el punto de prueba con pytest para el modulo de device, que se construyó en el archivo device.py, siguiendo los docstrings para su construcción y comentalo respectivamente. Incluye los cambios en el archivo.

#### Propuesta de la IA

Copilot generó el bloque de pruebas para auditar el funcionamiento del controlador central, siguiendo las instrucciones de los docstrings e incluyendo la documentación necesaria.

#### Decisión y cambios realizados

Se aceptó el código después de confirmar resultados positivos al ejecutar `pytest` y de revisar los comentarios generados.

#### Justificación

El funcionamiento auditado por las pruebas resultó correcto.

---

### Entrada 12 — Pruebas para el módulo de memoria (`recorder.py`)

#### Objetivo

Construir pruebas con `pytest` para el módulo de memoria desarrollado en `recorder.py`.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> revisa este archivo, aquí quiero construir el punto de prueba con pytest para el modulo de memoria, que se construyó en el archivo recorder.py, siguiendo los docstrings para su construcción y comentalo respectivamente. Incluye los cambios en el archivo.

#### Propuesta de la IA

Copilot generó los escenarios de prueba con `pytest`, reemplazando los esqueletos vacíos con la lógica de validación correspondiente y sus respectivos comentarios.

#### Decisión y cambios realizados

Se aceptó el código tras ejecutar las pruebas y confirmar resultados positivos.

#### Justificación

Se validó el correcto funcionamiento del módulo antes de conservar el código en el proyecto.

---

### Entrada 13 — Pruebas para ISP y DIP

#### Objetivo

Generar 2 pruebas por cada uno de los principios ISP y DIP (4 en total), siguiendo la estructura ya trabajada en entradas anteriores.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Genera un código con pytest para generar 2 pruebas por cada uno de los 2 principios ISP y DIP, sigue la estructura trabajada con anterioridad, comenta las lineas para mejorar la comprensión.

#### Propuesta de la IA

Copilot generó el código de prueba con los 4 tests en total.

#### Decisión y cambios realizados

Se aceptó el código después de ejecutar las pruebas en terminal y confirmar resultados positivos.

#### Justificación

Los resultados obtenidos al probar el código con `pytest` confirmaron que era correcto.

---

## Semana 2

### Entrada 1 — Construcción del Product Backlog

#### Objetivo

Construir el Product Backlog del sistema de monitoreo IoT para una bodega industrial: historias de usuario, prioridades bajo el esquema MoSCoW, estimaciones mediante story points y escenarios de aceptación en formato Given-When-Then.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ayúdame a construir el Product Backlog de un sistema de monitoreo IoT para una bodega industrial. Necesito historias de usuario redactadas en el formato "Como... quiero... para...", cada una con una prioridad bajo el esquema MoSCoW (Must, Should, Could, Won't Have), una estimación en story points y al menos 2 escenarios de aceptación escritos con la estructura Given-When-Then. Cubre registro de lecturas, detección de anomalías por umbrales, envío de alertas por consola y archivo, muestreo cíclico, orquestación de varios sensores, simulación de datos, pruebas de integración, validación de rango físico, persistencia histórica y gestión dinámica de umbrales.

#### Propuesta de la IA

Copilot generó un documento con 10 historias de usuario (US-01 a US-10), cada una con su prioridad MoSCoW, su estimación en story points y sus respectivos escenarios Given-When-Then, cubriendo desde el registro estructurado de lecturas (`SensorReading`) hasta la gestión dinámica de umbrales sin necesidad de reiniciar el sistema.

#### Decisión y cambios realizados

Se aceptó la estructura general del backlog. Se revisaron los valores numéricos propuestos en los distintos escenarios (umbrales, tolerancias de tiempo, distribuciones estadísticas) para verificar que fueran coherentes entre historias relacionadas, y se ajustaron los rangos de temperatura y humedad de US-08 para que correspondieran con los umbrales ya definidos en US-02.

#### Justificación

Un backlog completo y verificable era indispensable antes de iniciar cualquier ciclo de TDD, ya que cada escenario Given-When-Then funciona como criterio de aceptación de las pruebas que se construirían más adelante.

---

### Entrada 2 — Desarrollo de `SensorRegistry` mediante TDD

#### Objetivo

Implementar la clase `SensorRegistry` siguiendo estrictamente el ciclo TDD (RED-GREEN-REFACTOR), respetando la regla de que cada commit de prueba debe preceder al commit del código correspondiente.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ayúdame a desarrollar SensorRegistry mediante TDD estricto para US-01. Primero necesito el test que compruebe que, al pedir un sensor con un ID que no existe (por ejemplo "GHOST-99"), se lance una excepción SensorNotFoundError. El test debe fallar por ImportError porque SensorRegistry todavía no existe. Después de confirmar la fase RED, ayúdame con la implementación mínima para pasar a GREEN, y por último sugiere un refactor que extraiga la validación del sensor sin romper las pruebas.

#### Propuesta de la IA

Copilot propuso primero la prueba `test_get_unknown_sensor_raises`, que instancia `SensorRegistry` y verifica con `pytest.raises(SensorNotFoundError)` que se lance la excepción esperada al pedir un sensor inexistente. Confirmada la fase RED (fallo por `ImportError`, ya que `SensorRegistry` todavía no existía), propuso la implementación mínima de la clase para que la prueba pasara (GREEN). Finalmente, para REFACTOR, sugirió extraer la validación del identificador del sensor en un método separado dentro de `SensorRegistry`.

#### Decisión y cambios realizados

Se siguieron las 3 fases en orden. Se creó primero el archivo de prueba y se confirmó su fallo (RED) con el commit `test: especificar SensorRegistry (RED) - us-01`. Se implementó después el código mínimo necesario (GREEN) con su propio commit, y finalmente se aplicó el refactor sugerido, registrado en un tercer commit.

#### Justificación

Que el commit de prueba siempre preceda al commit de código deja evidencia clara del ciclo TDD en el historial de Git, y confirma que la implementación surgió a partir de una prueba que realmente falló primero.

---

### Entrada 3 — Auditoría del backlog con criterios Gherkin

#### Objetivo

Auditar las 10 historias de usuario del backlog aplicando criterios Gherkin (verificabilidad, ambigüedad, casos borde faltantes) para decidir cuáles conservar como núcleo del sprint.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Quiero que audites mis user stories con criterios Gherkin, se supone que se hicieron para un sistema de monitoreo IOT para bodega industrial. Las primeras 3 deben ser de núcleo con las siguientes características: SensorReading, AnomalyDetector (umbrales inyectados, no hardcodeados) y AlertManager (estrategia abstracta + Console y File) para tener una cobertura del 80% mínimo en el test. Las siguientes preguntas te servirán para descartar o decirme que corregir: ¿es verificable? ¿es ambiguo? ¿qué caso borde falta?
> Usa esos criterios para elegir alguno o algunos de los 10 que estan escritos y dime el porque de tu decisión.

#### Propuesta de la IA

Copilot revisó las 10 user stories, aplicando los criterios Gherkin a cada una. Determinó que 2 debían descartarse por no cumplir los requisitos, y que otras 4 necesitaban ajustes por ambigüedades, imprecisiones, falta de verificabilidad o ausencia del caso de error.

#### Decisión y cambios realizados

Se solicitó a la IA aplicar los cambios directamente en el archivo: sustituir las 2 historias descartadas por otras que sí cumplieran los criterios, y corregir las irregularidades detectadas en las otras 4.

#### Justificación

Aplicar criterios objetivos de verificabilidad, ambigüedad y casos borde antes de iniciar el desarrollo evita construir pruebas de TDD sobre historias de usuario mal definidas.

---

### Entrada 4 — Desarrollo de US-01 (`SensorReading`) mediante TDD

#### Objetivo

Implementar `SensorReading` siguiendo el ciclo TDD, de modo que el sistema registre lecturas válidas en un objeto inmutable y rechace lecturas con datos corruptos, según los escenarios definidos en el backlog.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ayúdame a desarrollar US-01 mediante TDD. Necesito una clase SensorReading que reciba un ID de sensor, temperatura y humedad, y que genere un objeto inmutable con esos datos más el timestamp exacto de recepción. Primero crea las pruebas que confirmen que una lectura válida se crea correctamente, y que una lectura con valores nulos o vacíos lanza un error de validación y se descarta. Después ayúdame con la implementación mínima para pasar esas pruebas.

#### Propuesta de la IA

**RED:** Copilot propuso 2 pruebas: la creación correcta de una lectura válida (verificando que el objeto resultante fuera inmutable y conservara el timestamp de recepción) y el rechazo de lecturas con valores nulos o vacíos mediante una excepción de validación. Ambas pruebas fallaron inicialmente porque `SensorReading` no existía todavía.

**GREEN:** propuso una clase inmutable que valida los campos recibidos antes de construir el objeto, y lanza una excepción de validación al detectar datos vacíos o nulos.

#### Decisión y cambios realizados

Se aceptaron las 2 pruebas por representar directamente los criterios de aceptación de US-01. Se confirmó la fase RED antes de aceptar la implementación mínima que las hacía pasar.

#### Justificación

Verificar primero el fallo de las pruebas confirma que la validación de datos no estaba implementada de antemano, y que la clase inmutable resultante corresponde exactamente a lo exigido por los escenarios Given-When-Then de US-01.

---

### Entrada 5 — Desarrollo de US-02 (`AnomalyDetector`) mediante TDD

#### Objetivo

Implementar `AnomalyDetector` con umbrales inyectados (no hardcodeados) que clasifique una lectura como anomalía si la temperatura o la humedad exceden sus umbrales.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ayúdame a desarrollar US-02 mediante TDD. Necesito una clase AnomalyDetector que reciba los umbrales de temperatura y humedad por constructor (no hardcodeados) y que marque una lectura como anomalía si cualquiera de los dos valores excede su umbral. Si ambos valores están fuera de rango, debe generar una sola marca de anomalía y no dos. Empieza con las pruebas antes que la implementación.

#### Propuesta de la IA

**RED:** Copilot generó pruebas para la detección de anomalía por temperatura fuera de umbral, la detección por humedad fuera de umbral, la detección cuando ambos parámetros están fuera de umbral (verificando que solo se genere una marca de anomalía y no dos) y la clasificación como "Normal" cuando la lectura está dentro de los parámetros esperados.

**GREEN:** implementó `AnomalyDetector` recibiendo los umbrales en el constructor y aplicando una condición OR lógica entre temperatura y humedad para decidir si la lectura es anómala.

#### Decisión y cambios realizados

Se aceptaron las 4 pruebas y la implementación mínima, verificando específicamente que los umbrales se inyectaran por constructor y no quedaran fijos dentro del código.

#### Justificación

Inyectar los umbrales en lugar de fijarlos en el código permite reconfigurar la sensibilidad del detector sin modificar su lógica interna, tal como lo exige el backlog.

---

### Entrada 6 — Desarrollo de US-03 (`AlertManager`) mediante TDD

#### Objetivo

Implementar `AlertManager` con una estrategia abstracta de notificación y dos implementaciones concretas (`Console` y `File`), incluyendo el manejo de errores al escribir en archivo.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ayúdame a desarrollar US-03 mediante TDD. Necesito un AlertManager que reciba una estrategia de notificación abstracta, con dos implementaciones: una que imprima la alerta en consola y otra que la escriba al final de un archivo alertas.log. Si la estrategia de archivo falla por falta de permisos, debe capturar la excepción, registrarla en el logger del sistema y evitar que el programa se bloquee. Empieza con las pruebas.

#### Propuesta de la IA

**RED:** Copilot propuso pruebas para la notificación de alerta por consola, el registro de alerta en archivo (verificando que se escribiera al final del archivo y que este se cerrara correctamente) y el fallo en la escritura a archivo (verificando que se capturara la excepción de permiso denegado sin bloquear el programa).

**GREEN:** implementó `AlertManager` con una clase abstracta `AlertStrategy` y dos subclases —una para consola y otra para archivo—, esta última con manejo de excepciones sobre errores de permisos.

#### Decisión y cambios realizados

Se aceptaron las 3 pruebas y la implementación mínima. Se verificó específicamente que un fallo de escritura no detuviera la ejecución del programa, tal como lo exige el escenario de error del backlog.

#### Justificación

Usar una estrategia abstracta permite añadir nuevos canales de alerta en el futuro sin modificar `AlertManager`, cumpliendo tanto el principio abierto/cerrado como el criterio de aceptación de US-03.

---

### Entrada 7 — Configuración del tablero Kanban en GitHub Projects

#### Objetivo

Configurar el tablero Kanban en GitHub Projects para documentar el Sprint 1, trasladando las historias del backlog escritas en texto plano a tarjetas organizadas por columna.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Para documentar correctamente mi Sprint 1 y cumplir con la rúbrica dada, necesito configurar mi tablero Kanban en GitHub Projects. Tengo mi archivo de Product Backlog con 10 historias de usuario y he seleccionado 5 para este sprint. Tu tarea es explicarme cómo debo estructurar las columnas (Product Backlog, Sprint, In Progress, Review, Done) y cuál es la forma correcta de trasladar mis historias redactadas en texto plano a tarjetas de GitHub para que la evidencia quede correctamente documentada y refleje mi avance con el código del núcleo.

#### Propuesta de la IA

Proporcionó una guía detallada sobre la configuración de GitHub Projects, aclarando que los archivos `.md` locales no se sincronizan automáticamente con la vista web. Recomendó utilizar la función de "Draft Issues" para transcribir los títulos exactos del backlog. Además, definió la distribución lógica de las tarjetas: las historias no seleccionadas debían ir a la columna "Product Backlog", las pendientes de desarrollo a "Sprint", y las historias de `SensorReading`, `AnomalyDetector` y `AlertManager` a la columna "Done".

#### Decisión y cambios realizados

Se aplicó la estructura sugerida creando manualmente las tarjetas directamente en el tablero. Se verificó que los títulos coincidieran letra por letra con el archivo original para no mezclar tareas técnicas con historias de usuario, y se acomodaron las tarjetas en las columnas correspondientes, reflejando el estado real del repositorio.

#### Justificación

Mantener los nombres exactos entre el backlog y las tarjetas evita ambigüedad entre las historias de usuario y las tareas técnicas de desarrollo, permitiendo que el tablero sirva como evidencia fiel del avance del sprint.


---
 
## Semana 3
 
### Entrada 1 — Guardar los datos de los sensores en una base de datos real
 
#### Objetivo
 
Dejar de perder los datos de sensores y lecturas cada vez que se apagaba el servidor, guardándolos en una base de datos de verdad.
 
#### Herramienta utilizada
 
`Copilot`
 
#### Prompt utilizado
 
> Necesito pasar mis datos de sensores y lecturas, que hasta ahora solo vivían en memoria, a una base de datos real. Ayúdame a crear las clases Sensor y Reading con la forma nueva de escribir modelos en SQLAlchemy, dejando claro que cada lectura pertenece a un sensor.
 
#### Propuesta de la IA
 
Copilot me dio las clases Sensor y Reading, indicando qué tipo de dato lleva cada columna (número, texto, fecha) y conectando ambas tablas para que cada lectura supiera a qué sensor pertenece.
 
#### Decisión y cambios realizados
 
Acepté la propuesta, pero revisé que todo estuviera escrito con la forma nueva de SQLAlchemy y no con la forma vieja que a veces la IA usa porque aprendió de tutoriales antiguos.
 
#### Justificación
 
Usar la forma nueva hace que todo el proyecto quede escrito de manera consistente (con los mismos tipos de dato en todos lados), y así puedo revisarlo con las mismas herramientas que ya uso en el resto del código, sin mezclar estilos distintos.
 
---
 
### Entrada 2 — Organizar el código en carpetas para que no se vuelva un desorden
 
#### Objetivo
 
Ordenar mi carpeta `app/` para que cada parte del código tuviera su lugar, en vez de tener todo mezclado.
 
#### Herramienta utilizada
 
`Copilot`
 
#### Prompt utilizado
 
> Quiero organizar mi API en carpetas separadas: una para los modelos de base de datos, otra para lo que valida los datos, otra para las consultas a la base de datos, otra para la lógica de mi programa y otra para lo que recibe las peticiones web. Ayúdame a entender qué debe hacer cada carpeta y cómo se comunican entre sí, para que la parte que recibe la petición no tenga que saber nada de cómo se guarda la información.
 
#### Propuesta de la IA
 
Copilot me explicó cómo debía verse esa separación: lo que recibe la petición solo la pasa a la siguiente parte, esa parte se encarga de la lógica, y solo una última parte habla directamente con la base de datos.
 
#### Decisión y cambios realizados
 
Acepté la forma de organizarlo y revisé, carpeta por carpeta, que ninguna parte se estuviera saltando ese orden (por ejemplo, que la que recibe la petición no estuviera hablando directo con la base de datos).
 
#### Justificación
 
Si en algún momento cambio de base de datos, no debería tener que tocar la parte que recibe las peticiones. Eso era justo lo que pedía la rúbrica de esta semana.
 
---
 
### Entrada 3 — Validar que los datos tengan sentido, y un error que encontré yo mismo
 
#### Objetivo
 
Que la API no aceptara datos sin sentido, como una humedad imposible o una unidad de medida que no existe.
 
#### Herramienta utilizada
 
`Copilot`
 
#### Prompt utilizado
 
> Necesito revisar los datos de una lectura antes de guardarla: que rechace temperaturas o humedades fuera de rango, y unidades que no reconozca. También ayúdame a escribir una prueba que confirme que, si mando un dato inválido, la API responde con un error y me dice exactamente cuál campo estuvo mal.
 
#### Propuesta de la IA
 
Copilot me dio la validación y también propuso la prueba para comprobar el error. Sin embargo, me pasó una línea de código incompleta —por un problema al copiar el formato— y esa línea no funcionaba como debía.
 
#### Decisión y cambios realizados
 
Al correr la prueba vi que fallaba y me di cuenta de que faltaba una parte de la línea. La corregí yo mismo y se lo hice saber a la IA antes de seguir con las demás pruebas.
 
#### Justificación
 
Si hubiera aceptado esa línea sin revisarla, habría dejado una prueba que nunca iba a funcionar bien, o que fallaba sin que yo me diera cuenta. Revisar el resultado antes de aceptarlo fue justo lo que evitó ese problema.
 
---
 
### Entrada 4 — Terminar el CRUD y subir mi Pull Request
 
#### Objetivo
 
Terminar todas las acciones que le faltaban a mi API (crear, ver, actualizar y borrar) y dejar el código listo para que lo revisaran.
 
#### Herramienta utilizada
 
`GitHub Copilot`
 
#### Prompt utilizado
 
> Ayúdame a terminar lo que le falta a mi API: poder actualizar una lectura y poder desactivar un sensor. Revisa que cada acción responda con el código correcto según lo que pasó, y que lo que mando al crear un registro sea diferente de lo que la API me regresa, para no exponer datos que no debería.
 
#### Propuesta de la IA
 
Copilot completó las dos acciones que faltaban, agregó el mensaje de error correcto cuando algo no existe, y separó lo que se manda al crear un registro de lo que la API regresa, para no dejar visible, por ejemplo, el ID antes de que existiera.
 
#### Decisión y cambios realizados
 
Probé cada acción a mano desde la documentación de mi API antes de aceptarla. Junté todos mis cambios de la semana y abrí mi Pull Request, con una descripción de qué hace y cómo probarlo.
 
#### Justificación
 
Separar lo que se manda de lo que se recibe evita que alguien controle datos que no le corresponden, y responder con el código correcto era parte de lo que se pedía esta semana.
 
---
 
### Entrada 5 — Revisar el código de un compañero
 
#### Objetivo
 
Aprender a revisar el trabajo de otra persona de forma útil, siguiendo la checklist que dio el coordinador.
 
#### Herramienta utilizada
 
`GitHub Copilot`
 
#### Prompt utilizado
 
> Voy a revisar el código de un compañero con la checklist de 10 puntos. Ayúdame a repasar qué cosas debo buscar como señal de alarma: por ejemplo, que meta reglas de su programa en la parte que recibe las peticiones, o que no cierre bien la conexión a la base de datos.
 
#### Propuesta de la IA
 
Copilot me recordó las señales más comunes: lógica del programa metida donde no debería (en vez de estar en su propio lugar), conexiones a la base de datos que no se cierran bien si algo falla, y devolver directamente los datos de la base sin pasar por la validación.
 
#### Decisión y cambios realizados
 
Descargué la rama de mi compañero, la probé en mi computadora y dejé comentarios señalando el archivo y la línea exacta, enfocándome en los puntos donde encontré lógica en el lugar equivocado.
 
#### Justificación
 
Revisar con algo concreto que buscar —y no solo decir "se ve bien"— era lo que pedía la actividad, y encontrar ese tipo de mezcla es de los errores más comunes en esta parte del curso.


---

## Semana 4

### Entrada 1 — Control de versiones de la base de datos con Alembic

#### Objetivo

Dejar de depender de que SQLAlchemy creara las tablas automáticamente al arrancar la app, y tener un historial de los cambios que le hago a la base de datos.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ya no quiero que mi base de datos se cree automáticamente cada vez que arranca mi app con Base.metadata.create_all. Ayúdame a instalar Alembic, conectarlo con mis modelos de SQLAlchemy y generar mi primera migración a partir de lo que ya tengo.

#### Propuesta de la IA

Copilot me guio para instalar e inicializar Alembic, me ayudó a importar mi `Base` dentro del archivo `env.py` para que Alembic supiera de qué modelos generar los cambios, y generó la primera migración automática con el comando `alembic revision --autogenerate`.

#### Decisión y cambios realizados

Apliqué esa primera migración con `alembic upgrade head` y confirmé que las tablas se crearan desde ese script y no desde el arranque de la aplicación.

#### Justificación

Si sigo dejando que la app cree las tablas sola, no tengo forma de saber qué cambió entre una versión y otra, ni de deshacer un cambio si algo sale mal. Con Alembic, cualquier cambio futuro a mis modelos (como agregar un campo a Sensor) queda registrado y se puede revisar o revertir.

---

### Entrada 2 — Contenedores, PostgreSQL y Docker Compose

#### Objetivo

Dejar SQLite (que es solo un archivo local) y pasar a PostgreSQL, además de asegurar que toda mi aplicación corra igual en cualquier computadora usando contenedores.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Necesito pasar mi base de datos de SQLite a PostgreSQL y levantar todo con Docker. Ayúdame a escribir el Dockerfile de mi API, cambiar la conexión de mi app para que apunte a Postgres, y armar un docker-compose.yml que levante tanto mi API como la base de datos con un solo comando.

#### Propuesta de la IA

Copilot me dio el Dockerfile con la imagen base de Python, la copia de mi `requirements.txt`, la instalación de dependencias y el comando de arranque con uvicorn. Después armó el `docker-compose.yml` con dos servicios: uno llamado `db` (con la imagen oficial de Postgres) y otro llamado `api` (construido desde mi Dockerfile), y me explicó cómo usar un volumen para que los datos de Postgres no se perdieran cada vez que apagara el contenedor.

#### Decisión y cambios realizados

Levanté todo con `docker compose up -d`, verifiqué que la API se conectara correctamente a la base de datos dentro del contenedor, y dejé las credenciales de Postgres como variables de entorno en vez de escribirlas directo en el archivo.

#### Justificación

Tener la API y la base de datos como dos servicios separados, pero conectados entre sí, es justo cómo se ve un proyecto real en producción, y usar variables de entorno para las credenciales evita dejarlas visibles dentro del repositorio.

---

### Entrada 3 — Integración continua con GitHub Actions

#### Objetivo

Que cada commit o Pull Request se revisara automáticamente antes de llegar a la rama `main`, sin que yo tuviera que acordarme de correr las pruebas a mano.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ayúdame a crear el workflow de GitHub Actions en .github/workflows/ci.yml, para que cada vez que suba un cambio, un servidor de GitHub instale Python, instale mis dependencias y corra mis pruebas con pytest.

#### Propuesta de la IA

Copilot me ayudó a definir los pasos del workflow: preparar el sistema, instalar Python, instalar dependencias y ejecutar pytest. La primera versión que armamos tenía errores de indentación en el YAML que hacían que el archivo no se leyera bien.

#### Decisión y cambios realizados

Subí el archivo, revisé los errores que marcaba GitHub Actions, y fui corrigiendo la indentación junto con la IA hasta que el flujo corrió completo y el check quedó en verde.

#### Justificación

Un archivo YAML mal indentado puede parecer un detalle mínimo, pero hace que todo el workflow falle sin ejecutar ni un solo paso; corregirlo era necesario para poder confiar en que cada cambio futuro se revisara solo, sin depender de que yo corriera las pruebas manualmente.

---

### Entrada 4 — Infraestructura como código y despliegue en Render

#### Objetivo

Publicar mi API y mi base de datos en internet, definiendo esa infraestructura en un archivo en vez de configurarla a mano dando clics en Render.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Quiero desplegar mi API junto con una base de datos PostgreSQL en Render, pero usando un archivo render.yaml en vez de configurar todo manualmente. Ayúdame a definir ahí los dos recursos y a conectar la base de datos con mi API.

#### Propuesta de la IA

Copilot me ayudó a escribir el `render.yaml` definiendo dos recursos: una base de datos PostgreSQL administrada por Render y un Web Service para mi API de FastAPI, y me mostró cómo pasar la variable `DATABASE_URL` de la base de datos hacia el servicio de la API para que quedaran conectados.

#### Decisión y cambios realizados

Conecté mi repositorio a Render, dejé que la plataforma leyera el `render.yaml`, y esperé a que construyera ambos servicios. Confirmé que mi API respondiera desde su nueva URL pública en HTTPS.

#### Justificación

Definir la infraestructura en un archivo, significa que toda la configuración de mis servicios queda guardada como parte del proyecto, y no depende de que yo recuerde cómo configuré todo la primera vez.

---

### Entrada 5 — Cuidar los datos sensibles y entender los entornos local vs. producción

#### Objetivo

Proteger las contraseñas y datos sensibles de mi proyecto, y entender bien la diferencia entre mi entorno local y el de producción.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ayúdame a revisar mi .gitignore para asegurarme de que mi archivo .env (donde tengo las contraseñas de mi Postgres local), la carpeta venv y el caché de Python nunca se suban al repositorio. También quiero entender por qué los secretos de producción no deben estar en mi código.

#### Propuesta de la IA

Copilot revisó mi `.gitignore` y confirmó que `.env`, `venv/` y `__pycache__` ya estaban bloqueados, y me explicó que en un entorno real (Site Reliability Engineering) los secretos de producción nunca viven en el código fuente, sino que se inyectan directamente desde la plataforma donde corre la aplicación, en este caso Render.

#### Decisión y cambios realizados

Dejé mi configuración de forma que la app lea las variables de entorno sin importar de dónde vengan: si corre localmente usa mi archivo `.env` con Postgres de Docker, y si corre en Render usa las variables que la plataforma le inyecta.

#### Justificación

Que mi aplicación no tenga que saber si está en mi computadora o en producción, y que la diferencia esté solo en de dónde vienen sus variables de entorno, es la misma idea de inyección de dependencias que ya había usado en la arquitectura de mi código, pero aplicada ahora a la configuración.

---

### Entrada 6 — Corregir seguridad y el pipeline de CI/CD
 
#### Objetivo
 
Resolver dos pendientes que seguían marcados como incompletos: seguridad de la configuración y despliegue continuo, aunque el código ya funcionaba bien.
 
#### Herramienta utilizada
 
`GitHub Copilot`
 
#### Prompt utilizado
 
> Mi revisión automática sigue marcando problemas en seguridad y en el despliegue continuo, aunque mi código funciona. Ayúdame a revisar si mi docker-compose.yml tiene contraseñas escritas directamente, cómo limpiar mi historial de Git si llegué a subir alguna, y por qué mi archivo ci.yml no está funcionando como debería.
 
#### Propuesta de la IA
 
Copilot revisó mi `docker-compose.yml` y confirmó que las credenciales debían moverse a un archivo `.env`; me explicó cómo usar herramientas como BFG Repo-Cleaner o `git filter-repo` para borrar del historial rastros antiguos de mi usuario y contraseña de PostgreSQL (`POSTGRES_USER` y `POSTGRES_PASSWORD`); y detectó que mi `ci.yml` tenía dos bloques de `steps:` dentro del mismo job, lo cual hacía que el segundo bloque no se ejecutara. También propuso agregar, al final del pipeline, un paso de despliegue automático a Render usando el `RENDER_API_KEY` y el `serviceId` de mi servicio, condicionado a que las pruebas pasaran primero.
 
#### Decisión y cambios realizados
 
Uní los dos bloques de `steps` en uno solo (checkout, instalación de Python, dependencias, lint, mypy, pytest), agregué el paso de despliegue condicionado al éxito de las pruebas, y limpié el historial de Git de las credenciales antiguas.
 
#### Justificación
 
No era que el código estuviera mal, sino que un detalle de formato en el archivo YAML impedía que todo el flujo se ejecutara completo, y tener contraseñas visibles en el historial de Git sigue siendo un riesgo aunque ya no estén en el código actual — por eso había que limpiarlas, no solo quitarlas del archivo. Con esto quedaron cubiertos los criterios de Pipeline de CI y Despliegue continuo de la rúbrica de esta semana.



## Semana 5

### Entrada 1 — Un primer intento fallido con Aider

#### Objetivo

Empezar el día usando Aider para avanzar en la lógica de negocio del proyecto.

#### Herramienta utilizada

`Aider`

#### Prompt utilizado

> Intenté configurar Aider en la terminal para empezar a trabajar con él desde ese lunes.

#### Propuesta de la IA

Aider no llegó a responder nada, porque la instalación falló por problemas de dependencias en mi entorno de Python.

#### Decisión y cambios realizados

En vez de perder más tiempo tratando de arreglarlo en ese momento, decidí dejarlo pendiente y abrir mi editor con GitHub Copilot para no perder el día.

#### Justificación

Insistir con una herramienta que no arranca puede consumir horas que se pueden usar en avanzar con otra cosa; preferí empezar a producir algo y regresar a Aider más tarde con la cabeza más fresca.

---

### Entrada 2 — Primer trabajo del día con Copilot: conversiones de unidades

#### Objetivo

Aprovechar que ya tenía a Copilot funcionando para avanzar en algo, aunque no fuera lo más importante del proyecto.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Escribe las funciones para estandarizar las lecturas de los sensores (conversiones de Celsius a Fahrenheit, etc.) y genérame los casos de prueba básicos en test_conversions.py.

#### Propuesta de la IA

Copilot generó las funciones de conversión y un archivo de pruebas básico para ellas.

#### Decisión y cambios realizados

Acepté ese código como un pequeño avance del día, aunque sabía que no era la parte central del proyecto.

#### Justificación

Mientras resolvía el problema con Aider, prefería tener algo de avance real en el repositorio en lugar de quedarme sin hacer nada.

---

### Entrada 3 — Documentación adelantada basada solo en las conversiones

#### Objetivo

Aprovechar ese pequeño avance para empezar a redactar la documentación que pedía la rúbrica (AI Code Review y ADR).

#### Herramienta utilizada

`Chat GPT`

#### Prompt utilizado

> Le pedí al asistente que me generara un borrador de AI Code Review y un ADR, basándonos únicamente en las funciones de conversión que ya tenía.

#### Propuesta de la IA

Me redactó ambos documentos, pero centrados solo en ese código de conversiones.

#### Decisión y cambios realizados

En un inicio los guardé como primer borrador, pensando que ya tenía adelantado algo de la documentación de la semana.

#### Justificación

Quería ir avanzando en varios frentes a la vez, aunque en ese momento no me di cuenta de que estaba documentando algo que no era el núcleo real del proyecto.

---

### Entrada 4 — Corrección de rumbo: comparar con la referencia de mi compañero

#### Objetivo

Revisar si esos primeros borradores de ADR y Code Review realmente cumplían con lo que pedía la rúbrica.

#### Herramienta utilizada

`Chat GPT`

#### Prompt utilizado

> Le pasé al asistente el archivo de AI Code Review de mi compañero y le pedí que lo usáramos como referencia para entender qué tan a fondo debía ir mi propia documentación (hallazgos, evaluación, decisión y TDD).

#### Propuesta de la IA

Al comparar, quedó claro que mis documentos eran muy pobres porque las conversiones de unidades no eran la parte central de la arquitectura del proyecto.

#### Decisión y cambios realizados

Descarté por completo el ADR y el Code Review que había hecho esa mañana, y decidí enfocarme en lo que realmente pedía la semana: el SensorService y la persistencia real de los datos.

#### Justificación

Documentar algo superficial solo por "tener algo" no cumplía con lo que pedía la rúbrica; era mejor frenar a tiempo que entregar documentación que no reflejara el trabajo real del proyecto.

---

### Entrada 5 — Logrando instalar Aider correctamente

#### Objetivo

Resolver el problema de instalación de Aider del inicio del día para poder usarlo en el resto de la semana.

#### Herramienta utilizada

`Chat GPT`

#### Prompt utilizado

> Le pedí ayuda para entender por qué había fallado la instalación de Aider y si había otra forma de instalarlo sin que chocara con las demás dependencias de mi proyecto.

#### Propuesta de la IA

Me explicó una forma distinta de instalarlo, usando un entorno virtual exclusivo solo para Aider, separado del entorno de mi proyecto.

#### Decisión y cambios realizados

Seguí esa recomendación y esta vez la instalación sí funcionó.

#### Justificación

Aislar Aider en su propio entorno evitó que sus dependencias chocaran con las de FastAPI, SQLAlchemy y el resto de librerías que ya tenía instaladas para el proyecto.

---

### Entrada 6 — Primer prompt formal a Aider: modelo de base de datos para conversiones

#### Objetivo

Ya con Aider funcionando y con el enfoque correcto (backend real), empezar a usarlo para crear el modelo de base de datos.

#### Herramienta utilizada

`Aider`

#### Prompt utilizado

> Aider, necesito crear el modelo de base de datos para manejar las conversiones de los sensores utilizando SQLAlchemy 2.0. Crea la tabla correspondiente asegurándote de usar Mapped y definir correctamente las relaciones con la tabla de sensores.

#### Propuesta de la IA

Aider generó el modelo con la sintaxis tipada de SQLAlchemy 2.0 y la relación hacia la tabla de sensores.

#### Decisión y cambios realizados

Acepté el modelo generado como punto de partida para seguir construyendo el resto de los servicios al día siguiente.

#### Justificación

Era el primer resultado real de Aider en el proyecto, y confirmar que respetaba la sintaxis moderna de SQLAlchemy (Mapped) me dio confianza para seguir delegándole tareas más grandes.

---

### Entrada 7 — Entendiendo el patrón Strategy antes de escribir código

#### Objetivo

Comprender bien el patrón Strategy antes de empezar a programar el AnomalyDetector, para aplicar correctamente el principio Abierto/Cerrado de SOLID.

#### Herramienta utilizada

`Chat GPT`

#### Prompt utilizado

> Le pedí al asistente que me explicara cómo funciona el patrón Strategy, y diseñamos juntos la clase abstracta AlertNotificationStrategy y dos clases concretas: SpyAlertStrategy y DatabaseAlertStrategy.

#### Propuesta de la IA

Me explicó el patrón con ejemplos y propuso la estructura de la clase abstracta y las dos implementaciones concretas.

#### Decisión y cambios realizados

Acepté ese diseño como base antes de escribir cualquier código.

#### Justificación

Entender el patrón antes de programarlo evita terminar con una clase abstracta mal pensada que haya que rehacer después; diseñar primero en papel es más barato que corregir código ya escrito.

---

### Entrada 8 — Redactando los 5 tests unitarios de anomalías

#### Objetivo

Tener listos los tests de detección de anomalías antes de pedirle a Aider que implementara el código.

#### Herramienta utilizada

`Chat GPT`

#### Prompt utilizado

> Le pedí al asistente que redactara los 5 tests unitarios para verificar la detección de anomalías, y discutimos cómo el SpyAlertStrategy iba a guardar las alertas en memoria.

#### Propuesta de la IA

Propuso los 5 tests, y sobre cómo validar las alertas guardadas, sugirió acceder al índice `alerts[0]` de la lista donde el Spy las almacena.

#### Decisión y cambios realizados

Acepté esa forma de validación y dejé los 5 tests listos, en fase RED, antes de pedir la implementación.

#### Justificación

Escribir los tests primero (aunque fallaran porque el código todavía no existía) aseguraba que la implementación que hiciera Aider después tuviera que ajustarse a un comportamiento ya definido, y no al revés.

---

### Entrada 9 — Delegando la implementación del patrón Strategy a Aider

#### Objetivo

Escribir el código de `AlertNotificationStrategy`, `SpyAlertStrategy` y `DatabaseAlertStrategy` ya con el diseño y los tests listos.

#### Herramienta utilizada

`Aider`

#### Prompt utilizado

> Aider, actúa como un Arquitecto de Software en Python. Implementa el patrón Strategy que definimos. Crea la clase abstracta AlertNotificationStrategy con el método send_alert. Implementa SpyAlertStrategy y DatabaseAlertStrategy. Asegúrate de añadir type hints estrictos para Mypy.

#### Propuesta de la IA

Aider generó las 3 clases respetando la estructura que ya habíamos diseñado, con los tipos anotados.

#### Decisión y cambios realizados

Corrí los 5 tests que ya tenía listos y confirmé que pasaran con esta implementación antes de aceptarla como definitiva.

#### Justificación

Como los tests ya estaban escritos desde antes, confirmar que pasaran era la forma más directa de saber si Aider había respetado el diseño acordado o se había desviado de él.

---

### Entrada 10 — Refactorizando ReadingService para respetar DIP

#### Objetivo

Corregir un problema que detecté en `ReadingService`, que estaba creando sus propias dependencias en vez de recibirlas desde fuera.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Le pedí ayuda a Copilot para refactorizar ReadingService, explicándole que estaba instanciando internamente sus dependencias (como el repositorio), lo cual rompía el principio de Inversión de Dependencias que ya habíamos aplicado en el resto del proyecto.

#### Propuesta de la IA

Me propuso mover esas dependencias al constructor de la clase, para que se le inyectaran desde afuera en vez de crearlas dentro.

#### Decisión y cambios realizados

Acepté el cambio y actualicé también los lugares donde se creaba `ReadingService`, para pasarle ahora sus dependencias.

#### Justificación

Si el servicio crea sus propias dependencias, no puedo reemplazarlas por versiones falsas en los tests; inyectarlas desde afuera es lo que permite probar el servicio sin depender de una base de datos real.

---

### Entrada 11 — Descubriendo que mis pruebas compartían estado entre sí

#### Objetivo

Entender por qué mis pruebas fallaban al correr solo el archivo `test_anomalies.py`, aunque pasaban si corría toda la suite completa.

#### Herramienta utilizada

`Chat GPT`

#### Prompt utilizado

> Le describí el síntoma al asistente: mis pruebas fallaban al ejecutarse solas pero pasaban si se ejecutaban junto con el resto, y le pregunté por qué podía estar pasando eso con una base de datos SQLite en memoria.

#### Propuesta de la IA

Me explicó que probablemente estaba reutilizando la misma base de datos en memoria entre varias pruebas, y que cada test debería tener su propia base de datos aislada para no depender del orden en que se ejecutaran.

#### Decisión y cambios realizados

Identifiqué que tenía que revisar cómo estaba creando la sesión de base de datos en mis pruebas, para que cada test arrancara con una base limpia en vez de compartir una sola instancia.

#### Justificación

Unas pruebas que solo pasan en cierto orden no son pruebas confiables; si algún día cambio el orden en que corren, podrían empezar a fallar sin que el código realmente esté roto.

---

### Entrada 12 — Agregando paginación al repositorio de lecturas

#### Objetivo

Que la API pudiera devolver las lecturas de un sensor por partes, en vez de todas de golpe.

#### Herramienta utilizada

`Aider`

#### Prompt utilizado

> Aider, modifica el método de consulta en el repositorio de lecturas. Añade soporte para paginación recibiendo limit y offset como enteros. Debe devolver una lista tipada de modelos Reading.

#### Propuesta de la IA

Aider modificó el método del repositorio para aceptar `limit` y `offset`, y devolvió una lista tipada de `Reading`.

#### Decisión y cambios realizados

Acepté el cambio y lo agregué a mi archivo `prompting.md` como uno de los ejemplos de prompt bueno que pedía la rúbrica de esta semana.

#### Justificación

La paginación evita que la API tenga que devolver miles de lecturas de golpe si un sensor lleva mucho tiempo activo, y era justo el tipo de tarea pequeña y concreta que la rúbrica pedía documentar con un prompt bien estructurado.

---

### Entrada 13 — Creando el esquema de salida ReadingResponse con Pydantic

#### Objetivo

Definir cómo se debía ver la respuesta de la API al consultar una lectura, separándola del modelo de base de datos.

#### Herramienta utilizada

`Aider`

#### Prompt utilizado

> Aider, genera un esquema Pydantic de salida llamado ReadingResponse. Debe incluir validación estricta y habilitar from_attributes=True para serializar objetos de SQLAlchemy.

#### Propuesta de la IA

Aider generó el esquema `ReadingResponse` con la configuración `from_attributes=True`, para poder construirlo directamente a partir de un objeto `Reading` de SQLAlchemy.

#### Decisión y cambios realizados

Acepté el esquema y lo usé como el `response_model` de los endpoints de lectura.

#### Justificación

Separar lo que devuelve la API de lo que vive en la base de datos evita exponer campos internos por accidente, y `from_attributes=True` me ahorraba tener que convertir manualmente cada objeto antes de regresarlo.

---

### Entrada 14 — Un dato inventado por Aider en un test HTTP

#### Objetivo

Escribir una prueba de integración que confirmara que la API responde con error 422 cuando se manda una temperatura inválida.

#### Herramienta utilizada

`Aider`

#### Prompt utilizado

> Escribe una prueba con pytest que envíe un POST HTTP al router de lecturas con una temperatura inválida y valide que retorna un error 422.

#### Propuesta de la IA

Aider generó la prueba, pero asumió que existía una variable llamada `client` disponible de forma global, cuando en realidad esa variable no existía así en mi proyecto; al correr la prueba, esto provocaba un `NameError`.

#### Decisión y cambios realizados

Rechacé esa primera versión y le di un prompt más específico: "Aider, corrige el código inyectando client como fixture de pytest en la firma de la función."

#### Justificación

Aceptar el código tal cual habría dejado una prueba que ni siquiera podía ejecutarse; Aider había asumido algo sobre la estructura de mi proyecto que no era cierto, y corregirlo evitó dejar ese error en el pipeline.

---

### Entrada 15 — Redactando el ADR-0001 de verdad

#### Objetivo

Documentar formalmente la arquitectura del proyecto, ahora que el SensorService ya estaba implementado con las dependencias bien inyectadas.

#### Herramienta utilizada

`Chat GPT`

#### Prompt utilizado

> Le pedí al asistente que me ayudara a redactar el ADR-0001 sobre la separación por capas, explicando cómo se comunican routers, services, repositories y models, y por qué usamos Protocol para lograr la Inversión de Dependencias.

#### Propuesta de la IA

Me propuso la estructura del ADR (contexto, decisión, consecuencias) y una redacción explicando por qué separar la lógica de negocio de SQLAlchemy mediante `Protocol` hace que el proyecto sea más fácil de probar y de cambiar en el futuro.

#### Decisión y cambios realizados

Acepté la estructura y ajusté la redacción con ejemplos específicos de mi propio proyecto, en lugar del borrador genérico del lunes.

#### Justificación

Este ADR sí reflejaba una decisión de arquitectura real que ya estaba implementada y podía defender con código, a diferencia del intento del lunes que documentaba algo que no era el núcleo del proyecto.

---

### Entrada 16 — El Code Review real: 9 hallazgos y un rechazo justificado

#### Objetivo

Someter mi archivo `reading_service.py`, ya terminado, a una revisión de código hecha por la IA.

#### Herramienta utilizada

`Chat GPT`

#### Prompt utilizado

> Le pedí al asistente que revisara mi archivo app/services/reading_service.py como si fuera un ingeniero senior en un code review, buscando violaciones de SOLID, casos borde sin manejar, riesgos de seguridad y problemas de rendimiento.

#### Propuesta de la IA

Me devolvió 9 hallazgos distintos, cada uno con una línea señalada y una corrección sugerida. Uno de ellos (CR-03) pedía implementar transacciones atómicas complejas para ciertas operaciones.

#### Decisión y cambios realizados

Rechacé específicamente el hallazgo CR-03.

#### Justificación

Consideré que agregar transacciones atómicas complejas era un sobrediseño para el alcance actual del proyecto; hubiera agregado complejidad sin un beneficio real en esta etapa, así que decidí no implementarlo y dejarlo documentado como un rechazo justificado.

---

### Entrada 17 — Corrigiendo los bugs críticos del Code Review con TDD

#### Objetivo

Corregir los hallazgos del Code Review que sí representaban riesgos reales: valores numéricos inválidos, fechas sin zona horaria, y pérdida de datos en el PATCH.

#### Herramienta utilizada

`Aider`

#### Prompt utilizado

> Aider, basándote en los hallazgos del Code Review, corrige ReadingUpdate. Usa exclude_unset para distinguir entre null y campos omitidos en el PATCH. Luego, en reading_service.py, añade protección explícita contra valores math.isnan y math.isinf en la temperatura. Asegúrate de que todas las fechas utilicen timezone.utc.

#### Propuesta de la IA

Aider modificó `ReadingUpdate` para diferenciar entre un campo que se manda como nulo a propósito y uno que simplemente no se envía, agregó las validaciones contra NaN e infinito, y unificó el uso de fechas con zona horaria UTC en todo el servicio.

#### Decisión y cambios realizados

Antes del cambio, corrí los tests y confirmé que fallaban por estos 3 problemas (fase ROJO); después de que Aider aplicó las correcciones, los volví a correr y pasaron todos (fase VERDE).

#### Justificación

Los 3 hallazgos aceptados eran errores reales que podían corromper datos en producción (un PATCH que borra información sin querer, temperaturas imposibles guardadas como válidas, y fechas mezcladas sin zona horaria); confirmar el fallo antes de la corrección era la única forma de estar seguro de que el arreglo realmente resolvía el problema.

---

### Entrada 18 — Cierre de semana: limpieza de la documentación y validación estricta

#### Objetivo

Dejar la documentación de IA lista para entrega y confirmar que todo el proyecto cumpliera con los estándares de calidad exigidos.

#### Herramienta utilizada

`Chat GPT`

#### Prompt utilizado

> Le pedí ayuda para revisar mi archivo AI_CODE_REVIEW.md y quitar cualquier parte que sonara a que la IA había inventado un hallazgo, dejando claro por escrito qué evaluación humana hubo detrás de cada cambio aceptado o rechazado.

#### Propuesta de la IA

Me ayudó a limpiar la redacción del documento, dejando explícita la decisión tomada en cada hallazgo (aceptado, corregido o rechazado) y el porqué.

#### Decisión y cambios realizados

Además de limpiar el documento, corrí yo mismo los comandos de validación final: `ruff check`, `mypy` y `pytest`.

#### Justificación

`ruff check` no marcó ningún problema, `mypy` no encontró errores de tipos, y `pytest` corrió 69 pruebas con una cobertura del 90.71%, superando el 80% que exigía la rúbrica; confirmar esto con los comandos reales, y no solo confiar en lo que decía la IA, era la única forma de estar seguro de que el proyecto realmente cumplía antes de entregarlo.


### Entrada 19 — Auditoría completa del proyecto con la checklist de 10 puntos
 
#### Objetivo
 
Someter todo el proyecto SensorHub (routers, services, repositories, models, schemas, tests y archivos de configuración) a una auditoría técnica estricta, usando la misma checklist de 10 puntos del peer review, antes de dar por cerrado el trabajo de la semana.
 
#### Herramienta utilizada
 
`GitHub Copilot`
 
#### Prompt utilizado
 
> Actúa como un Ingeniero de Software Principal y Evaluador Técnico de Código muy estricto. Necesito que realices una auditoría completa del código de este espacio de trabajo (proyecto SensorHub) utilizando la "Checklist de revisión por pares de 10 puntos". Por favor, analiza todos los archivos del repositorio (routers, services, repositories, models, schemas, tests y archivos de configuración) y genera un reporte detallado evaluando punto por punto los siguientes criterios:
>
> ### LOS 10 PUNTOS DE REVISIÓN A EVALUAR:
> 1. ¿El PR se entiende y se puede probar sin preguntar?: Revisa si hay instrucciones claras, comandos de ejecución de servidor y payload JSON de prueba.
> 2. La estructura oficial del repositorio se respeta: Revisa que el código esté en 'app/' con 'routers/', 'services/', 'repositories/', 'models/', 'schemas/', 'db.py' y que cada carpeta contenga su '__init__.py'. Las carpetas semanales no deben importarse desde 'app/'.
> 3. Cada capa hace solo lo suyo: Revisa que el router solo atienda HTTP y delegue al servicio; que el servicio contenga la lógica de negocio y que el repositorio sea el único que acceda a SQLAlchemy (los routers o servicios no deben importar o instanciar SQLAlchemy directamente).
> 4. Verbos, rutas y códigos de estado REST: GET /sensors/{id}/readings -> 200, POST /sensors/{id}/readings -> 201, GET /readings/{id} -> 200, PATCH /readings/{id} -> 200, DELETE /readings/{id} -> 204. Cualquier código de estado incorrecto o ruta mal diseñada debe ser señalada.
> 5. Paginación y filtros en lecturas: Revisa que 'GET /sensors/{id}/readings' use 'limit' y 'offset' en la base de datos (no en Python) y filtre por rango de fechas '?from=...&to=...'.
> 6. Pydantic valida entrada y salida con física real: Revisa que los schemas de entrada y salida estén separados (response_model declarado en routers) y que rechace unidades inválidas o valores imposibles en temperatura/humedad.
> 7. Uso de HTTPException y códigos correctos: Los errores del servicio deben traducirse a excepciones HTTP controladas (400, 404, 409, 422) sin fugar trazas SQL ni provocar errores 500.
> 8. Persistencia con SQLAlchemy 2.x: Los modelos deben usar la API tipada 'Mapped[...]' con 'mapped_column(...)'. Revisa que no use código de la versión 1.x (Column, session.query) ni tenga bases de datos (.db) versionadas en git.
> 9. DIP y cierre de sesiones: Revisa que el servicio dependa de un 'Protocol' (Abstracción) y que en 'dependencies.py' (o donde use la sesión) se use 'yield' con 'finally: session.close()' para liberar conexiones de red.
> 10. Suite de pruebas, linters y git: Ejecuta mentalmente o inspecciona los tests. La cobertura debe estimarse en >=80%, sin base de datos real compartida entre tests y sin archivos temporales '__pycache__' versionados.
>
> ### REQUERIMIENTO ESPECIAL DE INTEGRACIÓN DE LA SEMANA 5:
> Adicionalmente, audita si implementó correctamente el patrón Strategy (AlertNotificationStrategy con DatabaseAlertStrategy y SpyAlertStrategy) para las anomalías, si desacopló el servicio de alertas y si sus aserciones en las pruebas usan accesos seguros por índice (ej. 'alerts[0]') para evitar fallas relacionales.
>
> ### FORMATO EXIGIDO PARA TU REPORTE:
> Para cada punto donde encuentres un fallo, una mala práctica o una oportunidad de mejora, indícame: ubicación (nombre del archivo y número de línea aproximado), qué observaste (qué está fallando o rompiendo la arquitectura) y qué propones exactamente en código para solucionarlo. Sé sumamente técnico, estricto y analítico.
 
#### Propuesta de la IA
 
Copilot revisó todo el repositorio punto por punto siguiendo la checklist, y regresó un reporte técnico señalando, para cada hallazgo, el archivo y la línea aproximada, qué estaba fallando y qué proponía en código para corregirlo. Entre los hallazgos más importantes señaló que el constructor de `ReadingService` tenía un valor por defecto que rompía la Inversión de Dependencias, que la suite de pruebas de anomalías no era confiable al correrse de forma aislada, y sugirió agregar un patrón transaccional complejo (Unit of Work) para las alertas.
 
#### Decisión y cambios realizados
 
Usé este reporte como punto de partida para revisar el proyecto a fondo: acepté investigar y corregir el problema del constructor de `ReadingService` y el de las pruebas aisladas, pero rechacé la sugerencia de agregar un patrón Unit of Work, por considerarlo sobrediseño para el alcance actual del proyecto.
 
#### Justificación
 
Pedirle a la IA una auditoría completa con una checklist estricta y un formato exigido (ubicación, qué observó, qué propone) me dio hallazgos mucho más específicos que una revisión superficial, y me permitió decidir con criterio cuáles corregir de inmediato y cuáles rechazar, en vez de aceptar todo el reporte de golpe.

 # Conclusiones de la Ronda 2 de Peer Review: Análisis Comparativo (Humano vs. IA)

## Conclusión 1: El ojo humano como guardián de las reglas de negocio y los contratos nominales
El criterio humano demostró ser insustituible para evaluar el cumplimiento de las directrices nominales del curso y la coherencia del diseño arquitectónico. Mientras que la IA validó el código de alertas como "funcional", el análisis humano detectó de inmediato desviaciones críticas frente a la rúbrica de la Semana 5, tales como el uso de `AlertStrategy` en lugar de `AlertNotificationStrategy`, la total ausencia de la clase `SpyAlertStrategy` (reemplazada erróneamente por mocks automáticos de librería) y el uso del método `send_alert` en lugar de `notify`. Asimismo, el análisis humano identificó problemas de acoplamiento de responsabilidades que la IA pasó por alto, como el hecho de que `DatabaseAlertStrategy` mezclara la persistencia en base de datos con salidas físicas por consola mediante `print`.

## Conclusión 2: La IA como herramienta táctica para la detección de casos borde y validación de tipos
La IA demostró una excelente capacidad analítica para realizar auditorías estáticas profundas y encontrar vulnerabilidades de datos y fallos en casos límite. El análisis asistido identificó de forma inmediata un error físico crítico en la capa de transporte: los esquemas de Pydantic permitían el ingreso de valores flotantes no finitos (`NaN` e infinitos), lo que corrompería la telemetría del sistema al persistirse en la base de datos. De igual forma, la IA fue muy efectiva al señalar la debilidad de los tipos en los protocolos de persistencia (el uso de diccionarios planos sin tipar) y la falta de restricciones en los parámetros de paginación de la API, áreas donde el ojo humano tiende a confiarse.

## Conclusión 3: El peligro de la "falsa seguridad" en la cobertura y la necesidad del enfoque híbrido
Esta comparativa evidenció que una cobertura de código alta (superior al 90% en el proyecto evaluado) puede generar una falsa sensación de robustez si las pruebas están mal aisladas. El análisis humano detectó un fallo crítico de integración que la cobertura ocultaba: las pruebas consumían un archivo de base de datos físico y compartido (`sensorhub.db`) en lugar de levantar instancias independientes en memoria (`sqlite:///:memory:`) para cada test, lo que provocaba contaminación de datos y dependencias en el orden de ejecución. 

El enfoque híbrido demuestra que la IA es un copiloto extraordinario para asegurar la calidad del código a nivel de sintaxis, tipos y casos borde matemáticos, pero el ingeniero humano sigue siendo el único capaz de guiar la arquitectura, asegurar el cumplimiento de las especificaciones del cliente y evitar el sobrediseño.

---

# Semana 6 - Integración final de SensorHub

## Entrada 20 - Planificación contra la guía y control humano de Git

### Objetivo

Convertir los RF y RNF de la semana 6 en una secuencia de trabajo verificable,
sin perder el control humano sobre los cambios.

### Herramienta utilizada

`Codex`

### Prompt utilizado

> Continúa la semana 6 en la rama semana6. Edita y prueba localmente, pero no
> hagas commit ni push hasta que yo revise los cambios.

### Propuesta de la IA

La IA comparó el estado del repositorio con RF-1 a RF-7 y RNF-1 a RNF-6,
propuso trabajar primero las brechas funcionales y después observabilidad,
infraestructura, CI/CD y documentación.

### Decisión y cambios realizados

Acepté la secuencia, pero mantuve bajo mi responsabilidad cada `git add`,
`commit` y `push`. También decidí llevar el backlog oficial en GitHub
Projects y eliminar la copia `SEMANA6_BACKLOG.md` para no mantener dos fuentes
de verdad.

### Justificación

Separar edición, revisión y publicación permitió comprobar cada incremento antes
de incorporarlo al historial. El tablero conserva el estado del trabajo y Git
conserva la evidencia técnica.

## Entrada 21 - Funcionalidad, observabilidad y manejo de fallos

### Objetivo

Cerrar RF-1 a RF-7 y las brechas de robustez sin agregar tracks opcionales.

### Herramienta utilizada

`Codex`

### Prompt utilizado

> Continúa con lo que sigue, explícame qué se modificará y pruébalo localmente.

### Propuesta de la IA

La IA propuso completar validaciones físicas, filtros por fecha, transiciones de
alertas, estadísticas, healthcheck con base de datos, métricas, logs JSON y un
manejador global de errores.

### Decisión y cambios realizados

Acepté cambios pequeños por requisito y revisé sus archivos antes de guardar
cada commit. Se conservaron respuestas compatibles con las pruebas existentes,
se añadió un `X-Request-ID` y se evitó mostrar trazas internas al cliente.

### Justificación

El alcance corresponde a SensorHub competente+ y cubre observabilidad real. La
suite final de esta etapa ejecutó 56 pruebas con 93.99% de cobertura, además de
Ruff y Mypy en verde.

## Entrada 22 - PostgreSQL, Alembic y CI/CD reproducible

### Objetivo

Demostrar que el sistema puede construirse desde cero y desplegar únicamente
después de validar calidad.

### Herramienta utilizada

`Codex`, Docker Desktop y GitHub Actions

### Prompt utilizado

> Trabaja en lo que sigue dentro del proyecto.

### Propuesta de la IA

La IA propuso healthchecks en Compose, espera explícita de PostgreSQL, ejecución
de Alembic al arrancar, usuario de contenedor sin privilegios y un pipeline
separado en calidad, construcción Docker y despliegue.

### Decisión y cambios realizados

Acepté la estrategia y autoricé una prueba temporal aislada con PostgreSQL. La
base de prueba confirmó la revisión `0001_sensorhub_schema` y las tablas
`sensors`, `readings`, `alert` y `alembic_version`. El volumen temporal se
eliminó al terminar. El workflow se validó con actionlint antes del commit.

### Justificación

La prueba real evitó confundir una configuración YAML válida con un sistema
funcional. Separar CI y CD garantiza que Render no reciba un commit que no haya
pasado pruebas y construcción.

## Entrada 23 - Documentación basada en evidencia

### Objetivo

Cumplir RNF-6 y preparar la defensa técnica sin documentar capacidades que aún
no estén verificadas.

### Herramienta utilizada

`Codex`

### Prompt utilizado

> Dale, empieza a trabajarlo.

### Propuesta de la IA

La IA consultó directamente la guía de estudio, revisó el código, los ADR y la
URL pública; después propuso reescribir el README, registrar la decisión de
persistencia/despliegue y crear un guion de demostración.

### Decisión y cambios realizados

Acepté documentar RF/RNF, arquitectura Mermaid, instalación, endpoints,
pruebas, observabilidad y CI/CD. La documentación deja explícito que
`/metrics` debe volver a comprobarse después del merge a `main`, porque la
versión pública anterior todavía respondía 404 en ese endpoint.

### Justificación

Una documentación defendible distingue entre lo probado localmente y lo
desplegado. Esto evita presentar como terminada una función que aún no está en
producción y deja una checklist concreta para el cierre.

## Entrada 24 - Verificación de producción y guion final

### Objetivo

Cerrar la evidencia de Semana 6 después del merge y adaptar la demostración a
un único video técnico de aproximadamente 10 minutos.

### Herramienta utilizada

`Codex`

### Prompt utilizado

> Primero vamos a cerrar el README y vas a darme el guion para el video.

### Propuesta de la IA

La IA propuso comprobar la versión pública antes de declarar terminada la
entrega, corregir el estado desactualizado del README y preparar fuera del
repositorio un guion de video con tiempos, acciones visibles y explicaciones
técnicas.

### Decisión y cambios realizados

Acepté la verificación controlada en producción. Se comprobaron `/health`,
`/metrics` y el flujo completo de RF-1 a RF-7 con un sensor temporal que quedó
desactivado. Después se actualizó el README y se preparó, como material personal
fuera del repositorio, un guion de 9:30 a 10:00 minutos.

### Justificación

La ejecución verde del pipeline demuestra que GitHub aceptó el despliegue,
pero la prueba directa confirma que la nueva versión y PostgreSQL realmente
responden. El guion reúne la demostración funcional y la defensa técnica sin
añadir características que pongan en riesgo la entrega.
