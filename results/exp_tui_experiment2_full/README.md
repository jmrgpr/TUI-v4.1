# Experimento 2: Causalidad, Prudencia y Proposito (TUI v4.2)

## Objetivo previsto
- Medir impacto de PGF/TUI sobre I_op, prudencia/anti-Goodhart, IPG y robustez out-of-sample.
- Comparar TUI/PGF (tui_only, pgf_light, pgf_heavy) contra baselines SOTA (PPO, A2C, DQN) en riesgos variables y con red team.

## Estado actual (24-11-2025)
- Este README es solo el plan: **no hay CSV, plots ni `master_results.csv` en este folder**.
- `scripts/run_full_experiment.py` hoy solo lanza variantes con `--dqn_control` (control/dqn_control/simbiosis); no ejecuta TUI/PGF puro.
- `scripts/run_ablation_quick.py` define TUI/PGF (tui_only, tui_pgf_light, tui_pgf_heavy con risk_scale), pero **no se ha ejecutado** (`results/sweep/fase2_instrumented` no existe).
- No hay evidencia de validacion causal (A/B/C) ni red team real; el entorno solo incluye red team sintetico.

## Que falta para completar el experimento
1) **Correr TUI/PGF sin DQN**: ejecutar `sim/prototipo_rl_simbiosis.py` con `--pgf_kappa/--pgf_lambda/--pgf_mix --risk_scale ...` y sin `--dqn_control`.
2) **Barridos multiseed/risk**: seeds [42,123,456], riesgos [0.5,1.0,1.5,2.0,3.0], episodios >=200 (y >=500/1000 para robustez).
3) **Baselines SOTA**: correr PPO/A2C/DQN (ej. `run_sota_comparison.py`) con la misma malla de seeds/risks.
4) **Red team**: repetir corridas con `--red_team` para medir robustez adversarial (actualmente solo generativo, sin humanos/bots).
5) **Consolidar**: `python scripts/consolidate_results.py` apuntando a las carpetas generadas para producir `results/master_results.csv`.
6) **Visualizar/reportar**: generar curvas de riesgo, boxplots e IPG, y guardar en este folder.

## Comandos rapidos sugeridos
- Ablacion TUI (smoke, 1 seed/2 riesgos):  
  `python scripts/run_ablation_quick.py --test`
- Ablacion completa TUI:  
  `python scripts/run_ablation_quick.py`
- Consolidar despues de cualquier batch:  
  `python scripts/consolidate_results.py`

## Logistica
- Guardar salidas en `results/exp_tui_experiment2_full/<subcarpeta>` o `results/sweep/fase2_instrumented`.
- Adjuntar `experiment_log.txt` y `master_results.csv` tras las corridas.
- Documentar hiperparametros usados (kappa/lambda/mix, sigma_thr, gamma_lcb, lambda_gaming) y modos (con/sin red_team).
