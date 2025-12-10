# To Do: Mejoras y Publicacion TUI-v4.2

Este To Do refleja el avance hacia evidencia empirica preliminar de alineacion escalable via Simbiosis Constitutiva y los siguientes pasos para robustez, reproducibilidad y publicacion.

## ✅ COMPLETADO (1 dic 2025)

### Smoke Test Fix (Fase 1)
- ✅ Diagnóstico problema pgf_mix: agentes simbiosis/TUI bloqueados (0/2000 ep >0)
- ✅ Causa raíz identificada: PGF_Neto negativo con pgf_mix=1.0 en entorno benigno
- ✅ Solución validada: 3 experimentos (pgf_mix 0.0/0.2/0.5) → 100% éxito
- ✅ Documentación exhaustiva: INDEX.md, DIAGNOSTICO, RESULTADOS_FIX_PGF_MIX, PLAN_ACCION
- ✅ Commit f9b8972: 9 MD files + 3 CSV fix + análisis completo
- ✅ Default pgf_mix actualizado: 1.0 → 0.2 en prototipo_rl_simbiosis.py
- ✅ Scripts automatización: run_validation_long.ps1 + analyze_validation_long.py
- ✅ Commit 2ca8159: Fase 2 iniciada, scripts listos

## 🔄 EN PROGRESO

### Validación Estadística Robusta (Fase 2)
- ⏳ Ejecutar runs largos: 1000 ep × 3 seeds (scripts creados, pendiente ejecución)
- ⏳ Análisis estadístico: convergencia, intervalos confianza, t-tests
- ⏳ Reporte VALIDATION_REPORT.md automático
- ⏳ Gráficos convergencia DOI-ready

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
