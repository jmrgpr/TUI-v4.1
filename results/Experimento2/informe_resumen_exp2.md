Informe rápido del Experimento 2 (Exp2)
=======================================

Fuente de datos
---------------
- Archivo usado: `results/Experimento2/master_results_clean.csv`.
- Contiene episodios por fila para agentes: `control`, `dqn_control`, `simbiosis`, `tui`.
- Riesgos: 0.5, 1.0, 1.5, 2.0, 3.0. Seeds: 42/123/456.
- No incluye métricas `robustez`/`flexibilidad` ni resultados SOTA (A2C/DQN/PPO); solo recompensas y tripwires por agente.

Resumen numérico (media por agente y riesgo)
--------------------------------------------
- **control**: recompensa ~ -3.2 a -4.0 al subir riesgo; tripwires muy bajos (0–3 máx, medias ~0.1–0.2).
- **dqn_control**: recompensa ~ -7.0 a -12.6; tripwires algo mayores (máx 5–10, medias ~0.2–0.4); alta dispersión con outliers negativos.
- **simbiosis**: recompensa ~ -25 a -27; tripwires hasta 10; varianza muy alta con outliers severos.
- **tui**: recompensa ~ -10.8 a -11.9; tripwires bajos (máx 2–4, medias ~0.1–0.3); variabilidad moderada.

Conclusiones con las métricas disponibles
-----------------------------------------
- En recompensa, **control** > **tui** ≈ **dqn_control** > **simbiosis**.
- En seguridad (tripwires), **control** y **tui** son los más seguros; **dqn_control** algo peor; **simbiosis** el más arriesgado.
- No es posible evaluar **robustez/flexibilidad** ni comparar contra SOTA porque esas métricas/datos no están en este master.

Limitaciones y trabajo pendiente
--------------------------------
1) Reexportar resultados SOTA (A2C/DQN/PPO) con metadatos completos (`seed`, `risk_level`, `red_team`, `episodes`, `steps_per_episode`) y métricas `robustez`/`flexibilidad`.  
2) Reconsolidar el master incluyendo SOTA y las métricas faltantes.  
3) Reejecutar el notebook de análisis apuntando al nuevo master para obtener comparativas completas (recompensa, tripwires, robustez, flexibilidad) y gráficos.

Qué hacer para cerrar el análisis
---------------------------------
- Ejecutar de nuevo los scripts SOTA con la versión corregida (`scripts/run_sota_a2c_dqn.py` y, si aplica, `run_sota_comparison.py`) para generar CSV por seed/riesgo.  
- Reconsolidar: `python scripts/consolidate_results.py --extra_paths results/Experimento2/data/sweep/fase2_full results/Experimento2/data/sota results/Experimento2`.  
- Actualizar el notebook `results/Experimento2/analisis_experimento2.ipynb` para leer el master reconsolidado y añadir gráficos de robustez/flexibilidad si las columnas están presentes.
