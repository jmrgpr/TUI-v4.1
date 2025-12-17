# Estadistica descriptiva e inferencial minima - v11

Fuente: `results/master_results_clean.csv` reconsolidado a partir de los CSV canonicos listados en `results/v11/CANONICAL_DATASET_v11.md`.

El analisis agrupa por `phase`, `agent` y `risk_scale`. Para F2, incluye un bootstrap no parametrico (ver `results/v11/data/bootstrap_stats_v11.csv`) que usa como unidad primaria la media por archivo `*_episodes.csv` (cluster por seed/run) para evitar pseudo-replicacion por episodio.

## Fase `F0_baseline`

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  attack_enabled attack_type                                                                                                                                                                                                         attack_params
    control        0.5  2 -20.017400 1.661984 -22.320792 -17.714008     NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        0.5  2 -24.075600 0.000000 -24.075600 -24.075600     NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        0.5  2  14.867119 0.362039  14.365359  15.368879     NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

## Fase `F1_highrisk`

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  attack_enabled attack_type                                                                                attack_params
    control        1.2 10 -56.828955 0.594532 -57.197450 -56.460460     NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
dqn_control        1.2 10 -60.031100 0.036870 -60.053952 -60.008248     NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
  simbiosis        1.2 10 -13.981472 0.271463 -14.149726 -13.813217     NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False

## Fase `F2_redteam`

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi   p_boot  attack_enabled          attack_type                                                                                                                                                                                                          attack_params
    control        1.2 10 -71.475665 0.639210 -71.871852 -71.079478      NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        1.2 10 -70.448240 1.260934 -71.229775 -69.666705 0.013197            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        1.2 10 -46.005093 7.246183 -50.496324 -41.513862 0.000400            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

## Notas rapidas

- Los p-values (`p_boot`) provienen del bootstrap no parametrico con unidad `run_mean_by_file` (media por seed/run).
- `attack_enabled` esta activo solo para la fase `F2_redteam`; `attack_params` resume los parametros del entorno que habilitan el ataque.
- Los intervalos de confianza son +/-1.96 errores estandar calculados sobre el numero de runs/archivos (`n`), donde cada archivo representa una configuracion (grid, seed).

El conjunto canónico y la comparativa F1/F2 se documentan en `results/v11/CANONICAL_DATASET_v11.md` y `results/v11/data/f2_vs_f1_diff.md`.