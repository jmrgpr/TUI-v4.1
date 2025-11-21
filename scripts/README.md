# scripts/

Utilidades y scripts auxiliares para el proyecto TUI-v4.1. / Utilities and helper scripts.

- `consolidate_results.py`: recorre `results/sweep/fase2`, `results/sota`, `artifacts/phase2`, `reports/phase2` (y rutas extra opcionales) y consolida todos los CSV en `results/master_results.csv` con columnas estandar (agent, seed, episodes, risk_scale, kappa, lambda, mix, pgf_neto, tripwires, robustez, flexibilidad, reward_total, filename). Detecta seeds y algoritmos por ruta/nombre (control/simbiosis/dqn_control/tui/ppo/a2c/dqn/sac/td3).
- `run_full_experiment.py`: automatiza el pipeline completo, parametrizable por CLI (seeds, episodios, PGF, base de salida, stop_on_fail). Flujo: barridos default y tuning (seeds 42/123/456, 200 ep), rerun robustez 500 ep, SOTA, consolidacion. Uso: `python scripts/run_full_experiment.py`.
- `merge_summaries.py`: utilidades de combinacion de resumenes (ver script).
- `fix.py`: script archivado desde la raiz para organizacion.

### Criterios operativos
- Evitar hardcoding: usa CLI o YAML para seeds/episodios/PGF y rutas.
- Abort on critical error: si un comando falla y usas `--stop_on_fail`, el pipeline sale con codigo !=0.
- Los CSV deben incluir `risk` en el nombre para que `risk_scale` se infiera; si no, guardar esa columna en los datos.

### Preflight (recomendado antes de batches largos)
- Plan documentado y firmado.
- Smoke test con 1 seed, 1 riesgo, pocos episodios.
- Rutas limpias y sin duplicados.
- Baselines SOTA: default + tuned light.
- Guardar top-k configs PGF y trazabilidad en `results/master_results.csv`.
