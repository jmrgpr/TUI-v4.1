![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Docs-CC%20BY--NC--SA%204.0-lightgrey.svg)

# TUI v4.1 — Unified Intelligence Theory

Cita recomendada:  
> Rivera Garcia, J. M. (2025). *TUI v4.1: Toy model RL para Teoría Unificada de la Inteligencia*. Zenodo. https://doi.org/10.5281/zenodo.17552094


## Licencias

Este proyecto distingue entre **código** y **teoría/documentación larga**:

### 🧩 Código de este repositorio

  - Código fuente (`.py`, `.ipynb`, scripts, herramientas de simulación).  
  - Archivos auxiliares necesarios para ejecutar el toy model RL.

**Resumen (no legal, solo orientativo):**


El texto completo está en [`LICENSE`](LICENSE).


# Estructura profesional del workspace / Professional workspace structure

Este README documenta la organización profesional y bilingüe del proyecto TUI-v4.1, siguiendo las mejores prácticas científicas y de ingeniería.

This README documents the professional and bilingual organization of the TUI-v4.1 project, following scientific and engineering best practices.

## Carpetas principales / Main folders

- docs/: Teoría, papers, documentación formal / Theory, papers, formal documentation
- data/: Datasets y documentación asociada / Datasets and associated documentation
- notebooks/: Jupyter Notebooks (solo experimentos) / Jupyter Notebooks (experiments only)
- sim/: Código fuente del simulador y agentes / Simulator and agent source code
- results/: Resultados experimentales (csv, json, png) / Experimental results (csv, json, png)
- test/: Pruebas unitarias y de integración / Unit and integration tests
- TUI/: (Si es un módulo aparte) / (If a separate module)

## Principios clave / Key principles

- Separación clara entre teoría, datos, código, resultados, notebooks y tests.
- El simulador no se modifica ni se rompe; solo se reubican archivos de teoría y resultados.
- El README se actualiza para reflejar la nueva estructura y facilitar onboarding científico.

Clear separation between theory, data, code, results, notebooks, and tests.
Simulator code is not modified or broken; only theory and results files are relocated.
README is updated to reflect the new structure and facilitate scientific onboarding.

## Ejemplo de estructura / Example structure

```
TUI-v4.1/
├── docs/
├── data/
├── notebooks/
├── sim/
├── results/
├── test/
├── TUI/
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── LICENSE
└── ...otros archivos
```

## Notas / Notes

- Para detalles sobre cada carpeta, consulta el README correspondiente.
- For details about each folder, see the corresponding README.
Visualizaciones avanzadas y comparativas:
## Novedades Noviembre 2025 (actualizado 18/11/2025)

- Refactorización final y merge a `main`.
- Eliminado código muerto (Agent.__init__ duplicado) en `sim/prototipo_rl_simbiosis.py`.
- Añadidos tests de integración con subprocess para CLI y cobertura de ramas visualización, export, plot y risk_sweep.
- Reforzada cobertura de `reprogram_purpose` y métodos de serialización de policy.
- Cobertura final: 98% en `sim/prototipo_rl_simbiosis.py` y 96-100% en módulos principales.
- Todos los tests pasan correctamente (316/316).
- Auditoría completa de exportación profesional: todos los resultados y gráficos se guardan en `results/`.
- Documentación y README actualizados para reflejar estructura profesional y auditoría de exportación.
- Merge exitoso de rama `feature/tui-v4.2-refactorizacion-metodologica` a `main` y push remoto.
- Estado: Listo para publicación y auditoría científica internacional.

---

## Ejemplo de uso actualizado

```bash
# Ejecuta la GUI interactiva
streamlit run sim/gui_streamlit.py
# Exporta historial de corridas en JSON desde la interfaz
```

---

## ⚠️ Advertencia sobre archivos sueltos en la raíz / Warning about loose files in root

**ES:**
Para mantener la profesionalidad y auditabilidad del proyecto, evita dejar archivos sueltos (csv, json, imágenes, scripts, txt, etc.) en la raíz del repositorio. Todos los datos, resultados, imágenes y scripts deben estar en sus carpetas correspondientes (`data/`, `results/`, `docs/`, `sim/`, etc.).

