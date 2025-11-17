
![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Docs-CC%20BY--NC--SA%204.0-lightgrey.svg)

# TUI v4.1 — Unified Intelligence Theory

Cita recomendada:  
> Rivera Garcia, J. M. (2025). *TUI v4.1: Toy model RL para Teoría Unificada de la Inteligencia*. Zenodo. https://doi.org/10.5281/zenodo.17552094

---

## Licencias

Este proyecto distingue entre **código** y **teoría/documentación larga**:

### 🧩 Código de este repositorio

- **Licencia:** [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **Alcanza a:**  
  - Código fuente (`.py`, `.ipynb`, scripts, herramientas de simulación).  
  - Archivos auxiliares necesarios para ejecutar el toy model RL.

**Resumen (no legal, solo orientativo):**

- ✅ Puedes usar, modificar, redistribuir e integrar el código (incluyendo uso comercial).
- ✅ Puedes crear derivados cerrados o integrarlo en otros sistemas.
- ✅ Debes conservar los avisos de copyright y licencia.
- ❌ No hay garantías; el código se entrega “AS IS”.

El texto completo está en [`LICENSE`](LICENSE).

---

### 📄 Teoría / preprint / contenido conceptual (Zenodo)

- **Licencia:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)  
- **Alcanza a:**  
  - El preprint teórico en Zenodo.  
  - Explicaciones largas de la teoría TUI v4.1 fuera de este repo (PDF, artículos, etc.).

**Resumen (no legal):**

- ✅ Uso académico y de investigación.  
- ✅ Citar con DOI y atribución a **José M. Rivera García**.  
- ✅ Compartir y adaptar, siempre bajo la misma licencia.  
- ❌ No usar el texto/teoría como base directa de productos comerciales sin acuerdo previo.

---

### Resumen práctico

| Tipo de contenido      | Licencia          | Uso comercial | Obligación principal                    |
|------------------------|-------------------|--------------|-----------------------------------------|
| Código de este repo    | Apache 2.0        | ✅ Permitido  | Mantener aviso de licencia/copyright    |
| Preprint / teoría (PDF)| CC BY-NC-SA 4.0   | ❌ No         | Atribuir y compartir bajo misma licencia|

---

## Zenodo

Este repositorio puede sincronizarse con Zenodo vía GitHub Actions (`.github/workflows/zenodo.yml`) usando la licencia de código:

