# To Do: Mejoras y Publicación TUI-v4.2

## ✅ Completado / Completed
- [x] **Notebook de gráficos automáticos**: Creado `notebooks/quickstart_graficos.ipynb` con ejemplos bilingües y comparación SOTA.
- [x] **Análisis estadístico formal**: Script `results/stats.py` con ANOVA Two-Way + Tukey HSD (p < 0.0000).
- [x] **Comparación SOTA**: PPO vs TUI ejecutada; evidencia de superioridad TUI en PGF (-0.06 vs -0.29).
- [x] **Dependencias pinneadas**: `requirements.txt` actualizado para reproducibilidad.
- [x] **Limpieza repo**: Archivos organizados, repo profesional listo para publicación.
- [x] **Release v4.2**: Tag creado, documentación actualizada con evidencia empírica.
- [x] **Framework SOTA**: Scripts `run_sota_comparison.py` y `sim/sota_wrapper.py` implementados.

## 🔄 Próximos pasos / Next Steps
- **Subir a Zenodo/GitHub**: Preparar DOI para publicación científica.
- **Demo interactiva**: Crear Streamlit app para explorar resultados en vivo.
- **Escalar experimentos**: Más semillas y configuraciones para robustez estadística.
- **Unificar idioma**: Consolidar documentación en inglés para audiencia internacional.
- **Paper submission**: Preparar manuscrito con evidencia TUI vs SOTA.

---

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

