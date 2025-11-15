![CI](https://github.com/jmrgpr/TUI-v4.1/actions/workflows/python-tests.yml/badge.svg)
![Version](https://img.shields.io/badge/version-4.2-blue)
![Docs](https://img.shields.io/badge/Docs-CC%20BY--NC--SA%204.0-lightgrey)
![DOI Dataset](https://zenodo.org/badge/DOI/10.5281/zenodo.17654593.svg)
![DOI Theory](https://img.shields.io/badge/DOI-10.5281/zenodo.17552094-blue)
![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)
![Reproducible](https://img.shields.io/badge/reproducible-validated-success)
![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

# TUI v4.2 - Unified Intelligence Theory (toy simulator)

<<<<<<< HEAD
ES: Simulador Gridworld para ejercer la Teoria Unificada de la Inteligencia (TUI v4.2). Incluye agentes Control (Q-table) y Simbiosis (DQN+PGF), exportacion DOI-ready, analisis estadistico y visualizaciones.  
EN: Gridworld simulator to exercise the Unified Intelligence Theory (TUI v4.2). Includes Control (Q-table) and Symbiosis (DQN+PGF) agents, DOI-ready export, statistical analysis, and visualizations.

## Logros recientes / Recent achievements
- Refactor del simulador y runners (v4.2).
- Cobertura de pruebas **100%** en `sim/`; integracion completa.
- Exportacion robusta (JSON/CSV) y trazabilidad por semilla (`--output_prefix`).
- Scripts de Fase 2 y comparacion SOTA (PPO/A2C/DQN) listos para reproducibilidad.
- Visualizaciones y estadistica (ANOVA, t-test) bilingues; notebooks de quickstart.

## Entorno recomendado / Reference environment
- Python 3.10 o 3.11  
- Dependencias clave (ver `requirements.txt` / `environment.yml`):  
  torch==2.1.0, stable-baselines3>=2.0.0, gymnasium>=0.28.1, pandas==2.0.3, numpy==1.24.3, matplotlib==3.7.2, seaborn==0.12.2, scipy==1.11.x

## Reproducibilidad rapida / Quick start
1) Crear entorno (Conda o venv) e instalar dependencias:  
   `pip install -r requirements.txt`
2) Experimento base:  
   `python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --risk_scale 1.0 --export results/run1.json`
3) Barrido de riesgo:  
   `python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes 100 --seed 42 --output_prefix results/sweep/fase2/seed42/sweep_default --dqn_control`
4) Comparacion SOTA (opcional):  
   `python run_sota_comparison.py`  # corre PPO/A2C/DQN en todos los risk_scale

## Estructura / Layout
- `sim/` : codigo del simulador, agentes, evaluador PGF, visualizaciones.
- `test/` : pruebas unitarias e integracion (pytest).
- `results/` : salidas JSON/CSV/PNG de experimentos.  
  - `sweep/` barridos de risk_scale (p.ej. `fase2/seed42/...`).  
  - `runs/` corridas individuales
  - `sota/` modelos y resúmenes PPO/A2C/DQN.  
  - `global_summaries/` consolidados (p.ej. `fase2_global_summary.csv`).  
- `docs/` : analisis y notas de resultados.
- `TUI/` : documentos de teoria (TUI v4.x, LaTeX/Markdown).
- `notebooks/` : cuadernos de analisis y graficos.
- `scripts/` : utilidades (fase2, merge de resumenes, comparacion SOTA).

## Limitaciones actuales / Current limitations
- Entorno "toy" Gridworld; sin benchmarks complejos (MuJoCo/Procgen).
- Comparacion SOTA centrada en PPO; otros algoritmos no evaluados.
- Algunos docs historicos mantienen acentos/LaTeX legacy para preservar la teoria.

### Ampliación de limitaciones

- **Supuestos del modelo y experimentos:**  
  El entorno simulado es un Gridworld simplificado, diseñado para ilustrar conceptos de la Teoría Unificada de la Inteligencia. Se asume que los agentes operan en un espacio discreto, con recompensas y penalizaciones definidas por el usuario. No se modelan dinámicas físicas complejas ni interacciones multiagente avanzadas.

- **Escenarios donde la metodología puede no ser aplicable:**  
  El enfoque TUI/PGF está optimizado para entornos discretos y problemas de decisión secuencial. No se recomienda para tareas de control continuo, simulaciones físicas realistas, ni benchmarks de alta dimensionalidad (MuJoCo, Procgen, etc.).
=======
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
>>>>>>> 603de3f (Change license to Apache 2.0 and update project info)

- **Fuentes de sesgo o incertidumbre experimental:**  
  Los resultados pueden verse afectados por la selección de semillas, episodios y parámetros de riesgo. La interpretación de métricas depende de la correcta configuración experimental. No se garantiza robustez ante cambios drásticos en la estructura del entorno o los agentes.

<<<<<<< HEAD
- **Restricciones técnicas:**  
  El simulador depende de librerías específicas (torch, stable-baselines3, gymnasium, etc.) y está optimizado para Python 3.10/3.11. El rendimiento puede verse limitado en hardware sin soporte para aceleración (GPU/CPU). La escalabilidad está pensada para experimentos medianos; no se recomienda para grandes clusters o HPC sin adaptación.

- **Limitaciones en la interpretación y generalización:**  
  Las métricas y visualizaciones reflejan el comportamiento en el entorno toy; no deben extrapolarse directamente a sistemas reales sin validación adicional. Los resultados son útiles para comparar variantes de agentes y estrategias, pero no constituyen pruebas definitivas de superioridad en otros dominios.

- **Limitaciones en la consolidación y comparativa SOTA:**  
  Los resultados SOTA (PPO, A2C, DQN) se consolidan automáticamente porque los archivos CSV incluyen el parámetro `risk` en el nombre y en las columnas. Sin embargo, el campo `red_team` queda siempre en `False` para SOTA, por lo que la comparativa en el master solo cubre ese modo. Esto difiere del pipeline principal, donde los agentes TUI pueden tener resultados tanto con `red_team=True` como `False`.  
  **Implicación:** La comparación entre SOTA y TUI debe realizarse considerando que SOTA solo opera en modo no adversarial (`red_team=False`). Se recomienda explicitar esta diferencia en los análisis y reportes para mantener la trazabilidad científica.

## Cobertura y calidad / Coverage & quality
- Cobertura `sim/`: **100%** (pytest con `--cov=sim`).  
- Target network en DQN; sin `eval()` inseguro (se usa `ast.literal_eval`).  
- Warnings graficos mitigados cerrando figuras; exportaciones en UTF-8.
- Comparacion SOTA ampliada (PPO, A2C, DQN) con sumarios por riesgo y global.

## Cómo citar / How to cite
- Teoría: https://doi.org/10.5281/zenodo.17552094  
- Dataset: https://doi.org/10.5281/zenodo.17654593  
La versión oficial del software es TUI v4.1. Consulta y usa el archivo `CITATION.cff` para BibTeX y detalles de la cita, incluyendo el identificador del software y commit hash.

## Contacto / Contact
jmrgpr@gmail.com | jrivera77@outlook.com | ORCID https://orcid.org/0009-0000-3013-725X

## FAQ rapida
- CI/CD y backend grafico? Se fuerza backend `Agg` en modulos de visualizacion para correr en entornos headless.
- Como reproducir coberturas? `python -m pytest --cov=sim --cov-report=term-missing`.
- Entorno recomendado? Python 3.10/3.11 + dependencias fijadas en `requirements.txt` / `environment.yml`.

---

## Estado actual y próximos pasos / Current status & next steps

**Estado actual:**
- El pipeline de experimentos está automatizado y validado (Exp1, Exp2 smoke test).
- Los scripts generan y consolidan resultados trazables por agente, semilla y riesgo.
- El notebook de análisis produce tablas y gráficos comparativos.
- La estructura del repositorio está limpia y documentada.

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
- Key dependencies (see `requirements.txt` / `environment.yml`):
  torch==2.1.0, stable-baselines3>=2.0.0, gymnasium>=0.28.1, pandas==2.0.3, numpy==1.24.3, matplotlib==3.7.2, seaborn==0.12.2, scipy==1.11.x

## Quick start
1) Create environment (Conda or venv) and install dependencies:
   `pip install -r requirements.txt`
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
- Theory: https://doi.org/10.5281/zenodo.17552094
- Dataset: https://doi.org/10.5281/zenodo.17654593
See `CITATION.cff` for BibTeX.

## Contact
jmrgpr@gmail.com | jrivera77@outlook.com | ORCID https://orcid.org/0009-0000-3013-725X

## Quick FAQ
- CI/CD and graphics backend? Backend `Agg` is forced in visualization modules to run in headless environments.
- How to reproduce coverage? `python -m pytest --cov=sim --cov-report=term-missing`.
- Recommended environment? Python 3.10/3.11 + dependencies fixed in `requirements.txt` / `environment.yml`.

---

## Estado actual y próximos pasos / Current status & next steps

**Estado actual:**
- El pipeline de experimentos está automatizado y validado (Exp1, Exp2 smoke test).
- Los scripts generan y consolidan resultados trazables por agente, semilla y riesgo.
- El notebook de análisis produce tablas y gráficos comparativos.
- La estructura del repositorio está limpia y documentada.

**Próximos pasos:**
- Ejecutar Exp2 completo (3 seeds × 5 riesgos), reconsolidar y actualizar notebook/reporte.
- Validar exportación de steps en los CSV para métricas avanzadas.
- Integrar nuevos hallazgos y figuras en el reporte preliminar.
- Lanzar Exp3 (búsqueda PGF) cuando se definan los grids.

**Recomendaciones:**
- Mantener README y reportes actualizados tras cada experimento.
- Documentar hallazgos relevantes y cambios en scripts/notebooks.
- Garantizar reproducibilidad y trazabilidad en cada etapa.

## Ejemplo de interpretación de resultados

Supón que ejecutas un experimento y obtienes la siguiente métrica en el CSV:

```
agent, risk_scale, avg_reward, std_reward
Control, 1.0, 85.2, 4.1
Simbiosis, 1.0, 92.7, 2.8
```

**¿Cómo interpretar estos valores?**

- `avg_reward` (recompensa promedio): Un valor más alto indica que el agente logra mejores resultados en el entorno simulado. En este ejemplo, el agente Simbiosis supera al Control.
- `std_reward` (desviación estándar): Un valor bajo indica que el desempeño es consistente entre episodios. Simbiosis no solo obtiene mayor recompensa, sino que lo hace de forma más estable.

**Recomendaciones:**
- Compara siempre ambos valores (promedio y desviación) para evaluar tanto el rendimiento como la estabilidad.
- Si la diferencia entre agentes es pequeña, revisa los parámetros y repite el experimento con más semillas para confirmar la tendencia.
- No extrapoles estos resultados directamente a entornos reales sin validación adicional; el entorno es un modelo simplificado.

## Dedicatoria / Dedication
Dedico este trabajo a Aurelio y Amarianis, a quienes amo con todo mi corazon.

---

# TUI v4.2 - Unified Intelligence Theory (toy simulator) [ENGLISH]

EN: Gridworld simulator to exercise the Unified Intelligence Theory (TUI v4.2). Includes Control (Q-table) and Symbiosis (DQN+PGF) agents, DOI-ready export, statistical analysis, and visualizations.

## Recent achievements
- Refactor of simulator and runners (v4.2).
- **100%** test coverage in `sim/`; full integration.
- Robust export (JSON/CSV) and seed traceability (`--output_prefix`).
- Phase 2 scripts and SOTA comparison (PPO/A2C/DQN) ready for reproducibility.
- Bilingual visualizations and statistics (ANOVA, t-test); quickstart notebooks.

## Reference environment
- Python 3.10 or 3.11
- Key dependencies (see `requirements.txt` / `environment.yml`):
  torch==2.1.0, stable-baselines3>=2.0.0, gymnasium>=0.28.1, pandas==2.0.3, numpy==1.24.3, matplotlib==3.7.2, seaborn==0.12.2, scipy==1.11.x

## Quick start
1) Create environment (Conda or venv) and install dependencies:
   `pip install -r requirements.txt`
2) Base experiment:
   `python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --risk_scale 1.0 --export results/run1.json`
