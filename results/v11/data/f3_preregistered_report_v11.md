# F3 preregistered analysis (v11)

Metrica primaria: `reward_env_total` (por run/seed; derivada de JSON `reward_env_evol`).

Family primaria (Holm-Bonferroni, alpha=0.05, two-sided, M=6):
- F1: simbiosis(m=0.0) vs control
- F1: simbiosis(m=0.0) vs dqn_control
- F2: simbiosis(m=0.0) vs control
- F2: simbiosis(m=0.0) vs dqn_control
- F1: simbiosis(m=0.2) vs simbiosis(m=0.0)
- F2: simbiosis(m=0.2) vs simbiosis(m=0.0)

Bootstrap: B=5000, seed=2025.

## Resultados (pooled grids 8+16)

| comparacion | nA | nB | delta media (A-B) | IC95% | p (2-sided) | p Holm (family) |
| --- | ---:| ---:| ---:| --- | ---:| ---:|
| F1:m0p0_simbiosis_vs_control | 10 | 10 | -1.88319 | [-2.29737, -1.4999] | 0.00039992 | 0.00239952 |
| F1:m0p0_simbiosis_vs_dqn_control | 10 | 10 | 1.31895 | [1.12366, 1.51858] | 0.00039992 | 0.0019996 |
| F2:m0p0_simbiosis_vs_control | 10 | 10 | 1.29206 | [0.423738, 2.21224] | 0.00319936 | 0.0127974 |
| F2:m0p0_simbiosis_vs_dqn_control | 10 | 10 | 0.264635 | [-0.832182, 1.37974] | 0.671066 | 1 |
| F1:pgf_ablation_m0p2_vs_m0p0 | 10 | 10 | 0 | [-0.284281, 0.280572] | 0.988602 | 1 |
| F2:pgf_ablation_m0p2_vs_m0p0 | 10 | 10 | 0 | [-1.20193, 1.16121] | 0.995801 | 0.995801 |

## Sensibilidad por grid
Ver `results/v11/data/f3_preregistered_stats_v11.csv` (incluye filas por grid8 y grid16).

## Sanity check (ablacion pgf_mix)

Este bloque verifica la preocupacion clasica de peer review: si el delta=0 en la ablacion es un artefacto.
Se calcula por pares (condicion, grid, seed) en `simbiosis`, comparando `pgf_mix=0.2` vs `pgf_mix=0.0`:

- Pares esperados (condicion x grid x seed): 20 (missing=0)
- reward_env_total diff (m0.2 - m0.0): min=0, max=0, mean=0, unique_diffs~=1
- reward_total diff (m0.2 - m0.0): min=16.8615, max=44.8007, mean=34.4546
- JSON check (por par): reward_env_evol sha256 iguales=20, missing/parse_fail=0, config_pgf_mix_mismatch=0

Interpretacion: en esta implementacion, `pgf_mix` cambia fuertemente `reward_total` (shaping) pero no altera `reward_env_total` para los mismos seeds/grids/condicion, por lo que la ablacion sobre `reward_env_total` produce delta=0.
