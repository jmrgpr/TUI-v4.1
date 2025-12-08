![CI](https://github.com/jmrgpr/TUI-v4.1/actions/workflows/python-tests.yml/badge.svg)
![Version](https://img.shields.io/badge/version-4.2-blue)
![Docs](https://img.shields.io/badge/Docs-CC%20BY--NC--SA%204.0-lightgrey)
![DOI Dataset](https://zenodo.org/badge/DOI/10.5281/zenodo.17654593.svg)
![DOI Theory](https://img.shields.io/badge/DOI-10.5281/zenodo.17552094-blue)
![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)
![Reproducible](https://img.shields.io/badge/reproducible-validated-success)
![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
## Limitaciones y amenazas a la validez / Limitations & Threats to Validity



**EN:**
- Experiments were conducted in a “toy RL” environment, not in complex benchmarks like MuJoCo or Procgen.
- SOTA comparison includes only PPO; other algorithms (A2C, SAC) were not evaluated.
- SOTA results are based on a single seed, which may limit statistical robustness.
- The number of episodes and configurations is limited; results may vary with different parameters.
- The η_acumulativo metric was not explicitly calculated.
- Results and conclusions should be interpreted as preliminary evidence, not definitive validation.

## Reproducibilidad rapida / Quick start
1) Crear entorno (Conda o venv) e instalar dependencias:  
   `pip install -r requirements.txt`
2) Experimento base:  
   `python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes 100 --seed 42 --output_prefix results/sweep/fase2/seed42/sweep_default --dqn_control`
4) Comparacion SOTA (opcional):  
   `python run_sota_comparison.py`  # corre PPO/A2C/DQN en todos los risk_scale

## Estructura / Layout
  - `runs/` corridas individuales
  - `sota/` modelos y resúmenes PPO/A2C/DQN.  
  - `global_summaries/` consolidados (p.ej. `fase2_global_summary.csv`).  
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

- **Fuentes de sesgo o incertidumbre experimental:**  
  Los resultados pueden verse afectados por la selección de semillas, episodios y parámetros de riesgo. La interpretación de métricas depende de la correcta configuración experimental. No se garantiza robustez ante cambios drásticos en la estructura del entorno o los agentes.

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
# TUI v4.2 — Unified Intelligence Theory

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

- **Fuentes de sesgo o incertidumbre experimental:**  
  Los resultados pueden verse afectados por la selección de semillas, episodios y parámetros de riesgo. La interpretación de métricas depende de la correcta configuración experimental. No se garantiza robustez ante cambios drásticos en la estructura del entorno o los agentes.

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
# TUI v4.2 — Unified Intelligence Theory
=======
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

- **Fuentes de sesgo o incertidumbre experimental:**  
  Los resultados pueden verse afectados por la selección de semillas, episodios y parámetros de riesgo. La interpretación de métricas depende de la correcta configuración experimental. No se garantiza robustez ante cambios drásticos en la estructura del entorno o los agentes.

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
# TUI v4.2 — Unified Intelligence Theory
=======
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

---

## 📊 Serie v10: Economía Viable + Curriculum Learning

### v10_viable (Baseline Single-Seed) ✅
**Estado**: Completado y congelado  
**Preregistro**: commit `e099ab9`  
**Resultados**: commit `cf1438c`  
**Fecha**: 5 de diciembre de 2025

**Resumen**:
- Economía viable validada (balance 8.0, step_cost -0.15, spawn_rate 0.40)
- Curriculum 4×4→6×6→8×8 con seed 42
- Gates superados: **93%, 68%, 87%** (últimos 100 eps)
- Transfer learning funcional (8×8 primer éxito ep 1)
- Breakthrough 6×6 documentado (ep 587, convergencia súbita)

📂 **Datos**: `results/pgf_v10_viable/`  
📄 **Reporte completo**: [REPORTE_FINAL_v10_viable.md](results/pgf_v10_viable/reportes/REPORTE_FINAL_v10_viable.md)  
📄 **Resumen ejecutivo**: [RESUMEN_EJECUTIVO.md](results/pgf_v10_viable/RESUMEN_EJECUTIVO.md)  
📊 **Figuras**: `results/pgf_v10_viable/figuras/` (6 visualizaciones)

**⚠️ Limitaciones conocidas**:
- **N=1** (una sola seed, seed=42)
- 6×6 sensible a hyperparameters (requirió ajustes epsilon 0.9, max_steps 50)
- Varianza 6×6 alta (peak 96% vs final 68%)

**🔄 Trabajo en progreso**:
- [ ] **Multi-seed validation** (N=5, seeds=[13,42,101,2025,9999]) → `pgf_v10_multiseed/`
- [ ] **Ablation study** (curriculum vs directo 8×8) → `pgf_v10_ablation/`
- [ ] **Análisis PGF offline** (I_op correlaciones) → `pgf_v10_pgf_offline/`
- [ ] **Escalado 16×16** (opcional) → `pgf_v10_scalability/`

**Próximos pasos v10**:
1. Robustez (multi-seed) → confirmar reproducibilidad
2. Causalidad (ablation) → demostrar curriculum necesario
3. Teoría (PGF offline) → conectar con TUI/PGF
4. Solo después: v11 (nueva familia experimentos)

📖 **Roadmap completo**: Ver [Fase 0-4 en documentación interna]

---

## Limitaciones actuales / Current limitations
- Entorno "toy" Gridworld; sin benchmarks complejos (MuJoCo/Procgen).
- Comparacion SOTA centrada en PPO; otros algoritmos no evaluados.
- Algunos docs historicos mantienen acentos/LaTeX legacy para preservar la teoria.

### Ampliación de limitaciones

- **Supuestos del modelo y experimentos:**  
  El entorno simulado es un Gridworld simplificado, diseñado para ilustrar conceptos de la Teoría Unificada de la Inteligencia. Se asume que los agentes operan en un espacio discreto, con recompensas y penalizaciones definidas por el usuario. No se modelan dinámicas físicas complejas ni interacciones multiagente avanzadas.

- **Escenarios donde la metodología puede no ser aplicable:**  
  El enfoque TUI/PGF está optimizado para entornos discretos y problemas de decisión secuencial. No se recomienda para tareas de control continuo, simulaciones físicas realistas, ni benchmarks de alta dimensionalidad (MuJoCo, Procgen, etc.).

- **Fuentes de sesgo o incertidumbre experimental:**  
  Los resultados pueden verse afectados por la selección de semillas, episodios y parámetros de riesgo. La interpretación de métricas depende de la correcta configuración experimental. No se garantiza robustez ante cambios drásticos en la estructura del entorno o los agentes.

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

Notas bilingües:
Todos los comentarios, docstrings y outputs están en español e inglés para facilitar colaboración internacional y reproducibilidad científica.

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


## Nota sobre herramientas utilizadas
Este proyecto fue desarrollado y documentado con apoyo de herramientas de inteligencia artificial (IA) para acelerar tareas de refactorización, documentación y validación técnica. Todas las decisiones científicas, experimentales y de diseño fueron tomadas por el autor humano, garantizando la trazabilidad y reproducibilidad del trabajo.

## Dedicatoria / Dedication
Dedico este trabajo a Aurelio y Amarianis, a quienes amo con todo mi corazón.

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

## Dedicatoria / Dedication
Dedico este trabajo a Aurelio y Amarianis, a quienes amo con todo mi corazon.

<<<<<<< HEAD
=======
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

>>>>>>> e960eb9 (Cobertura 99%, smoke test validado, artefactos exportados y simulador robusto listo para publicación.)
---