3) Risk sweep:
   `python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes 100 --seed 42 --output_prefix results/sweep/fase2/seed42/sweep_default --dqn_control`
4) SOTA comparison (optional):
   `python run_sota_comparison.py`  # runs PPO/A2C/DQN for all risk_scale

## Layout
- `sim/`: simulator code, agents, PGF evaluator, visualizations.
- `test/`: unit and integration tests (pytest).
- `results/`: experiment outputs (JSON/CSV/PNG).
  - `sweep/`: risk_scale sweeps (e.g. `fase2/seed42/...`).
  - `runs/`: individual runs.
  - `sota/`: PPO/A2C/DQN models and summaries.
  - `global_summaries/`: consolidated results (e.g. `fase2_global_summary.csv`).
- `docs/`: analysis and result notes.
- `TUI/`: theory documents (TUI v4.x, LaTeX/Markdown).
- `notebooks/`: analysis and graphics notebooks.
- `scripts/`: utilities (phase2, summary merge, SOTA comparison).

## Current limitations
- "Toy" Gridworld environment; no complex benchmarks (MuJoCo/Procgen).
- SOTA comparison focused on PPO; other algorithms not evaluated.
- Some historical docs retain accents/LaTeX legacy to preserve theory.

### Extended limitations

- **Model and experiment assumptions:**
  The simulated environment is a simplified Gridworld, designed to illustrate concepts from the Unified Intelligence Theory. Agents operate in a discrete space, with rewards and penalties defined by the user. No complex physical dynamics or advanced multi-agent interactions are modeled.

