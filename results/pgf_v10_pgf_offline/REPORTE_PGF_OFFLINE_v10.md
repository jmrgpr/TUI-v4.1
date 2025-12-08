# REPORTE_PGF_OFFLINE_v10

## Resumen Ejecutivo
Análisis offline de PGF/I_op sobre episodios v10_viable y multi-seed. Se estudia la correlación PGF ↔ éxito y overhead, y la firma PGF de políticas sanas vs colapsadas.

## Resultados y figuras

### Estadísticos principales

| Fase         | PGF (media ± std) | I_op (media ± std) | Correlación PGF/I_op |
|--------------|-------------------|--------------------|----------------------|
| 4x4 (102250) | 1.94 ± 1.22       | 0.48 ± 0.08        | 0.63                 |
| 6x6 (102250) | 1.79 ± 1.32       | 0.40 ± 0.08        | 0.51                 |
| 8x8 (102250) | 1.21 ± 1.25       | 0.42 ± 0.08        | 0.44                 |

### Figuras
- Histogramas de PGF e I_op por fase (ver carpeta `analysis/`)
- Tablas resumen por CSV

## Interpretación y limitaciones
- La correlación PGF/I_op disminuye con el tamaño del entorno.
- Las políticas sanas muestran PGF alto y I_op estable; colapsos se reflejan en PGF bajo.
- Limitación: el mapeo de variables es aproximado, no incluye todos los eventos del entorno.

---
*Reporte generado automáticamente el 8/12/2025 por GitHub Copilot.*
