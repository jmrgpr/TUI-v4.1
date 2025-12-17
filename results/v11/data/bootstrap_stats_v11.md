# Bootstrap no parametrico (cluster por seed/run) - v11

Este bootstrap estima la diferencia de medias vs `control` usando como unidad primaria el promedio por archivo (`*_episodes.csv`).
Se excluyen `results/v11/F2_redteam/raw` y `results/v11/archived` para evitar duplicados.

Parametros: B=5000, seed=2025.

     phase  risk_scale       agent  mean_diff   ci95_lo   ci95_hi   p_boot  n_agent  n_control             unit    B
F2_redteam         1.2 dqn_control   1.027425  0.223485  1.870914 0.013197       10         10 run_mean_by_file 5000
F2_redteam         1.2   simbiosis  25.470572 21.233820 29.885995 0.000400       10         10 run_mean_by_file 5000