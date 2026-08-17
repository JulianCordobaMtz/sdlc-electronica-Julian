# Reporte de Auditoría de Código con IA - Semana 5
**Estudiante:** José Julián Córdoba Martínez
**Proyecto:** SensorHub API (EDSIA)
**Módulo auditado:** app/services/sensor_service.py (Lógica de negocio, administración de dispositivos y gestión de alertas)

Este documento detalla la revisión crítica asistida por Inteligencia Artificial realizada sobre nuestro servicio de gestión de sensores. A través de esta auditoría, evaluamos el código generado, identificamos vacíos lógicos de robustez y seguridad, y analizamos las decisiones de diseño mediante un proceso de ingeniería reflexivo, estableciendo justificaciones técnicas para cada una de las propuestas aceptadas y rechazadas.

## Primera Revisión con IA: Tabla de Hallazgos y Decisiones
A continuación se presenta la evaluación detallada de las propuestas de mejora sugeridas por la IA para nuestro servicio de sensores:

| ID | Hallazgo | Evaluación | Decisión |
|---|---|---|---|
| SR-01 | Dependencia directa del repositorio concreto en lugar de una abstracción | El servicio dependía directamente de la implementación específica de base de datos SQL. Si en el futuro cambiamos SQLite por otro motor o queremos probar el servicio en aislamiento, se complica el diseño por un acoplamiento rígido. | ACEPTADO |
| SR-02 | Falta de validación en la creación del identificador del sensor | El método create_sensor no validaba si el sensor_id provisto era nulo, vacío o con tipos incorrectos, lo que arriesgaba fallas de consistencia o errores inesperados de base de datos. | ACEPTADO |
| SR-03 | Comparación de existencia débil sin check de identidad explícito | El condicional para verificar si un sensor ya existía no utilizaba una validación estricta de identidad (is not None), lo que podría generar comportamientos ambiguos ante retornos no booleanos. | ACEPTADO |
| SR-04 | No se validaban valores no finitos (NaN/Infinity) en el umbral de alerta | El valor de alert_threshold se insertaba directamente a la base de datos sin verificar si era un número real válido, lo que permitiría propagar datos corruptos de punto flotante en el sistema. | ACEPTADO |
| SR-05 | Ausencia de validaciones para prevenir la mutación de campos inmutables en PATCH | En el método update_sensor, no se controlaba que el cliente pudiera intentar enviar o alterar campos protegidos como el identificador del sensor (sensor_id). | ACEPTADO |
| SR-06 | Borrado físico en lugar de borrado lógico (Soft Delete) | El método delete_sensor eliminaba físicamente el registro de la base de datos, lo que dejaría huérfanas las lecturas de telemetría históricas o rompería de golpe la integridad referencial. | ACEPTADO |
| SR-07 | Exposición directa de entidades ORM en los métodos de salida | El servicio retornaba directamente los modelos de SQLAlchemy en lugar de mapearlos a esquemas Pydantic, incrementando el acoplamiento y arriesgando errores de sesión fuera de la transacción. | ACEPTADO |
| SR-08 | Captura y manejo de excepciones de base de datos en cada método | La IA propuso envolver cada método en bloques try/except individuales para atrapar fallas de constraints y timeouts directamente dentro del servicio. | RECHAZADO |

## Justificación de Decisiones de Diseño

### Decisiones Aceptadas (Soft Delete, DIP y Robustez de Datos)

**Inversión de Dependencias (DIP) mediante Protocolos (SR-01):**
Justificación: Al definir un SensorRepositoryProtocol utilizando la clase Protocol de Python, desacoplamos por completo la lógica de negocio de la tecnología de almacenamiento. Esto nos permite inyectar fakes en memoria durante las pruebas unitarias, acelerando la ejecución de la suite de pruebas y permitiendo probar el servicio sin necesidad de levantar una base de datos real.

**Validación de Entrada y Blindaje ante NaN/Infinity (SR-02, SR-04 y SR-05):**
Justificación: En aplicaciones industriales de telemetría, el backend de la API debe comportarse de forma defensiva. Validar que el identificador del sensor sea un texto válido no vacío y utilizar math.isfinite para asegurar que el umbral de alerta sea un valor numérico real es indispensable. Esto previene estados corruptos donde un sensor con umbral NaN deshabilite silenciosamente todas las alertas del sistema.

**Borrado Lógico o Soft Delete (SR-06):**
Justificación: Eliminar físicamente un dispositivo de la base de datos en un entorno productivo es una mala práctica de Site Reliability Engineering (SRE). Implementar una bandera is_active = False nos permite marcar el sensor como inactivo para nuevas lecturas, manteniendo intacto el registro histórico de telemetría asociado y salvaguardando la integridad referencial.

**Uso de Esquemas Pydantic de Salida (SR-07):**
Justificación: Separar las clases del modelo de datos de base de datos (SQLAlchemy) de los contratos de entrada y salida (Pydantic) evita fugas de información interna y previene errores de tipo DetachedInstanceError cuando FastAPI serializa la respuesta fuera del contexto de la transacción de base de datos.

### Decisión Rechazada (Control de Excepciones en Capa de Servicio - SR-08)
Justificación: Rechazamos envolver cada consulta de base de datos en bloques try/except locales dentro del servicio. Hacer esto violaría el Principio de Responsabilidad Única (SRP) al saturar la capa de negocio con control de excepciones específico del almacenamiento. La decisión óptima de arquitectura es permitir que las excepciones graves de persistencia se propaguen hacia arriba, donde un middleware global o un manejador de excepciones centralizado de FastAPI en la capa de routers se encarga de traducirlas a respuestas HTTP adecuadas (como un código 400 o 409). Esto mantiene el código de nuestro servicio limpio y legible.

