# F8_CLOSURE_REPORT (v11)

**Fecha:** YYYY-MM-DD  
**Fase:** F8 (replicación H1-only; CFR, high-stakes `B=40`)  
**Condición base:** `F2_redteam` (high-stakes `B=40`, `red_team_prob=0.03`)  
**Repositorio:** TUI-v4.1  
**Commit (preregistro):** `TBD`

## Objetivo del cierre
Dejar F8 en estado **auditable y peer-review proof**: (i) outputs canónicos (CSV) versionados, (ii) trazabilidad de JSON por hashes sin subir datos brutos, y (iii) análisis preregistrado publicado para el endpoint primario CFR.

## Artefactos canónicos (citas exactas)

### Protocolo / preregistro
- Preregistro canónico: `results/v11/F8/PREREGISTRO_F8_v11.md`
- Log de desviaciones: `results/v11/F8/F8_DEVIATIONS_LOG_v11.md`

### Datos y trazabilidad (confirmatorio)
- Outputs canónicos (CSV): `results/v11/F8/F2_redteam/stkH/rt*/`
- Dataset canónico (CSV `*_episodes.csv` + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto extendido de JSON (sha256 + rutas, sin subir JSON): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`

### Resultados y análisis (confirmatorio)
- Reporte preregistrado F8 (endpoint CFR + McNemar exact): `results/v11/data/f8_preregistered_report_v11.md`
- Tabla preregistrada F8: `results/v11/data/f8_preregistered_stats_v11.csv`
- Run-level metrics: `results/v11/data/f8_run_metrics_v11.csv`

## Confirmaciones mínimas (checklist)
- Separación física por fase: `results/v11/F8/` (sin mezclar con F4–F7).
- Conteo canónico esperado (base): 80 CSV `*_episodes.csv` (2 grupos × 40 runs) bajo `results/v11/F8/F2_redteam/stkH/rt*/`.
- (Si expansión) Conteo canónico esperado (total): 120 CSV `*_episodes.csv` (2 grupos × 60 runs).
- JSON por run no se versionan; se auditan por hashes en el manifiesto extendido.
- El análisis preregistrado se ejecuta desde `scripts/f8_preregistered_analysis_v11.py`.

## Resultados confirmatorios (endpoint CFR)
Completar con el contenido de `results/v11/data/f8_preregistered_report_v11.md`:
- Resumen por grupo (pooled grids 8+16)
- H1: ΔCFR, IC95%, p (McNemar exact), decisión (PASS / INCONCLUSIVE)

## Desviaciones del preregistro
Registrar desviaciones **antes** de análisis completo en:
- `results/v11/F8/F8_DEVIATIONS_LOG_v11.md`

Estado al cierre: (sin desviaciones / con desviaciones; listar).

