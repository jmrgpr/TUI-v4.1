# F4 preregistered analysis (v11)

Endpoint primario: **CFR** (Catastrophic Failure Rate) = proporción de runs con `catastrophes_total >= B`.
Catástrofe: episodio con `starvation=1` (info['starvation'] cuando done=True). Budget congelado: `B=3`.

Family confirmatoria (Holm-Bonferroni, alpha=0.05):
- H1: S0-H vs C-H (Fisher exact, 2-sided) + MESI_CFR=0.20
- H2: interacción (S0-H vs C-H) - (S0-L vs C-L) (permutación dd, 2-sided)
- H3: S2-H vs S0-H (Fisher exact, 2-sided) + MESI_CFR=0.20

Bootstrap CI: B=5000, seed=2025. Permutación dd: B=20000.

## Resumen por grupo (pooled grids 8+16)

| grupo | n | CFR | catástrofes (sum) | episodios promedio |
| --- | ---:| ---:| ---:| ---:|
| C-H | 10 | 1.000 | 30 | 7.8 |
| C-L | 10 | 1.000 | 1807 | 200.0 |
| S0-H | 10 | 1.000 | 30 | 13.6 |
| S0-L | 10 | 1.000 | 1519 | 200.0 |
| S2-H | 10 | 1.000 | 30 | 13.6 |
| S2-L | 10 | 1.000 | 1519 | 200.0 |

## Resultados confirmatorios (pooled)

| hipótesis | comparación | ΔCFR | IC95% | p (test) | p Holm | decisión |
| --- | --- | ---:| --- | ---:| ---:| --- |
| H1 | H1: S0-H vs C-H | 0.000 | [0.000, 0.000] | 1 (fisher_exact_2sided) | 1 | INCONCLUSIVE |
| H2 | H2: interaction (S0-H vs C-H) - (S0-L vs C-L) | 0.000 | [0.000, 0.000] | 1 (permutation_dd (B=20000)) | 1 | INCONCLUSIVE |
| H3 | H3: S2-H vs S0-H | 0.000 | [0.000, 0.000] | 1 (fisher_exact_2sided) | 1 | INCONCLUSIVE |

## Sensibilidad por grid
Ver `results/v11/data/f4_preregistered_stats_v11.csv` (incluye filas grid=8 y grid=16).

## Trazabilidad
- Runs (run-level metrics): `results/v11/data/f4_run_metrics_v11.csv`
- Tabla preregistrada: `results/v11/data/f4_preregistered_stats_v11.csv`
