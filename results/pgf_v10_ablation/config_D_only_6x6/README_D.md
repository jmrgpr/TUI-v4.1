
# Configuración D – Solo 6x6

Entrenamiento solo en 6x6, con budget completo.

## Parámetros principales
- grid_size=6
- initial_resources=8.0
- step_cost=-0.15
- resource_spawn_rate=0.40
- goal_reward=20.0
- DQN idéntico a v10_viable
- Episodios: 2500
- Seeds: [42, 13, 101]

## Archivos fuente
- `episodes_6x6_only_{seed}.csv`
- `summary_D.csv`

## Mapeo de métricas a columnas CSV
| Métrica             | Columna en CSV                | Ejemplo de archivo |
|---------------------|-------------------------------|-------------------|
| Éxito total         | `success_rate_total`          | summary_D.csv |
| Éxito últimos 100   | `success_last_100`            | summary_D.csv |
| Gate (%)            | `gate`                        | summary_D.csv |
| Gate pasado         | `gate_passed`                 | summary_D.csv |
| Primer éxito        | `first_success_episode`       | summary_D.csv |
| Convergencia        | `convergence_episode`         | summary_D.csv |

## Ejemplo de extracción de métricas
Para obtener el éxito últimos 100 en 6x6, seed 42:
	- Archivo: `summary_D.csv`
	- Columna: `success_last_100`

## Interpretación y trazabilidad
- Evaluar si el 6x6 es suficiente como crisol comparando con baseline y directo 8x8.
- Documentar cualquier hallazgo relevante y citar siempre el archivo y columna de origen.

---

*Este README ha sido revisado para trazabilidad y claridad. Revisión: 2025-12-05.*