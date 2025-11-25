## Índice de experimentos (series 9.x y 10.x)

Este README resume los scripts activos de las series 9.x y 10.x y dónde están sus resultados. Todo lo anterior (análisis, smokes, validaciones, utilitarios) quedó en `scripts/experimentos_previos/`.

### Serie 9.x (baseline curriculum)
- `run_experiment_9_curriculum.py`: Experimento 9 – Curriculum base (versión original 9.0). Resultados en `results/pgf_v9/`.
- `run_experiment_9.1_robust.py`: Experimento 9.1 – Curriculum robustecido. Resultados en `results/pgf_v9.1/`.

### Serie 10.x (economía, curriculum y escalado)
- `run_experiment_10_adaptive.py`: Experimento 10 (v10.0) – Curriculum adaptativo 8×8 inicial. Resultados en `results/pgf_v10/`.
- `run_experiment_10.1_balanced.py`: Experimento 10.1 – Economía balanceada. Resultados en `results/pgf_v10.1/`.
- `run_experiment_10.2_harder.py`: Experimento 10.2 – Economía más dura. Resultados en `results/pgf_v10.2/`.
- `run_experiment_10.3_critical.py`: Experimento 10.3 – Caso crítico/economía trivial. Resultados en `results/pgf_v10.3/`.
- `run_experiment_10.4_austere.py`: Experimento 10.4 – Economía austera (inviable). Resultados en `results/pgf_v10.4/`.
- `run_experiment_10.5_viable_economy.py`: Experimento 10.5 – Economía “viable” (pre-fixes). Resultados en `results/pgf_v10.5/`.
- `run_experiment_10.6_exploratory_16x16.py`: Exploratorio 16×16 (v10.6). Resultados en `results/pgf_v10.6_exploratory_16x16/`.
- `run_experiment_10.8_goal_oriented.py` (smoke): Test rápido con goal_reward; resultados en `results/pgf_v10.8/resultados/smoke_test_v10.8_goal_oriented/`.
- `run_experiment_10.9_rapid.py` (smoke): Test rápido ajustes no-lineales; resultados en `results/pgf_v10.9/resultados/smoke_test_v10.9_rapid/`.
- `run_experiment_10_adaptive.py` (fixes recientes de goal detection): pruebas en `results/pgf_v11/resultados/smoke_test_v11_20251205_083906/`.

### Experimentos previos y utilitarios
- Todo lo demás (análisis, smokes antiguos, validaciones, oráculos alternos, utilidades) está en `scripts/experimentos_previos/`. Los resultados correspondientes se agruparon en `results/experimentos_previos/` o `results/smoke_tests/` y `results/validations/`.

# scripts/ (menú rápido) [ENGLISH]

Utilidades y runners para TUI-v4.1.

## Experimentos
- **Exp1 (baseline sweep)**: `sim/prototipo_rl_simbiosis.py --risk_sweep ...`  
  *Incluye control/dqn_control/simbiosis.*  
  Salidas típicas: `results/sweep/fase1` o `results/sweep/fase2/...`.

- **Exp2 (TUI/PGF instrumentado)**:
  - Rápido: `python scripts/run_ablation_quick.py [--test]` (tui_only, tui_pgf_light, tui_pgf_heavy con seeds/risks predefinidos).
  - Pipeline completo: `python scripts/run_full_experiment.py` (barridos default/tuning con dqn_control + bloque `sweep_tui` para TUI/PGF puro + robustez + SOTA + consolidado). Usa `--stop_on_fail`, `--output_base` y flags PGF/risks/red_team según sea necesario.

- **Exp3 (búsqueda PGF)**: `scripts/run_search_pgf.py` (placeholder; definir grids y activar ejecución cuando se apruebe).

Consulta el archivo `scripts/EXPERIMENTS.md` para un índice rápido de Exp1/Exp2, parámetros recomendados, rutas de salida y estado de ejecución.

## Plan Experimento 2 + SOTA (versión final)

1. Ejecutar el pipeline principal (TUI + variantes)
python scripts/run_full_experiment.py --seeds 42 123 456 --episodes_default 1000 --episodes_robust 1000 --output_base results/sweep/fase2_full --stop_on_fail
(Puedes ajustar episodios para smoke test.)

2. Ejecutar comparativa SOTA (PPO/A2C/DQN, solo red_team=False)
python scripts/run_sota_a2c_dqn.py

3. Consolidar todos los resultados
No limpies ni borres outputs antes de consolidar.
python scripts/consolidate_results.py

4. Verificar artefactos generados
results/master_results.csv
results/sota_ppo_global_summary.csv
results/sota_a2c_global_summary.csv
results/sota_dqn_global_summary.csv
results/sota_all_global_summary.csv
sweep_*_summary.csv y CSV individuales

5. Documentar en experiment_log.txt y README
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