- **Scenarios where the methodology may not apply:**
  The TUI/PGF approach is optimized for discrete environments and sequential decision problems. Not recommended for continuous control tasks, realistic physical simulations, or high-dimensional benchmarks (MuJoCo, Procgen, etc.).

- **Sources of bias or experimental uncertainty:**
  Results may be affected by seed selection, episodes, and risk parameters. Metric interpretation depends on correct experimental setup. Robustness is not guaranteed against drastic changes in environment or agent structure.

- **Technical restrictions:**
  The simulator depends on specific libraries (torch, stable-baselines3, gymnasium, etc.) and is optimized for Python 3.10/3.11. Performance may be limited on hardware without acceleration (GPU/CPU). Scalability is intended for medium experiments; not recommended for large clusters or HPC without adaptation.

- **Limitations in interpretation and generalization:**
  Metrics and visualizations reflect behavior in the toy environment; do not extrapolate directly to real systems without further validation. Results are useful for comparing agent variants and strategies, but do not constitute definitive proof of superiority in other domains.

- **Limitations in consolidation and SOTA comparison:**
  SOTA results (PPO, A2C, DQN) are automatically consolidated because the CSV files include the `risk` parameter in the name and columns. However, the `red_team` field always remains `False` for SOTA, so the comparison in the master only covers this mode. This differs from the main pipeline, where TUI agents can have results with both `red_team=True` and `False`.  
  **Implication:** The comparison between SOTA and TUI should be made considering that SOTA only operates in non-adversarial mode (`red_team=False`). It is recommended to explicitly state this difference in analyses and reports to maintain scientific traceability.

