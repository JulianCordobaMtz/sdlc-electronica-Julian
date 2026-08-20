# Guía de demo y presentación de SensorHub

## Preparación

- Confirma que `/docs`, `/health` y `/metrics` respondan en producción.
- Abre GitHub Actions en la última ejecución verde.
- Prepara los JSON en un bloc de notas para no escribirlos durante la grabación.
- Usa identificadores nuevos para que la demo sea repetible.
- Graba la pantalla a 1080p y mantén abierta solamente la información necesaria.

## Video de respaldo: 3-5 minutos

### 0:00-0:25 - Problema

> SensorHub recibe telemetría IoT, valida que sea físicamente posible, detecta
> anomalías y conserva alertas trazables en PostgreSQL.

Muestra la URL pública y Swagger.

### 0:25-1:00 - Crear sensor

```json
{
  "sensor_id": "TEMP-DEMO-01",
  "name": "Temperatura de caldera",
  "type": "temperatura",
  "location": "Laboratorio",
  "alert_threshold": 30
}
```

Ejecuta `POST /sensors` y señala `is_active: true`.

### 1:00-1:40 - Lecturas y validación

Registra una lectura normal:

```json
{"value": 25, "unit": "C"}
```

Menciona que temperatura, humedad y presión tienen reglas físicas por unidad.
Si hay tiempo, muestra que `-300 C` es rechazada.

### 1:40-2:30 - Anomalía y alerta

Registra:

```json
{"value": 40, "unit": "C"}
```

Consulta `GET /alerts?status=open` y muestra severidad, valor y umbral. Cambia
el estado primero a `acknowledged` y después a `resolved`:

```json
{"status": "acknowledged"}
```

```json
{"status": "resolved"}
```

### 2:30-3:10 - Consulta y estadísticas

Muestra paginación/filtros en lecturas y ejecuta
`GET /sensors/TEMP-DEMO-01/statistics`. Explica mínimo, máximo, promedio y
cantidad.

### 3:10-3:45 - Producción y observabilidad

Abre `/health` y `/metrics`. Explica que el healthcheck ejecuta una consulta
a PostgreSQL y que los logs JSON incluyen un request ID.

### 3:45-4:30 - Calidad y cierre

Muestra GitHub Actions en verde, la cobertura superior al 80% y el diagrama
Mermaid del README.

> El resultado es un servicio pequeño pero reproducible: código en capas,
> pruebas, migraciones, observabilidad y despliegue controlado.

## Presentación técnica: 10 minutos

| Tiempo | Contenido |
|---|---|
| 0:00-1:00 | Problema, alcance y RF-1 a RF-7 |
| 1:00-2:30 | Diagrama y flujo Router -> Service -> Repository |
| 2:30-5:30 | Demo de sensor, lectura, anomalía, alerta y estadísticas |
| 5:30-6:30 | Healthcheck, métricas y logs JSON |
| 6:30-7:30 | Pruebas, cobertura y CI/CD |
| 7:30-8:30 | ADR-0001: capas y DIP |
| 8:30-9:20 | ADR-0002: PostgreSQL y Alembic |
| 9:20-10:00 | Limitaciones, siguiente paso y cierre |

## Preguntas técnicas probables

### ¿Por qué usar DIP?

La lógica depende de protocolos, no de SQLAlchemy. Así se prueba con fakes y se
puede sustituir la persistencia sin reescribir los casos de uso.

### ¿Qué pasa si PostgreSQL falla?

`/health` devuelve 503, Render considera la instancia no saludable y Compose
evita iniciar la API antes de que PostgreSQL acepte conexiones.

### ¿Cómo escalarías a 1,000 sensores?

Mantendría la API sin estado, añadiría réplicas, un pool de conexiones y
procesamiento asíncrono para la ingesta. Antes mediría latencia, volumen y
cuellos de botella; no agregaría componentes sin evidencia.

### ¿Por qué no usar `create_all`?

Porque no versiona la evolución del esquema. Alembic permite reproducir y
auditar cada cambio.

### ¿Qué significa 94% de cobertura?

Indica qué líneas ejecutó la suite, no garantiza ausencia de errores. Se combina
con pruebas de integración, casos borde, Ruff, Mypy y revisión humana.

## Checklist final

- [ ] RF-1 a RF-7 comprobados en producción.
- [ ] Pipeline de `main` en verde y despliegue completado.
- [ ] README y ambos ADR visibles en GitHub.
- [ ] Video de 3-5 minutos reproducible.
- [ ] Presentación ensayada sin leer este documento.
