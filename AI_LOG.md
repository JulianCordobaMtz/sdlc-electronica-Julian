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