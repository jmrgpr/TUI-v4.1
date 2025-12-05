# Configuración D – Solo 6×6

Entrenamiento solo en 6×6, con budget completo.

## Parámetros
- grid_size=6
- initial_resources=8.0
- step_cost=-0.15
- resource_spawn_rate=0.40
- goal_reward=20.0
- DQN idéntico a v10_viable
- Episodios: 2500
- Seeds: [42, 13, 101]

## Archivos
- episodes_6x6_only_{seed}.csv
- summary_D.csv

## Interpretación
Evaluar si el 6×6 es suficiente como crisol comparando con baseline y directo 8×8.