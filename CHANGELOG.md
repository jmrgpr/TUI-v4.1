# CHANGELOG

## [2025-11-19] Upload a Zenodo: Timestamp de Evidencia Preliminar
- Subido dataset a Zenodo v2: https://doi.org/10.5281/zenodo.17654593
- Archivos incluidos: CSVs de comparacion PPO vs TUI, analisis bilingue `analisis_sota_concepto.md`.
- Descripcion: Evidencia preliminar de paralisis prudencial en RL SOTA vs resiliencia en TUI.
- DOI blindado para prioridad intelectual y citabilidad.
- Actualizado README.md con nueva cita recomendada.
- Fecha y hora: 19/11/2025.

-## [2025-11-19] Comparacion SOTA con PPO: Evidencia empirica de superioridad TUI
- Ejecutado `run_sota_comparison.py`: Entrenamiento de PPO en 5 escalas de riesgo (0.5-3.0).
- Resultados: PPO optimiza recompensa (371 en riesgo bajo) pero falla en PGF (-0.29 vs -0.06 de TUI).
- Validacion: Agentes TUI mantienen alineacion PGF escalable; PPO no logra simbiosis constitutiva.
- Archivos generados: `results/sota_ppo_global_summary.csv` y modelos individuales.
- Fecha y hora de documentacion: 19/11/2025.
- Analisis estadistico formal implementado: ANOVA Two-Way + Tukey HSD en `results/stats.py`.
- Resultados estadisticos significativos (p < 0.0000) entre agentes Control, DQN y Simbiosis; interpretacion preliminar en el contexto experimental.
- Interaccion agente-riesgo confirmada, apoyando hipotesis de "tension de riesgo".
- Framework SOTA preparado: Wrapper Gymnasium y script de comparacion con PPO.
- Dependencias actualizadas para reproducibilidad y benchmarking.

## [2025-11-21] Comparacion SOTA ampliada (PPO/A2C/DQN)
- `run_sota_comparison.py` ahora ejecuta PPO, A2C y DQN sobre risk_scale 0.5-3.0, generando resumentes por algoritmo y uno combinado.
- Archivos generados: `results/sota_<algo>_global_summary.csv` y `results/sota_all_global_summary.csv`.
- Ajustes para evaluacion headless (matplotlib Agg) y mezcla PGF/reward parametrizable en el prototipo para calibrar penalizaciones.

## [2025-11-19] Analisis Estadistico y Comparacion SOTA
- Implementado `results/stats.py`: Analisis ANOVA Two-Way + Tukey HSD para validar hipotesis estadisticamente.
- Agregadas dependencias: statsmodels, stable-baselines3, shimmy, gymnasium.
- Creado `sim/sota_wrapper.py`: Wrapper Gymnasium para entorno SimbiosisEnv.
- Creado `run_sota_comparison.py`: Entrenamiento de agentes PPO SOTA y exportacion de resultados.
- Habilita comparacion con baselines state-of-the-art (PPO/A2C) para benchmarking cientifico.
- Fecha y hora de documentacion: 19/11/2025.

## [2025-11-19] Pinnear dependencias para reproducibilidad cientifica
- Actualizado `requirements.txt` con versiones fijas (ej: torch==2.1.0, numpy==1.24.3).
- Eliminadas entradas duplicadas y agregado nbformat==5.9.2.
- Garantiza reproducibilidad exacta para experimentos y publicacion.
- Fecha y hora de documentacion: 19/11/2025.

## [2025-11-19] Notebook de Quickstart para Graficos Automaticos
- Creado `notebooks/quickstart_graficos.ipynb`: Notebook bilingue para generacion automatica de graficos desde archivos CSV de resultados.
- Incluye ejemplos de graficos de linea, barras e interactivos con Plotly.
- Actualizado `requirements.txt` con dependencias adicionales (nbformat para Plotly).
- Documentacion actualizada en `README.md` y `notebooks/README_notebooks.md`.
- Fecha y hora de documentacion: 19/11/2025.

## [2025-11-17] Refactor Metodologico - Eliminacion del Oraculo en DQN (3:19 PM)
- Eliminado el metodo `calcular_metricas` interno del agente DQN para evitar sesgo metodologico (oraculo) y asegurar pureza en experimentos RL.
- Externalizado el calculo de metricas PGF a `EvaluatorPGF` independiente, garantizando que el agente reciba recompensas como valores negros.
- Actualizados todos los tests dependientes para usar el evaluador externo en lugar del metodo interno del agente.
- Agregado nuevo test `test_pgf_logic_independence` que valida la separacion de logica PGF del agente.
- Cobertura de tests mantenida en 97% (ligera disminucion por eliminacion de codigo interno).
- Fecha y hora de documentacion: 3:19 PM, 11-17-2025.

## [2025-11-17] Mejora de Cobertura de Tests a 95%
- Agregados tests para cubrir lineas faltantes en `sim/gui_streamlit.py` (except en seed, validacion de parametros, comparacion historica).
- Agregados tests para cubrir el bloque `if __name__ == "__main__"` en `sim/toy_ped_rl_excel.py` usando runpy.
- Agregados tests para cubrir branches en `sim/prototipo_rl_simbiosis.py` (logging condicional, barrido de risk_scale, DQN control).
- Cobertura global mejorada de 92% a 95%, con modulos principales en 96-99%.
- Fecha y hora de documentacion: 11-17-2025.

## [2025-11-13] Proveniencia y estructura de datos
- Se agrega el archivo `Caceria de sistemas inteligencia riesgo.txt` con documentacion detallada de fuentes, estructura y referencias del dataset principal.
- Se actualiza el `README.md` para citar el nuevo archivo y resaltar la transparencia y trazabilidad de los datos.

## [2025-11-13] Mejoras en simuladores
- Correcciones y mejoras en los modulos de simulacion (Aprendizaje Simbiotico, PED en sistemas reales, Sensibilidad de Pesos).
- Scripts y datos listos para publicacion y revision cientifica.

## [2025-11-17] Limpieza y profesionalizacion de resultados experimentales
- Se movieron archivos de test y resultados experimentales (`test.csv`, `test.json`, `test_control.csv`, `test_simbiosis.csv`, `test_sweep.json`, `test_sweep_control.csv`) desde la raiz a la carpeta `results/` para mejorar trazabilidad y limpieza del workspace.
- Se elimino el archivo temporal vacio `test_export_empty.json`.
- Motivo: centralizar resultados siguiendo estructura profesional.
