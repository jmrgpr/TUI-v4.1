
# Configuración A – Curriculum Baseline

Esta carpeta contiene la referencia al baseline v10_viable (no se reentrena).

## Archivos fuente
- Symlinks o copias de:
  - `results/pgf_v10_viable/resultados/phase*_*.csv`
  - `curriculum_summary_*.csv`

## Mapeo de métricas a columnas CSV
| Métrica             | Columna en CSV                | Ejemplo de archivo |
|---------------------|-------------------------------|-------------------|
| Éxito total         | `success_rate_total`          | curriculum_summary_102250.csv |
| Éxito últimos 100   | `success_last_100`            | curriculum_summary_102250.csv |
| Gate (%)            | `gate`                        | curriculum_summary_102250.csv |
| Gate pasado         | `gate_passed`                 | curriculum_summary_102250.csv |
| Primer éxito        | `first_success_episode`       | curriculum_summary_102250.csv |
| Convergencia        | `convergence_episode`         | curriculum_summary_102250.csv |

## Ejemplo de extracción de métricas
Para obtener el éxito últimos 100 en 8x8, seed 42:
  - Archivo: `curriculum_summary_102250.csv`
  - Columna: `success_last_100`

## Interpretación y trazabilidad
- Comparar con las variantes B, D y C para evaluar la importancia del curriculum.
- Documentar cualquier hallazgo relevante y citar siempre el archivo y columna de origen.

---

*Este README ha sido revisado para trazabilidad y claridad. Revisión: 2025-12-05.*