## Coverage & quality
- Coverage `sim/`: **100%** (pytest with `--cov=sim`).
- Target network in DQN; no unsafe `eval()` (uses `ast.literal_eval`).
- Graphics warnings mitigated by closing figures; exports in UTF-8.
- SOTA comparison expanded (PPO, A2C, DQN) with risk and global summaries.

## How to cite
- Theory: https://doi.org/10.5281/zenodo.17552094
- Dataset: https://doi.org/10.5281/zenodo.17654593
See `CITATION.cff` for BibTeX.

## Contact
jmrgpr@gmail.com | jrivera77@outlook.com | ORCID https://orcid.org/0009-0000-3013-725X

## Quick FAQ
- CI/CD and graphics backend? Backend `Agg` is forced in visualization modules to run in headless environments.
- How to reproduce coverage? `python -m pytest --cov=sim --cov-report=term-missing`.
- Recommended environment? Python 3.10/3.11 + dependencies fixed in `requirements.txt` / `environment.yml`.

---

## Estado actual y próximos pasos / Current status & next steps

**Estado actual:**
- El pipeline de experimentos está automatizado y validado (Exp1, Exp2 smoke test).
- Los scripts generan y consolidan resultados trazables por agente, semilla y riesgo.
- El notebook de análisis produce tablas y gráficos comparativos.
- La estructura del repositorio está limpia y documentada.

