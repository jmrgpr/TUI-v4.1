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

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled attack_type                                                                                attack_params
    control        1.2 10 -56.828955 0.594532 -57.197450 -56.460460     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
dqn_control        1.2 10 -60.031100 0.036870 -60.053952 -60.008248     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
  simbiosis        1.2 10 -13.981472 0.271463 -14.149726 -13.813217     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False

### Fase `F2_redteam`

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi   p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                          attack_params
    control        1.2 10 -71.475665 0.639210 -71.871852 -71.079478      NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        1.2 10 -70.448240 1.260934 -71.229775 -69.666705 0.013197     0.013197            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        1.2 10 -46.005093 7.246183 -50.496324 -41.513862 0.000400     0.000800            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F3`

Nota: F3 se reporta aqui solo como descriptivo agregado. Para el analisis preregistrado (por condicion F1/F2 y pgf_mix, con Holm M=6), ver `results/v11/data/f3_preregistered_report_v11.md`.

      agent risk_scale  n      mean       std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                           attack_params
    control        1.2 20 -64.15231  7.537587 -67.455803 -60.848817     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        1.2 20 -65.23967  5.413948 -67.612437 -62.866903     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        1.2 40 -47.22058 21.572395 -53.905934 -40.535225     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F4`

Nota: F4 fija `F2_redteam` y redefine el endpoint primario como CFR (catastrofes por budget run-level). Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado de CFR (Fisher + Holm) ver `results/v11/data/f4_preregistered_report_v11.md`.

    agent risk_scale  n       mean       std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                          attack_params
  control        1.2 21 -67.119815  5.670546 -69.545147 -64.694482     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 40 -51.837504 18.164448 -57.466725 -46.208283     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F5`

Nota: F5 mantiene high-stakes `B=3` y cambia el endpoint primario a `episodes_completed` (tiempo-hasta-agotar-budget). Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f5_preregistered_report_v11.md`.

    agent risk_scale  n       mean       std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                          attack_params
  control        1.2 11 -62.977111  4.614102 -65.703871 -60.250351     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=123;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 20 -45.117730 20.243781 -53.989959 -36.245502     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=123;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F6`

Nota: F6 mantiene high-stakes `B=3` y vuelve a CFR como endpoint primario, pero calibra `red_team_prob` via un piloto preregistrado (seleccion de p*). Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f6_preregistered_report_v11.md` y el piloto en `results/v11/data/f6_pilot_selection_v11.md`.

    agent risk_scale  n       mean       std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                           attack_params
  control        1.2 11 -60.596146  3.092370 -62.423620 -58.768672     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=123;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 20 -40.572841 21.540708 -50.013472 -31.132209     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=123;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F7`

Nota: F7 calibra el budget `B` -> `B*` para des-saturar el endpoint CFR bajo high-stakes. Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f7_preregistered_report_v11.md` y el piloto B* en `results/v11/data/f7_pilot_selection_v11.md`.

    agent risk_scale  n       mean       std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                           attack_params
  control        1.2 20 -64.408602  1.693598 -65.150854 -63.666350     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=111;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 40 -45.901729 18.999511 -51.789738 -40.013719     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=111;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F8`

Nota: F8 es una replicacion H1-only (S0-H vs C-H) para CFR sin Holm. Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f8_preregistered_report_v11.md`.

    agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                           attack_params
  control        1.2 40 -63.994048 1.365819 -64.417320 -63.570776     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=601;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 40 -62.810082 2.379650 -63.547543 -62.072621     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=601;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `untracked`

     agent risk_scale  n   mean  std  ci95_lo  ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                         attack_params
_tmp_smoke    unknown  2 -60.53  0.0   -60.53   -60.53     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=20;seed=42;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

## Metrica `reward_env_total`

### Fase `F0_baseline`

      agent risk_scale  n     mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled attack_type                                                                                                                                                                                                         attack_params
    control        0.5  2 -20.0174 1.661984 -22.320792 -17.714008     NaN          NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        0.5  2 -24.0756 0.000000 -24.075600 -24.075600     NaN          NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        0.5  2 -22.6649 0.452548 -23.292100 -22.037700     NaN          NaN           False        none grid_size=16;risk_scale=0.5;risk_level=low;pgf_mix=0.2;episodes=100;seed=42;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F1_highrisk`

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled attack_type                                                                                attack_params
    control        1.2 10 -56.828955 0.594532 -57.197450 -56.460460     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
dqn_control        1.2 10 -60.031100 0.036870 -60.053952 -60.008248     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False
  simbiosis        1.2 10 -58.712150 0.337448 -58.921302 -58.502998     NaN          NaN           False        none grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=False

### Fase `F2_redteam`

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi   p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                          attack_params
    control        1.2 10 -71.475665 0.639210 -71.871852 -71.079478      NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        1.2 10 -70.448240 1.260934 -71.229775 -69.666705 0.011598     0.011598            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        1.2 10 -70.183605 1.429226 -71.069448 -69.297762 0.002400     0.004799            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.2;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F3`

