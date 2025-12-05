# Resultados – Configuración A (Curriculum Baseline)

## Resumen
- Baseline v10_viable, sin reentrenar.
- Symlinks o copias de los archivos originales.

## Mapeo de métricas a columnas CSV
| Métrica                 | Columna en CSV         | Ejemplo de archivo              |
|-------------------------|------------------------|---------------------------------|
| Éxito últimos 100       | success_last_100       | curriculum_summary_102250.csv   |
| Gate (%)                | gate                   | curriculum_summary_102250.csv   |
| Episodio primer éxito   | first_success_episode  | curriculum_summary_102250.csv   |
| Convergencia            | convergence_episode    | curriculum_summary_102250.csv   |

## Ejemplo de extracción de métricas
Para obtener el éxito últimos 100 en 8x8, seed 42:
- Archivo: `curriculum_summary_102250.csv`
- Columna: `success_last_100`

## Interpretación y trazabilidad
- Comparar con variantes B, D, C para evaluar la importancia del curriculum.
- Documentar cualquier hallazgo relevante y citar siempre el archivo y columna de origen.

---

*Plantilla revisada para trazabilidad y claridad. Revisión: 2025-12-05.*