**Próximos pasos:**
- Ejecutar Exp2 completo (3 seeds × 5 riesgos), reconsolidar y actualizar notebook/reporte.
- Validar exportación de steps en los CSV para métricas avanzadas.
- Integrar nuevos hallazgos y figuras en el reporte preliminar.
- Lanzar Exp3 (búsqueda PGF) cuando se definan los grids.

**Recomendaciones:**
- Mantener README y reportes actualizados tras cada experimento.
- Documentar hallazgos relevantes y cambios en scripts/notebooks.
- Garantizar reproducibilidad y trazabilidad en cada etapa.

## Ejemplo de interpretación de resultados

Supón que ejecutas un experimento y obtienes la siguiente métrica en el CSV:

```
agent, risk_scale, avg_reward, std_reward
Control, 1.0, 85.2, 4.1
Simbiosis, 1.0, 92.7, 2.8
```

**¿Cómo interpretar estos valores?**

- `avg_reward` (recompensa promedio): Un valor más alto indica que el agente logra mejores resultados en el entorno simulado. En este ejemplo, el agente Simbiosis supera al Control.
- `std_reward` (desviación estándar): Un valor bajo indica que el desempeño es consistente entre episodios. Simbiosis no solo obtiene mayor recompensa, sino que lo hace de forma más estable.

**Recomendaciones:**
- Compara siempre ambos valores (promedio y desviación) para evaluar tanto el rendimiento como la estabilidad.
- Si la diferencia entre agentes es pequeña, revisa los parámetros y repite el experimento con más semillas para confirmar la tendencia.
- No extrapoles estos resultados directamente a entornos reales sin validación adicional; el entorno es un modelo simplificado.

## Corrección crítica y plan experimental

Se ha identificado una discrepancia en la interpretación de los resultados entre los modos `red_team` y `sota`. Aunque ambos deberían ser comparables, existen diferencias en la configuración y los resultados que requieren atención.

**Próximos pasos:**
1. Revisar la implementación actual de los modos `red_team` y `sota` para identificar diferencias en la configuración y ejecución de los experimentos.
2. Realizar pruebas controladas para comparar directamente los resultados de ambos modos bajo las mismas condiciones.
3. Documentar cualquier discrepancia encontrada y ajustar los análisis y reportes anteriores según sea necesario.
4. Considerar la unificación de los modos o, alternativamente, proporcionar una explicación detallada de las diferencias en la documentación del proyecto.

## Dedicatoria / Dedication
Dedico este trabajo a Aurelio y Amarianis, a quienes amo con todo mi corazon.

---

# TUI v4.2 - Unified Intelligence Theory (toy simulator) [ENGLISH]

EN: Gridworld simulator to exercise the Unified Intelligence Theory (TUI v4.2). Includes Control (Q-table) and Symbiosis (DQN+PGF) agents, DOI-ready export, statistical analysis, and visualizations.

## Recent achievements
- Refactor of simulator and runners (v4.2).
- **100%** test coverage in `sim/`; full integration.
- Robust export (JSON/CSV) and seed traceability (`--output_prefix`).
- Phase 2 scripts and SOTA comparison (PPO/A2C/DQN) ready for reproducibility.
- Bilingual visualizations and statistics (ANOVA, t-test); quickstart notebooks.

