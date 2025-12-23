# F7_CLOSURE_REPORT (v11)

**Fecha:** 2025-12-23  
**Fase:** F7 (calibración budget `B` → `B*` + confirmatorio CFR, high-stakes)  
**Condición base:** `F2_redteam` (high-stakes con `B*`)  
**Repositorio:** TUI-v4.1  
**Commit (selección B*):** `0bc72ff`

## Objetivo del cierre
Dejar F7 en estado **auditable y peer-review proof**: (i) outputs canónicos (CSV) versionados, (ii) trazabilidad de JSON por hashes sin subir datos brutos, y (iii) análisis preregistrado publicado con control de error familiar.

## Artefactos canónicos (citas exactas)

### Protocolo / preregistro
- Preregistro canónico: `results/v11/F7/PREREGISTRO_F7_v11.md`
- Log de desviaciones: `results/v11/F7/F7_DEVIATIONS_LOG_v11.md`

### Piloto (calibración, no confirmatorio)
- Selección de `B*` (reporte): `results/v11/data/f7_pilot_selection_v11.md`
- Tabla piloto (CFR por candidato): `results/v11/data/f7_pilot_table_v11.csv`
- Selección `B*` (JSON canónico): `results/v11/F7/analysis/f7_pilot_selection_v11.json`

### Datos y trazabilidad (confirmatorio)
- Outputs canónicos (CSV): `results/v11/F7/F2_redteam/stkH/rt*/`
- Dataset canónico (CSV `*_episodes.csv` + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto extendido de JSON (sha256 + rutas, sin subir JSON): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`

### Resultados y análisis (confirmatorio)
- Reporte preregistrado F7 (endpoint CFR + McNemar exact + Holm): `results/v11/data/f7_preregistered_report_v11.md`
- Tabla preregistrada F7: `results/v11/data/f7_preregistered_stats_v11.csv`
- Run-level metrics: `results/v11/data/f7_run_metrics_v11.csv`

## Confirmaciones mínimas (checklist)
- Separación física por fase: `results/v11/F7/` (sin mezclar con F4–F6).
- Piloto ejecutado y `B*` seleccionado según regla preregistrada (ver reporte/JSON).
- Conteo canónico (confirmatorio): 60 CSV `*_episodes.csv` (3 grupos × 20 runs) bajo `results/v11/F7/F2_redteam/stkH/rt*/`.
- JSON por run no se versionan; se auditan por hashes en el manifiesto extendido.
- El análisis preregistrado se ejecuta desde `scripts/f7_preregistered_analysis_v11.py`.

## Resultados confirmatorios (endpoint CFR)
Selección de budget:
- `B* = 40` (ver `results/v11/F7/analysis/f7_pilot_selection_v11.json` y `results/v11/data/f7_pilot_selection_v11.md`).

Según `results/v11/data/f7_preregistered_report_v11.md`, el endpoint primario **CFR** (budget-exhaustion) deja de saturar (headroom real) y la family confirmatoria (Holm-Bonferroni, alpha=0.05; MESI_CFR=0.20) arroja:

- Resumen por grupo (pooled grids 8+16; n=20 por grupo): C-H CFR=0.950, S0-H CFR=0.650, S2-H CFR=0.750.
- H1 (S0-H vs C-H): ΔCFR=-0.300, IC95%=[-0.500, -0.100], p=0.03125, p Holm=0.0625 → **INCONCLUSIVE**.
- H3 (S2-H vs S0-H): ΔCFR=+0.100, IC95%=[-0.150, 0.350], p=0.6875, p Holm=0.6875 → **INCONCLUSIVE**.

Nota: el objetivo metodológico de F7 (evitar ceiling effect) se cumple. Con la expansión preregistrada (n=20 por grupo), H1 queda cerca del umbral (p sin ajustar <0.05) pero no pasa Holm.

## Desviaciones del preregistro
Registrar desviaciones **antes** de análisis completo en:
- `results/v11/F7/F7_DEVIATIONS_LOG_v11.md`

Estado al cierre: **sin desviaciones registradas** (ver log).
