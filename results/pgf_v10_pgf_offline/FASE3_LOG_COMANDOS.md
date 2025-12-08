# FASE3_LOG_COMANDOS.md

Log de comandos y scripts ejecutados durante Fase 3 (PGF offline).

[2025-12-08] Preparación de carpetas y snapshot de datos.

## Enriquecimiento de CSVs con PGF e I_op

Fecha: 2025-12-08
Script creado: scripts/compute_pgf_offline_v10.py
Comando de ejemplo:

python scripts/compute_pgf_offline_v10.py results/pgf_v10_pgf_offline/raw/phase1_4x4_20251205_102250.csv results/pgf_v10_pgf_offline/enriched/phase1_4x4_20251205_102250_enriched.csv

Se ejecutará el script sobre todos los CSVs en `raw/` y se guardarán los resultados en `enriched/`.

## Análisis avanzado de PGF offline

Fecha: 2025-12-08
Script creado: scripts/analyze_pgf_offline_v10.py
Comando de ejemplo:

python scripts/analyze_pgf_offline_v10.py results/pgf_v10_pgf_offline/enriched/

El script genera correlaciones, histogramas y tablas resumen para cada CSV enriquecido.
Además produce el archivo global `pgf_vs_success_summary.csv` con:
- medias y desviaciones de PGF e I_op,
- tasa de éxito media (`success_rate`),
- correlaciones PGF–I_op, PGF–success y PGF–steps.

Resultados en results/pgf_v10_pgf_offline/analysis/

## Consolidación y documentación de resultados

Fecha: 2025-12-08
- Se consolidaron los resultados del análisis avanzado en la carpeta analysis.
- Se completó el reporte oficial REPORTE_PGF_OFFLINE_v10.md con estadísticas, correlaciones y observaciones.
- Todas las figuras y tablas están disponibles para revisión y publicación.
