
# REPORTE_FASE4_SCALABILITY_v10.md

## Resumen ejecutivo

Fase 4 evalúa la escalabilidad del stack v10 en grids 16×16 bajo dos configuraciones (sin y con regularización), usando dos semillas (42, 101) y 3000 episodios por experimento. El objetivo es determinar el límite operativo antes de pasar a v11.

## Metodología

- Script oficial: `scripts/run_fase4_scalabilidad_v10.py`
- 2 configuraciones (F4a: sin regularización, F4b: con regularización)
- 2 semillas (42, 101)
- 3000 episodios por experimento
- Resultados guardados y auditados en carpetas designadas

## Resultados y figuras

Los resultados individuales se encuentran en los CSVs de cada configuración y semilla. El análisis consolidado y comparativo está documentado en `analisis_scalability/consolidado_fase4_v10.md`.

**Principales métricas:**
- success, steps, overhead, PGF, I_op

**Figuras y visualizaciones:**
- (Pendiente de generación gráfica; se recomienda visualizar curvas de éxito y episodios por configuración)

## Interpretación y limitaciones

- La ejecución fue estable y reproducible.
- No se observó éxito significativo en los primeros episodios; se recomienda análisis estadístico y visualización completa para confirmar aprendizaje.
- El protocolo v10 muestra robustez, pero se requiere mayor exploración para confirmar escalabilidad efectiva.

## Trazabilidad y reproducibilidad

- Preregistro: `PREREGISTRO_FASE4_SCALABILITY_v10.md`
- Log de comandos: `FASE4_LOG_COMANDOS.md`
- Análisis consolidado: `analisis_scalability/consolidado_fase4_v10.md`

---
*Reporte generado automáticamente el 8/12/2025 por GitHub Copilot.*
