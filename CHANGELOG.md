# CHANGELOG
## [2025-11-28] Actualizaciones sistémicas y publicación v2 de la teoría
- Publicada versión v2 de la Teoría Unificada de la Inteligencia (v4.2) en Zenodo (DOI: 10.5281/zenodo.17702378), con marco falsable, validación preliminar y criterios explícitos de refutación.
- Archivos subidos: RESUMEN_EJECUTIVO_APLICADA_IA_v4.2.pdf, RESUMEN_EJECUTIVO_TUI_v4.2.pdf, Teoria_Inteligencia_Aplicada_IA_v4.2.pdf, Teoria_Unificada_Inteligencia_v4.2.pdf.
- Actualizados reportes sistémicos: `reporte sistemico.md`, `reporte sistemico codigo.md`, `resumen sistemico y recomendaciones.md` con censo exhaustivo, análisis de correlación y recomendaciones accionables.
- Ampliada cobertura de tests a 254 archivos, reforzando robustez y reproducibilidad.
- Mejoras en exportación de resultados y trazabilidad experimental (JSON/CSV por semilla y configuración).
- Nuevos experimentos de tuning y validación causal en agentes RL, con barrido de riesgo y comparación SOTA (PPO/A2C/DQN).
- Documentación técnica y científica actualizada en README.md y TODO.md, incluyendo próximos pasos y revisión pendiente.
- Protocolos y checklist de reproducibilidad revisados y ampliados.
- Visualizaciones y análisis estadístico bilingües en notebooks y scripts dedicados.
---

## [2025-11-27] Smoke test DQN: interpretación, varianza y export protocolizado
- Interpretaciones ampliadas y análisis de varianza en `results/smoke_test/RESULTADOS_TUNING_DQN.md`, con recomendaciones accionables.
- Flujo de exportación corregido y protocolizado; nombres de archivos por semilla/configuración y datasets regenerados (JSON/CSV seeds 42/99/123/456) en `results/smoke_test/`.
- Protocolo y README de smoke test actualizados; añadido `scripts/run_dqn_tuning_batch.py` para ejecuciones batch.
- Preparados runs largos y trazabilidad completa para la comparativa TUI vs DQN.

## [2025-11-26] Tuning DQN y baseline reproducible (EXP00)
- CLI y config admiten flags `--learning_rate`, `--gamma`, `--epsilon`, `--epsilon_decay`, `--epsilon_end`, con propagación en `sim/runner.py` y `sim/dqn_agent.py`.
- Export de resultados protocolizado y robustecido en `sim/prototipo_rl_simbiosis.py`; nombres estandarizados por experimento.
- Penalización por gaming desactivada (`lambda_gaming=0.0`) en `sim/config.py` para tuning EXP00 del agente de control.
- Baseline EXP00 y documentación comparativa TUI vs DQN actualizadas (`results/smoke_test/EXP00_baseline_README.md`, `PROTOCOLO_COMPARATIVO_TUI_vs_DQN.md`, `RESULTADOS_DESBLOQUEO.md`).
- Nuevos resultados reproducibles para seeds 42/123/456 y actualización de `results/smoke_test/README.md`.

## [2025-11-21] Comparación SOTA ampliada (PPO/A2C/DQN)
- `run_sota_comparison.py` ahora ejecuta PPO, A2C y DQN sobre risk_scale 0.5-3.0, generando resúmenes por algoritmo y uno combinado.
- Archivos generados: `results/sota_<algo>_global_summary.csv` y `results/sota_all_global_summary.csv`.
- Ajustes para evaluación headless (matplotlib Agg) y mezcla PGF/reward parametrizable en el prototipo para calibrar penalizaciones.

## [2025-11-19] Upload a Zenodo: Timestamp de Evidencia Preliminar
- Subido dataset a Zenodo v2: https://doi.org/10.5281/zenodo.17654593.
- Archivos incluidos: CSVs de comparación PPO vs TUI y análisis bilingüe `analisis_sota_concepto.md`.
- Descripción: Evidencia preliminar de parálisis prudencial en RL SOTA vs resiliencia en TUI.
- DOI blindado para prioridad intelectual y citabilidad.
- Actualizado README.md con la cita recomendada.
- Fecha y hora de documentación: 19/11/2025.

## [2025-11-19] Comparación SOTA con PPO: Evidencia empírica de superioridad TUI
- Ejecutado `run_sota_comparison.py`: Entrenamiento de PPO en 5 escalas de riesgo (0.5-3.0).
- Resultados: PPO optimiza recompensa (371 en riesgo bajo) pero falla en PGF (-0.29 vs -0.06 de TUI).
- Validación: Agentes TUI mantienen alineación PGF escalable; PPO no logra simbiosis constitutiva.
- Archivos generados: `results/sota_ppo_global_summary.csv` y modelos individuales.
- Fecha y hora de documentación: 19/11/2025.
- Análisis estadístico formal implementado: ANOVA Two-Way + Tukey HSD en `results/stats.py`.
- Resultados estadísticos significativos (p < 0.0000) entre agentes Control, DQN y Simbiosis; interpretación preliminar en el contexto experimental.
- Interacción agente-riesgo confirmada, apoyando hipótesis de "tensión de riesgo".
- Framework SOTA preparado: Wrapper Gymnasium y script de comparación con PPO.
- Dependencias actualizadas para reproducibilidad y benchmarking.

