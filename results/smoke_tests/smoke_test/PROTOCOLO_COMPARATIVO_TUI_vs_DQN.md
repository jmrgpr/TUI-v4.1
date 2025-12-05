# Protocolo comparativo TUI/PGF vs DQN-Control (FASE 4)

**Objetivo:** Comparar el desempeño del agente TUI/PGF contra el DQN-Control en el entorno easy 3x3, bajo condiciones controladas y reproducibles.

## Configuración experimental
- Entorno: easy 3x3, risk_scale=0.5
- Episodios: 1000
- Seeds: 42, 123, 456
- Métricas principales:
  - Reward media (últimos 100 episodios)
  - % episodios con reward > 0
  - Opcional: riesgo asumido, tiempo hasta la meta

## Agentes a comparar
- Tabular Q-learning (referencia)
- DQN-Control baseline (sin TUI, lambda_gaming=0.0, state_mode=coords_only)
- TUI/PGF (agente prudencial, misma observación y entorno)

## Comandos sugeridos
### DQN-Control
```
python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --grid_size 3 --risk_scale 0.5 --dqn_control --lambda_gaming 0.0 --learning_rate 0.001 --gamma 0.95 --epsilon 0.2 --output_prefix results/smoke_test/dqn_control_easy_seed42
```
### TUI/PGF
```
python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --grid_size 3 --risk_scale 0.5 --tui_only --pgf_mix 1.0 --output_prefix results/smoke_test/tui_pgf_easy_seed42
```

## Protocolo de análisis
- Ejecutar ambos agentes con las tres seeds.
- Registrar los resultados en JSON y CSV.
- Comparar las métricas principales y graficar la distribución de recompensas.
- Documentar si TUI/PGF se comporta igual, peor o mejor que DQN-Control.
- Anotar limitaciones (entorno benigno, risk_scale fijo, etc.).

## Resultado esperado
Primer resultado empírico serio: comparación directa TUI vs DQN en un entorno donde ambos pueden aprender.

---
**FASE 4 documentada. Listo para commit/tag y ejecución.**
