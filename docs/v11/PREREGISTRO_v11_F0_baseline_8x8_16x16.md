
# PREREGISTRO_v11_F0_baseline_8x8_16x16.md

## Statement doctrinal
El objetivo de v11 es demostrar que la economía viable y la regularización escalan a 16×16, usando PGF solo como métrica/constraint (prohibido como reward/shaping). Esta decisión es doctrinal y cierra explícitamente la lección de v10: PGF como reward está prohibido por diseño.

## Preregistro experimento v11.F0 – Baseline 8×8 y 16×16

### Objetivo
Demostrar que el stack mínimo de v11 (DQN + regularización obligatoria + nueva exploración + representación 16×16) mantiene el desempeño en 8×8 y explora el límite en 16×16.

### Diseño experimental
- Entorno: environment_v2 (nombre de clase/archivo logueado en summary)
- Arquitectura: igual a v10 F2 (capas [N1, N2, ...])
- Regularización: L2_weight_decay=1e-4, dropout=0.1 (ajustar según config)
- PGF_reward = OFF, PGF_shaping = OFF
- Episodios: 8×8 (1500), 16×16 (3000)
- Seeds:
  - Smoke test: [42] (8×8, 500 episodios)
  - Batch inicial: [42, 13] (añadir 101 solo si ambas son razonables)
- Flags y config documentados explícitamente

### Gates de éxito
- 8×8: ≥80% éxito en ≥2/3 seeds (últimos 100 episodios)
- 16×16: ≥20% éxito en ≥2/3 seeds, sin colapsos

### Outputs
- results/v11/F0_baseline_8x8_16x16/
- REPORTE_v11_F0_baseline_8x8_16x16.md (template: Setup, Hiperparámetros, Resultados, Discusión)

### Preguntas clave
- ¿Se mantiene el desempeño en 8×8?
- ¿Qué tan lejos llega v11 en 16×16 con el stack mínimo?

---
*Documento actualizado el 10/12/2025 por GitHub Copilot para alineación total con el Protocolo v11 Final.*
