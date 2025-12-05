# Resultados – Configuración C (Inverse Curriculum)

## Resumen
- Entrenamiento con curriculum inverso (de 8x8 a menor dificultad).
- Documentar setup y diferencias respecto a A y B.

## Mapeo de métricas a columnas CSV
| Métrica                 | Columna en CSV         | Ejemplo de archivo    |
|-------------------------|------------------------|-----------------------|
| Éxito últimos 100       | success_last_100       | summary_C.csv         |
| Gate (%)                | gate                   | summary_C.csv         |
| Episodio primer éxito   | first_success_episode  | summary_C.csv         |
| Convergencia            | convergence_episode    | summary_C.csv         |

## Ejemplo de extracción de métricas
Para obtener el éxito últimos 100 en 8x8, seed 42:
- Archivo: `summary_C.csv`
- Columna: `success_last_100`

## Interpretación y trazabilidad
- Comparar con A y B para evidenciar el impacto del curriculum inverso.
- Documentar cualquier hallazgo relevante y citar siempre el archivo y columna de origen.

---

*Plantilla creada y revisada para trazabilidad y claridad. Revisión: 2025-12-05.*
