# Configuración B – Directo 8×8

Entrenamiento solo en 8×8, sin curriculum.

## Parámetros
- grid_size=8
- initial_resources=8.0
- step_cost=-0.15
- resource_spawn_rate=0.40
- goal_reward=20.0
- DQN idéntico a v10_viable
- Episodios: 2500
- Seeds: [42, 13, 101]

## Archivos
- episodes_direct_8x8_{seed}.csv
- summary_B.csv

## Interpretación
Comparar success_last_100 con baseline (A) para evaluar la importancia del curriculum.