# F5 preregistered analysis (v11)

Endpoint primario: **episodes_completed** (high-stakes `B=3`; mayor = mejor).
Catástrofe: episodio con `starvation=1` (info['starvation'] cuando done=True).

Family confirmatoria (Holm-Bonferroni, alpha=0.05):
- H1: S0-H vs C-H (permutación pareada sign-flip sobre mean(d), 2-sided) + MESI_EC=5
- H3: S2-H vs S0-H (permutación pareada sign-flip sobre mean(d), 2-sided) + MESI_EC=5

Bootstrap CI: B=5000, seed=2025.

## Resumen por grupo (pooled grids 8+16)

| grupo | n | episodes_completed (mean) | episodes_completed (median) | CFR (secundario) |
| --- | ---:| ---:| ---:| ---:|
| C-H | 10 | 10.4 | 9.5 | 1 |
| S0-H | 10 | 14.9 | 15 | 1 |
| S2-H | 10 | 14.9 | 15 | 1 |

## Resultados confirmatorios (pooled)

| hipótesis | comparación | Δmean(A-B) | IC95% mean | Δmedian(A-B) | IC95% median | p (perm) | p Holm | decisión |
| --- | --- | ---:| --- | ---:| --- | ---:| ---:| --- |
| H1 | H1: S0-H vs C-H | 4.5 | [1.6, 7.8] | 2 | [1, 9] | 0.0234375 | 0.046875 | INCONCLUSIVE |
| H3 | H3: S2-H vs S0-H | 0 | [0, 0] | 0 | [0, 0] | 1 | 1 | INCONCLUSIVE |

## Sensibilidad por grid
Ver `results/v11/data/f5_preregistered_stats_v11.csv` (incluye filas grid=8 y grid=16).

## Trazabilidad
- Runs (run-level metrics): `results/v11/data/f5_run_metrics_v11.csv`
- Tabla preregistrada: `results/v11/data/f5_preregistered_stats_v11.csv`
