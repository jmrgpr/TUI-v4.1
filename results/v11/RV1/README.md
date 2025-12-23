# RV1 (v11 post-errata) — Repair Validation

RV1 existe para validar (de forma **preregistrada**) que el fix en `sim/runner.py`:

1) **Permite aprendizaje acumulativo entre episodios** (agente persistente por run), y
2) Es robusto ante **mismatch de dimensión** en estados DQN (`coords_only` / estados cortos), y
3) Muestra una **señal mínima de aprendizaje intra-run** antes de re-intentar calibraciones (B / `red_team_prob`).

> RV1 **no** es un experimento “de teoría”. Es validación de ingeniería para habilitar fases posteriores (F7+).

## Estructura (alineada al estilo F4–F6)

- Preregistro y auditoría:
  - `results/v11/RV1/PREREGISTRO_REPAIR_VALIDATION_v11.md`
  - `results/v11/RV1/RV1_DEVIATIONS_LOG_v11.md`
  - `results/v11/RV1/RV1_CLOSURE_REPORT.md` (se completa al cerrar)
- Outputs de RV1 (se crean al ejecutar):
  - `results/v11/RV1/rv1_run_metrics.csv`
  - `results/v11/RV1/rv1_invariants.json`

## Cómo ejecutar (manual, por ahora)

RV1 se corre con el runner dedicado:

```powershell
python results/v11/RV1/run_RV1_v11.py
```

Preflight (sin ejecutar):

```powershell
python results/v11/RV1/run_RV1_v11.py --dry-run
```

Smoke test corto (no canónico; escribe en `_tmp_smoke`):

```powershell
python results/v11/RV1/run_RV1_v11.py --smoke
```

Parámetros congelados por defecto (según preregistro):
- `episodes=200`, `grid=16`, `seeds={42,101,13}`
- `risk_scale=1.2`, `risk_level=high`, `red_team_prob=0.03`
- stakes **LOW** (sin budget) para observar aprendizaje intra-run.

Al terminar, completa `RV1_CLOSURE_REPORT.md` con PASS/FAIL según el preregistro.
