


# TUI v4.1 Toy Model — RL Symbiosis

Este repositorio contiene el toy model oficial de la Teoría Unificada de la Inteligencia (TUI v4.1), con validación experimental de la hipótesis H1: "La inteligencia emerge al capitalizar el riesgo, no al evitarlo".

**Actualización Nov 2025:**
- PGF redefine el reward para premiar explícitamente la reducción de riesgo entre pasos (prudencia).
- Logging profesional: se reportan por episodio supervivencia, tasa de tripwires/shocks, evolución de PGF y reward ambiental.
- Los experimentos permiten comparar control vs simbiosis en distintos niveles de riesgo (`risk_scale` parametrizable, sin hardcoding).
- Todas las métricas y comentarios son bilingües y alineados con la teoría TUI v4.1.

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
