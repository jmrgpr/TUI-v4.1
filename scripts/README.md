Parámetros: seeds 42/123/456, episodios 1000, riesgos 0.5–3.0, red_team=False en SOTA, limitaciones (solo Gridworld).

6. Si hay notebook de análisis, ejecútalo
Ejecuta el notebook de análisis (por ejemplo, analysis_phase2.ipynb) para generar tablas y gráficos comparativos con los resultados consolidados.

Nota: No limpies ni borres outputs antes de consolidar, para asegurar que todos los resultados estén presentes en el master y en los análisis.

Fecha: 2025-11-25
Autor: jmrgpr

## Consolidado
- `consolidate_results.py`: recorre `results/sweep/fase2`, `results/sota`, `artifacts/phase2`, `reports/phase2` (y rutas extra opcionales) y escribe `results/master_results.csv` con columnas estándar (agent, seed, episodes, risk_scale, kappa, lambda, mix, pgf_neto, tripwires, robustez, flexibilidad, reward_total, filename). Detecta seeds/algoritmos por ruta/nombre (control/simbiosis/dqn_control/tui/ppo/a2c/dqn/sac/td3). Asegura que los CSV tengan `risk` en el nombre o columna `risk_scale`.

## Utilidades
- `merge_summaries.py`: utilidades de combinación de resúmenes.
- `fix.py`: script archivado.

## Preflight recomendado
- Smoke test: 1 seed, 1-2 riesgos, pocos episodios; verificar que se generen CSV con `risk_scale`.
- Usar `--stop_on_fail` si quieres abortar en errores.
- Fijar seeds y `PYTHONIOENCODING=utf-8`; cerrar figuras matplotlib si corres muchos plots.

# Recomendación para consolidación SOTA

- Para evitar problemas de consolidación, asegúrate de que todos los archivos de resultados SOTA (a2c, dqn, ppo) estén guardados en la carpeta results/sota/.
- Si los outputs SOTA están en la raíz de results/, usa la consolidación con rutas explícitas:
  python -c "from scripts.consolidate_results import consolidate_csvs; consolidate_csvs(extra_paths=['results/sweep/fase2_full','results','results/sota'])"
- Así garantizas que todos los agentes aparezcan en master_results.csv y la trazabilidad sea completa.

# ---[2025-11-25 | Corrección robusta SOTA y consolidación]---

Se ha mejorado el script de consolidación para detectar el agente (ppo, a2c, dqn, etc.) tanto por la ruta como por el nombre de archivo. Esto permite que los resultados SOTA sean correctamente consolidados aunque los archivos estén fuera de la carpeta results/sota/.

Recomendaciones para próximas tiradas:
- Guarda siempre los outputs SOTA en results/sota/ (subcarpetas por agente).
- Si algún archivo SOTA queda fuera, puedes consolidar con rutas explícitas:
  python -c "from scripts.consolidate_results import consolidate_csvs; consolidate_csvs(extra_paths=['results','results/sota'])"
- Verifica que todos los agentes aparecen en master_results.csv tras cada consolidación.
- El script ahora es tolerante a errores de ubicación, pero mantener la estructura recomendada facilita la trazabilidad y reproducibilidad.

Ejemplo de workflow robusto:
1. Ejecuta el pipeline y la comparativa SOTA.
2. Consolidación estándar: python scripts/consolidate_results.py
3. Si falta algún agente, usa la consolidación con extra_paths.
4. Documenta cualquier incidencia en experiment_log.txt y README.

Fecha: 2025-11-25
Autor: jmrgpr
=======
# scripts/

Esta carpeta contiene utilidades y scripts auxiliares para el proyecto TUI-v4.1.

- fix.py: script archivado desde la raíz para organización.
>>>>>>> 482f801 (Organización: archivos de test y utilidades archivados en carpetas correspondientes (test/, results/, scripts/). Documentación actualizada en README. Estructura más clara y reproducible.)
