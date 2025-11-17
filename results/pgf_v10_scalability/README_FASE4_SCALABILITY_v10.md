
# README_FASE4_SCALABILITY_v10.md

Esta carpeta contiene todos los resultados, reportes y scripts de la Fase 4 (Escalabilidad) de la serie v10.

## Estructura

- `config_E_16x16_noreg/` : Resultados sin regularización (F4a)
- `config_F_16x16_reg/`   : Resultados con regularización (F4b)
- `analisis_scalability/` : CSVs resumen y análisis
- `figuras/`              : Figuras y visualizaciones
- `PREREGISTRO_FASE4_SCALABILITY_v10.md` : Preregistro formal
- `FASE4_LOG_COMANDOS.md` : Log de auditoría
- `REPORTE_FASE4_SCALABILITY_v10.md`     : Reporte técnico

## Ejecución oficial

- Script ejecutado: `scripts/run_fase4_scalabilidad_v10.py` (2 configs × 2 seeds × 3000 episodios)
- Resultados generados y auditados en las carpetas designadas
- Consolidación y análisis en `analisis_scalability/consolidado_fase4_v10.md`

## Cómo reproducir

1. Ejecutar el script oficial para cada configuración y semilla.
2. Verificar los resultados en las carpetas correspondientes.
3. Consultar el análisis consolidado y el log de comandos para trazabilidad.

## Documentación y trazabilidad

- Preregistro: `PREREGISTRO_FASE4_SCALABILITY_v10.md`
- Log de comandos: `FASE4_LOG_COMANDOS.md`
- Análisis consolidado: `analisis_scalability/consolidado_fase4_v10.md`

Toda la fase está documentada, versionada y es completamente reproducible.
