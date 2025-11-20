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

## [2025-11-19] Upload a Zenodo: Timestamp de Evidencia Preliminar
- Subido dataset a Zenodo v2: https://doi.org/10.5281/zenodo.17654593
- Archivos incluidos: CSVs de comparacion PPO vs TUI, analisis bilingue `analisis_sota_concepto.md`.
- Descripcion: Evidencia preliminar de paralisis prudencial en RL SOTA vs resiliencia en TUI.
- DOI blindado para prioridad intelectual y citabilidad.
- Actualizado README.md con nueva cita recomendada.
- Fecha y hora: 19/11/2025.

## [2025-11-19] Comparacion SOTA con PPO: Evidencia empirica de superioridad TUI
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

## [2025-11-17] Refactor Metodológico - Eliminación del Oráculo en DQN (3:19 PM)
- Eliminado el método `calcular_metricas` interno del agente DQN para evitar sesgo metodológico (oráculo) y asegurar pureza en experimentos RL.
- Externalizado el cálculo de métricas PGF a `EvaluatorPGF` independiente, garantizando que el agente reciba recompensas como valores negros.
- Actualizados todos los tests dependientes para usar el evaluador externo en lugar del método interno del agente.
- Agregado nuevo test `test_pgf_logic_independence` que valida la separación de lógica PGF del agente.
- Cobertura de tests mantenida en 97% (ligera disminución por eliminación de código interno).
- Fecha y hora de documentación: 3:19 PM, 11-17-2025.

## [2025-11-17] Mejora de Cobertura de Tests a 95%
- Agregados tests para cubrir lineas faltantes en `sim/gui_streamlit.py` (except en seed, validacion de parametros, comparacion historica).
- Agregados tests para cubrir el bloque `if __name__ == "__main__"` en `sim/toy_ped_rl_excel.py` usando runpy.
- Agregados tests para cubrir branches en `sim/prototipo_rl_simbiosis.py` (logging condicional, barrido de risk_scale, DQN control).
- Cobertura global mejorada de 92% a 95%, con modulos principales en 96-99%.
- Fecha y hora de documentacion: 11-17-2025.

## [2025-11-13] Proveniencia y estructura de datos
- Se agrega el archivo `Caceria de sistemas inteligencia riesgo.txt` con documentación detallada de fuentes, estructura y referencias del dataset principal.
- Se actualiza el `README.md` para citar el nuevo archivo y resaltar la transparencia y trazabilidad de los datos.

## [2025-11-13] Mejoras en simuladores
- Correcciones y mejoras en los modulos de simulacion (Aprendizaje Simbiotico, PED en sistemas reales, Sensibilidad de Pesos).
- Scripts y datos listos para publicacion y revision cientifica.

## [2025-11-17] Limpieza y profesionalización de resultados experimentales
- Se movieron archivos de test y resultados experimentales (`test.csv`, `test.json`, `test_control.csv`, `test_simbiosis.csv`, `test_sweep.json`, `test_sweep_control.csv`) desde la raíz a la carpeta `results/` para mejorar trazabilidad y limpieza del workspace.
- Se eliminó el archivo temporal vacío `test_export_empty.json`.
- Motivo: centralizar resultados siguiendo estructura profesional.

Para detalles de versiones anteriores, consulte el historial de commits en GitHub.