```yaml
license: "Apache-2.0"

El preprint teórico (documento largo) permanece con licencia CC BY-NC-SA 4.0 en su DOI:
https://doi.org/10.5281/zenodo.17552094


---

TUI v4.1 Toy Model — RL Symbiosis

Este repositorio contiene el toy model oficial de la Teoría Unificada de la Inteligencia (TUI v4.1), con validación experimental de la hipótesis H1:

> "La inteligencia emerge al capitalizar el riesgo, no al evitarlo".



Actualización Nov 2025:

PGF premia reducción de riesgo entre pasos (prudencia), con comentarios bilingües y sin hardcoding.

Logging profesional y bilingüe: supervivencia, tripwires/shocks, PGF, reward ambiental, flexibilidad, robustez, acción óptima (Q-optimal).

Visualizaciones avanzadas y comparativas:

Evolución temporal de PGF, reward, flexibilidad, robustez y Q-optimal.

Boxplots, heatmaps y scatterplots para comparar agentes.

Interpretación automática bilingüe en todos los gráficos y consola.


Análisis estadístico avanzado:

Intervalos de confianza (SEM y t-IC) en flexibilidad, robustez y Q-optimal.

Tests estadísticos (t-test, ANOVA) en visuales y consola.

Resúmenes tabulares bilingües y exportación de métricas avanzadas en CSV y JSON.


Experimentos parametrizables: comparar control vs simbiosis en distintos niveles de riesgo (risk_scale), CLI profesional y sin hardcoding.

Exportación DOI-ready en JSON/CSV y gráficos.

Docstrings y comentarios bilingües para reproducibilidad internacional.

Todas las métricas y comentarios son bilingües y alineados con la teoría TUI v4.1.

Los experimentos permiten comparar control vs simbiosis en distintos niveles de riesgo (risk_scale parametrizable).

Gráficos avanzados: evolución temporal de métricas, scatterplot PGF vs reward, heatmap de tripwires, boxplots y visualización interactiva.

Análisis estadístico avanzado: intervalos de confianza en flexibilidad, robustez y Q-optimal; t-test y ANOVA para comparar agentes; interpretación automática bilingüe en consola y visuales.


Estructura

TUI-v4.1/
├── sim/
│   ├── tui_toy_rl.py          # Toy model RL oficial
│   ├── dqn_agent.py           # Agente DQN
│   └── results/
│       └── run_1000ep_seed42.json
├── README.md
└── requirements.txt

Instalación

pip install -r requirements.txt

Ejecución

# Ejemplo profesional, sin números mágicos / Professional example, no magic numbers
python sim/tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 1.0 --visualize --plot --export sim/results/run_1000ep_seed42.json

Para comparar curvas de riesgo:

python sim/tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 0.5 --export sim/results/run_risk05.json
python sim/tui_toy_rl.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 1.5 --export sim/results/run_risk15.json

Flujo de comparación automática / Automatic comparison workflow

La GUI y los scripts ejecutan siempre la comparación científica Control vs Simbiosis, registrando todas las métricas relevantes y exportando resultados en formatos profesionales (CSV, JSON, PNG). El logging y los gráficos incluyen interpretación automática bilingüe.

Control:   reward=-4.95, tripwires=0.04, shocks=0.01, survival=95.0
Simbiosis: reward=+455.86, tripwires=1.71, shocks=0.42, survival=580.0
→ α ≈ 0.36
PGF evolutivo y reward ambiental reportados por episodio.

Visualizaciones avanzadas generadas automáticamente:

Curvas de riesgo comparativas (risk curves) entre agentes y por risk_scale.

Boxplots y heatmaps de métricas agregadas (flexibilidad, robustez, Q-optimal).

Evolución temporal de PGF, reward, flexibilidad, robustez y Q-optimal.

Intervalos de confianza (SEM/t-IC) y análisis estadístico (t-test, ANOVA) en visuales y consola.

Interpretación automática bilingüe en todos los gráficos y outputs.


Exportación avanzada:

Resultados en JSON y CSV con métricas por episodio (flexibilidad, robustez, Q-optimal).

Gráficos en PNG listos para publicación.

Resúmenes tabulares bilingües en consola y visuales.


Ejemplo de uso de visualizaciones avanzadas / Example: advanced visualizations

Dashboard de métricas agregadas / Aggregated metrics dashboard

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

El dashboard muestra en consola y exporta en CSV/JSON la media, desviación estándar e intervalo de confianza de cada métrica por agente y risk_scale, con interpretación automática bilingüe.

from sim.visualizaciones import (
    curva_riesgo_comparativa,
    boxplot_metricas,
    heatmap_metricas,
    analisis_estadistico,
)

# Curvas de riesgo comparativas
curva_riesgo_comparativa(riesgo_control, riesgo_simbiosis,
                         export_path='results/risk_curves.png')

# Boxplot de flexibilidad
boxplot_metricas(flex_control, flex_simbiosis, 'Flexibilidad',
                 export_path='results/boxplot_flex.png')

# Heatmap de robustez por agente y risk_scale
heatmap_metricas(matriz_robustez, etiquetas, 'Robustez',
                 export_path='results/heatmap_robust.png')

# Análisis estadístico bilingüe
analisis_estadistico(flex_control, flex_simbiosis, 'Flexibilidad')

Todos los gráficos y análisis incluyen interpretación automática bilingüe (ES/EN) y exportación profesional.

Flags principales

--episodes: número de episodios / number of episodes

--seed: semilla aleatoria / random seed

--grid_size: tamaño del grid / grid size

--risk_scale: escala de riesgo (parametrizable, prudencial) / risk scale (parametric, prudential)

--visualize: muestra ASCII del agente B / ASCII visualization of agent B

--plot: gráfico I_op vs P_riesgo / plot I_op vs P_riesgo

--export: exporta resultados a JSON/CSV / export results to JSON/CSV


Exportación y reproducibilidad / Export & reproducibility

Todos los resultados, métricas y visualizaciones pueden exportarse desde la GUI o los scripts en formatos listos para publicación (CSV, JSON, PNG). El código y los comentarios son bilingües y reproducibles internacionalmente.

Semillas numpy, torch y cuda

Resultados exportables y visualización en vivo

Logging profesional y bilingüe / Professional bilingual logging


Requisitos

Python 3.8+

numpy, torch, matplotlib


## Calidad del Código y Cobertura / Code Quality and Coverage

Este proyecto mantiene estándares profesionales de calidad de código, con un enfoque en reproducibilidad, robustez y mejores prácticas. Se han implementado 281 tests automatizados que cubren excepciones, edge cases y visualizaciones avanzadas.

### Cobertura de Tests / Test Coverage
- **Cobertura global en módulos sim/**: 99% (16 líneas faltantes, principalmente docstrings no ejecutables).
- **Módulos con 100% cobertura**:
  - `sim/__init__.py`
  - `sim/dqn_agent.py`
  - `sim/gui_streamlit.py`
  - `sim/gui_utils.py`
  - `sim/toy_ped_rl.py`
  - `sim/visualizaciones.py`
- **Módulos con cobertura alta**:
  - `sim/prototipo_rl_simbiosis.py`: 97% (16 líneas faltantes en branches específicos y docstrings).
  - `sim/toy_ped_rl_excel.py`: 99% (1 línea faltante en exportación).
- **Mejores prácticas aplicadas**:
  - Tests con monkeypatch para simular excepciones sin hardcoding.
  - Ejecución de scripts bajo coverage para cubrir `__main__` blocks.
  - Manejo robusto de errores en visualizaciones y exports.
  - Código bilingüe (ES/EN) para colaboración internacional.
  - Sin números mágicos, parametrizable y reproducible.

Esta cobertura refleja dedicación a la perfección, validando la hipótesis H1 de TUI v4.1 con código confiable y listo para publicación científica.

Contacto

Para colaboración, dudas o sugerencias: jmrgpr [at] gmail.com


---

Notas bilingües:
Todos los comentarios, docstrings y outputs están en español e inglés para facilitar colaboración internacional y reproducibilidad científica.![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Docs-CC%20BY--NC--SA%204.0-lightgrey.svg)

# TUI v4.1 — Unified Intelligence Theory

Cita recomendada:  
> Rivera Garcia, J. M. (2025). *TUI v4.1: Toy model RL para Teoría Unificada de la Inteligencia*. Zenodo. https://doi.org/10.5281/zenodo.17552094

---

## Licencias

Este proyecto distingue entre **código** y **teoría/documentación larga**:

### 🧩 Código de este repositorio

- **Licencia:** [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **Alcanza a:**  
  - Código fuente (`.py`, `.ipynb`, scripts, herramientas de simulación).  
  - Archivos auxiliares necesarios para ejecutar el toy model RL.

**Resumen (no legal, solo orientativo):**

- ✅ Puedes usar, modificar, redistribuir e integrar el código (incluyendo uso comercial).
- ✅ Puedes crear derivados cerrados o integrarlo en otros sistemas.
- ✅ Debes conservar los avisos de copyright y licencia.
- ❌ No hay garantías; el código se entrega “AS IS”.

El texto completo está en [`LICENSE`](LICENSE).

---

### 📄 Teoría / preprint / contenido conceptual (Zenodo)

- **Licencia:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)  
- **Alcanza a:**  
  - El preprint teórico en Zenodo.  
  - Explicaciones largas de la teoría TUI v4.1 fuera de este repo (PDF, artículos, etc.).

**Resumen (no legal):**

- ✅ Uso académico y de investigación.  
- ✅ Citar con DOI y atribución a **José M. Rivera García**.  
- ✅ Compartir y adaptar, siempre bajo la misma licencia.  
- ❌ No usar el texto/teoría como base directa de productos comerciales sin acuerdo previo.

---

### Resumen práctico

| Tipo de contenido      | Licencia          | Uso comercial | Obligación principal                    |
|------------------------|-------------------|--------------|-----------------------------------------|
| Código de este repo    | Apache 2.0        | ✅ Permitido  | Mantener aviso de licencia/copyright    |
| Preprint / teoría (PDF)| CC BY-NC-SA 4.0   | ❌ No         | Atribuir y compartir bajo misma licencia|

---

## Zenodo

Este repositorio puede sincronizarse con Zenodo vía GitHub Actions (`.github/workflows/zenodo.yml`) usando la licencia de código:

```yaml
license: "Apache-2.0"
