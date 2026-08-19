# Semana 6 - Backlog trazable de SensorHub

## Objetivo de entrega

Entregar SensorHub en nivel **competente+**: RF-1 a RF-7 operativos en
producción, arquitectura en capas con DIP, cobertura mínima de 80%, CI/CD,
PostgreSQL con migraciones Alembic, observabilidad y documentación defendible.

No se agrega un track opcional hasta que todo el alcance competente+ esté en
verde y desplegado.

## Estado inicial y brechas

| ID | Estado al iniciar S6 | Evidencia o brecha | Prioridad |
|---|---|---|---|
| RF-1 | Parcial | CRUD y desactivación existen; faltan validaciones y pruebas de duplicados | P0 |
| RF-2 | Implementado | Valida tipo, unidad, rango físico y sensor activo | P0 |
| RF-3 | Casi listo | Paginación y fechas existen; faltan casos borde de integración | P0 |
| RF-4 | Implementado | Genera alertas WARNING/CRITICAL por umbral | P0 |
| RF-5 | Parcial | Consulta y cambio de estado existen; falta validar transiciones | P0 |
| RF-6 | Implementado | Estadísticas por sensor y periodo con pruebas | P0 |
| RF-7 | Parcial | `/health` existe; faltan comprobación de BD y métricas | P0 |
| RNF-1 | Parcial | Capas y DIP en sensores/lecturas; alertas aún usan repositorio en router | P0 |
| RNF-2 | Cumple base | 87% y tests de integración; mantener umbral al agregar código | P0 |
| RNF-3 | Parcial | CI con lint, mypy y tests; validar CD real y sus secretos | P0 |
| RNF-4 | Parcial | Migración inicial lista; falta verificar Compose con PostgreSQL | P0 |
| RNF-5 | Pendiente | No hay logs JSON ni manejo global de errores | P0 |
| RNF-6 | Parcial | README, ADR-0001 y AI_LOG existen; falta diagrama, ADR-0002 y consolidación | P1 |

## Mini-sprint 1 - Núcleo confiable

- [x] Auditar línea base: 16 tests, 87% de cobertura, Ruff y Mypy en verde.
- [x] Implementar RF-6 con mínimo, máximo, promedio y cantidad por periodo.
- [x] Completar validación física por tipo de sensor en dominio puro.
- [x] Rechazar lecturas para sensores inexistentes o inactivos.
- [ ] Validar estados y transiciones de alertas mediante un servicio.
- [ ] Añadir pruebas de integración para RF-1 a RF-6 y conservar cobertura >= 80%.

## Mini-sprint 2 - Producción y evidencia

- [x] Crear migración Alembic inicial y eliminar `create_all` del arranque.
- [ ] Implementar `/health` con comprobación de base de datos y `/metrics`.
- [ ] Añadir logs JSON y manejo global consistente de errores.
- [ ] Verificar Docker Compose con PostgreSQL desde cero.
- [ ] Confirmar CI, CD y URL pública con una ejecución real.
- [ ] Reescribir README con instalación, API, diagrama Mermaid y demo.
- [ ] Crear ADR-0002 para migraciones y estrategia de despliegue.
- [ ] Consolidar AI_LOG y preparar video de 3-5 minutos.

## Criterio de congelamiento

El jueves se congelan funcionalidades. Si existe retraso, se recorta en este
orden: componentes opcionales, métricas avanzadas y estadísticas. Nunca se
recortan CRUD, lecturas, alertas, pruebas, CI/CD, despliegue ni documentación
mínima.
