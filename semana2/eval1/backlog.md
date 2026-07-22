# Product Backlog - Sistema de Monitoreo IoT para Bodega Industrial

## US-01: Registro estructurado de lecturas (SensorReading)
Como operador de una bodega,
quiero que el sistema registre de forma estructurada la temperatura y humedad junto con su identificador y marca de tiempo,
para garantizar que los datos de los sensores sean registrables.

* **Prioridad:** Must Have
* **Estimación:** 2 puntos

**Scenario: Creación de una lectura válida**
* **Given** un sensor válido con ID "BODEGA-01"
* **When** el sensor emite una lectura de 25.0 °C y 50.0% de humedad
* **Then** el sistema crea un objeto que no se pueda modificar con esos valores
* **And** la lectura incluye el timestamp exacto de recepción

**Scenario: Rechazo de lecturas con formato corrupto**
* **Given** el sistema procesando datos de entrada
* **When** se recibe una lectura con valores nulos o vacíos
* **Then** el sistema lanza un error de validación
* **And** la lectura se descarta

---

## US-02: Detección paramétrica de anomalías (AnomalyDetector)
Como gerente de la bodega,
quiero que el sistema revise las lecturas contra umbrales configurables,
para detectar automáticamente condiciones que pongan en riesgo el inventario.

* **Prioridad:** Must Have
* **Estimación:** 5 puntos
* **Lógica de detección:** Se marca como "Anomalía" si CUALQUIERA de los parámetros excede su umbral (OR lógico)

**Scenario: Detección por temperatura fuera de umbral**
* **Given** un detector configurado con umbrales de T=35.0 y H=80.0
* **When** ingresa una lectura de 36.5 °C y 60.0% de humedad
* **Then** el sistema marca la lectura como "Anomalía"
* **And** retorna un valor a los emisores de alerta

**Scenario: Detección por humedad fuera de umbral**
* **Given** un detector configurado con umbrales de T=35.0 y H=80.0
* **When** ingresa una lectura de 28.0 °C y 85.0% de humedad
* **Then** el sistema marca la lectura como "Anomalía"
* **And** retorna un valor a los emisores de alerta

**Scenario: Ambos parámetros fuera de umbral**
* **Given** un detector configurado con umbrales de T=35.0 y H=80.0
* **When** ingresa una lectura de 38.5 °C y 82.0% de humedad
* **Then** el sistema marca la lectura como "Anomalía"
* **And** genera exactamente UNA alerta (no duplicada)

**Scenario: Lectura dentro de parámetros normales**
* **Given** el mismo detector con umbrales T=35.0 y H=80.0
* **When** ingresa una lectura de 28.0 °C y 70.0% de humedad
* **Then** el sistema la clasifica como "Normal"
* **And** no se dispara ninguna bandera de anomalía

---

## US-03: Enrutamiento de alertas multicanal (AlertManager)
Como supervisor de turno,
quiero que las anomalías detectadas se envíen a la consola o a un archivo de registro según la configuración,
para tener tanto la alerta visual como un almacenamiento del suceso.

* **Prioridad:** Must Have
* **Estimación:** 5 puntos

**Scenario: Notificación de alerta por consola**
* **Given** el gestor de alertas instanciado con la estrategia "Console"
* **When** recibe un evento de anomalía de temperatura
* **Then** el mensaje de alerta se imprime en la salida estándar 

**Scenario: Registro de alerta en archivo de texto**
* **Given** el gestor de alertas instanciado con la estrategia "File"
* **When** recibe un evento de anomalía de humedad
* **Then** el mensaje se escribe al final del archivo "alertas.log"
* **And** el archivo se cierra de forma segura

**Scenario: Fallo en escritura a archivo**
* **Given** el gestor de alertas con estrategia "File" apuntando a una carpeta sin permisos de escritura
* **When** recibe un evento de anomalía
* **Then** captura la excepción de permiso denegado
* **And** registra el error en el logger del sistema
* **And** no causa que el programa se bloquee

---

## US-04: Temporizador de muestreo cíclico
Como operador de planta,
quiero que el sistema dispare la recolección de datos cada 30 segundos ±100ms,
para mantener un monitoreo constante sin saturar el procesador ni el almacenamiento.

