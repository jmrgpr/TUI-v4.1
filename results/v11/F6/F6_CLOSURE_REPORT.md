# F6_CLOSURE_REPORT (v11)

**Fecha:** 2025-12-23  
**Fase:** F6 (calibración `red_team_prob` → `p*` + confirmatorio CFR, high-stakes `B=3`)  
**Condición base:** `F2_redteam` (high-stakes `B=3`)  
**Repositorio:** TUI-v4.1

## Objetivo del cierre
Dejar F6 en estado **auditable y peer-review proof**: (i) outputs canónicos (CSV) versionados, (ii) trazabilidad de JSON por hashes sin subir datos brutos, y (iii) análisis preregistrado publicado con control de error familiar.

## Artefactos canónicos (citas exactas)

### Protocolo / preregistro
- Preregistro canónico: `results/v11/F6/PREREGISTRO_F6_v11.md`
- Log de desviaciones: `results/v11/F6/F6_DEVIATIONS_LOG_v11.md`

### Piloto (calibración, no confirmatorio)
- Selección de `p*` (reporte): `results/v11/data/f6_pilot_selection_v11.md`
- Tabla piloto (CFR por candidato): `results/v11/data/f6_pilot_table_v11.csv`

### Datos y trazabilidad (confirmatorio)
- Outputs canónicos (CSV): `results/v11/F6/F2_redteam/stkH/rt*/`
- Dataset canónico (CSV `*_episodes.csv` + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto extendido de JSON (sha256 + rutas, sin subir JSON): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`

### Resultados y análisis (confirmatorio)
- Reporte preregistrado F6 (endpoint CFR + McNemar exact + Holm): `results/v11/data/f6_preregistered_report_v11.md`
- Tabla preregistrada F6: `results/v11/data/f6_preregistered_stats_v11.csv`
- Run-level metrics: `results/v11/data/f6_run_metrics_v11.csv`

### Reconsolidación y descriptivos globales (si aplica)
- Master reconsolidado: `results/master_results_clean.csv`
- Descriptivos globales: `results/v11/data/stats_report_v11.md`

## Confirmaciones mínimas (checklist)
- Separación física por fase: `results/v11/F6/` (sin mezclar con F4/F5).
- Piloto ejecutado y `p*` seleccionado según regla preregistrada (ver reporte).
- Conteo canónico esperado (confirmatorio): 30 CSV `*_episodes.csv` (3 grupos × 10 runs) bajo `results/v11/F6/F2_redteam/stkH/rt*/`.
- JSON por run no se versionan; se auditan por hashes en el manifiesto extendido.
- El análisis preregistrado se ejecuta desde `scripts/f6_preregistered_analysis_v11.py`.

## Resultados confirmatorios (endpoint CFR)
Según `results/v11/data/f6_pilot_selection_v11.md`, el piloto no logró evitar saturación: `CFR_control(p)=1.0` para todos los candidatos `{0.03, 0.05, 0.07}`, por lo que la regla determinística seleccionó `p* = 0.03` (empate → p menor).

Según `results/v11/data/f6_preregistered_report_v11.md`, el endpoint primario **CFR** volvió a saturar en 1.0 en todos los grupos (C-H, S0-H, S2-H), por lo que:
- H1 (S0-H vs C-H): **INCONCLUSIVE** (ΔCFR=0, p=1, p Holm=1).
- H3 (S2-H vs S0-H): **INCONCLUSIVE** (ΔCFR=0, p=1, p Holm=1).

Nota: el secundario `episodes_completed` difiere descriptivamente (C-H mean≈22.7 vs S0-H/S2-H mean≈29.0), pero no es un claim confirmatorio en F6.

## Desviaciones del preregistro
Registrar desviaciones **antes** de análisis completo en:
- `results/v11/F6/F6_DEVIATIONS_LOG_v11.md`

Estado al cierre: **sin desviaciones registradas** (ver log).
