# F5_CLOSURE_REPORT (v11)

**Fecha:** YYYY-MM-DD  
**Fase:** F5  
**Condición fija:** `F2_redteam` (high-stakes `B=3`)  
**Repositorio:** TUI-v4.1

## Objetivo del cierre
Dejar F5 en estado **auditable y peer-review proof**: (i) outputs canónicos (CSV) versionados, (ii) trazabilidad de JSON por hashes sin subir datos brutos, y (iii) análisis preregistrado publicado con control de error familiar.

## Artefactos canónicos (citas exactas)

### Protocolo / preregistro
- Preregistro canónico: `results/v11/F5/PREREGISTRO_F5_v11.md`
- Log de desviaciones: `results/v11/F5/F5_DEVIATIONS_LOG_v11.md`

### Datos y trazabilidad
- Outputs canónicos (CSV): `results/v11/F5/F2_redteam/stkH/`
- Dataset canónico (CSV `*_episodes.csv` + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto extendido de JSON (sha256 + rutas, sin subir JSON): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`

### Resultados y análisis
- Reporte preregistrado F5 (endpoint `episodes_completed` + Holm): `results/v11/data/f5_preregistered_report_v11.md`
- Tabla preregistrada F5: `results/v11/data/f5_preregistered_stats_v11.csv`
- Run-level metrics: `results/v11/data/f5_run_metrics_v11.csv`

### Reconsolidación y descriptivos globales (si aplica)
- Master reconsolidado: `results/master_results_clean.csv`
- Descriptivos globales: `results/v11/data/stats_report_v11.md`

## Confirmaciones mínimas (checklist)
- Separación física por fase: `results/v11/F5/` (sin mezclar con F4).
- Conteo canónico esperado: 30 CSV `*_episodes.csv` (3 grupos × 10 runs) bajo `results/v11/F5/F2_redteam/stkH/`.
- JSON por run no se versionan; se auditan por hashes en el manifiesto extendido.
- El análisis preregistrado se ejecuta desde `scripts/f5_preregistered_analysis_v11.py`.

## Resultados confirmatorios (endpoint `episodes_completed`)
*(Completar al cerrar, citando `results/v11/data/f5_preregistered_report_v11.md`.)*

## Desviaciones del preregistro
Registrar desviaciones **antes** de análisis completo en:
- `results/v11/F5/F5_DEVIATIONS_LOG_v11.md`

