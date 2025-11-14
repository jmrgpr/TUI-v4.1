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


## Output esperado
```
Control:   reward=-4.95, tripwires=0.04, shocks=0.01, survival=95.0
Simbiosis: reward=+455.86, tripwires=1.71, shocks=0.42, survival=580.0
→ α ≈ 0.36
PGF evolutivo y reward ambiental reportados por episodio.

Gráficos generados automáticamente:
- Evolución temporal de PGF, reward, flexibilidad, robustez y Q-optimal.
- Boxplots y heatmaps comparativos por agente y risk_scale.
- Scatterplot PGF vs reward final.
- Intervalos de confianza y tests estadísticos (t-test, ANOVA) en visuales y consola.
- Interpretación automática bilingüe en todos los outputs.

Exportación avanzada:
- Resultados en JSON y CSV con métricas por episodio (flexibilidad, robustez, Q-optimal).
- Resúmenes tabulares bilingües en consola y visuales.
```


## Flags principales
- `--episodes`: número de episodios / number of episodes
- `--seed`: semilla aleatoria / random seed
- `--grid_size`: tamaño del grid / grid size
- `--risk_scale`: escala de riesgo (parametrizable, prudencial) / risk scale (parametric, prudential)
- `--visualize`: muestra ASCII del agente B / ASCII visualization of agent B
- `--plot`: gráfico I_op vs P_riesgo / plot I_op vs P_riesgo
- `--export`: exporta resultados a JSON/CSV / export results to JSON/CSV


## Reproducibilidad
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
