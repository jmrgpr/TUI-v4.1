# Bootstrap no parametrico (cluster por seed/run) - v11

Este bootstrap estima la diferencia de medias vs `control` usando como unidad primaria el promedio por archivo (`*_episodes.csv`).
Se excluyen `results/v11/F2_redteam/raw` y `results/v11/archived` para evitar duplicados.

Parametros: B=5000, seed=2025.

Metricas:
- `reward_total`: media de la columna `Recompensa` (recompensa total exportada; para Simbiosis puede incluir mezcla con PGF).
- `reward_env_total`: recompensa ambiental por episodio (sumatoria por step) estimada desde `reward_env_evol` en el JSON del run.

     phase  risk_scale           metric       agent  mean_diff   ci95_lo   ci95_hi   p_boot  p_boot_holm  n_agent  n_control             unit    B
F2_redteam         1.2     reward_total dqn_control   1.027425  0.223485  1.870914 0.013197     0.013197       10         10 run_mean_by_file 5000
F2_redteam         1.2     reward_total   simbiosis  25.470572 21.233820 29.885995 0.000400     0.000800       10         10 run_mean_by_file 5000
F2_redteam         1.2 reward_env_total dqn_control   1.027425  0.247111  1.857824 0.011598     0.011598       10         10 run_mean_by_file 5000
F2_redteam         1.2 reward_env_total   simbiosis   1.292060  0.387671  2.172688 0.002400     0.004799       10         10 run_mean_by_file 5000