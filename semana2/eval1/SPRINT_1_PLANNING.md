# Sprint 1 Planning

## Sprint Goal
Establecer el núcleo de procesamiento de datos del sistema de monitoreo IoT, permitiendo la recepción estandarizada de lecturas, la detección precisa de anomalías mediante umbrales configurables y la emisión de alertas por múltiples canales.

## User Stories seleccionadas (5) y su justificación
Se seleccionaron las historias fundamentales que permiten que un dato fluya desde que se lee hasta que detona una alarma, estableciendo la base para la automatización cíclica y la orquestación de múltiples sensores.

### 1. US-01: Registro estructurado de lecturas (SensorReading)
* **Justificación:** Es el objeto de transferencia de datos base. Todo el sistema depende de que los datos de temperatura y humedad viajen de forma inmutable y estandarizada.
* **Tareas (3h):**
  * T1: Configurar entorno de pruebas para la historia (0.5h)
  * T2: Implementar prueba RED y clase `SensorReading` con atributos inmutables (1.5h)
  * T3: Refactorización y validación de cobertura (0.5h)

### 2. US-02: Detección paramétrica de anomalías (AnomalyDetector)
* **Justificación:** Es el motor de reglas del negocio. Necesitamos evaluar si los datos de `SensorReading` superan los límites permitidos.
* **Tareas (3h):**
  * T1: Diseñar pruebas (RED) para inyección de umbrales (1h)
  * T2: Implementar validación de temperatura `T > 35` (1h)
  * T3: Implementar validación de humedad `H > 80%` (1h)

### 3. US-03: Enrutamiento de alertas multicanal (AlertManager)
* **Justificación:** Prepara el terreno para el patrón Strategy, permitiendo que el sistema decida cómo notificar (consola o archivo) sin acoplarse a un solo método.
* **Tareas (3.5h):**
  * T1: Crear interfaz/clase base abstracta con método de envío (1h)
  * T2: Implementar `ConsoleStrategy` y su prueba RED/GREEN (1h)
  * T3: Implementar `FileStrategy` para registro en disco y pruebas asociadas (1.5h)

### 4. US-04: Temporizador de muestreo cíclico
* **Justificación:** Esencial para que el sistema opere de forma continua y autónoma, alimentando el núcleo de procesamiento sin intervención humana cada 30 segundos.
* **Tareas (3h):**
  * T1: Configurar mock de reloj de sistema (1h)
  * T2: Implementar ciclo de recolección de 30s con tolerancia (1h)
  * T3: Agregar validación para evitar solapamientos de lecturas (1h)

### 5. US-05: Orquestación del arreglo de 10 sensores
* **Justificación:** Conecta el núcleo de procesamiento de un sensor individual a una red completa de monitoreo, cubriendo toda la extensión física de la bodega.
* **Tareas (3h):**
  * T1: Crear clase orquestadora y lista de IDs de sensores (1h)
  * T2: Implementar iterador de consultas a sensores (1h)
  * T3: Manejo de errores por timeout de sensores (1h)

## Definition of Done (DoD)
*Los criterios de aceptación de este Sprint están definidos en el archivo `DEFINITION_OF_DONE.md` ubicado en la raíz de la carpeta semana2.*