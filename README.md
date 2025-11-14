# Propuesta de GUI / GUI Proposal

## Módulos principales / Main modules

- `sim/prototipo_rl_simbiosis.py`: Script principal de experimentos RL y comparación Control vs Simbiosis.
- `sim/dqn_agent.py`: Agente DQN profesional, bilingüe y parametrizable.
- `sim/visualizaciones.py`: Visualizaciones avanzadas, dashboards, boxplots, heatmaps, análisis estadístico y exportación profesional.
- `sim/gui_streamlit.py`: GUI interactiva con Streamlit para controlar parámetros, visualizar resultados, comparar agentes y exportar métricas.
- `sim/gui_utils.py`: Utilidades científicas para intervalos de confianza, t-test, ANOVA, interpretación automática bilingüe y exportación.
- `sim/__init__.py`: Inicializa el paquete `sim` para importación profesional.

## Wireframe conceptual / Conceptual Wireframe

- Vista principal: Panel de control con parámetros de simulación (episodios, semilla, risk_scale, tipo de agente).
- Visualización: Área de gráficos avanzados (curvas de riesgo, boxplots, heatmaps, dashboards).
- Resultados: Exportación y resumen estadístico bilingüe.
- Navegación: Menú lateral para cambiar entre simulación, visualización y análisis.

## Ejecución de la GUI / Run the GUI

Para usar la interfaz interactiva profesional:

```powershell
streamlit run sim/gui_streamlit.py
```

Permite controlar parámetros, comparar agentes (Control vs Simbiosis), visualizar métricas avanzadas, exportar resultados y obtener interpretación automática bilingüe.

---

- **Frontend:** Streamlit (Python, web, fácil despliegue, integración directa con scripts y visualizaciones matplotlib/seaborn).
- **Alternativa:** Dash (Plotly) para visualizaciones interactivas avanzadas.
- **Backend:** Python puro, reutilizando los módulos existentes (`sim/`, `notebooks/`, `visualizaciones.py`).
- **Exportación:** Soporte para CSV, JSON y PNG directamente desde la interfaz.

## Plan incremental / Incremental Implementation Plan

1. **MVP:**
  - Panel de parámetros y botón de ejecución.
  - Visualización básica de resultados (curva de riesgo, boxplot).
  - Exportación de resultados.
2. **Iteración 2:**
  - Dashboards interactivos, heatmaps y análisis estadístico.
  - Resúmenes bilingües automáticos.
3. **Iteración 3:**
  - Personalización avanzada (selección de agente, comparación múltiple).
  - Exportación DOI-ready y visualización de logs.

## Justificación / Justification

Streamlit permite una integración rápida y profesional con los módulos científicos existentes, es multiplataforma y facilita el despliegue web o local. Dash es una alternativa si se requiere mayor interactividad. El enfoque incremental asegura entregas funcionales y validación continua.
# TUI v4.1 Toy Model — RL Symbiosis

Este repositorio contiene el toy model oficial de la Teoría Unificada de la Inteligencia (TUI v4.1), con validación experimental de la hipótesis H1: "La inteligencia emerge al capitalizar el riesgo, no al evitarlo".

**Actualización Nov 2025:**
- PGF premia reducción de riesgo entre pasos (prudencia), con comentarios bilingües y sin hardcoding.
- Logging profesional y bilingüe: supervivencia, tripwires/shocks, PGF, reward ambiental, flexibilidad, robustez, acción óptima (Q-optimal).
- Visualizaciones avanzadas y comparativas:
  - Evolución temporal de PGF, reward, flexibilidad, robustez y Q-optimal.
  - Boxplots, heatmaps y scatterplots para comparar agentes.
  - Interpretación automática bilingüe en todos los gráficos y consola.
- Análisis estadístico avanzado:
  - Intervalos de confianza (SEM y t-IC) en flexibilidad, robustez y Q-optimal.
  - Tests estadísticos (t-test, ANOVA) en visuales y consola.
  - Resúmenes tabulares bilingües y exportación de métricas avanzadas en CSV y JSON.
- Experimentos parametrizables: comparar control vs simbiosis en distintos niveles de riesgo (`risk_scale`), CLI profesional y sin hardcoding.
- Exportación DOI-ready en JSON/CSV y gráficos.
- Docstrings y comentarios bilingües para reproducibilidad internacional.
- Todas las métricas y comentarios son bilingües y alineados con la teoría TUI v4.1.
- Los experimentos permiten comparar control vs simbiosis en distintos niveles de riesgo (`risk_scale` parametrizable).
- Gráficos avanzados: evolución temporal de métricas, scatterplot PGF vs reward, heatmap de tripwires, boxplots y visualización interactiva.
- Análisis estadístico avanzado: intervalos de confianza en flexibilidad, robustez y Q-optimal; t-test y ANOVA para comparar agentes; interpretación automática bilingüe en consola y visuales.

## Estructura

