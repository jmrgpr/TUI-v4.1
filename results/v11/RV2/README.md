# RV2 (v11 post-errata) — Repair Validation (GO/NO-GO por invariantes)

RV2 existe para resolver lo que RV1 mostró: el fix de `sim/runner.py` **sí** estabilizó el ciclo de vida del agente y los shapes, pero el criterio de “señal mínima E1” fue demasiado estricto/no-informativo para decidir GO/NO-GO.

En RV2:
- **GO/NO-GO depende solo de invariantes** (I1/I2).
- E1/E2 se reportan como **descriptivos** (no gating).

## Estructura (alineada al estilo F4–F6 / RV1)

- Preregistro y auditoría:
  - `results/v11/RV2/PREREGISTRO_RV2_v11.md`
  - `results/v11/RV2/RV2_DEVIATIONS_LOG_v11.md`
  - `results/v11/RV2/RV2_CLOSURE_REPORT.md`
- Runner:
  - `results/v11/RV2/run_RV2_v11.py`
- Outputs canónicos (se crean al ejecutar):
  - `results/v11/RV2/rv2_run_metrics.csv`
  - `results/v11/RV2/rv2_invariants.json`

## Ejecutar

Preflight:

```powershell
python results/v11/RV2/run_RV2_v11.py --dry-run
```

Smoke (no canónico):

```powershell
python results/v11/RV2/run_RV2_v11.py --smoke
```

Ejecución completa:

```powershell
python results/v11/RV2/run_RV2_v11.py
```

