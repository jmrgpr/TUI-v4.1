# Experimento TUI + PGF vs SOTA (2025)

## Resumen técnico
- Pipeline completado sin errores críticos; master y log generados.
- Agentes presentes: simbiosis (TUI+PGF), control, dqn_control, ppo, tui (solo summaries). Riesgos 0.5, 1.0, 1.5, 2.0, 3.0.

## Resultados científicos
- **PGF_neto y tripwires:** DQN-Control supera a TUI+PGF en reward y empata/ligeramente gana en PGF_neto/tripwires. No hay señal de superioridad general de TUI+PGF.
- **Tuning PGF:** kappa=2.0, lambda=0.05, mix=0.8 evita la parálisis: TUI pasa de recompensa muy baja a comportamiento competitivo.
- **Seguridad en riesgo alto:** TUI+PGF tuning logra menos tripwires que DQN-Control en riesgo alto, a costa de recompensa. Apoya la prudencia constitutiva en escenarios de seguridad.
- **PPO:** No es baseline fiable en este master (posible política de inacción).
- **Limitaciones:** El master no incluye robustez/flexibilidad ni metadata de tuning vs default/rerun; riesgo se infiere del filename; SOTA incompleto (no A2C, PPO inconsistente).

## Próximos pasos recomendados
1. Reconsolidar capturando episodes/kappa/lambda/mix, robustez y flexibilidad, y marcar config (default/tuning/rerun).
2. Homogeneizar export SOTA (PPO/A2C/DQN) con reward/tripwires comparables por seed/riesgo.
3. Reanalizar con estadística (IC95%, MW + Holm/FDR, tamaños de efecto) y, si procede, ablation TUI sin PGF o PGF menos severo.

## Estructura
- `master_results.csv`: resultados consolidados reales.
- `experiment_log.txt`: log real del pipeline.
- `analysis_phase2.ipynb`: notebook de análisis/visualización (copia del notebook real).
- `plots/`: gráficas/tablas generadas (ejecutar el notebook).
- `README_estructura.md`: guía de organización de esta carpeta.
- `README.md`: este resumen.

---

# TUI + PGF vs SOTA Experiment (2025)

## Technical summary
- Pipeline completed without critical errors; master and log generated.
- Agents present: symbiosis (TUI+PGF), control, dqn_control, ppo, tui (summaries only). Risks 0.5–3.0.

## Scientific results
- **PGF_neto and tripwires:** DQN-Control beats TUI+PGF on reward and matches/slightly wins on PGF_neto/tripwires; no clear superiority of TUI+PGF overall.
- **PGF tuning:** kappa=2.0, lambda=0.05, mix=0.8 avoids paralysis; TUI moves from very low reward to competitive behavior.
- **High-risk safety:** Tuned TUI+PGF triggers fewer tripwires than DQN-Control at high risk, sacrificing reward—supports prudence for safety-prioritized settings.
- **PPO:** Not a reliable baseline here (possible inaction policy).
- **Limitations:** Master lacks robustness/flexibility and config metadata; risk inferred from filename; SOTA incomplete (no A2C, PPO inconsistent).

## Next steps
1. Re-consolidate capturing episodes/kappa/lambda/mix, robustness/flexibility, and config flags (default/tuning/rerun).
2. Homogenize SOTA export (PPO/A2C/DQN) with comparable reward/tripwires per seed/risk.
3. Re-analyze with statistics (CI95%, MW + Holm/FDR, effect sizes) and, if needed, ablation TUI without PGF or softer PGF.

## Folder structure
- `master_results.csv`: consolidated results (real).
- `experiment_log.txt`: pipeline log (real).
- `analysis_phase2.ipynb`: analysis/visualization notebook (copied from notebooks).
- `plots/`: generated plots/tables (run the notebook).
- `README_estructura.md`: folder organization guide.
- `README.md`: this summary.
