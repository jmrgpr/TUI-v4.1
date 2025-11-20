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


Este To Do actualizado refleja el progreso hacia evidencia empírica preliminar de alineación escalable vía Simbiosis Constitutiva.

---

## 🔄 Próximos pasos ampliados / Expanded Next Steps

### Expansión y robustez experimental
- Expandir experimentos a más semillas y episodios (mayor robustez estadística y validación cruzada).
- Agregar comparación con algoritmos A2C y SAC (framework SOTA ya preparado, falta ejecución y análisis).
- Planificar experimentos adicionales con benchmarks más complejos (MuJoCo, Procgen, etc.).
- Documentar y automatizar la exportación de resultados para facilitar auditoría y reproducibilidad.

### Visualización y análisis
- Mejorar visualizaciones y análisis estadístico: agregar más métricas, gráficos avanzados y interpretación bilingüe.
- Mantener y ampliar el notebook de gráficos automáticos (`notebooks/quickstart_graficos.ipynb`).

### Infraestructura y reproducibilidad
- Subir a Zenodo/GitHub: preparar DOI para publicación científica.
- Explorar integración de Dockerfile para facilitar despliegue y replicación.
- Revisar y actualizar el protocolo de reproducibilidad y checklist de publicación.
- Mantener la cobertura de tests y agregar pruebas para nuevos módulos/algoritmos.

### Documentación y publicación
- Consolidar documentación bilingüe y preparar versión en inglés para publicación internacional.
- Preparar materiales para onboarding científico y colaborativo.
- Paper submission: preparar manuscrito con evidencia TUI vs SOTA.

---
Estas tareas reflejan las mejores prácticas para la siguiente fase del proyecto, asegurando robustez, reproducibilidad y apertura internacional.