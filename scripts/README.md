# scripts/ (menú rápido) [ENGLISH]

Utilidades y runners para TUI-v4.1.

## Experimentos
- **Exp1 (baseline sweep)**: `sim/prototipo_rl_simbiosis.py --risk_sweep ...`  
  *Incluye control/dqn_control/simbiosis.*  
  Salidas típicas: `results/sweep/fase1` o `results/sweep/fase2/...`.

- **Exp2 (TUI/PGF instrumentado)**:
  - Rápido: `python scripts/run_ablation_quick.py [--test]` (tui_only, tui_pgf_light, tui_pgf_heavy con seeds/risks predefinidos).
  - Pipeline completo: `python scripts/run_full_experiment.py` (barridos default/tuning con dqn_control + bloque `sweep_tui` para TUI/PGF puro + robustez + SOTA + consolidado). Usa `--stop_on_fail`, `--output_base` y flags PGF/risks/red_team según sea necesario.

- **Exp3 (búsqueda PGF)**: `scripts/run_search_pgf.py` (placeholder; definir grids y activar ejecución cuando se apruebe).

## Consolidado
- `consolidate_results.py`: recorre `results/sweep/fase2`, `results/sota`, `artifacts/phase2`, `reports/phase2` (y rutas extra opcionales) y escribe `results/master_results.csv` con columnas estándar (agent, seed, episodes, risk_scale, kappa, lambda, mix, pgf_neto, tripwires, robustez, flexibilidad, reward_total, filename). Detecta seeds/algoritmos por ruta/nombre (control/simbiosis/dqn_control/tui/ppo/a2c/dqn/sac/td3). Asegura que los CSV tengan `risk` en el nombre o columna `risk_scale`.

## Utilidades
- `merge_summaries.py`: utilidades de combinación de resúmenes.
- `fix.py`: script archivado.

## Preflight recomendado
- Smoke test: 1 seed, 1-2 riesgos, pocos episodios; verificar que se generen CSV con `risk_scale`.
- Usar `--stop_on_fail` si quieres abortar en errores.
- Fijar seeds y `PYTHONIOENCODING=utf-8`; cerrar figuras matplotlib si corres muchos plots.
