# Experimento 2: Causalidad, Prudencia y Propósito en TUI v4.2

## Objetivos
- Evaluar la causalidad de P_riesgo sobre el desempeño operativo (I_op), prudencia/anti-Goodhart, IPG (propósito) y robustez fuera de muestra.
- Comparar variantes TUI/PGF contra baselines SOTA (PPO, A2C, DQN) en entornos de riesgo variable.

## Diseño Experimental
- **Cohorts:** control (riesgo bajo/fijo) vs intervención (riesgo alto/dinámico).
- **Variantes:** tui_only, pgf_light, pgf_heavy, PPO, A2C, DQN.
- **Parámetros sugeridos:** multiseed (42, 123, 456), ≥1000 episodios por entorno/configuración.
- **Entornos:** base y red team adaptativo.

## Proceso de Ejecución
1. Preparar entorno limpio y dependencias.
2. Ejecutar el batch con el comando:
   ```
   python scripts/run_full_experiment.py --seeds 42 123 456 --episodes 1000 --risk_scales 0.5 1.0 --variants tui_only pgf_light pgf_heavy --sota ppo a2c dqn --sigma_thr ... --gamma ... --lambda_G ... --red_team on/off --output_prefix results/exp_tui_experiment2_full/...
   ```
3. Consolidar resultados con `scripts/consolidate_results.py`.
4. Analizar y visualizar con el notebook de análisis.

## Estructura de Resultados
- `master_results.csv`: datos consolidados de todos los runs (se generará al correr el batch).
- `experiment_log.txt`: log de ejecución y parámetros (se generará al correr el batch).
- `plots/`: gráficos y tablas generados (pendiente).
- CSVs individuales por variante, seed y entorno.

## Métricas y Columnas Clave
- PGF_neto, tripwires, reward_total, robustez, flexibilidad, IPG.
- Gap proxy↔valor, MTTD, MTTR, rollback%.
- Flags de intervención de riesgo y propósito, parámetros de prudencia (sigma_thr, gamma, lambda_G), indicadores de gating/gaming.

## Reproducibilidad
- Versiones de scripts y dependencias documentadas en `requirements.txt` y `environment.yml`.
- Parámetros y configuración exportados en los logs.

## Notas
- Este README describe el diseño y ejecución esperada del experimento 2. Los batch completos aún no se han corrido; al ejecutarlos se crearán los archivos mencionados.
- Para dudas o reproducibilidad, contactar al autor principal.
