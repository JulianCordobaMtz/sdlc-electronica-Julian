# Sprint 1 Planning

## Sprint Goal
Establecer el núcleo de procesamiento de datos del sistema de monitoreo IoT, permitiendo la recepción estandarizada de lecturas, la detección precisa de anomalías mediante umbrales configurables y la emisión de alertas por múltiples canales.

## User Stories seleccionadas (5) y su justificación
Se seleccionaron las historias fundamentales que permiten que un dato fluya desde que se lee hasta que detona una alarma. Sin este núcleo, no se puede construir el simulador ni la interfaz.

### 1. US-01: Estructura de Lectura de Sensor (SensorReading)
* **Justificación:** Es el objeto de transferencia de datos base. Todo el sistema depende de que los datos de temperatura y humedad viajen de forma inmutable y estandarizada.
* **Tareas (≤ 4h):**
  * T1: Configurar entorno de pruebas para la historia (0.5h)
  * T2: Implementar prueba RED y clase `SensorReading` con atributos inmutables (1.5h)
  * T3: Refactorización y validación de cobertura (0.5h)

### 2. US-02: Detector de Anomalías (AnomalyDetector)
* **Justificación:** Es el motor de reglas del negocio. Necesitamos evaluar si los datos de `SensorReading` superan los límites permitidos.
* **Tareas (≤ 4h):**
  * T1: Diseñar pruebas (RED) para inyección de umbrales (1h)
  * T2: Implementar validación de temperatura `T > 35` (1h)
  * T3: Implementar validación de humedad `H > 80%` (1h)

### 3. US-03: Gestor de Alertas Abstracto (AlertManager)
* **Justificación:** Prepara el terreno para el patrón Strategy, permitiendo que el sistema decida cómo notificar sin acoplarse a un solo método.
* **Tareas (≤ 4h):**
  * T1: Crear interfaz/clase base abstracta con método de envío (1.5h)
  * T2: Implementar tests para asegurar que la abstracción funciona (1h)

### 4. US-04: Estrategia de Alerta por Consola
* **Justificación:** Es el mecanismo más rápido de retroalimentación visual para el operario en el cuarto de control.
* **Tareas (≤ 4h):**
  * T1: Escribir test (RED) para salida estándar (1h)
  * T2: Implementar `ConsoleStrategy` heredando del Gestor (1h)

### 5. US-05: Estrategia de Alerta por Archivo
* **Justificación:** Permite mantener un registro auditable (log) de las anomalías para revisiones futuras de calidad.
* **Tareas (≤ 4h):**
  * T1: Escribir test (RED) simulando escritura de archivo (1.5h)
  * T2: Implementar `FileStrategy` para escritura en disco (1.5h)

## Definition of Done (DoD)
*Los criterios de aceptación de este Sprint están definidos en el archivo `DEFINITION_OF_DONE.md` ubicado en la raíz de la carpeta semana2.*