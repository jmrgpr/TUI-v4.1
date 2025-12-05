# Resultados – Configuración D (Solo 6x6)

## Resumen
- Entrenamiento solo en 6x6, sin curriculum ni transfer.
- Documentar setup y diferencias respecto a A y B.

## Mapeo de métricas a columnas CSV
| Métrica                 | Columna en CSV         | Ejemplo de archivo    |
|-------------------------|------------------------|-----------------------|
| Éxito últimos 100       | success_last_100       | summary_D.csv         |
| Gate (%)                | gate                   | summary_D.csv         |
| Episodio primer éxito   | first_success_episode  | summary_D.csv         |
| Convergencia            | convergence_episode    | summary_D.csv         |

## Ejemplo de extracción de métricas
Para obtener el éxito últimos 100 en 6x6, seed 42:
- Archivo: `summary_D.csv`
- Columna: `success_last_100`

## Interpretación y trazabilidad
- Comparar con A y B para evidenciar el impacto del curriculum y transfer.
- Documentar cualquier hallazgo relevante y citar siempre el archivo y columna de origen.

---

*Plantilla revisada para trazabilidad y claridad. Revisión: 2025-12-05.*
