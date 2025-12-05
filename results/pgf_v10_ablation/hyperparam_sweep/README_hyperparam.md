# Sweep de Hiperparámetros

Entrenamiento variando sistemáticamente LR, gamma, batch size, etc.

## Parámetros
- Variaciones de LR, gamma, batch size
- Seeds: [42, 13]
- Episodios: 1000

## Archivos
- episodes_hyperparam_{seed}_LR{lr}_G{gamma}_B{batch}.csv
- summary_hyperparam.csv

## Interpretación
Medir la sensibilidad del desempeño a los hiperparámetros.