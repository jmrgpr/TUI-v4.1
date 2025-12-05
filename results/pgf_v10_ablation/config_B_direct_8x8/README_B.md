
# Configuración B – Directo 8x8

Entrenamiento solo en 8x8, sin curriculum.

## Parámetros principales
- grid_size=8
- initial_resources=8.0
- step_cost=-0.15
- resource_spawn_rate=0.40
- goal_reward=20.0
- DQN idéntico a v10_viable
- Episodios: 2500
- Seeds: [42, 13, 101]

## Archivos fuente
- `episodes_direct_8x8_{seed}.csv`
- `summary_B.csv`

## Mapeo de métricas a columnas CSV
| Métrica             | Columna en CSV                | Ejemplo de archivo |
|---------------------|-------------------------------|-------------------|
| Éxito total         | `success_rate_total`          | summary_B.csv |
| Éxito últimos 100   | `success_last_100`            | summary_B.csv |
| Gate (%)            | `gate`                        | summary_B.csv |
| Gate pasado         | `gate_passed`                 | summary_B.csv |
| Primer éxito        | `first_success_episode`       | summary_B.csv |
| Convergencia        | `convergence_episode`         | summary_B.csv |

## Ejemplo de extracción de métricas
Para obtener el éxito últimos 100 en 8x8, seed 42:
	- Archivo: `summary_B.csv`
	- Columna: `success_last_100`

## Interpretación y trazabilidad
- Comparar `success_last_100` con baseline (A) para evaluar la importancia del curriculum.
- Documentar cualquier hallazgo relevante y citar siempre el archivo y columna de origen.

---

*Este README ha sido revisado para trazabilidad y claridad. Revisión: 2025-12-05.*