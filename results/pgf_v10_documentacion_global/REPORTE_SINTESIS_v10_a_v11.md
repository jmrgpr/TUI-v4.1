# REPORTE_SINTESIS_v10_a_v11.md

## Síntesis científica y puente de diseño: v10 → v11

Este documento resume los hallazgos clave de v10 y define los requisitos y cambios para la apertura de v11.

### Qué se queda para v11

- Economía viable y robusta
- Regularización como feature principal
- 8×8 directo como caballo de batalla

### Qué se descarta

- Shaping PGF como reward (prohibido)
- RewardExtra (inestable)
- Curriculum inverso (frágil)

### Qué hay que rediseñar

- Representación para 16×16+
- Política de exploración para grids grandes
- Uso de PGF solo como métrica offline y constraint, no como reward directo

### Requisitos para v11

- Preregistro explícito de cambios derivados de v10
- Pipeline reproducible y auditable
- Documentación y logs desde el inicio

---
*Documento generado automáticamente el 8/12/2025 por GitHub Copilot.*
