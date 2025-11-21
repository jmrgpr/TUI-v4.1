# Estructura de `results/`

Organización profesional para análisis y reproducibilidad. Cada subcarpeta tiene un propósito claro y evita colisiones entre experimentos.

## Tabla resumen

| Carpeta/Subcarpeta      | Script que la llena                | Descripción columnas principales |
|-------------------------|------------------------------------|----------------------------------|
| sweep/faseX/seedYY/     | prototipo_rl_simbiosis.py, runner.py | risk, reward, pgf, tripwires, ...|
| runs/                   | prototipo_rl_simbiosis.py           | episodio, reward, pgf, ...       |
| sota/algoritmo/         | sota_wrapper.py, runner.py          | episodio, reward, ...            |
| global_summaries/       | merge_summaries.py                  | resumen global, medias, ...      |
| old/                    | manual, legacy, limpieza            | variable, legacy, imágenes, scripts antiguos |

## Detalles

- **sweep/**: Barridos de parámetros. Subniveles por fase y semilla para evitar colisiones y facilitar análisis comparativo.
- **runs/**: Resultados de corridas largas (ej. 2000 episodios, episodios completos).
- **sota/**: Resultados de algoritmos SOTA, separados por tipo si hay muchos archivos (ejemplo: sota/ppo/, sota/a2c/...).
- **global_summaries/**: Resúmenes globales, medias, comparativos entre experimentos y algoritmos.
- **old/**: Legacy, experimentos previos, imágenes, scripts antiguos, carpetas como `corrida_100/`, `fase2/`, `pruebas_codigo/`, y archivos como `stats.py`, `1.png`, `2.png`, `3.png`.

> Actualiza esta tabla si agregas scripts, carpetas o columnas nuevas. La estructura está lista para reproducibilidad y limpieza científica.
