# Ejercicio de Prompting Efectivo - Semana 5

## Tarea 1: Consulta Filtrada y Paginada de Lecturas (Capa de Repositorio)
*Objetivo:* Obtener las lecturas de un sensor aplicando paginación (`limit` y `offset`) y filtros opcionales de fecha (`from_date` y `to_date`), considerando únicamente los registros activos.

### Prompt Pobre
> "Crea una funcion para buscar lecturas de un sensor con SQAlchemy con paginación"

#### Resultado del Prompt Pobre
La IA generó una consulta genérica utilizando la sintaxis obsoleta de SQLAlchemy 1.x (`session.query(Reading)`). Además, no manejó la inyección de dependencias por constructor de nuestra clase `ReadingRepository` omitió el filtrado de borrado lógico (`is_active`) y aplicó de forma obligatoria los filtros de fecha, lo cual rompería la API si el cliente no envía parámetros de tiempo.

```python
def get_by_sensor(session, sensor_id, limit, offset, from_date, to_date):
    return (
        session.query(ReadingModel)
        .filter(
            ReadingModel.sensor_id == sensor_id,
            ReadingModel.timestamp >= from_date,  # Rompe si from_date es None
            ReadingModel.timestamp <= to_date     # Rompe si to_date es None
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
```    

###  Prompt Bueno (Estructurado)
> **[Contexto]:** Estoy desarrollando una API de telemetría IoT con FastAPI y SQLAlchemy 2.0 (con la API tipada `Mapped[...]`). Tengo un repositorio llamado `ReadingRepository` que recibe la sesión en su constructor (`self.db: Session`). El modelo ORM de base de datos es `ReadingModel`. 
> **[Tarea específica]:** Necesito escribir el método `get_by_sensor` dentro de la clase `ReadingRepository` que reciba `sensor_id: str`, `limit: int`, `offset: int`, `from_date` (datetime opcional) y `to_date` (datetime opcional).
> **[Restricciones]:**
> 1. Usa la sintaxis estricta de SQLAlchemy 2.x con `select()` y `self.db.scalars().all()`.
> 2. Filtra por `ReadingModel.sensor_id` y asegúrate de incluir únicamente registros activos.
> 3. Los filtros `from_date` y `to_date` son opcionales; solo debes aplicar las cláusulas `where` si estas variables contienen datos.
> 4. Aplica la paginación usando los métodos `.offset(offset).limit(limit)` sobre el objeto `stmt`.
> **[Formato de entrega]:** Proporciona únicamente la función limpia con anotaciones de tipo compatibles con Mypy.

#### Resultado del Prompt Bueno
La IA devolvió el método optimizado que coincide de forma exacta con la implementación de persistencia de nuestro proyecto:

```python
def get_by_sensor(
    self, sensor_id: str, limit: int, offset: int, from_date, to_date
):
    stmt = select(ReadingModel).where(
        ReadingModel.sensor_id == sensor_id,
        ReadingModel.is_active
    )
    if from_date:
        stmt = stmt.where(ReadingModel.timestamp >= from_date)
    if to_date:
        stmt = stmt.where(ReadingModel.timestamp <= to_date)
        
    stmt = stmt.offset(offset).limit(limit)
    return self.db.scalars(stmt).all()
```

## Tarea 2: Creación de Esquema de Entrada con Pydantic v2 (Capa de Esquemas)
*Objetivo:* Definir el esquema de validación `SensorIn` para registrar un nuevo sensor en la API, asegurando que los campos sean requeridos de la forma correcta y que la documentación interactiva de Swagger UI muestre ejemplos claros de uso.

### Prompt Pobre
> "Crea un esquema de pydantic para un sensor en fastapi"

#### Resultado del Prompt Pobre
La IA generó una clase genérica sin conocer los requisitos de nuestro hardware IoT. Usó un `id` secuencial de tipo entero (`int`) en lugar de nuestro identificador alfanumérico real (`sensor_id: str`), omitió por completo el campo obligatorio `name` y utilizó la sintáxis obsoleta de importación `Optional` de la librería `typing` en lugar de la unión de tipos más moderna de Python. Además, no incluyó metadatos de documentación con ejemplos, lo que provocaría un error HTTP 422 inmediato al intentar usar la API en producción.

```python
from pydantic import BaseModel
from typing import Optional

class SensorIn(BaseModel):
    id: int  # Error: Tu API necesita 'sensor_id' de tipo string 
    location: Optional[str] = None  # Sintáxis obsoleta 
    type: str
```


