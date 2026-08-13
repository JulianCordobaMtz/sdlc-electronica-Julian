# Reporte de Auditoría de Código con IA - Semana 5

Este documento detalla la revisión técnica por pares asistida por Inteligencia Artificial realizada sobre los archivos reales creados por GitHub Copilot: el módulo de producción `semana5/conversions.py` y su suite de pruebas unitarias `tests/test_conversions.py`.

---

## Análisis Técnico de los Archivos Existentes

### 1. Módulo de Producción: `semana5/conversions.py`
El código generado muestra un excelente estándar de calidad de software y alineación con las buenas prácticas de Python 3.12:
* **Uso de tipado estricto:** Incluye el import de `from __future__ import annotations` y anotaciones de tipo claras (`c: float) -> float`.
* **Inmutabilidad y constantes:** Define las constantes físicas del cero absoluto utilizando la anotación de tipo `Final[float]` de la librería `typing` (ej. `ABSOLUTE_ZERO_C_IN_C: Final[float] = -273.15`). Esto emula el comportamiento de constantes compiladas en C y evita alteraciones accidentales.
* **Encapsulamiento del módulo:** El uso de la lista de exportación explícita `__all__` restringe de forma profesional los componentes que se exponen al importar el módulo con comodín (`import *`).

### 2. Suite de Pruebas: `tests/test_conversions.py`
La suite de pruebas original está muy bien diseñada:
* **Manejo de punto flotante:** Utiliza correctamente la función `approx` de pytest para evitar falsos negativos ocasionados por la aritmética de precisión IEEE 754 de Python (ej. `assert fahrenheit_to_celsius(32.0) == approx(0.0)`).
* **Validación de Excepciones:** No solo comprueba que se lance `ValueError`, sino que captura el objeto de la excepción con `as exc` y realiza una aserción estricta de que el mensaje de error contiene la explicación sobre el cero absoluto (`assert "por debajo del cero absoluto" in str(exc.value)`).

---

## Hallazgos de Auditoría y Decisiones de Diseño (Trade-offs)

### Sugerencia 1: Comprobación de Viaje Redondo ("Round-Trip Consistency")
* **Sugerencia de la IA:** Implementar una prueba matemática para garantizar que realizar la conversión de Celsius a otra unidad y luego de vuelta al valor Celsius original de forma cíclica conserve la consistencia exacta de los datos.
* **Veredicto:** **ACEPTADO**.
* **Justificación:** En telemetría IoT, los datos fluyen continuamente de un formato de escala a otro. Asegurar matemáticamente que la conversión "ida y vuelta" no tenga derivas ni pérdidas por redondeo binario acumulado es indispensable para la confiabilidad.

### Sugerencia 2: Reemplazo del tipo nativo `float` por `decimal.Decimal`
* **Sugerencia de la IA:** Migrar el tipado y las operaciones matemáticas de `float` a la clase `Decimal` de la biblioteca estándar de Python para evitar cualquier pérdida infinitesimal de precisión.
* **Veredicto:** **RECHAZADO**.
* **Justificación técnica:** Los sensores físicos industriales de SensorHub (como un sensor de temperatura RTD PT100) reportan telemetría con una resolución física máxima de 1 o 2 decimales (ej. `24.53` °C). El uso de `Decimal` se ejecuta por software en Python (ralentizando los cálculos hasta 100 veces en comparación con `float` a nivel de CPU) y rompe la serialización nativa de JSON con Pydantic y FastAPI. Mantener `float` nativo es la decisión óptima para el balance de rendimiento y escala de SensorHub.

### Sugerencia 3: Vulnerabilidad en la Validación ante valores `NaN` (Not a Number)
* **Sugerencia de la IA:** Analizar y documentar qué sucede cuando un sensor envía un valor nulo de hardware del tipo `NaN` (Not a Number) debido a una falla eléctrica o física en el sensor.
* **Veredicto:** **ACEPTADO**.
* **Justificación:** En Python, cualquier comparación lógica que involucre un valor `NaN` utilizando los operadores `<` o `>` siempre devuelve `False` (ej. `float('nan') < -273.15` evalúa a `False`). Como resultado, el valor corrupto `NaN` bypassaba la validación del cero absoluto y se propagaba en la base de datos de producción de SensorHub. Se documentó este comportamiento en las pruebas unitarias avanzadas.

---

## 🧪 Suite Incremental (5 Nuevos Tests de Calidad)

Para cumplir con la rúbrica y blindar la aplicación, se agregaron las siguientes pruebas avanzadas que complementan las de Copilot, atacando límites de precisión infinitesimales, evasión dinámica de tipos y tolerancia a fallas de hardware:

1. **`test_precision_limite_infinitesimal_cero_absoluto`:** Comprueba la precisión en los decimales límite. Mientras `-273.15` pasa felizmente, `-273.15001` falla de inmediato.
2. **`test_conversions_nan_handling`:** Evalúa y documenta la propagación de valores matemáticos rotos del tipo `NaN` en los convertidores.
3. **`test_conversions_infinity_handling`:** Verifica que los límites infinitos negativos (físicamente imposibles) se bloqueen adecuadamente con `ValueError`, mientras que los infinitos positivos se propagan.
4. **`test_dynamic_type_evasion_at_runtime`:** Simula flujos de ejecución reales donde se evade la firma estática (ej. texto corrupto que entra a la API) garantizando que el sistema lance un `TypeError` nativo y no un estado indefinido.