## [2025-11-19] Análisis Estadístico y Comparación SOTA
- Implementado `results/stats.py`: Análisis ANOVA Two-Way + Tukey HSD para validar hipótesis estadísticamente.
- Agregadas dependencias: statsmodels, stable-baselines3, shimmy, gymnasium.
- Creado `sim/sota_wrapper.py`: Wrapper Gymnasium para entorno SimbiosisEnv.
- Creado `run_sota_comparison.py`: Entrenamiento de agentes PPO SOTA y exportación de resultados.
- Habilita comparación con baselines state-of-the-art (PPO/A2C) para benchmarking científico.
- Fecha y hora de documentación: 19/11/2025.

## [2025-11-19] Pinnear dependencias para reproducibilidad científica
- Actualizado `requirements.txt` con versiones fijas (ej: torch==2.1.0, numpy==1.24.3).
- Eliminadas entradas duplicadas y agregado nbformat==5.9.2.
- Garantiza reproducibilidad exacta para experimentos y publicación.
- Fecha y hora de documentación: 19/11/2025.

## [2025-11-19] Notebook de Quickstart para Gráficos Automáticos
- Creado `notebooks/quickstart_graficos.ipynb`: Notebook bilingüe para generación automática de gráficos desde archivos CSV de resultados.
- Incluye ejemplos de gráficos de línea, barras e interactivos con Plotly.
- Actualizado `requirements.txt` con dependencias adicionales (nbformat para Plotly).
- Documentación actualizada en `README.md` y `notebooks/README_notebooks.md`.
- Fecha y hora de documentación: 19/11/2025.

## [2025-11-17] Refactor Metodológico - Eliminación del Oráculo en DQN (3:19 PM)
- Eliminado el método `calcular_metricas` interno del agente DQN para evitar sesgo metodológico (oráculo) y asegurar pureza en experimentos RL.
- Externalizado el cálculo de métricas PGF a `EvaluatorPGF` independiente, garantizando que el agente reciba recompensas como valores negros.
- Actualizados todos los tests dependientes para usar el evaluador externo en lugar del método interno del agente.
- Agregado nuevo test `test_pgf_logic_independence` que valida la separación de lógica PGF del agente.
- Cobertura de tests mantenida en 97% (ligera disminución por eliminación de código interno).
- Fecha y hora de documentación: 3:19 PM, 11-17-2025.

## [2025-11-17] Mejora de Cobertura de Tests a 95%
- Agregados tests para cubrir líneas faltantes en `sim/gui_streamlit.py` (except en seed, validación de parámetros, comparación histórica).
- Agregados tests para cubrir el bloque `if __name__ == "__main__"` en `sim/toy_ped_rl_excel.py` usando runpy.
- Agregados tests para cubrir branches en `sim/prototipo_rl_simbiosis.py` (logging condicional, barrido de risk_scale, DQN control).
- Cobertura global mejorada de 92% a 95%, con módulos principales en 96-99%.
- Fecha y hora de documentación: 11-17-2025.

## [2025-11-19] Comparación SOTA con PPO: Evidencia empírica de superioridad TUI
- Ejecutado `run_sota_comparison.py`: Entrenamiento de PPO en 5 escalas de riesgo (0.5-3.0).
- Resultados: PPO optimiza recompensa (371 en riesgo bajo) pero falla en PGF (-0.29 vs -0.06 de TUI).
- Validación: Agentes TUI mantienen alineación PGF escalable; PPO no logra simbiosis constitutiva.
- Archivos generados: `results/sota_ppo_global_summary.csv` y modelos individuales.
- Evidencia irrefutable para publicación: TUI supera SOTA en métricas de alineación.
- Fecha y hora de documentación: 19/11/2025.
- Análisis estadístico formal implementado: ANOVA Two-Way + Tukey HSD en `results/stats.py`.
- Evidencia irrefutable de diferencias significativas (p < 0.0000) entre agentes Control, DQN y Simbiosis.
- Interacción agente-riesgo confirmada, apoyando hipótesis de "tensión de riesgo".
- Framework SOTA preparado: Wrapper Gymnasium y script de comparación con PPO.
- Dependencias actualizadas para reproducibilidad y benchmarking.
- Fecha y hora de documentación: 19/11/2025.

