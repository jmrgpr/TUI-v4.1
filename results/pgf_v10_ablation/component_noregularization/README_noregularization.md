# Ablation sin Regularización

Entrenamiento sin técnicas de regularización (sin epsilon decay, sin batchnorm, etc.).

## Parámetros
- Curriculum estándar
- Sin regularización
- Seeds: [42, 13]
- Episodios: 1000

## Archivos
- episodes_noregularization_{seed}.csv
- summary_noregularization.csv

## Interpretación
Medir el impacto de quitar regularización en la estabilidad y éxito del agente.