```
TUI-v4.1/
├── sim/
│   ├── tui_toy_rl.py          # Toy model RL oficial
│   ├── dqn_agent.py           # Agente DQN
│   └── results/
│       └── run_1000ep_seed42.json
├── README.md
└── requirements.txt
```

## Instalación
```bash
pip install -r requirements.txt
```


## Ejecución

```powershell
# Ejemplo profesional, sin números mágicos / Professional example, no magic numbers
python sim/tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 1.0 --visualize --plot --export sim/results/run_1000ep_seed42.json
```

Para comparar curvas de riesgo:
```powershell
python sim/tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 0.5 --export sim/results/run_risk05.json
python sim/tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 1.5 --export sim/results/run_risk15.json
```


## Flujo de comparación automática / Automatic comparison workflow

La GUI y los scripts ejecutan siempre la comparación científica Control vs Simbiosis, registrando todas las métricas relevantes y exportando resultados en formatos profesionales (CSV, JSON, PNG). El logging y los gráficos incluyen interpretación automática bilingüe.

---

```
Control:   reward=-4.95, tripwires=0.04, shocks=0.01, survival=95.0
Simbiosis: reward=+455.86, tripwires=1.71, shocks=0.42, survival=580.0
→ α ≈ 0.36
PGF evolutivo y reward ambiental reportados por episodio.

Visualizaciones avanzadas generadas automáticamente:
- Curvas de riesgo comparativas (risk curves) entre agentes y por risk_scale.
- Boxplots y heatmaps de métricas agregadas (flexibilidad, robustez, Q-optimal).
- Evolución temporal de PGF, reward, flexibilidad, robustez y Q-optimal.
- Intervalos de confianza (SEM/t-IC) y análisis estadístico (t-test, ANOVA) en visuales y consola.
- Interpretación automática bilingüe en todos los gráficos y outputs.

Exportación avanzada:
- Resultados en JSON y CSV con métricas por episodio (flexibilidad, robustez, Q-optimal).
- Gráficos en PNG listos para publicación.
- Resúmenes tabulares bilingües en consola y visuales.
```

### Ejemplo de uso de visualizaciones avanzadas / Example: advanced visualizations
# Dashboard de métricas agregadas / Aggregated metrics dashboard

```python
from sim.visualizaciones import dashboard_metricas

metricas_dict = {
  'Control': {
    'Flexibilidad': flex_control,
    'Robustez': robust_control,
    'Q-optimal': qopt_control
  },
  'Simbiosis': {
    'Flexibilidad': flex_simbiosis,
    'Robustez': robust_simbiosis,
    'Q-optimal': qopt_simbiosis
  }
}
dashboard_metricas(metricas_dict, export_path='results/dashboard_metricas.csv')
dashboard_metricas(metricas_dict, export_path='results/dashboard_metricas.json')
```

El dashboard muestra en consola y exporta en CSV/JSON la media, desviación estándar y intervalo de confianza de cada métrica por agente y risk_scale, con interpretación automática bilingüe.

```python
from sim.visualizaciones import curva_riesgo_comparativa, boxplot_metricas, heatmap_metricas, analisis_estadistico

# Curvas de riesgo comparativas
curva_riesgo_comparativa(riesgo_control, riesgo_simbiosis, export_path='results/risk_curves.png')

# Boxplot de flexibilidad
boxplot_metricas(flex_control, flex_simbiosis, 'Flexibilidad', export_path='results/boxplot_flex.png')

# Heatmap de robustez por agente y risk_scale
heatmap_metricas(matriz_robustez, etiquetas, 'Robustez', export_path='results/heatmap_robust.png')

# Análisis estadístico bilingüe
analisis_estadistico(flex_control, flex_simbiosis, 'Flexibilidad')
```

Todos los gráficos y análisis incluyen interpretación automática bilingüe (ES/EN) y exportación profesional.


## Flags principales
- `--episodes`: número de episodios / number of episodes
- `--seed`: semilla aleatoria / random seed
- `--grid_size`: tamaño del grid / grid size
- `--risk_scale`: escala de riesgo (parametrizable, prudencial) / risk scale (parametric, prudential)
- `--visualize`: muestra ASCII del agente B / ASCII visualization of agent B
- `--plot`: gráfico I_op vs P_riesgo / plot I_op vs P_riesgo
- `--export`: exporta resultados a JSON/CSV / export results to JSON/CSV


## Exportación y reproducibilidad / Export & reproducibility

Todos los resultados, métricas y visualizaciones pueden exportarse desde la GUI o los scripts en formatos listos para publicación (CSV, JSON, PNG). El código y los comentarios son bilingües y reproducibles internacionalmente.

---
- Semillas numpy, torch y cuda
- Resultados exportables y visualización en vivo
- Logging profesional y bilingüe / Professional bilingual logging


## Requisitos
- Python 3.8+
- numpy, torch, matplotlib


## Contacto
Para colaboración, dudas o sugerencias: jmrgpr [at] gmail.com
---
**Notas bilingües:**
Todos los comentarios, docstrings y outputs están en español e inglés para facilitar colaboración internacional y reproducibilidad científica.