Nota: F3 se reporta aqui solo como descriptivo agregado. Para el analisis preregistrado (por condicion F1/F2 y pgf_mix, con Holm M=6), ver `results/v11/data/f3_preregistered_report_v11.md`.

      agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                           attack_params
    control        1.2 20 -64.152310 7.537587 -67.455803 -60.848817     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
dqn_control        1.2 20 -65.239670 5.413948 -67.612437 -62.866903     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
  simbiosis        1.2 40 -64.447878 5.893849 -66.274400 -62.621355     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=False;red_team_prob=0.0;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F4`

Nota: F4 fija `F2_redteam` y redefine el endpoint primario como CFR (catastrofes por budget run-level). Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado de CFR (Fisher + Holm) ver `results/v11/data/f4_preregistered_report_v11.md`.

    agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                          attack_params
  control        1.2 20 -67.256680 5.782161 -69.790824 -64.722537     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 40 -67.752083 3.009114 -68.684617 -66.819548     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=101;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F5`

Nota: F5 mantiene high-stakes `B=3` y cambia el endpoint primario a `episodes_completed` (tiempo-hasta-agotar-budget). Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f5_preregistered_report_v11.md`.

    agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                          attack_params
  control        1.2 10 -62.960222 4.863333 -65.974547 -59.945897     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=123;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 20 -64.596527 1.475884 -65.243362 -63.949692     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=123;red_team=True;red_team_prob=0.1;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F6`

Nota: F6 mantiene high-stakes `B=3` y vuelve a CFR como endpoint primario, pero calibra `red_team_prob` via un piloto preregistrado (seleccion de p*). Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f6_preregistered_report_v11.md` y el piloto en `results/v11/data/f6_pilot_selection_v11.md`.

    agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                           attack_params
  control        1.2 10 -60.874663 3.110817 -62.802768 -58.946559     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=123;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 20 -61.439574 1.219588 -61.974082 -60.905066     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=123;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F7`

Nota: F7 calibra el budget `B` -> `B*` para des-saturar el endpoint CFR bajo high-stakes. Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f7_preregistered_report_v11.md` y el piloto B* en `results/v11/data/f7_pilot_selection_v11.md`.

    agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                           attack_params
  control        1.2 20 -64.408602 1.693598 -65.150854 -63.666350     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=111;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 40 -63.681340 2.478047 -64.449295 -62.913386     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=111;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

### Fase `F8`

Nota: F8 es una replicacion H1-only (S0-H vs C-H) para CFR sin Holm. Este reporte muestra solo descriptivos de recompensa; para el analisis preregistrado ver `results/v11/data/f8_preregistered_report_v11.md`.

    agent risk_scale  n       mean      std    ci95_lo    ci95_hi  p_boot  p_boot_holm  attack_enabled          attack_type                                                                                                                                                                                                           attack_params
  control        1.2 40 -63.994048 1.365819 -64.417320 -63.570776     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=601;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3
simbiosis        1.2 40 -62.810082 2.379650 -63.547543 -62.072621     NaN          NaN            True red_team_adversarial grid_size=16;risk_scale=1.2;risk_level=high;pgf_mix=0.0;episodes=200;seed=601;red_team=True;red_team_prob=0.03;red_team_impact=-1.0;red_team_move_tripwire_prob=0.4;red_team_add_shock_prob=0.3;red_team_block_prob=0.3

## Notas rapidas

- Los p-values (`p_boot`) provienen del bootstrap no parametrico con unidad `run_mean_by_file` (media por seed/run) y se reportan solo para F2 vs control.
- `p_boot_holm` aplica correccion Holm (por metrica) a las comparaciones de F2 vs control.
- `attack_enabled` esta activo para `F2_redteam`, `F4`, `F5`, `F6`, `F7` y `F8` (F4-F8 fijan variantes de F2_redteam); `attack_params` resume los parametros del entorno que habilitan el ataque.
- Para F3, el reporte preregistrado (family primaria Holm M=6) esta en `results/v11/data/f3_preregistered_report_v11.md`.
- Para F4, el reporte preregistrado (endpoint CFR + Holm) esta en `results/v11/data/f4_preregistered_report_v11.md`.
- Para F5, el reporte preregistrado (endpoint episodes_completed + Holm) esta en `results/v11/data/f5_preregistered_report_v11.md`.
- Para F6, el reporte preregistrado (endpoint CFR + McNemar + Holm) esta en `results/v11/data/f6_preregistered_report_v11.md` y el piloto en `results/v11/data/f6_pilot_selection_v11.md`.
- Para F7, el reporte preregistrado (endpoint CFR + McNemar + Holm) esta en `results/v11/data/f7_preregistered_report_v11.md` y el piloto B* en `results/v11/data/f7_pilot_selection_v11.md`.
- Para F8, el reporte preregistrado (endpoint CFR, H1-only sin Holm) esta en `results/v11/data/f8_preregistered_report_v11.md`.
- Los intervalos de confianza son +/-1.96 errores estandar calculados sobre el numero de runs/archivos (`n`), donde cada archivo representa una configuracion (grid, seed).

El conjunto canonico y la comparativa F1/F2 se documentan en `results/v11/CANONICAL_DATASET_v11.md` y `results/v11/data/f2_vs_f1_diff.md`.