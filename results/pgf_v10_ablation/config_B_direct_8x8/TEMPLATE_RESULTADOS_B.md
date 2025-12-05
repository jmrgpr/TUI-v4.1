# Resultados – Configuración B (Directo 8x8)

## Resumen
- Entrenamiento directo en 8x8, sin curriculum.
- Documentar setup y diferencias respecto a A.

## Mapeo de métricas a columnas CSV
| Métrica                 | Columna en CSV         | Ejemplo de archivo    |
|-------------------------|------------------------|-----------------------|
| Éxito últimos 100       | success_last_100       | summary_B.csv         |
| Gate (%)                | gate                   | summary_B.csv         |
| Episodio primer éxito   | first_success_episode  | summary_B.csv         |
| Convergencia            | convergence_episode    | summary_B.csv         |

## Ejemplo de extracción de métricas
Para obtener el éxito últimos 100 en 8x8, seed 42:
- Archivo: `summary_B.csv`
- Columna: `success_last_100`

## Interpretación y trazabilidad
- Comparar con A para evidenciar el impacto del curriculum.
- Documentar cualquier hallazgo relevante y citar siempre el archivo y columna de origen.

---

*Plantilla revisada para trazabilidad y claridad. Revisión: 2025-12-05.*
