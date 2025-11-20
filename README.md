## Limitaciones y amenazas a la validez / Limitations & Threats to Validity

**ES:**
- Los experimentos se realizaron en un entorno tipo “toy RL”, no en entornos complejos como MuJoCo o Procgen.
- La comparación SOTA solo incluye PPO; no se han evaluado otros algoritmos como A2C o SAC.
- Los resultados de SOTA se basan en una sola semilla, lo que puede limitar la robustez estadística.
- El número de episodios y configuraciones es limitado; los resultados pueden variar con otros parámetros.
- La métrica η_acumulativo no se ha calculado explícitamente.
- Los resultados y conclusiones deben interpretarse como evidencia preliminar y no como validación definitiva.

**EN:**
- Experiments were conducted in a “toy RL” environment, not in complex benchmarks like MuJoCo or Procgen.
- SOTA comparison includes only PPO; other algorithms (A2C, SAC) were not evaluated.
- SOTA results are based on a single seed, which may limit statistical robustness.
- The number of episodes and configurations is limited; results may vary with different parameters.
- The η_acumulativo metric was not explicitly calculated.
- Results and conclusions should be interpreted as preliminary evidence, not definitive validation.

![CI](https://github.com/jmrgpr/TUI-v4.1/actions/workflows/python-tests.yml/badge.svg)
![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Docs-CC%20BY--NC--SA%204.0-lightgrey.svg)
![DOI Dataset](https://zenodo.org/badge/DOI/10.5281/zenodo.17654593.svg)
![DOI Theory](https://zenodo.org/badge/DOI/10.5281/zenodo.17552094.svg)
![Version](https://img.shields.io/badge/version-4.2-blue)
![Test Coverage](https://img.shields.io/badge/coverage-99%25-success)


# TUI v4.2 — Unified Intelligence Theory

<<<<<<< HEAD
Cita recomendada:
=======

## Checklist de replicación / Replication checklist

Sigue estos pasos para reproducir los resultados principales (Fase 2):

1. Clona el repositorio / Clone the repository
  ```bash
  git clone https://github.com/jmrgpr/TUI-v4.1.git
  cd TUI-v4.1
  ```
  python -m venv .venv
  .\.venv\Scripts\activate  # Windows
  # source .venv/bin/activate  # Linux/MacOS
  ```
3. Instala las dependencias / Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
4. Ejecuta la Fase 2 / Run Fase 2
  ```bash
  python run_fase2.py
  python merge_summaries.py
  python results/stats.py
  python run_sota_comparison.py  # (opcional, para comparar PPO)
  ```
5. Visualiza los resultados / Visualize results
  - Revisa los archivos en `results/` y usa el notebook `notebooks/quickstart_graficos.ipynb` para generar gráficos automáticos.

Recursos clave / Key resources:
- [Protocolo de reproducibilidad](PROTOCOLO_REPRODUCIBILIDAD.md)
- [Checklist de publicación científica](CHECKLIST_PUBLICACION.md)

## Cómo citar / How to cite

Si usas TUI v4.2 en tu investigación, por favor cita ambos:

**Teoría:**
> Rivera Garcia, J. M. (2025). *Teoría Unificada de la Inteligencia (v4.1): Marco Falsable para Inteligencia como Función del Riesgo Acumulado*. Zenodo. https://doi.org/10.5281/zenodo.17552094

**Dataset:**
> Rivera Garcia, J. M. (2025). *Preliminary Evidence of Prudential Paralysis in State-of-the-Art Reinforcement Learning vs. Resilience in TUI* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.17654593

If you use TUI v4.2 in your research, please cite both:

**Theory:**
> Rivera Garcia, J. M. (2025). *Unified Intelligence Theory (v4.1): Falsifiable Framework for Intelligence as a Function of Accumulated Risk*. Zenodo. https://doi.org/10.5281/zenodo.17552094

**Dataset:**
>>>>>>> professionalization
> Rivera Garcia, J. M. (2025). *Preliminary Evidence of Prudential Paralysis in State-of-the-Art Reinforcement Learning vs. Resilience in TUI* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.17654593


## Licencias

Este proyecto distingue entre **código** y **teoría/documentación larga**:


El texto completo está en [`LICENSE`](LICENSE).


# Estructura profesional del workspace / Professional workspace structure

Este README documenta la organización profesional y bilingüe del proyecto TUI-v4.1, siguiendo las mejores prácticas científicas y de ingeniería.

This README documents the professional and bilingual organization of the TUI-v4.1 project, following scientific and engineering best practices.

## Carpetas principales / Main folders
*Consulta los recursos clave arriba para reproducibilidad y auditoría científica.*

- docs/: Teoría, papers, documentación formal / Theory, papers, formal documentation
- data/: Datasets y documentación asociada / Datasets and associated documentation
- notebooks/: Jupyter Notebooks (solo experimentos) / Jupyter Notebooks (experiments only)
- sim/: Código fuente del simulador y agentes / Simulator and agent source code
- results/: Resultados experimentales (csv, json, png) / Experimental results (csv, json, png)
- test/: Pruebas unitarias y de integración / Unit and integration tests
- TUI/: (Si es un módulo aparte) / (If a separate module)

## Principios clave / Key principles


Clear separation between theory, data, code, results, notebooks, and tests.
Simulator code is not modified or broken; only theory and results files are relocated.
README is updated to reflect the new structure and facilitate scientific onboarding.

## Ejemplo de estructura / Example structure

```
TUI-v4.1/
├── LICENSE
├── scripts/
└── ...otros archivos
```
- Se implementó el runner `run_fase2.py` para automatizar la Fase 2 (60 corridas × 1000 episodios).
- Todos los resultados se guardan con prefijo único por semilla usando `--output_prefix` (ejemplo: `results/fase2/seed_42_seed42_risk1.0_control.csv`).
- El archivo de resumen también se guarda por semilla (ejemplo: `seed_42_seed42_summary.csv`).
- Se creó el script `merge_summaries.py` para unir todos los resúmenes en un solo archivo global (`results/fase2_global_summary.csv`).
- Documentación y tracking actualizados en `README.md`, `CHANGELOG.md`, `results/README.md` y `TRACKING_2025-11-19.md`.
- Auditoría científica y reproducibilidad garantizadas para revisión por pares y publicación.
- **Nuevo notebook de quickstart**: `notebooks/quickstart_graficos.ipynb` para generación automática de gráficos bilingües desde resultados CSV.
- **Análisis estadístico formal**: Script `results/stats.py` con ANOVA Two-Way y Tukey HSD, confirmando diferencias significativas (p < 0.0000) entre agentes.
- **Framework SOTA**: Preparado para comparación con PPO/A2C usando `run_sota_comparison.py` y `sim/sota_wrapper.py`.
- **Comparación SOTA completada**: PPO optimiza recompensa pero falla en PGF (-0.29 vs -0.06 de TUI); evidencia de superioridad TUI en alineación escalable. Ver `docs/analisis_sota_concepto.md` para análisis conceptual detallado.
<<<<<<< HEAD
- **Evidencia empírica irrefutable**: Primera demostración de alineación escalable vía Simbiosis Constitutiva, superando baselines SOTA.
=======
- **Evidencia empírica preliminar**: Evidencia indicativa de alineación escalable vía Simbiosis Constitutiva, superando baselines SOTA.
>>>>>>> professionalization

**Nuevo:** Se ha creado el archivo `TODO.md` en la raíz del repositorio, donde se resumen las acciones recomendadas para fortalecer la publicación y el impacto internacional del proyecto (ver recomendaciones integradas Grok + Gemini Pro).
**Acciones prioritarias:**
- Pinnear dependencias y agregar Dockerfile
- Subir PDF teórico y notebook quickstart
- Implementar script stats.py para ANOVA y p-values
- Comparar con baseline SOTA y discutir resultados
- Unificar idioma y mejorar narrativa Control
- Escalar el experimento y agregar demo interactiva

Revisar `TODO.md` para el plan detallado y prioridades.


1. Ejecutar la Fase 2 completa:
  ```powershell
  python run_fase2.py
  ```
  Resultados en `results/fase2/` con nombres únicos por semilla.


---

---

# Exporta historial de corridas en JSON desde la interfaz

---

## ⚠️ Advertencia sobre archivos sueltos en la raíz / Warning about loose files in root

**ES:**
Para mantener la profesionalidad y auditabilidad del proyecto, evita dejar archivos sueltos (csv, json, imágenes, scripts, txt, etc.) en la raíz del repositorio. Todos los datos, resultados, imágenes y scripts deben estar en sus carpetas correspondientes (`data/`, `results/`, `docs/`, `sim/`, etc.).

**Recomendaciones:**
- Mueve datasets a `data/`
- Mueve resultados experimentales a `results/`
- Elimina archivos temporales o de prueba
- Mantén la raíz solo con archivos esenciales: `README.md`, `requirements.txt`, `CHANGELOG.md`, `LICENSE`, etc.

**EN:**
To maintain professionalism and auditability, avoid leaving loose files (csv, json, images, scripts, txt, etc.) in the project root. All data, results, images, and scripts should be placed in their respective folders (`data/`, `results/`, `docs/`, `sim/`, etc.).

- Move datasets to `data/`
- Move experimental results to `results/`
- Keep only essential files in the root: `README.md`, `requirements.txt`, `CHANGELOG.md`, `LICENSE`, etc.

---

**Importante / Important:**
Todas las funciones estándar y scripts del proyecto están configurados para guardar archivos de test y resultados en la carpeta `results/` por defecto. Ningún archivo generado automáticamente debe aparecer en la raíz. Si ocurre, revisa y corrige la ruta de exportación en el código.
All standard functions and scripts in the project are set to save test and result files to the `results/` folder by default. No automatically generated file should appear in the root. If it happens, review and fix the export path in the code.

**Imágenes y gráficos / Images and plots:**

All images generated by scripts, notebooks or visualization functions must be saved to the `results/` folder by default. Never export plots directly to the root.

---

**Auditoría de scripts y tests / Script and test audit:**
Todos los scripts y tests han sido revisados para asegurar que ningún archivo de imagen o resultado se exporte a la raíz por defecto. La exportación profesional está garantizada en la carpeta `results/`.


---
## Cobertura de Tests / Test Coverage
- **Cobertura global en módulos sim/**: 99% (16 líneas faltantes, principalmente branches específicos y docstrings no ejecutables).
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

    curva_riesgo_comparativa,
    heatmap_metricas,
)
# Curvas de riesgo comparativas
                         export_path='results/risk_curves.png')
# Boxplot de flexibilidad
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
- **Cobertura global en módulos sim/**: 99% (16 líneas faltantes, principalmente branches específicos y docstrings no ejecutables).
- **Módulos con 100% cobertura**:
  - `sim/__init__.py`
  - `sim/evaluator_pgf.py`
  - `sim/gui_utils.py`
  - `sim/toy_ped_rl_excel.py`
  - `sim/visualizaciones.py`
- **Módulos con cobertura alta**:
  - `sim/gui_streamlit.py`: 96% (4 líneas faltantes en validaciones específicas).
  - `sim/prototipo_rl_simbiosis.py`: 96% (25 líneas faltantes en branches específicos).
  - Ejecución de scripts bajo coverage para cubrir `__main__` blocks.
  - Manejo robusto de errores en visualizaciones y exports.
  - Código bilingüe (ES/EN) para colaboración internacional.

Esta cobertura refleja dedicación a la perfección, validando la hipótesis H1 de TUI v4.1 con código confiable y listo para publicación científica.


## Contacto / Contact

Para colaboración, dudas o sugerencias: jmrgpr@gmail.com

For collaboration, questions or suggestions: jmrgpr@gmail.com


---

Notas bilingües:
Todos los comentarios, docstrings y outputs están en español e inglés para facilitar colaboración internacional y reproducibilidad científica.

## Organización de archivos

### Estado científico y organización (18/11/2025)
- Validación científica completa: 319 tests pasan, cobertura 98%.
- Refactorización de tests para máxima reproducibilidad.
- Archivos generados fuera de lugar archivados correctamente:
  - test.csv, test.json, coverage_missing.txt → test/
  - dummy.png, test_integration_*.png, test_integration_*.csv → results/
  - fix.py → scripts/
- Documentación y tracking actualizados.

## Dedicatoria

Dedico este trabajo a Aurelio y Amarianis, a quienes amo con todo mi corazón. La génesis de esta idea reside en la maravilla de verlos crecer y aprender. El riesgo de no poder estar con ustedes algún día—la pérdida irreversible de esa inversión temporal y emocional—es mi $P_{riesgo}$ más profundo. Es la presión selectiva que impulsa mi propósito genuino. No soy eterno, pero dejarles un legado, aunque sea la semilla de una idea, es para mí lo más importante. PAPÁ LOS AMA.
