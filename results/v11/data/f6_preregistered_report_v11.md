# F6 preregistered analysis (v11)

Endpoint primario: **CFR** (Catastrophic Failure Rate) = proporción de runs con `catastrophes_total >= B` (budget-exhaustion). Budget congelado: `B=3`.

Family confirmatoria (Holm-Bonferroni, alpha=0.05):
- H1: S0-H vs C-H (McNemar exact, 2-sided) + MESI_CFR=0.20
- H3: S2-H vs S0-H (McNemar exact, 2-sided) + MESI_CFR=0.20

Bootstrap CI (pares): B=5000, seed=2025.

Directorio canónico analizado: `results/v11/F6/F2_redteam/stkH/rt0p03`

## Resumen por grupo (pooled grids 8+16)

| grupo | n | CFR | catástrofes (sum) | episodios promedio |
| --- | ---:| ---:| ---:| ---:|
| C-H | 10 | 1.000 | 30 | 22.7 |
| S0-H | 10 | 1.000 | 30 | 29.0 |
| S2-H | 10 | 1.000 | 30 | 29.0 |

## Resultados confirmatorios (pooled)

| hipótesis | comparación | ΔCFR (A-B) | IC95% | p (McNemar) | p Holm | decisión |
| --- | --- | ---:| --- | ---:| ---:| --- |
| H1 | H1: S0-H vs C-H | 0.000 | [0.000, 0.000] | 1 | 1 | INCONCLUSIVE |
| H3 | H3: S2-H vs S0-H | 0.000 | [0.000, 0.000] | 1 | 1 | INCONCLUSIVE |

## Sensibilidad por grid
Ver `results/v11/data/f6_preregistered_stats_v11.csv` (incluye filas grid=8 y grid=16).

## Trazabilidad
- Runs (run-level metrics): `results/v11/data/f6_run_metrics_v11.csv`
- Tabla preregistrada: `results/v11/data/f6_preregistered_stats_v11.csv`
- Piloto p*: `results/v11/data/f6_pilot_selection_v11.md` y `results/v11/data/f6_pilot_table_v11.csv`