* **Prioridad:** Must Have
* **Estimación:** 3 puntos
* **Tolerancia temporal:** ±100ms (29.9s a 30.1s es aceptable)

**Scenario: Ejecución del ciclo de lectura dentro de tolerancia**
* **Given** el reloj interno del sistema funcionando
* **When** transcurren entre 29.9 y 30.1 segundos desde el último muestreo
* **Then** se activa un evento para leer los sensores
* **And** se reinicia el temporizador

**Scenario: Prevención de lecturas superpuestas**
* **Given** un ciclo de lectura en progreso (tomando más de 5 segundos)
* **When** el temporizador marca los 30 segundos nuevamente
* **Then** el sistema no inicia uno nuevo hasta que el actual termine
* **And** el siguiente ciclo se dispara dentro de 100ms tras completar el anterior

---

## US-05: Orquestación del arreglo de 10 sensores
Como administrador de la red,
quiero que el sistema central consulte de manera secuencial o concurrente a 10 nodos de sensores distintos,
para cubrir todas las zonas físicas de la bodega industrial.

* **Prioridad:** Must Have
* **Estimación:** 3 puntos

**Scenario: Muestreo completo de la red**
* **Given** una lista registrada de 10 IDs de sensores activos
* **When** inicia el ciclo de lectura de 30 segundos
* **Then** el sistema recolecta exactamente 10 lecturas independientes
* **And** las pasa al detector de anomalías

**Scenario: Sensor fuera de línea (Timeout)**
* **Given** el ciclo de lectura en progreso
* **When** el sensor "BODEGA-05" no responde dentro de la red IoT
* **Then** el sistema registra un error de lectura para ese ID
* **And** continúa consultando al resto de los sensores sin detenerse

---

## US-06: Simulación de datos para verificación de alarmas
Como desarrollador de pruebas,
quiero que un simulador genere lecturas de temperatura y humedad siguiendo una distribución normal (Gauss),
para poder validar el sistema con datos realistas en lugar de números estáticos.

* **Prioridad:** Should Have
* **Estimación:** 8 puntos
* **Distribución esperada:** Normal μ=25°C, σ=2°C; Normal μ=60%, σ=5%

**Scenario: Generación de datos dentro de ±1 desviación estándar**
* **Given** el simulador configurado con media=25 °C, desv.est.=2 °C para temperatura
* **When** se generan 1000 lecturas
* **Then** el 68% ± 2% cae entre 23 °C y 27 °C (±1σ)
* **And** el promedio muestral está entre 24.8 y 25.2 °C

**Scenario: Generación de picos anómalos (colas de distribución)**
* **Given** el simulador operando con media=25 °C, desv.est.=2 °C
* **When** se generan 1000 lecturas
* **Then** menos del 3% supera 31 °C (≥3σ)
* **And** menos del 3% es inferior a 19 °C (≤-3σ)

---

## US-07: Verificación de integración a largo plazo
Como supervisor del sistema de monitoreo,
quiero ejecutar una prueba simulando 10 sensores durante 60 ciclos ininterrumpidos,
para garantizar que el sistema es estable y levanta las alertas correctamente con el tiempo.

* **Prioridad:** Should Have
* **Estimación:** 5 puntos

**Scenario: Ejecución exitosa de los 60 ciclos**
* **Given** el entorno de pruebas configurado
* **When** se lanza el script de integración de 10 sensores por 60 lecturas
* **Then** el sistema procesa 600 lecturas en total
* **And** el validador final confirma que todas las alertas esperadas fueron generadas

**Scenario: Fallo por pérdida de datos**
* **Given** la prueba de 60 ciclos en ejecución
* **When** el sistema omite registrar más del 1% de las lecturas esperadas
* **Then** la prueba de integración falla explícitamente

---

## US-09: Persistencia histórica completa en Base de Datos
Como analista de datos,
quiero que todas las lecturas se guarden en una base de datos local,
para poder generar reportes mensuales del clima de la bodega.

* **Prioridad:** Won't Have
* **Estimación:** 8 puntos

**Scenario: Guardado de historial completo**
* **Given** la conexión a SQLite establecida
* **When** llega cualquier tipo de lectura
* **Then** se ejecuta un INSERT en la tabla de historial
* **And** la base de datos se mantiene optimizada