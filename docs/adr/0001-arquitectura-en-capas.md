# ADR 0001: Arquitectura en Capas y Desacoplamiento de Persistencia mediante Protocolos (DIP)

* Estado: Aceptado
* Fecha: 2026-08-14
* Contexto: SensorHub API (EDSIA)

## Contexto y Problema

En las primeras fases de desarrollo de la API SensorHub, el código de los endpoints (routers) tendía a acoplarse directamente con la lógica de negocio y con las consultas específicas de la base de datos (SQLAlchemy). Este acoplamiento (código espagueti) presenta tres problemas críticos de escalabilidad y mantenimiento:

1. Falta de modularidad: Cualquier cambio en la estructura de la base de datos obliga a modificar la capa de routers HTTP.
2. Imposibilidad de pruebas aisladas: No se puede probar la lógica de negocio en un entorno de integración continua (CI) rápido sin levantar una base de datos real (SQLite o PostgreSQL), lo que añade latencia y riesgo de contaminación de estado entre pruebas.
3. Violación del Principio de Inversión de Dependencias (DIP): Las capas de alto nivel (lógica de negocio) dependen directamente de implementaciones de bajo nivel (capa de datos/SQLAlchemy).

En la electrónica y sistemas embebidos, este problema equivale a acoplar la lógica de un algoritmo de control directamente con las lecturas de los registros de un sensor físico específico (por ejemplo, leer directamente por I2C dentro del bucle principal). Si el hardware cambia o el sensor se descontinúa, todo el firmware se rompe. En software, el equivalente es acoplar la lógica web a la persistencia SQL.

## Decisión

Para resolver estos problemas, hemos implementado una arquitectura limpia basada en separación de responsabilidades y desacoplamiento de interfaces, aplicando los siguientes mecanismos técnicos:

1. Separación Estricta de 4 Capas:
   * Presentación (Routers): Recibe las solicitudes HTTP, valida el contrato de entrada con Pydantic y delega todo el procesamiento al servicio.
   * Lógica de Negocio (Services): Contiene las reglas operativas independientes de la plataforma (como las validaciones de negocio, soft delete y límites físicos).
   * Acceso a Datos (Repositories): Encapsula todas las operaciones de persistencia mediante SQLAlchemy.
   * Modelos (Models): Define el esquema de la base de datos relacional.

2. Inversión de Dependencias por Protocolos (DIP):
   * El servicio SensorService ya no depende de la clase concreta SQLAlchemySensorRepository.
   * En su lugar, definimos una interfaz estructural mediante typing.Protocol llamada SensorRepositoryProtocol en la capa de servicios.
   * El repositorio se inyecta en el constructor del servicio (__init__), asegurando que el servicio solo conozca el contrato de métodos y no la tecnología de base de datos subyecente.

3. Independencia de Esquemas HTTP en Datos:
   * El repositorio de base de datos es agnóstico a la capa web. No utiliza esquemas de validación de FastAPI o Pydantic (como SensorUpdate).
   * El método update del repositorio recibe diccionarios crudos de Python (dict[str, Any]), aislando la persistencia de los contratos de serialización HTTP.

## Alternativas consideradas

### Alternativa A: Mantener un diseño monolítico sin capas (Acoplamiento Directo)
Esta alternativa conserva un único archivo o módulo donde los routers ejecutan consultas SQL directamente usando sesiones de SQLAlchemy de forma local.

* Por qué se descartó: Aunque reduce el número de archivos iniciales, introduce una severa rigidez. Hace que las pruebas automatizadas dependan obligatoriamente de una base de datos física activa, violando el Principio de Responsabilidad Única (SRP) y bloqueando el pipeline de CI ante fallos de infraestructura. Además, dificulta la comprensión del flujo de datos por parte de otros desarrolladores.

### Alternativa B: Implementar interfaces basadas en Clases Abstractas (abc.ABC)
Esta alternativa consiste en definir una clase abstracta base para el repositorio, de la cual deba heredar formalmente el repositorio real de base de datos.

* Por qué se descartó: El uso de abc.ABC impone un tipado nominal estricto. Esto obliga a que cualquier repositorio falso (Fake) o real tenga que heredar explícitamente de la clase base abstracta de Python, incrementando el acoplamiento jerárquico. Se prefirió typing.Protocol debido a que implementa "duck typing" estático (tipado estructural), permitiendo que cualquier clase que cumpla con las firmas requeridas sea aceptada automáticamente por Mypy, facilitando la creación de mocks y fakes ligeros sin herencia rígida.

## Consecuencias

### Positivas
* Testabilidad en Aislamiento: Es posible simular el comportamiento del repositorio de datos en microsegundos usando fakes en memoria (como FakeSensorRepository), permitiendo probar el 100% de la lógica de negocio en el pipeline de GitHub Actions de forma rápida y sin efectos secundarios.
* Bajo Acoplamiento: Podemos migrar el motor de base de datos de SQLite a PostgreSQL (o incluso cambiar de ORM) modificando únicamente la implementación del repositorio, sin alterar una sola línea de lógica de negocio o de routers.
* Alta Cohesión: Cada archivo tiene una responsabilidad única y delimitada. El router solo responde HTTP, el servicio solo valida reglas físicas y el repositorio solo ejecuta comandos SQL.
* Facilidad de Mantenimiento: Las fallas se aíslan rápidamente. Si un test unitario de negocio falla, el error está garantizado en la lógica del servicio y no en la conexión de base de datos.

### Negativas
* Incremento de Archivos: Requiere crear más clases y definir protocolos de comunicación intermedios, aumentando la cantidad de boilerplate inicial del código base.
* Mantenimiento de Contratos: Cualquier cambio en la firma del repositorio real (como añadir parámetros o cambiar tipos de datos) requiere actualizar el protocolo para evitar que el analizador estático (Mypy) falle.

## Condiciones que podrían justificar revisar esta decisión

Esta decisión de diseño deberá reconsiderarse si aparece evidencia de una o más de las siguientes condiciones:
* Migración a Tecnologías No Relacionales: Si el sistema cambia su motor de persistencia a una base de datos No SQL (como MongoDB o Redis) que requiera patrones de acceso a datos completamente incompatibles con las firmas de métodos síncronos declaradas en nuestros protocolos.
* Cuellos de Botella de Rendimiento Críticos: Si la serialización y el paso de datos entre las capas de servicio y repositorio introduce latencias inaceptables bajo pruebas de carga masiva, justificando la omisión de capas intermedias para lecturas de solo lectura de alto rendimiento (CQRS).
* Requerimientos de Microservicios: Si el dominio del sistema SensorHub madura lo suficiente como para exigir que la gestión de sensores y la ingesta de telemetría se dividan en servicios independientes con bases de datos físicamente separadas.

## Resultado

Se implementa y valida de forma exitosa el desacoplamiento en capas de SensorService utilizando el protocolo SensorRepositoryProtocol. Las pruebas unitarias demostraron un aislamiento completo de la base de datos física, logrando ejecutarse de manera instantánea en el entorno de desarrollo y en el pipeline de GitHub Actions. El analizador Mypy certifica que las dependencias de tipos se respetan estrictamente de arriba hacia abajo sin fugas de abstracción.

## Referencias

* Robert C. Martin, Clean Architecture: A Craftsman's Guide to Software Structure and Design.
* Martin Fowler, Refactoring: Improving the Design of Existing Code.
* Python PEP 544 – Protocols: Structural subtyping (static duck typing).