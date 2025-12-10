# Actualización de documentación sobre agentes SOTA

Fecha: 25/11/2025

## Estado de la integración SOTA en Experimento2

- Los agentes SOTA PPO, A2C y DQN fueron ejecutados y sus resultados están presentes en la carpeta `results/Experimento2`.
- Los archivos `sota_ppo_riskX.X_summary.csv`, `sota_a2c_riskX.X_summary.csv`, y `sota_dqn_riskX.X_summary.csv` contienen los resultados para cada algoritmo y nivel de riesgo.
- El archivo `sota_dqn_global_summary.csv` consolida los resultados globales de DQN SOTA.
- Los scripts responsables de la ejecución SOTA son `scripts/run_sota_a2c_dqn.py` y el pipeline `scripts/run_full_experiment.py`.
- La documentación previa no reflejaba explícitamente la presencia de estos resultados, pero ahora queda aclarado y documentado.

## Recomendación

- Se recomienda revisar periódicamente la integración y análisis de los resultados SOTA en el notebook principal y en los informes generados.
- Si se agregan nuevos algoritmos SOTA, actualizar esta documentación y los scripts correspondientes.

---

Esta actualización garantiza que la presencia y documentación de los agentes SOTA en el proyecto quede clara y trazable para futuras revisiones y análisis.
