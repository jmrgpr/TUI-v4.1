# Notebooks de Análisis y Visualización / Analysis and Visualization Notebooks

(Opcional) Carpeta para notebooks de análisis, visualización y experimentos interactivos.

Ejemplo: TUI-v4.1_analysis.ipynb

## Quickstart Gráficos / Quickstart Graphics

- **Archivo**: `quickstart_graficos.ipynb`
- **Propósito**: Notebook bilingüe (español/inglés) para generar automáticamente gráficos principales desde los archivos CSV de resultados experimentales.
- **Funcionalidades**:
  - Carga automática de datos desde `../results/`
  - Gráficos de línea (recompensa promedio por escala de riesgo)
  - Gráficos de barras (frecuencia de agentes)
  - Gráficos interactivos con Plotly
- **Instrucciones**: Ejecutar las celdas en orden. Requiere librerías instaladas en `requirements.txt`.
- **Uso**: Ideal para onboarding rápido y exploración de resultados sin código adicional.

## Notas / Notes

- Mantener notebooks enfocados en análisis y visualización, no en código de simulación.
- Exportar gráficos generados a `../results/` para consistencia.
