![CI](https://github.com/jmrgpr/TUI-v4.1/actions/workflows/python-tests.yml/badge.svg) ![Version](https://img.shields.io/badge/version-4.2-blue) ![Docs](https://img.shields.io/badge/Docs-CC%20BY--NC--SA%204.0-lightgrey) ![DOI Dataset](https://zenodo.org/badge/DOI/10.5281/zenodo.17654593.svg) ![DOI Theory](https://zenodo.org/badge/DOI/10.5281/zenodo.17552094.svg)

# TUI v4.2 - Unified Intelligence Theory (toy simulator)

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
   `python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes 100 --seed 42 --output_prefix results/sweep_risk`
4) Comparacion SOTA (opcional):  
   `python run_sota_comparison.py`  # corre PPO/A2C/DQN en todos los risk_scale

## Estructura / Layout
- `sim/` : codigo del simulador, agentes, evaluador PGF, visualizaciones.
- `test/` : pruebas unitarias e integracion (pytest).
- `results/` : salidas JSON/CSV/PNG de experimentos.
- `docs/` : analisis y notas de resultados.
- `TUI/` : documentos de teoria (TUI v4.x, LaTeX/Markdown).
- `notebooks/` : cuadernos de analisis y graficos.
- `scripts/` : utilidades (fase2, merge de resumenes, comparacion SOTA).

## Limitaciones actuales / Current limitations
- Entorno "toy" Gridworld; sin benchmarks complejos (MuJoCo/Procgen).
- Comparacion SOTA centrada en PPO; otros algoritmos no evaluados.
- Algunos docs historicos mantienen acentos/LaTeX legacy para preservar la teoria.

## Cobertura y calidad / Coverage & quality
- Cobertura `sim/`: **100%** (pytest con `--cov=sim`).  
- Target network en DQN; sin `eval()` inseguro (se usa `ast.literal_eval`).  
- Warnings graficos mitigados cerrando figuras; exportaciones en UTF-8.
- Comparacion SOTA ampliada (PPO, A2C, DQN) con sumarios por riesgo y global.

## Como citar / How to cite
- Teoria: https://doi.org/10.5281/zenodo.17552094  
- Dataset: https://doi.org/10.5281/zenodo.17654593  
Ver `CITATION.cff` para BibTeX.

## Contacto / Contact
jmrgpr@gmail.com | jrivera77@outlook.com | ORCID https://orcid.org/0009-0000-3013-725X

## FAQ rapida
- ¿CI/CD y backend gráfico? Se fuerza backend `Agg` en módulos de visualización para correr en entornos headless.
- ¿Cómo reproducir coberturas? `python -m pytest --cov=sim --cov-report=term-missing`.
- ¿Entorno recomendado? Python 3.10/3.11 + dependencias fijadas en `requirements.txt` / `environment.yml`.

---

## Dedicatoria / Dedication
Dedico este trabajo a Aurelio y Amarianis, a quienes amo con todo mi corazon.
