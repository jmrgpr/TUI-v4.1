## Optimización del buffer de memoria en DQNAgent / DQNAgent memory buffer optimization

- El buffer de memoria ahora almacena los estados y siguientes estados como arrays numpy (`np.array`), evitando conversiones repetidas durante el entrenamiento.
- Esto mejora la eficiencia del entrenamiento y reduce el coste de CPU por batch.
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

## Entorno de referencia / Reference Environment

**ES:**
Se recomienda el siguiente entorno para máxima reproducibilidad. Las dependencias están fijadas en `requirements.txt` y `environment.yml`.

*   **Python:** 3.10 / 3.11
*   **Dependencias principales:**
    ```
    torch==2.1.0
    stable-baselines3>=2.0.0
    gymnasium>=0.28.1
    pandas==2.0.3
    numpy==1.24.3
    matplotlib==3.7.2
    seaborn==0.12.2
    ```

**EN:**
The following environment is recommended for maximum reproducibility. Dependencies are pinned in `requirements.txt` and `environment.yml`.

---

<<<<<<< HEAD
## Cita recomendada / Recommended citation

## Checklist de replicación / Replication checklist
## Entorno de referencia / Reference environment

Se recomienda el siguiente entorno para máxima reproducibilidad:

**Python:** 3.10 o 3.11

**Dependencias principales (requirements.txt):**

```
tqdm==4.66.1
pillow==10.0.1
jupyter==1.0.0
torch==2.1.0
numpy==1.24.3
matplotlib==3.7.2
pytest==7.4.0
seaborn==0.12.2
streamlit==1.28.1
scipy==1.11.3
pandas==2.0.3
scikit-learn==1.3.0
plotly==5.15.0
altair==5.1.2
nbformat==5.9.2
statsmodels==0.14.0
stable-baselines3>=2.0.0
shimmy>=0.2.1
gymnasium>=0.28.1
```

Para mayor facilidad de replicación, se recomienda crear el entorno con venv o Conda y usar el archivo requirements.txt incluido.

**Opción recomendada (Conda):**
1. Clona el repositorio / Clone the repository
  ```bash
  git clone https://github.com/jmrgpr/TUI-v4.1.git
  cd TUI-v4.1
  ```
2. Crea el entorno con Conda / Create the environment with Conda
  ```bash
  conda env create -f environment.yml
  conda activate tui-v4.1
  ```
3. Ejecuta los scripts principales / Run main scripts
  ```bash
  python run_fase2.py
  python merge_summaries.py
  python results/stats.py
  python run_sota_comparison.py  # (opcional, para comparar PPO)
  ```
4. Visualiza los resultados / Visualize results
  - Revisa los archivos en `results/` y usa el notebook `notebooks/quickstart_graficos.ipynb` para generar gráficos automáticos.

**Opción alternativa (venv + pip):**
1. Clona el repositorio / Clone the repository
  ```bash
  git clone https://github.com/jmrgpr/TUI-v4.1.git
  cd TUI-v4.1
  ```
2. Crea el entorno virtual / Create the virtual environment
  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate  # Windows
  # source .venv/bin/activate  # Linux/MacOS
  ```
3. Instala las dependencias / Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
4. Ejecuta los scripts principales / Run main scripts
  ```bash
  python run_fase2.py
  python merge_summaries.py
  python results/stats.py
  python run_sota_comparison.py  # (opcional, para comparar PPO)
  ```
5. Visualiza los resultados / Visualize results
  - Revisa los archivos en `results/` y usa el notebook `notebooks/quickstart_graficos.ipynb` para generar gráficos automáticos.

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
> Rivera Garcia, J. M. (2025). *Preliminary Evidence of Prudential Paralysis in State-of-the-Art Reinforcement Learning vs. Resilience in TUI* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.17654593
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
**Evidencia empírica preliminar**: Los resultados actuales ofrecen evidencia indicativa de alineación escalable vía Simbiosis Constitutiva, superando al baseline SOTA (PPO) en el entorno de prueba.
**Plan de trabajo**: El archivo `TODO.md` resume las acciones recomendadas para fortalecer la publicación y el impacto internacional del proyecto.

---

## Calidad del Código y Cobertura / Code Quality and Coverage

Este proyecto mantiene altos estándares de calidad de código, con un enfoque en reproducibilidad y robustez. Se han implementado tests automatizados que cubren el 99% del código base del simulador (`sim/`).

### Cobertura de Tests / Test Coverage

## Cobertura y seguridad del código / Code coverage & safety
## Flexibilidad para experimentación / Hyperparameter flexibility

- El tamaño de las capas ocultas de la red DQN (`hidden_dim`) ahora es configurable desde el constructor de `DQNAgent` y `DQNNet`.
- Esto permite ajustar la arquitectura fácilmente para búsqueda de hiperparámetros y experimentos avanzados.

- Cobertura global de tests: **99%** en módulos principales (`sim/`)
- Implementada target network en DQN para mayor estabilidad y reproducibilidad.
- Eliminado uso inseguro de `eval()`; ahora se usa `ast.literal_eval()` para cargar policies.
- Todos los cambios verificados por tests automáticos (pytest).

## Contacto / Contact

Para colaboración, dudas o sugerencias: jmrgpr@gmail.com

For collaboration, questions or suggestions: jmrgpr@gmail.com

---

## Dedicatoria / Dedication

Dedico este trabajo a Aurelio y Amarianis, a quienes amo con todo mi corazón.