## Reference environment
- Python 3.10 or 3.11
- Key dependencies (see `requirements.txt` / `environment.yml`):
  torch==2.1.0, stable-baselines3>=2.0.0, gymnasium>=0.28.1, pandas==2.0.3, numpy==1.24.3, matplotlib==3.7.2, seaborn==0.12.2, scipy==1.11.x

## Quick start
1) Create environment (Conda or venv) and install dependencies:
   `pip install -r requirements.txt`
2) Base experiment:
   `python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --risk_scale 1.0 --export results/run1.json`
3) Risk sweep:
   `python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes 100 --seed 42 --output_prefix results/sweep/fase2/seed42/sweep_default --dqn_control`
4) SOTA comparison (optional):
   `python run_sota_comparison.py`  # runs PPO/A2C/DQN for all risk_scale

## Layout
- `sim/`: simulator code, agents, PGF evaluator, visualizations.
- `test/`: unit and integration tests (pytest).
- `results/`: experiment outputs (JSON/CSV/PNG).
  - `sweep/`: risk_scale sweeps (e.g. `fase2/seed42/...`).
  - `runs/`: individual runs.
  - `sota/`: PPO/A2C/DQN models and summaries.
  - `global_summaries/`: consolidated results (e.g. `fase2_global_summary.csv`).
- `docs/`: analysis and result notes.
- `TUI/`: theory documents (TUI v4.x, LaTeX/Markdown).
- `notebooks/`: analysis and graphics notebooks.
- `scripts/`: utilities (phase2, summary merge, SOTA comparison).

## Current limitations
- "Toy" Gridworld environment; no complex benchmarks (MuJoCo/Procgen).
- SOTA comparison focused on PPO; other algorithms not evaluated.
- Some historical docs retain accents/LaTeX legacy to preserve theory.

### Extended limitations

- **Model and experiment assumptions:**
  The simulated environment is a simplified Gridworld, designed to illustrate concepts from the Unified Intelligence Theory. Agents operate in a discrete space, with rewards and penalties defined by the user. No complex physical dynamics or advanced multi-agent interactions are modeled.

- **Scenarios where the methodology may not apply:**
  The TUI/PGF approach is optimized for discrete environments and sequential decision problems. Not recommended for continuous control tasks, realistic physical simulations, or high-dimensional benchmarks (MuJoCo, Procgen, etc.).

- **Sources of bias or experimental uncertainty:**
  Results may be affected by seed selection, episodes, and risk parameters. Metric interpretation depends on correct experimental setup. Robustness is not guaranteed against drastic changes in environment or agent structure.

- **Technical restrictions:**
  The simulator depends on specific libraries (torch, stable-baselines3, gymnasium, etc.) and is optimized for Python 3.10/3.11. Performance may be limited on hardware without acceleration (GPU/CPU). Scalability is intended for medium experiments; not recommended for large clusters or HPC without adaptation.

- **Limitations in interpretation and generalization:**
  Metrics and visualizations reflect behavior in the toy environment; do not extrapolate directly to real systems without further validation. Results are useful for comparing agent variants and strategies, but do not constitute definitive proof of superiority in other domains.

- **Limitations in consolidation and SOTA comparison:**
  SOTA results (PPO, A2C, DQN) are automatically consolidated because the CSV files include the `risk` parameter in the name and columns. However, the `red_team` field always remains `False` for SOTA, so the comparison in the master only covers this mode. This differs from the main pipeline, where TUI agents can have results with both `red_team=True` and `False`.  
  **Implication:** The comparison between SOTA and TUI should be made considering that SOTA only operates in non-adversarial mode (`red_team=False`). It is recommended to explicitly state this difference in analyses and reports to maintain scientific traceability.

## Coverage & quality
- Coverage `sim/`: **100%** (pytest with `--cov=sim`).
- Target network in DQN; no unsafe `eval()` (uses `ast.literal_eval`).
- Graphics warnings mitigated by closing figures; exports in UTF-8.
- SOTA comparison expanded (PPO, A2C, DQN) with risk and global summaries.

