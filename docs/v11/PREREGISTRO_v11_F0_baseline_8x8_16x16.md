# PREREGISTRO_v11_F0_baseline_8x8_16x16.md

## Preregistro experimento v11.F0 – Baseline 8×8 y 16×16

### Objetivo

Demostrar que el stack mínimo de v11 (DQN + regularización obligatoria + nueva exploración + representación 16×16) mantiene el desempeño en 8×8 y explora el límite en 16×16.

### Diseño experimental

- Grids: 8×8 y 16×16
- Seeds: 42, 101
- Componentes:
  - DQN
  - Regularización ON (como en F2/F4)
  - Sin shaping PGF, sin reward_extra
  - Nueva política de exploración para 16×16 (epsilon schedule lento o dos fases)
- Outputs:
  - results/v11_alpha/F0_baseline_8x8_16x16/
  - REPORTE_v11_F0_baseline.md

### Preguntas clave
- ¿Se mantiene el desempeño en 8×8?
- ¿Qué tan lejos llega v11 en 16×16 con el stack mínimo?

---
*Documento generado automáticamente el 8/12/2025 por GitHub Copilot.*
