# ADR 0002: PostgreSQL, Alembic y despliegue reproducible

- Estado: Aceptado
- Fecha: 2026-08-20
- Contexto: entrega final de SensorHub

## Contexto

SensorHub necesita conservar sensores, lecturas y alertas en producción. Crear
las tablas con `Base.metadata.create_all()` durante el arranque no registra la
evolución del esquema y puede producir diferencias entre desarrollo,
integración continua y Render. Además, iniciar la API antes de que PostgreSQL
acepte conexiones provoca fallos intermitentes.

La entrega exige Docker Compose con PostgreSQL, migraciones Alembic, CD a
producción, healthcheck y configuración exclusivamente mediante variables de
entorno.

## Decisión

1. PostgreSQL será la persistencia de desarrollo en Compose y de producción en
   Render. SQLite se conserva como alternativa local y base aislada de pruebas.
2. Alembic será la única autoridad para crear y evolucionar el esquema. La
   revisión inicial crea `sensors`, `readings` y `alert`.
3. El contenedor ejecutará `alembic upgrade head` antes de Uvicorn.
4. Compose esperará el resultado de `pg_isready` antes de iniciar la API y
   ambos servicios publicarán un healthcheck.
5. `DATABASE_URL` llegará por variables de entorno. La aplicación normalizará
   las URLs de Render para usar el controlador `psycopg`.
6. GitHub Actions separará calidad, construcción Docker y despliegue. El trabajo
   de despliegue requerirá los dos anteriores y solo se ejecutará para un push a
   `main`.
7. Render tendrá desactivado el auto-deploy directo para evitar dos despliegues
   del mismo commit; el pipeline solicitará el despliegue mediante la API.

## Alternativas consideradas

### Mantener SQLite en producción

Se descartó porque el sistema desplegado necesita una base administrada,
concurrente y persistente. El sistema de archivos del servicio web de Render es
efímero.

### Ejecutar `create_all` en cada arranque

Se descartó porque no versiona cambios ni permite revisar qué transformación se
aplicó. Tampoco sustituye correctamente migraciones de columnas o restricciones.

### Ejecutar migraciones manualmente

Se descartó porque depende de memoria humana y permite desplegar código contra
un esquema antiguo. El arranque automatizado falla antes de exponer una versión
inconsistente.

### Usar simultáneamente auto-deploy de Render y GitHub Actions

Se descartó porque puede construir dos veces el mismo commit y vuelve ambigua la
evidencia de qué pipeline autorizó producción.

## Consecuencias

### Positivas

- El esquema puede reconstruirse desde una base vacía.
- El mismo Dockerfile se usa localmente y en Render.
- La API no inicia hasta que PostgreSQL está disponible.
- Un fallo de lint, tipos, pruebas o construcción bloquea el despliegue.
- La versión desplegada puede asociarse con un SHA de Git.

### Negativas

- Un error en una migración impide que el contenedor inicie.
- La API key de Render debe administrarse como secreto de GitHub.
- Cada cambio de modelo requiere una nueva revisión Alembic.
- SQLite no reproduce todas las particularidades de PostgreSQL; por ello se
  mantiene una comprobación real con Compose antes de entregar.

## Evidencia de validación

- La revisión `0001_sensorhub_schema` se aplicó sobre una base vacía.
- Compose creó `alembic_version`, `sensors`, `readings` y `alert`.
- PostgreSQL y API alcanzaron estado saludable.
- `/health` confirmó la conexión y `/metrics` respondió dentro del contenedor.
- El workflow fue validado con actionlint y la suite local quedó en verde.

## Condiciones para revisar esta decisión

Se reconsiderará si las migraciones deben ejecutarse como un trabajo previo
independiente, si aparecen varias réplicas iniciando a la vez o si el despliegue
requiere una estrategia blue/green con rollback automático.