## How to cite
- Theory: https://doi.org/10.5281/zenodo.17552094
- Dataset: https://doi.org/10.5281/zenodo.17654593
See `CITATION.cff` for BibTeX.

## Contact
jmrgpr@gmail.com | jrivera77@outlook.com | ORCID https://orcid.org/0009-0000-3013-725X

## Quick FAQ
- CI/CD and graphics backend? Backend `Agg` is forced in visualization modules to run in headless environments.
- How to reproduce coverage? `python -m pytest --cov=sim --cov-report=term-missing`.
- Recommended environment? Python 3.10/3.11 + dependencies fixed in `requirements.txt` / `environment.yml`.

---

## Estado actual y próximos pasos / Current status & next steps

**Estado actual:**
- El pipeline de experimentos está automatizado y validado (Exp1, Exp2 smoke test).
- Los scripts generan y consolidan resultados trazables por agente, semilla y riesgo.
- El notebook de análisis produce tablas y gráficos comparativos.
- La estructura del repositorio está limpia y documentada.

**Próximos pasos:**
- Ejecutar Exp2 completo (3 seeds × 5 riesgos), reconsolidar y actualizar notebook/reporte.
- Validar exportación de steps en los CSV para métricas avanzadas.
- Integrar nuevos hallazgos y figuras en el reporte preliminar.
- Lanzar Exp3 (búsqueda PGF) cuando se definan los grids.

**Recomendaciones:**
- Mantener README y reportes actualizados tras cada experimento.
- Documentar hallazgos relevantes y cambios en scripts/notebooks.
- Garantizar reproducibilidad y trazabilidad en cada etapa.

## Ejemplo de interpretación de resultados

Supón que ejecutas un experimento y obtienes la siguiente métrica en el CSV:

```
agent, risk_scale, avg_reward, std_reward
Control, 1.0, 85.2, 4.1
Simbiosis, 1.0, 92.7, 2.8
```

**¿Cómo interpretar estos valores?**

- `avg_reward` (recompensa promedio): Un valor más alto indica que el agente logra mejores resultados en el entorno simulado. En este ejemplo, el agente Simbiosis supera al Control.
- `std_reward` (desviación estándar): Un valor bajo indica que el desempeño es consistente entre episodios. Simbiosis no solo obtiene mayor recompensa, sino que lo hace de forma más estable.

**Recomendaciones:**
- Compara siempre ambos valores (promedio y desviación) para evaluar tanto el rendimiento como la estabilidad.
- Si la diferencia entre agentes es pequeña, revisa los parámetros y repite el experimento con más semillas para confirmar la tendencia.
- No extrapoles estos resultados directamente a entornos reales sin validación adicional; el entorno es un modelo simplificado.

## Corrección crítica y plan experimental

Se ha identificado una discrepancia en la interpretación de los resultados entre los modos `red_team` y `sota`. Aunque ambos deberían ser comparables, existen diferencias en la configuración y los resultados que requieren atención.

**Próximos pasos:**
1. Revisar la implementación actual de los modos `red_team` y `sota` para identificar diferencias en la configuración y ejecución de los experimentos.
2. Realizar pruebas controladas para comparar directamente los resultados de ambos modos bajo las mismas condiciones.
3. Documentar cualquier discrepancia encontrada y ajustar los análisis y reportes anteriores según sea necesario.
4. Considerar la unificación de los modos o, alternativamente, proporcionar una explicación detallada de las diferencias en la documentación del proyecto.

## Dedicatoria / Dedication
Dedico este trabajo a Aurelio y Amarianis, a quienes amo con todo mi corazon.

---
=======
Este repositorio puede sincronizarse con Zenodo vía GitHub Actions (`.github/workflows/zenodo.yml`) usando la licencia de código:

```yaml
license: "Apache-2.0"
<<<<<<< HEAD
>>>>>>> 603de3f (Change license to Apache 2.0 and update project info)
=======

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
>>>>>>> 6f926b7 (Update README with TUI v4.1 details and instructions)
