# sdlc-electronica-Julian
# Proyecto de Electrónica y SDLC: Driver UART y Controladores ESP32

Este repositorio contiene el proyecto de Ciclo de Vida del Desarrollo de Software, enfocado en la implementación de un sistema de lectura y procesamiento de sensores a través de un driver UART simulado para microcontroladores (como el ESP32).

## Reflexión sobre los Principios SOLID
Durante el desarrollo de este proyecto, la aplicación de los principios SOLID fue fundamental para transformar un código acoplado en una arquitectura profesional, modular y altamente testeable:

* **SRP (Responsabilidad Única):** La división del sistema en módulos independientes (`parsers.py` para decodificar, `recorder.py` para almacenar, `config.py` para parámetros) nos permitió aislar las responsabilidades. Si hay un error en la memoria, no afectamos la decodificación.
* **OCP (Abierto/Cerrado) y LSP (Sustitución de Liskov):** Al crear una arquitectura basada en clases abstractas, el sistema está abierto a la extensión (podemos agregar nuevos tipos de sensores o decodificadores) sin modificar el núcleo del controlador. Las clases derivadas funcionan como reemplazos perfectos de sus clases base.
* **ISP (Segregación de Interfaces) y DIP (Inversión de Dependencias):** Estos principios transformaron la forma de probar el código. En lugar de que el `ControladorCentral` dependiera de un sensor I2C físico rígido, lo hicimos depender de una `AbstraccionSensor`. Esto nos permitió inyectar clases *Mock* (simuladas por software) durante las pruebas con `pytest`. Además, limpiar las interfaces evitó obligar a los componentes a implementar métodos que físicamente no pueden realizar.

## Bitácora de Inteligencia Artificial (`AI_LOG.md`)
El proceso de diseño, estructuración y resolución de problemas fue documentado en el archivo `AI_LOG.md`. 
Cumpliendo con los requerimientos, la bitácora contiene el registro detallado del desarrollo, incluyendo **más de 3 entradas específicas** que se estructuran de la siguiente manera:
1. **El Prompt:** El contexto, error o instrucción proporcionada.
2. **Lo que produjo la IA:** El análisis, explicación teórica o bloque de código sugerido.
3. **Mi decisión y el porqué:** El análisis crítico como ingeniero sobre por qué se aceptó la arquitectura sugerida, cómo se adaptó para cumplir con los estándares del proyecto (ej. asegurar que el framework fuera compatible con las pruebas de Pytest) y las correcciones aplicadas a la lógica de la IA.

## Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **Testing:** Pytest (Mocks, validación de excepciones e Inyección de Dependencias)
* **Paradigma:** Programación Orientada a Objetos (POO) y Clean Architecture