### Prompt Bueno (Estructurado)
> **[Contexto]:** Estoy desarrollando el endpoint de creación de sensores `POST /sensors/` en una API de telemetría IoT llamada SensorHub usando FastAPI y Pydantic v2. Los sensores físicos se identifican con códigos alfanuméricos únicos creados por el usuario (como `"TEMP-01"` o `"BODEGA-02"`).
> **[Tarea específica]:** Diseña la clase de validación de entrada `SensorIn` que hereda de la clase `BaseModel` de Pydantic.
> **[Restricciones]:**
> 1. Usa exclusivamente la sintaxis nativa de Pydantic v2.
> 2. El identificador obligatorio debe llamarse `sensor_id` (de tipo `str`) e incluir un decorador `Field` con un ejemplo descriptivo como `"TEMP-01"` para documentar la API.
> 3. Los campos obligatorios `name` y `type` también deben contener ejemplos de uso claros dentro de un decorador `Field` (como `"Sensor de caldera"` y `"temperatura"`).
> 4. Los campos `location` y `alert_threshold` deben ser opcionales y admitir valores nulos, configurando `None` por defecto mediante la sintaxis moderna de unión de tipos (`str | None = None` y `float | None = None`). 
> **[Formato de entrega]:** Proporciona únicamente el código de Python limpio y bien tabulado de la clase del esquema.

#### Resultado del Prompt Bueno
La IA generó el esquema de validación robusto y autodocumentado que coincide de forma exacta con la implementación real de nuestro proyecto:

```python
from pydantic import BaseModel, Field

class SensorIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    name: str = Field(..., examples=["Sensor de caldera"])
    type: str = Field(..., examples=["temperatura"])
    location: str | None = None
    alert_threshold: float | None = None
```


## Tarea 3: Prueba de Estructura de Errores con TestClient (Capa de Pruebas)
*Objetivo:* Validar mediante pruebas automatizadas con `pytest` y `TestClient` que las excepciones por límites físicos en las lecturas de los sensores generen un error HTTP 422 y devuelvan la estructura de error JSON correcta con la ubicación exacta del campo inválido.

### Prompt Pobre
> "Genera un test de fastapi con pytest que mande un error de lectura"

#### Resultado del Prompt Pobre
La IA generó un código de prueba genérico que no utilizaba la configuración de aislamiento de base de datos de nuestro entorno de pruebas (SQLite en memoria). Además, no creaba el sensor padre requerido por la llave foránea antes de intentar registrar la lectura, y realizaba un `assert` débil que solo comprobaba el código de estado `422` sin verificar la estructura interna del JSON ni validar en qué campo ocurrió la falla de validación física.

```python
# tests/test_api.py (Simulación de código malo generado por la IA)

def test_create_reading_invalid(client):
    # ERROR: No crea el sensor padre y no valida la ubicación del error en el JSON
    payload = {
        "value": -300,
        "unit": "C"
    }
    response = client.post("/sensors/TEMP-03/readings", json=payload)
    assert response.status_code == 422
```


### Prompt Bueno (Estructurado)
> **[Contexto]:** Estoy desarrollando pruebas automatizadas con `pytest` y `TestClient` para mi API de telemetría IoT llamada SensorHub. La base de datos de prueba está configurada con SQLite en memoria y se limpia automáticamente antes de cada test gracias a la fixture `setup_db`.
> **[Tarea específica]:** Escribe la función de prueba `test_validacion_fisica_cero_absoluto_devuelve_422` para validar el comportamiento del endpoint al intentar registrar una lectura de temperatura inválida.
> **[Restricciones]:**
> 1. Primero, realiza una petición `POST` a `/sensors` para crear el sensor padre con `"sensor_id": "TEMP-03"`, `"name": "Sensor 3"` y `"type": "temperatura"`.
> 2. Envía una petición `POST` al endpoint `/sensors/TEMP-03/readings` enviando un valor de temperatura físicamente imposible en el universo (`-300` °C).
> 3. Verifica que el código HTTP de respuesta sea exactamente `422 Unprocessable Entity`.
> 4. Asegura de forma estricta que la respuesta JSON contenga el reporte de error de Pydantic detallando que la localización del fallo está en el campo `"value"` del cuerpo de la petición (`["body", "value"]`).
> 
> **[Formato de entrega]:** Proporciona únicamente el código de Python limpio de la función pytest.

#### Resultado del Prompt Bueno
La IA generó la prueba con la aserción exacta y robusta que coincide de forma idéntica con el código que tenemos implementado en nuestra suite de pruebas:

```python
def test_validacion_fisica_cero_absoluto_devuelve_422():
    # Creamos el sensor
    client.post(
        "/sensors", 
        json={"sensor_id": "TEMP-03", "name": "Sensor 3", "type": "temperatura"}
    )
    
    # Intentamos registrar una temperatura imposible en el universo
    response = client.post("/sensors/TEMP-03/readings", json={
        "value": -300,  # Falla la validación Pydantic
        "unit": "C"
    })
    assert response.status_code == 422
    # Validamos que Pydantic nos devuelva el error en el campo 'value'
    assert response.json()["detail"]["loc"] == ["body", "value"]
```