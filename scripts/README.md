# scripts/

Utilidades y scripts auxiliares para el proyecto TUI-v4.1.

- `consolidate_results.py`: recorre `results/sweep/fase2`, `results/sota`, `artifacts/phase2` y `reports/phase2` para consolidar todos los CSV en `results/master_results.csv` con columnas estándar (agent, seed, episodes, risk_scale, kappa, lambda, mix, pgf_neto, tripwires, robustez, flexibilidad, reward_total, filename). Detecta seeds y algoritmos (control/simbiosis/dqn_control/tui/ppo/a2c/dqn/sac/td3) por ruta/nombre.
- `merge_summaries.py`: utilidades de combinación de resúmenes (ver script para uso).
- `fix.py`: script archivado desde la raíz para organización.
