# F8 preregistered analysis (v11)

Endpoint primario: **CFR** (Catastrophic Failure Rate) = proporción de runs con `catastrophes_total >= B` (budget-exhaustion). `B=40`.

Family confirmatoria: m=1 (sin Holm).
- H1: S0-H vs C-H (McNemar exact, 2-sided) + MESI_CFR=0.20

Bootstrap CI (pares): B=5000, seed=2025.

Directorio canónico analizado: `results/v11/F8/F2_redteam/stkH/rt0p03`

## Resumen por grupo (pooled grids 8+16)

| grupo | n | CFR | catástrofes (sum) | episodios promedio |
| --- | ---:| ---:| ---:| ---:|
| C-H | 40 | 1.000 | 1600 | 124.5 |
| S0-H | 40 | 0.400 | 795 | 165.0 |

## Resultado confirmatorio (pooled)

| hipótesis | comparación | ΔCFR (A-B) | IC95% | p (McNemar) | decisión |
| --- | --- | ---:| --- | ---:| --- |
| H1 | H1: S0-H vs C-H | -0.600 | [-0.750, -0.450] | 1.19209e-07 | PASS |

## Sensibilidad por grid
Ver `results/v11/data/f8_preregistered_stats_v11.csv` (incluye filas grid=8 y grid=16).

## Trazabilidad
- Runs (run-level metrics): `results/v11/data/f8_run_metrics_v11.csv`
- Tabla preregistrada: `results/v11/data/f8_preregistered_stats_v11.csv`
