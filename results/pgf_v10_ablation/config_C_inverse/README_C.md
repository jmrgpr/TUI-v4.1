# Configuración C – Curriculum Inverso

Entrenamiento en orden inverso: 8×8 → 6×6 → 4×4.

## Parámetros
- Fase 1: 8×8
- Fase 2: 6×6
- Fase 3: 4×4
- Episodios: igual que curriculum estándar
- Seeds: [42, 13, 101]

## Archivos
- episodes_inverse_{seed}.csv
- summary_C.csv

## Interpretación
Comparar desempeño con baseline para evaluar si el orden del curriculum importa.