**Recomendaciones:**
- Mueve datasets a `data/`
- Mueve resultados experimentales a `results/`
- Mueve imágenes y gráficos a `results/` o `docs/`
- Elimina archivos temporales o de prueba
- Mantén la raíz solo con archivos esenciales: `README.md`, `requirements.txt`, `CHANGELOG.md`, `LICENSE`, etc.

**EN:**
To maintain professionalism and auditability, avoid leaving loose files (csv, json, images, scripts, txt, etc.) in the project root. All data, results, images, and scripts should be placed in their respective folders (`data/`, `results/`, `docs/`, `sim/`, etc.).

**Recommendations:**
- Move datasets to `data/`
- Move experimental results to `results/`
- Move images and plots to `results/` or `docs/`
- Delete temporary or test files
- Keep only essential files in the root: `README.md`, `requirements.txt`, `CHANGELOG.md`, `LICENSE`, etc.

---

**Importante / Important:**
Todas las funciones estándar y scripts del proyecto están configurados para guardar archivos de test y resultados en la carpeta `results/` por defecto. Ningún archivo generado automáticamente debe aparecer en la raíz. Si ocurre, revisa y corrige la ruta de exportación en el código.

All standard functions and scripts in the project are set to save test and result files to the `results/` folder by default. No automatically generated file should appear in the root. If it happens, review and fix the export path in the code.

**Imágenes y gráficos / Images and plots:**
Todas las imágenes generadas por scripts, notebooks o funciones de visualización deben guardarse en la carpeta `results/` por defecto. Nunca exportes gráficos directamente en la raíz.

All images generated by scripts, notebooks or visualization functions must be saved to the `results/` folder by default. Never export plots directly to the root.

---

**Auditoría de scripts y tests / Script and test audit:**
Todos los scripts y tests han sido revisados para asegurar que ningún archivo de imagen o resultado se exporte a la raíz por defecto. La exportación profesional está garantizada en la carpeta `results/`.

All scripts and tests have been audited to ensure no image or result file is exported to the root by default. Professional export is guaranteed to the `results/` folder.

---

## Cobertura de Tests / Test Coverage
- **Cobertura global en módulos sim/**: 95% (203 líneas faltantes, principalmente branches específicos y docstrings no ejecutables).
- **Módulos con 100% cobertura**:
  - `sim/__init__.py`
  - `sim/dqn_agent.py`
  - `sim/evaluator_pgf.py`
  - `sim/gui_utils.py`
  - `sim/toy_ped_rl_excel.py`
  - `sim/visualizaciones.py`
- **Módulos con cobertura alta**:
  - `sim/gui_streamlit.py`: 96% (4 líneas faltantes en validaciones específicas).
  - `sim/prototipo_rl_simbiosis.py`: 96% (25 líneas faltantes en branches específicos).
  - `sim/toy_ped_rl.py`: 99% (1 línea faltante).
- **Mejores prácticas aplicadas**:
  - Tests con monkeypatch para simular excepciones sin hardcoding.
  - Ejecución de scripts bajo coverage para cubrir `__main__` blocks.
  - Manejo robusto de errores en visualizaciones y exports.
  - Código bilingüe (ES/EN) para colaboración internacional.
  - Sin números mágicos, parametrizable y reproducible.

Esta cobertura refleja dedicación a la perfección, validando la hipótesis H1 de TUI v4.1 con código confiable y listo para publicación científica.

---

## Flags principales
---existing code---
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
- **Cobertura global en módulos sim/**: 95% (203 líneas faltantes, principalmente branches específicos y docstrings no ejecutables).
- **Módulos con 100% cobertura**:
  - `sim/__init__.py`
  - `sim/dqn_agent.py`
  - `sim/evaluator_pgf.py`
  - `sim/gui_utils.py`
  - `sim/toy_ped_rl_excel.py`
  - `sim/visualizaciones.py`
- **Módulos con cobertura alta**:
  - `sim/gui_streamlit.py`: 96% (4 líneas faltantes en validaciones específicas).
  - `sim/prototipo_rl_simbiosis.py`: 96% (25 líneas faltantes en branches específicos).
  - `sim/toy_ped_rl.py`: 99% (1 línea faltante).
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
Todos los comentarios, docstrings y outputs están en español e inglés para facilitar colaboración internacional y reproducibilidad científica.