## Segunda Revisión: Casos Borde para Pruebas
Para garantizar la inmunidad de nuestro servicio de sensores frente a datos corruptos y fallas lógicas, seleccionamos 5 escenarios críticos que debían ser cubiertos mediante pruebas de robustez automatizadas:
* Rechazar identificadores de sensores que sean cadenas vacías o nulos explícitos.
* Bloquear la creación de sensores con umbrales de alerta (alert_threshold) que contengan valores matemáticamente inválidos como NaN o Infinity.
* Validar que la operación de borrado cambie el estado de actividad del sensor a falso (is_active = False) pero conserve el registro en la base de datos para no romper la integridad histórica de los datos.
* Garantizar que en las actualizaciones parciales (PATCH) se bloquee cualquier intento de modificar campos protegidos o inmutables.
* Certificar que el servicio pueda ser probado en total aislamiento del motor de base de datos SQL inyectando un repositorio fake en memoria compatible con el protocolo diseñado.

## Evidencia RED
Antes de implementar los cambios en nuestro servicio sensor_service.py, agregamos las nuevas aserciones correspondientes en nuestra suite de pruebas para documentar el comportamiento defectuoso inicial. Al ejecutar el comando de pruebas en la terminal de VS Code:

```bash
python -m pytest tests/test_sensor_service.py -q
```

Obtuvimos los siguientes resultados de falla:
`5 failed, 12 passed`

Los cinco fallos reportados revelaron las siguientes vulnerabilidades reales de producción:
* **test_create_sensor_invalid_id_rejected:** El servicio creó el sensor con un ID vacío en lugar de lanzar la excepción ValueError.
* **test_create_sensor_nan_threshold_rejected:** El servicio persistió el umbral de alerta NaN de forma exitosa sin aplicar filtros.
* **test_sensor_soft_delete_preserves_historical_data:** El método delete_sensor realizó una operación de borrado físico directo (session.delete), removiendo el registro por completo de la base de datos.
* **test_update_sensor_blocks_immutable_fields:** La actualización parcial permitió alterar de forma no autorizada el campo del identificador único del sensor.
* **test_sensor_service_dip_isolation_without_db:** La prueba arrojó un error de inicialización debido a que el servicio requería una instancia directa de SQLAlchemySensorRepository y no aceptaba implementaciones mockeadas.

## Correcciones Implementadas
Para transicionar todas nuestras pruebas a verde, modificamos la implementación de nuestro servicio aplicando cambios mínimos, limpios y estrictamente necesarios:
* **Implementación de validaciones físicas de entrada:** En el método create_sensor, añadimos un check temprano que valida que sensor_id sea un string no vacío y aplicamos math.isfinite() sobre el umbral de alerta.
* **Refactorización a Soft Delete:** Modificamos el método de borrado en el servicio para que, en lugar de solicitar la eliminación física al repositorio, actualice la propiedad is_active = False y guarde el cambio, asegurando la permanencia del registro histórico.
* **Bloqueo de campos protegidos en actualización:** Filtramos el diccionario de datos de actualización en update_sensor para ignorar y descartar explícitamente cualquier llave relacionada con el identificador del sensor antes de invocar la persistencia.
* **Desacoplamiento mediante interfaces:** Modificamos la firma de inicialización de nuestro SensorService para aceptar cualquier objeto que implemente el protocolo SensorRepositoryProtocol en lugar de una clase concreta.

## Evidencia GREEN
Después de realizar las correcciones en el servicio, ejecutamos nuevamente nuestra suite de pruebas para certificar la estabilidad y resolución de los fallos de robustez detectados:

```bash
python -m pytest tests/test_sensor_service.py -q
```

Obtuvimos un resultado impecable en verde:
`5 passed`

Esto confirma que las 5 pruebas de auditoría pasaron exitosamente del estado RED al estado GREEN, blindando el servicio de gestión de sensores contra fallas lógicas y corrupción de telemetría en base de datos.

## Validación Estática de Calidad
Para garantizar la calidad y el cumplimiento de las directrices de formateo y tipado estricto exigidas por el curso, pasamos el código corregido por las herramientas de validación estática del proyecto:

**Ruff (Linter y Formateador):**
```bash
python -m ruff check app tests
```
Resultado: Sin errores detectados. Código alineado con PEP 8.

**Mypy (Verificador de Tipos Estáticos):**
```bash
python -m mypy app
```
Resultado: Éxito en la verificación. Cero errores de inconsistencia de tipos en firmas o declaraciones.

## Conclusión de la Revisión
La utilización de técnicas de revisión asistida por Inteligencia Artificial demostró ser una herramienta valiosa de code review. Sin embargo, su valor real radica en el análisis crítico humano. Al evaluar cada hallazgo, no solo adoptamos las sugerencias de robustez técnica como el Soft Delete o el blindaje ante valores no finitos, sino que supimos rechazar propuestas que comprometen la arquitectura limpia del monolito, como la incorporación innecesaria de bloques try/except locales dentro del servicio. Este proceso reflexivo eleva la calidad técnica y arquitectónica de la API SensorHub para su entrega de la Semana 5.
