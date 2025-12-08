# PREREGISTRO_v11_alpha.md

## Preregistro inicial – Protocolo TUI v11 (alpha)

Este preregistro define los cambios, objetivos y criterios derivados de la síntesis v10, para la apertura científica de v11.

### Cambios clave respecto a v10

- Nueva representación para grids 16×16+
- Regularización como componente obligatorio
- PGF solo como métrica offline y constraint
- Política de exploración adaptada para entornos grandes

### Objetivos

- Superar la frontera operativa de v10 en 16×16 (ver REPORTE_FASE4_SCALABILITY_v10.md)
- Mantener reproducibilidad y trazabilidad total (ver README_MASTER_v10.md)
- Documentar todos los experimentos y logs desde el inicio

### Metodología

- Seeds recomendadas: 42, 101 (consistente con v10)
- Grids objetivo: 8×8 y 16×16
- Formato de logs: markdown y CSV, siguiendo los ejemplos de F4
- Referencias directas a reportes v10: REPORTE_ABLATION_v10.md, REPORTE_ABLATION_COMPONENTES_v10.md, REPORTE_PGF_OFFLINE_v10.md, REPORTE_FASE4_SCALABILITY_v10.md

### Criterios de éxito

- Gate: >20% éxito en 16×16 con overhead aceptable
- Robustez en 8×8 y 16×16
- Documentación y logs completos

---
*Documento generado automáticamente el 8/12/2025 por GitHub Copilot.*
