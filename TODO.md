# To Do: Mejoras y Publicacion TUI-v4.2

Este To Do refleja el avance hacia evidencia empirica preliminar de alineacion escalable via Simbiosis Constitutiva y los siguientes pasos para robustez, reproducibilidad y publicacion.

## Proximos pasos ampliados

### Expansion y robustez experimental
- Expandir experimentos a mas semillas y episodios (robustez estadistica y validacion cruzada).
- Agregar comparacion con A2C, DQN y (si se soporta) SAC; framework SOTA ya extendido, falta ejecucion/analisis.
- Planificar experimentos en benchmarks mas complejos (MuJoCo, Procgen, etc.).
- Documentar y automatizar la exportacion de resultados para auditoria y reproducibilidad.

### Visualizacion y analisis
- Mejorar visualizaciones y analisis estadistico: mas metricas, graficos avanzados, interpretacion bilingue.
- Mantener y ampliar el notebook de graficos automaticos (`notebooks/quickstart_graficos.ipynb`).

### Infraestructura y reproducibilidad
- Subir a Zenodo/GitHub: preparar DOI para publicacion cientifica.
- Evaluar integracion de Dockerfile para despliegue y replicacion.
- Revisar y actualizar el protocolo de reproducibilidad y checklist de publicacion.
- Mantener cobertura de tests y agregar pruebas para nuevos modulos/algoritmos.

### Documentacion y publicacion
- Consolidar documentacion bilingue y preparar version en ingles para publicacion internacional.
- Preparar materiales de onboarding cientifico y colaborativo.
- Redactar manuscrito con evidencia TUI vs SOTA para envio a revista/conferencia.

### Revisión pendiente (documentos sistémicos, 2025-11-28)
- Completar censo exhaustivo (detallar reports/, results/ completos, htmlcov/, session_runs.json, None.json, temp.tex).
- Añadir en `resumen sistemico y recomendaciones.md` los datos de correlación: n, método (Pearson/Spearman), IC/SE, control de múltiples comparaciones y versión de dataset/experimento.
- Citar módulos/tests que respaldan la alineación teoría↔código (p.ej., sim/environment.py con PED, tests de penalizaciones/riesgo).
- Hacer recomendaciones accionables con parámetros/fechas/responsables (p.ej., preregistro en OSF con ID, grid de β_riesgo, bootstrap B, AIC/BIC).
- Notar que el conteo de tests (254) es al 2025-11-28; actualizar si crece.
