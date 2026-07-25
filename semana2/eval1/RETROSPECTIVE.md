# Sprint Retrospective - Sprint 1

## ¿Qué salió bien?
* Se concretó la creación de 10 User Stories ambientadas hacia una simulación de una bodega industrial con 10 sensores de temperatura y humedad, haciendo uso de los criterios Gherkin, story points y priorización MoSCow.  
* Se logró implementar el núcleo del sistema eligiendo 3 historias (recepción de lecturas, detección de anomalías y gestión de alertas) siguiendo estrictamente la metodología TDD.
* Se superó la meta mínima del 80% de cobertura, alcanzando un 91% global con las pruebas pasando en verde.
* Se incluyó una inyección de dependencias (umbrales en el detector y estrategias abstractas en las alertas) dejó el código altamente modular y fácil de escalar.

## ¿Qué fallas existieron?
* Hubo fricción al trasladar el Product Backlog al Sprint Planning, ya que inicialmente se confundieron tareas técnicas y acciones como implementar la estrategia de consola o archivo.
* La situación de historias de Usuario incompletas, lo que desfasó la documentación varias veces.
* La falta de manejo de los comandos de git hizo que aveces se confundieran los puntos donde había que pasar de una carpeta a otra, además de los tests.
* El manejo de ramas en Git se volvió confuso al intentar aplicar parches rápidos sobre historias que ya se consideraban terminadas, por lo que en una ocasión se terminó por eliminar una rama para volver a construirla.
* Hubo cierto atraso con respecto a la generación de los commits, ya que no siempre se entendía el proposito de los tests o se encontraban errores en la implementación TDD.

## Acciones concretas para el próximo Sprint
* Alineación estricta de Backlog: Antes de iniciar el desarrollo, el equipo verificará que los nombres de las tarjetas en el tablero coincidan con el Product Backlog, manejando las divisiones técnicas solo como subtareas.
* Flujo de trabajo de Git: Establecer una regla de no hacer arreglos rápidos en ramas terminadas; si hay un error, se creará una rama de refactor o fix debidamente nombrada para mantener el historial limpio.