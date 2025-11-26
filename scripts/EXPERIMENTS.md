# Experimentos TUI-v4.1

Estado y flujo para los experimentos principales. Actualizado: 2025-11-25.

## Cambios recientes y trazabilidad
- Se han consolidado y corregido todos los resultados y scripts principales.
- Se generaron PDFs de los documentos clave en español e inglés (`La Teoría del Miedo Inteligente.pdf`, `The Theory of Intelligent Fear.pdf`).
- El notebook de análisis y los informes resumen están actualizados y documentados.
- Todos los cambios han sido comiteados y sincronizados con el repositorio remoto.


## Exp1 – Baseline (control/dqn_control/simbiosis)
- Objetivo: barrido de `risk_scale` en Gridworld para control, DQN-Control y Simbiosis.
- Script: `sim/prototipo_rl_simbiosis.py --risk_sweep ...` (también invocado por el bloque “default” de `scripts/run_full_experiment.py`).
- Parámetros recomendados: `--risk_scale` en [0.5, 1.0, 1.5, 2.0, 3.0], seeds multivaluadas (42/123/456), episodios según plan.
- Salida: `results/sweep_*` con JSON/CSV y `sweep_*_summary.csv`.
- Estado: barridos históricos existen en `results/sweep_risk_seed42_*`; no hay `master_results.csv` vigente tras la limpieza. Ejecutar y consolidar según sea necesario.

## Exp2 – Ablación/Comparativa TUI/PGF
- Objetivo: comparar TUI/PGF puro (tui_only, tui_pgf_light, tui_pgf_heavy) contra control/dqn_control/simbiosis (y SOTA si se desea) en la misma malla de seeds/risks.
- Scripts:
  - Rápido: `scripts/run_ablation_quick.py` (tui_only/light/heavy con seeds/risks predefinidos).
  - Completo: `scripts/run_full_experiment.py` (bloques default, tuning y `sweep_tui`; opcional SOTA).
  - SOTA: ejecutar y reconsolidar para obtener comparativas robustas (recompensa, robustez, flexibilidad).

- Ejemplo de ejecución completa:
  - `python scripts/run_full_experiment.py --seeds 42 123 456 --episodes_default <episodios> --episodes_robust <episodios> --output_base results/sweep/fase2_full --stop_on_fail`
- Consolidado (después de cualquier batch):
  - `python scripts/consolidate_results.py` → genera `results/master_results.csv`.
- Estado: solo smoke tests previos; no hay ejecución completa ni `master_results.csv` actual. Exp2 completo pendiente.

## Notas generales y pendientes
**Pendientes clave:**
- Reexportar resultados SOTA con metadatos y métricas completas.
- Reconsolidar el master con todos los agentes y métricas.
- Reejecutar el notebook y actualizar los informes finales.
- Validar que los PDFs y documentación estén accesibles y legibles.

Tras cada corrida, ejecutar `scripts/consolidate_results.py` y verificar `results/master_results.csv` y los `sweep_*_summary.csv`.
Documentar seeds, episodios, riesgos y limitaciones (Gridworld, SOTA opcional) en el log del experimento correspondiente.
## Notas generales
- Tras cada corrida, ejecutar `scripts/consolidate_results.py` y verificar `results/master_results.csv` y los `sweep_*_summary.csv`.
- Documentar seeds, episodios, riesgos y limitaciones (Gridworld, SOTA opcional) en el log del experimento correspondiente.
