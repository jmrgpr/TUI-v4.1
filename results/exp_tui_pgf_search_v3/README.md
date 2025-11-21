# Experimento 3 (diseño): búsqueda sistemática PGF para TUI

Estado: diseño (sin corridas aún).  
Objetivo: explorar hiperparámetros PGF para encontrar configuraciones donde TUI supere a los baselines en seguridad + utilidad, manteniendo comparabilidad con los experimentos 1 y 2.

## Variables oficiales (matriz base intacta)
- seeds: [42, 123, 456]
- risk_scale: [0.5, 1.0, 1.5, 2.0, 3.0] (igual que Exp1/Exp2)
- episodes: 200 (mantener igual para comparabilidad; opcional 500 para runs largos)
- métricas registradas: reward_total, tripwires, pgf_neto, robustez, flexibilidad, steps (si el simulador exporta), safety_adj_reward, sau_beta1, sau_beta2
- hiperparámetros PGF: kappa, lambda, mix (a barrer en mallas discretas)
- agente baseline fijo: control, dqn_control, ppo (sin cambios)
- variantes TUI previstas: tui_only, tui_pgf_light, tui_pgf_heavy, más combinaciones nuevas del barrido

## Carperta de resultados
`results/exp_tui_pgf_search_v3/`  
Se crearán subcarpetas para runs crudos, plots y logs cuando se lancen las corridas.

## Plan (borrador)
1) Barrido grosero de kappa/lambda/mix en mallas discretas (p. ej., kappa ∈ {0.5,1.0,1.5,2.0}, lambda ∈ {0.05,0.1,0.2}, mix ∈ {0.3,0.5,0.8}) con seeds/risks/episodes fijos.
2) Consolidar con `scripts/consolidate_results.py` (ya soporta safety_adj_reward y sau_beta1/2).
3) Seleccionar top configs según safety_adj_reward o sau_beta2 (prioriza menor tripwires). Opcional: Pareto seguridad–utilidad.
4) Barrido fino en la región top (zoom).
5) Plots/README actualizados con hallazgos comparables a Exp1/Exp2.

## Scripts
- `scripts/run_search_pgf.py` (placeholder en este repo): definirá mallas de hiperparámetros, generará comandos para `sim/prototipo_rl_simbiosis.py` y llamará al consolidado. A implementar cuando arranquen las corridas.

## Reglas de comparabilidad
- No cambiar seeds/risks/episodes base.
- Misma convención de nombres de CSV: incluir risk, seed, agente, episodes, kappa, lambda, mix en el nombre/path.
- Consolidar con el mismo script para que las métricas sean comparables con Exp1 y Exp2.
