# Definition of Done (DoD)

Para que una Historia de Usuario (US) se considere terminada e integrable a la rama principal, debe cumplir obligatoriamente con los siguientes criterios:

1. **Criterios Gherkin:** Todos los escenarios definidos en Gherkin para la historia de usuario deben estar implementados como pruebas automatizadas que pasen exitosamente.
2. **Cobertura de Código:** La ejecución de Pytest debe reportar una cobertura de pruebas mayor o igual al 80% (`--cov-fail-under=80`).
3. **Análisis Estático (Linters):** El código debe estar completamente limpio y pasar sin errores las validaciones de `ruff` y `mypy`.
4. **Auto-revisión (Pull Request):** Los cambios deben integrarse a través de un Pull Request (PR), habiendo leído línea por línea antes de autorizar el merge.
5. **Documentación:** La documentación correspondiente debe estar actualizada reflejando los nuevos cambios.