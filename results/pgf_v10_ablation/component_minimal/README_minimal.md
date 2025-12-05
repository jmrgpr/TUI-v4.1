# Ablation Mínima (Control Negativo)

Entrenamiento en un solo entorno (6×6 o 8×8) sin shaping, transfer, curriculum ni reward extra.

## Parámetros
- Solo reward por goal y penalización por step
- Sin shaping ni transfer
- Seeds: [42, 13]
- Episodios: 1000

## Archivos
- episodes_minimal_{seed}.csv
- summary_minimal.csv

## Interpretación
Evalúa el desempeño del agente en la versión más simple del entorno.