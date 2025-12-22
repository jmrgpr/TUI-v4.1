# Estadistica descriptiva e inferencial minima - v11

Fuente: `results/master_results_clean.csv` reconsolidado a partir de los CSV canonicos listados en `results/v11/CANONICAL_DATASET_v11.md`.

El analisis agrupa por `phase`, `agent` y `risk_scale`. Para F2, incluye un bootstrap no parametrico (ver `results/v11/data/bootstrap_stats_v11.csv`) que usa como unidad primaria la media por archivo `*_episodes.csv` (cluster por seed/run) para evitar pseudo-replicacion por episodio.

## Metrica y unidad (muy importante)

- Este reporte incluye dos metricas de recompensa:
  - `reward_total`: promedio por run del campo `Recompensa` en `*_episodes.csv` (recompensa total exportada por episodio).
  - `reward_env_total`: promedio por run de la recompensa ambiental por episodio (sumatoria por step), estimada desde `reward_env_evol` en el JSON del run.
- Para `simbiosis`, `reward_total` puede incluir mezcla con PGF cuando `pgf_mix>0` (reward shaping). Ver `results/v11/ANEXO_TECNICO_v11.md`.
- `n` es el numero de runs/archivos (no episodios).

## Metrica `reward_total`

### Fase `F0_baseline`

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled attack_type                                                                                                                                                                                                         attack_params
    control        0.5  2 -20.017400 1.661984 -22.320792 -17.714008     NaN          NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        0.5  2 -24.075600 0.000000 -24.075600 -24.075600     NaN          NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        0.5  2  14.867119 0.362039  14.365359  15.368879     NaN          NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F1_highrisk`

      agent risk_scale  n       mean       std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled attack_type                                                                                attack_params
    control        1.2 20 -56.828955  0.578675 -57.082570 -56.575340     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
dqn_control        1.2 20 -60.031100  0.035887 -60.046828 -60.015372     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
  simbiosis        1.2 30 -28.891698 21.448609 -36.566984 -21.216412     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False

### Fase `F2_redteam`

      agent risk_scale  n       mean       std    ci95_lo    ci95_hi   p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                          attack_params
    control        1.2 20 -71.475665  0.622162 -71.748339 -71.202991      NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        1.2 20 -70.448240  1.227303 -70.986129 -69.910351 0.013197     0.013197            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        1.2 30 -54.064597 12.946641 -58.697493 -49.431701 0.000400     0.000800            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

## Metrica `reward_env_total`

### Fase `F0_baseline`

      agent risk_scale  n     mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled attack_type                                                                                                                                                                                                         attack_params
    control        0.5  2 -20.0174 1.661984 -22.320792 -17.714008     NaN          NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        0.5  2 -24.0756 0.000000 -24.075600 -24.075600     NaN          NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        0.5  2 -22.6649 0.452548 -23.292100 -22.037700     NaN          NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F1_highrisk`

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled attack_type                                                                                attack_params
    control        1.2 20 -56.828955 0.578675 -57.082570 -56.575340     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
dqn_control        1.2 20 -60.031100 0.035887 -60.046828 -60.015372     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
  simbiosis        1.2 30 -58.712150 0.325604 -58.828666 -58.595634     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False

### Fase `F2_redteam`

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi   p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                          attack_params
    control        1.2 20 -71.475665 0.622162 -71.748339 -71.202991      NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        1.2 20 -70.448240 1.227303 -70.986129 -69.910351 0.011598     0.011598            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        1.2 30 -70.183605 1.379062 -70.677096 -69.690114 0.002400     0.004799            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

## Notas rapidas

- Los p-values (`p_boot`) provienen del bootstrap no parametrico con unidad `run_mean_by_file` (media por seed/run) y se reportan solo para F2 vs control.
- `p_boot_holm` aplica correccion Holm (por metrica) a las comparaciones de F2 vs control.
- `attack_enabled` esta activo solo para la fase `F2_redteam`; `attack_params` resume los parametros del entorno que habilitan el ataque.
- Los intervalos de confianza son +/-1.96 errores estandar calculados sobre el numero de runs/archivos (`n`), donde cada archivo representa una configuracion (grid, seed).

El conjunto canonico y la comparativa F1/F2 se documentan en `results/v11/CANONICAL_DATASET_v11.md` y `results/v11/data/f2_vs_f1_diff.md`.