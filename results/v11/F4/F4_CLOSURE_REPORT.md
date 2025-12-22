# F4_CLOSURE_REPORT (v11)

**Fecha:** 2025-12-22  
**Fase:** F4 (stakes run-level `B=3` + CFR)  
**Condición fija:** `F2_redteam` (`red_team_prob=0.1`)  
**Repositorio:** TUI-v4.1

## Objetivo del cierre
Dejar F4 en estado **auditable y peer-review proof**: (i) outputs canónicos (CSV) versionados, (ii) trazabilidad de JSON por hashes sin subir datos brutos, y (iii) análisis preregistrado publicado con control de error familiar.

## Artefactos canónicos (citas exactas)

### Protocolo / preregistro
- Preregistro canónico: `results/v11/F4/PREREGISTRO_F4_v11.md`
- Adenda (stakes run-level + endpoint CFR): `results/v11/F4/F4_ADENDA_01.md`
- Log de desviaciones: `results/v11/F4/F4_DEVIATIONS_LOG_v11.md`

### Datos y trazabilidad
- Outputs canónicos (CSV) por stakes/agent: `results/v11/F4/F2_redteam/stkL/` y `results/v11/F4/F2_redteam/stkH/`
- Dataset canónico (CSV `*_episodes.csv` + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto extendido de JSON (sha256 + rutas, sin subir JSON): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`

### Resultados y análisis
- Reporte preregistrado F4 (endpoint CFR + Holm): `results/v11/data/f4_preregistered_report_v11.md`
- Tabla preregistrada F4 (pooled + sensibilidad por grid): `results/v11/data/f4_preregistered_stats_v11.csv`
- Run-level metrics (catástrofes, CFR, episodios): `results/v11/data/f4_run_metrics_v11.csv`

### Reconsolidación y descriptivos globales
- Master reconsolidado desde episodios: `results/master_results_clean.csv`
- Descriptivos globales (incluye F4 como fase separada): `results/v11/data/stats_report_v11.md`
- Tabla de descriptivos (incluye F4 como fase separada): `results/v11/data/stats_summary_v11.csv`

## Confirmaciones mínimas (checklist)
- Separación física por stakes (evita mezcla low/high): `results/v11/F4/F2_redteam/stkL/` y `results/v11/F4/F2_redteam/stkH/`
- Conteo canónico esperado: 60 CSV `*_episodes.csv` (6 grupos × 10 runs) bajo `results/v11/F4/F2_redteam/`.
- Los JSON por run no se versionan (tamaño); se auditan por hashes en el manifiesto extendido.
- El análisis preregistrado se ejecuta desde `scripts/f4_preregistered_analysis_v11.py` y publica las salidas citadas.

## Resultado confirmatorio (endpoint CFR)
Según `results/v11/data/f4_preregistered_report_v11.md`, el endpoint primario **CFR** saturó en 1.0 (budget agotado) en todos los grupos, por lo que:
- H1 (S0-H vs C-H) queda **inconcluso** para apoyar un efecto (ΔCFR=0, p≈1.0).
- H3 (S2-H vs S0-H) queda **inconcluso** (ΔCFR=0, p≈1.0).
- H2 (interacción) queda **inconcluso** (dd≈0, p≈1.0).

Nota: aunque el endpoint confirmatorio no discrimina (CFR=1), el secundario `episodes_completed` muestra diferencias descriptivas en high-stakes (ver `results/v11/data/f4_run_metrics_v11.csv`). Esto se reporta como secundario/exploratorio (no claim confirmatorio).

## Desviaciones del preregistro
Las desviaciones (si existen) deben registrarse **antes** de análisis completo en:
- `results/v11/F4/F4_DEVIATIONS_LOG_v11.md`

Estado al cierre: **sin desviaciones registradas** (ver log).

