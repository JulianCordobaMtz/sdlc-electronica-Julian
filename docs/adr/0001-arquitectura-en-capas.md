# 0001. Arquitectura en Capas Desacopladas con Inversión de Dependencias (DIP)

* **Fecha:** 2026-08-13
* **Estado:** Aceptado
* **Contexto:**
  El sistema SensorHub está diseñado para procesar telemetría proveniente de múltiples dispositivos IoT. Si acoplamos la capa de presentación (FastAPI), la lógica de negocio (detección de anomalías) y el motor de persistencia física (SQLAlchemy / SQLite) en un solo script, el sistema se vuelve costoso de mantener, imposible de escalar e inviable para realizar pruebas de integración y unitarias eficientes. 
  
  Además, al venir de un paradigma de desarrollo de bajo nivel (C / firmware), la tentación inicial es mantener buffers globales y funciones aisladas, lo cual rompe los principios de diseño orientado a objetos y la extensibilidad exigida en el software de servidor.

* **Decisión:**
  Adoptamos de forma estricta una **Arquitectura en Capas (4 Capas)** apoyada en el Principio de Inversión de Dependencias (DIP):
  
  1. **Capa de Presentación (Routers):** Exclusivamente responsable de gestionar las peticiones y respuestas HTTP utilizando FastAPI. No ejecuta validaciones físicas ni lógica de persistencia. Su única dependencia es la abstracción del servicio.
  2. **Capa de Lógica de Negocio (Services):** Concentra todas las reglas operativas de SensorHub (como la evaluación de alertas). Es agnóstica de los endpoints HTTP y se comunica con la capa de datos mediante abstracciones (Interfaces / Protocols).
  3. **Capa de Acceso a Datos (Repositories):** Encapsula el acceso físico al motor de persistencia mediante consultas SQL. El servicio no sabe si los datos se guardan en un archivo, en memoria o en una base PostgreSQL remota.
  4. **Capa de Dominio (Models y Schemas):** Define la estructura de datos ORM con SQLAlchemy 2.0 y el contrato de entrada/salida de datos web mediante esquemas Pydantic.

  La Inyección de Dependencias se implementa a nivel de código de Python usando clases abstractas y protocols, y se orquesta dinámicamente en los controladores web mediante el sistema `Depends` de FastAPI.

* **Consecuencias:**
  * **Pros (Ventajas):**
    * **Testabilidad Absoluta:** Al inyectar las dependencias, podemos aislar el Service y probarlo al 100% usando un repositorio falso en memoria (`InMemoryRepository`), sin requerir conectividad de base de datos para correr nuestras pruebas en GitHub Actions.
    * **Independencia Tecnológica:** Podemos migrar la base de datos local de desarrollo (SQLite) hacia producción (PostgreSQL en Docker / Render) sin alterar una sola línea de código de los Routers ni de la Lógica de Negocio.
    * **Cohesión y Bajo Acoplamiento:** Cada archivo tiene una única responsabilidad clara (SRP), facilitando las revisiones de código y el trabajo colaborativo.
  * **Contras (Desventajas):**
    * **Mayor cantidad de archivos iniciales (Boilerplate):** Requiere crear más carpetas y archivos desde el inicio (`routers`, `services`, `repositories`, `models`, `schemas`) que un script de API monolítico simple.