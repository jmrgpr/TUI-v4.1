# Ablation sin Transfer

Entrenamiento con curriculum, pero reiniciando pesos en cada fase (sin transfer).

## Parámetros
- Curriculum estándar
- Sin transferencia de pesos entre fases
- Seeds: [42, 13]
- Episodios: 1000

## Archivos
- episodes_notransfer_{seed}.csv
- summary_notransfer.csv

## Interpretación
Medir el impacto de no transferir conocimiento entre fases.