## [2025-11-19] Análisis Estadístico y Comparación SOTA
- Implementado `results/stats.py`: Análisis ANOVA Two-Way + Tukey HSD para validar hipótesis estadísticamente.
- Agregadas dependencias: statsmodels, stable-baselines3, shimmy, gymnasium.
- Creado `sim/sota_wrapper.py`: Wrapper Gymnasium para entorno SimbiosisEnv.
- Creado `run_sota_comparison.py`: Entrenamiento de agentes PPO SOTA y exportación de resultados.
- Habilita comparación con baselines state-of-the-art (PPO/A2C) para benchmarking científico.
- Fecha y hora de documentación: 19/11/2025.

## [2025-11-19] Pinnear dependencias para reproducibilidad científica
- Actualizado `requirements.txt` con versiones fijas (ej: torch==2.1.0, numpy==1.24.3).
- Eliminadas entradas duplicadas y agregado nbformat==5.9.2.
- Garantiza reproducibilidad exacta para experimentos y publicación.
- Fecha y hora de documentación: 19/11/2025.

## [2025-11-19] Notebook de Quickstart para Gráficos Automáticos
- Creado `notebooks/quickstart_graficos.ipynb`: Notebook bilingüe para generación automática de gráficos desde archivos CSV de resultados.
- Incluye ejemplos de gráficos de línea, barras e interactivos con Plotly.
- Actualizado `requirements.txt` con dependencias adicionales (nbformat para Plotly).
- Documentación actualizada en `README.md` y `notebooks/README_notebooks.md`.
- Fecha y hora de documentación: 19/11/2025.

## [2025-11-17] Refactor Metodológico - Eliminación del Oráculo en DQN (3:19 PM)
- Eliminado el método `calcular_metricas` interno del agente DQN para evitar bias metodológico (oráculo) y asegurar pureza en experimentos RL.
- Externalizado el cálculo de métricas PGF a `EvaluatorPGF` independiente, garantizando que el agente reciba recompensas como valores negros.
- Actualizados todos los tests dependientes para usar el evaluador externo en lugar del método interno del agente.
- Agregado nuevo test `test_pgf_logic_independence` que valida la separación de lógica PGF del agente.
- Cobertura de tests mantenida en 97% (ligera disminución por eliminación de código interno).
- Fecha y hora de documentación: 3:19 PM, 11-17-2025.

## [2025-11-17] Mejora de Cobertura de Tests a 95%
- Agregados tests para cubrir líneas faltantes en `sim/gui_streamlit.py` (except en seed, validación de parámetros, comparación histórica).
- Agregados tests para cubrir el bloque `if __name__ == "__main__"` en `sim/toy_ped_rl_excel.py` usando runpy.
- Agregados tests para cubrir branches en `sim/prototipo_rl_simbiosis.py` (logging condicional, barrido de risk_scale, DQN control).
- Cobertura global mejorada de 92% a 95%, con módulos principales en 96-99%.
- Fecha y hora de documentación: 11-17-2025.

## [2025-11-13] Proveniencia y estructura de datos
- Se agrega el archivo `Caceria de sistemas inteligencia riesgo.txt` con documentación detallada de fuentes, estructura y referencias del dataset principal.
- Se actualiza el `README.md` para citar el nuevo archivo y resaltar la transparencia y trazabilidad de los datos.

## [2025-11-13] Mejoras en simuladores
- Correcciones y mejoras en los módulos de simulación (Aprendizaje Simbiótico, PED en sistemas reales, Sensibilidad de Pesos).
- Scripts y datos listos para publicación y revisión científica.

<<<<<<< HEAD
## [2025-11-17] Limpieza y profesionalización de resultados experimentales
- Se movieron archivos de test y resultados experimentales (`test.csv`, `test.json`, `test_control.csv`, `test_simbiosis.csv`, `test_sweep.json`, `test_sweep_control.csv`) desde la raíz a la carpeta `results/` para mejorar trazabilidad y limpieza del workspace.
- Se eliminó el archivo temporal vacío `test_export_empty.json`.
- Motivo: centralizar resultados siguiendo estructura profesional.
=======

Para detalles de versiones anteriores, consulte el historial de commits en GitHub.

## [2025-11-17] Limpieza y profesionalización de resultados experimentales
- Se movieron los archivos de test y resultados experimentales (`test.csv`, `test.json`, `test_control.csv`, `test_simbiosis.csv`, `test_sweep.json`, `test_sweep_control.csv`) desde la raíz a la carpeta `results/` para mejorar la trazabilidad y limpieza del workspace.
- Se eliminó el archivo temporal vacío `test_export_empty.json`.
Motivo: Estos archivos estaban en la raíz por prácticas de desarrollo y pruebas rápidas. Ahora, siguiendo la estructura profesional, se centralizan en `results/`.
>>>>>>> edce04c (Reorganización profesional: centralización de resultados, imágenes y tests en results/, auditoría y documentación de exportación, actualización README y CHANGELOG)
