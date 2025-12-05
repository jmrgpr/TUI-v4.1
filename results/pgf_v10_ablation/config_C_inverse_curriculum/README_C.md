# Configuración C – Inverse Curriculum

Esta carpeta contiene los resultados de la variante con curriculum inverso (entrenamiento comenzando en 8x8 y reduciendo dificultad).

## Parámetros principales
- grid_size inicial=8, reducción progresiva
- initial_resources variable
- DQN idéntico a v10_viable
- Episodios: 2500
- Seeds: [42, 13, 101]

## Archivos fuente
- `episodes_inverse_curriculum_{seed}.csv`
- `summary_C.csv`

## Mapeo de métricas a columnas CSV
| Métrica             | Columna en CSV                | Ejemplo de archivo |
|---------------------|-------------------------------|-------------------|
| Éxito total         | `success_rate_total`          | summary_C.csv |
| Éxito últimos 100   | `success_last_100`            | summary_C.csv |
| Gate (%)            | `gate`                        | summary_C.csv |
| Gate pasado         | `gate_passed`                 | summary_C.csv |
| Primer éxito        | `first_success_episode`       | summary_C.csv |
| Convergencia        | `convergence_episode`         | summary_C.csv |

## Ejemplo de extracción de métricas
Para obtener el éxito últimos 100 en 8x8, seed 42:
  - Archivo: `summary_C.csv`
  - Columna: `success_last_100`

## Interpretación y trazabilidad
- Comparar con las configuraciones A y B para evaluar el impacto del curriculum inverso.
- Documentar cualquier hallazgo relevante y citar siempre el archivo y columna de origen.

---

*Este README ha sido creado y revisado para trazabilidad y claridad. Revisión: 2025-12-05.*
