# F1_highrisk v11 – Resultados finales

Este experimento pone a prueba la TUI/Simbiosis en condiciones de alto riesgo, siguiendo la estructura y trazabilidad establecidas en F0_baseline.

## Resumen
- Batch F1_highrisk completado con `risk_scale = 1.2`, `risk_level = high` en grids 8×8 y 16×16.
- Seeds: 42, 101, 13, 7, 99; 200 episodios por combinación agente×grid×seed.
- Todas las configuraciones cumplen el criterio GO de longitud de episodio (~30 pasos):
  - Grid 8×8: medias 29.8–30 pasos; mínimos en control 15–26, en DQN-Control 17–30; Simbiosis siempre 30/30.
  - Grid 16×16: medias ≈30 pasos; DQN-Control presenta mínimos puntuales de 27 y 17 pasos, pero medias ≈30; control y simbiosis se mantienen en 30/30.
- Recompensa: Control muy negativa; Simbiosis mucho menos negativa (≈+42–44 puntos frente a Control), DQN-Control similar a Control.
- Flexibilidad y robustez: prácticamente idénticas entre agentes; robustez media cercana a 1 en todos los casos.
- Riesgo y PGF: Simbiosis reduce riesgo efectivo medio frente a Control y mantiene PGF bruto comparable, con diferencias significativas en riesgo efectivo (p < 0.05, Bonferroni).
- Tripwires y surprise: tasas bajas en todos los runs, sin anomalías ni colapsos de seguridad.

## Estructura de carpetas
- `grid8/riskhigh/{control,simbiosis,dqn_control}/`
- `grid16/riskhigh/{control,simbiosis,dqn_control}/`
- `raw/`, `analysis/`, `metadata.json`, `README.md`

## Objetivo
Evaluar la robustez, seguridad y alineación de la TUI/PGF bajo condiciones adversas (riesgo alto, incidentes frecuentes) y comparar Simbiosis frente a Control clásico y DQN-Control en términos de recompensa, riesgo efectivo y PGF.

## Preregistro
Ver `PREREGISTRO_F1_v11.md` para detalles completos del diseño experimental, hipótesis y criterios de evaluación. El preregistro fijaba inicialmente `risk_scale = 1.5`; tras el piloto se ajustó a `risk_scale = 1.2` para mantener un entorno de alto riesgo pero estable y científicamente viable.

---

## Fases y estado de ejecución
- **Fase 1A – Piloto GO/NO-GO (completada):**
  - Run archivado: `raw/archivados/grid8_riskhigh_seed42_piloto50_v11.*` (prefijo original, sobreescrituras previas; no usar).
  - Run limpio (GO): prefijo `grid8_riskhigh_r1p2_seed42_piloto50_v11` con `risk_scale = 1.2`, seed 42, 50 episodios, grid 8×8. Longitudes ≈30 pasos para los tres agentes (criterio GO cumplido).
- **Fase 1B – Batch principal (COMPLETADA):**
  - Seeds: 42, 101, 13, 7, 99.
  - Grids: 8×8 y 16×16.
  - Episodios: 200 por combinación agente×grid×seed.
  - Prefijos de salida: `grid8_riskhigh_r1p2_seedXX_v11`, `grid16_riskhigh_r1p2_seedXX_v11` bajo `raw/`.
  - Longitudes de episodio: medias ≈30 pasos en todos los casos, con mínimos más bajos en Control y DQN-Control pero Simbiosis siempre saturando el horizonte de 30 pasos.
- **Red team:** no se emplea red_team en F1; F2 reservará `red_team = True` y ataques adversariales explícitos.

---

## Comandos usados (batch F1_highrisk v11)

Los runs del batch principal se lanzaron con el siguiente patrón de comando:

```powershell
python -m sim.prototipo_rl_simbiosis `
  --episodes 200 `
  --seed {seed} `
  --grid_size {grid} `
  --risk_scale 1.2 `
  --risk_level high `
  --dqn_control `
  --pgf_mix 0.2 `
  --output_prefix results/v11/F1_highrisk/raw/grid{grid}_riskhigh_r1p2_seed{seed}_v11
```

Con `{seed} ∈ {42, 101, 13, 7, 99}` y `{grid} ∈ {8, 16}`. Los detalles completos de comandos concretos y parámetros globales se documentan en `metadata.json`.

---

## Archivos clave
Nota: los artefactos en `analysis/` se conservaron como analisis exploratorio inicial. Para resultados canonicos y comparables a nivel serie v11 (unidad primaria run/seed), usar:
- `results/v11/data/stats_report_v11.md`
- `results/v11/data/bootstrap_stats_v11.md`
- `results/v11/CANONICAL_DATASET_v11.md`

- `raw/`: JSON y CSV de episodios por combinación agente×grid×seed (incluye piloto y batch principal).
- `analysis/analisis_F1_v11.ipynb`: notebook de análisis exploratorio y generación de tablas.
- `analysis/longitudes_F1_v11.csv`: resumen de longitudes de episodio por grid/seed/agente.
- `analysis/stat_tests_F1_v11.csv`: (DEPRECATED) tests por episodio; puede incurrir en pseudo-replicacion.
- `analysis/reporte_final_F1_v11.md`: (DEPRECATED) reporte no alineado con el cierre canonico de la serie v11.
- `analysis/export_graficos_F1_v11.py`: script para exportar boxplots e histogramas por agente y grid.
- `metadata.json`: metadatos del experimento, parámetros globales, seeds, grids y resumen de resultados.

---

## Resultados científicos (síntesis)
- En el dataset canonico de la serie v11, F1 (risk_scale=1.2; sin ataque) muestra una diferencia clara en recompensa media entre agentes: `simbiosis` es mucho menos negativa que `control` y `dqn_control` (ver `results/v11/data/stats_report_v11.md`).
- La evidencia inferencial principal para la serie v11 usa unidad por run/seed (no por episodio) y queda en `results/v11/data/bootstrap_stats_v11.md` (para F2) y en las tablas por fase en `results/v11/data/stats_report_v11.md`.

Para el contexto completo de F1 dentro de la serie (F0/F1/F2), ver `results/v11/INFORME_CIENTIFICO_SERIE_V11.md`.

---

## Diagnóstico DQN (opcional)

Se recomienda ejecutar un script de diagnóstico específico sobre las políticas DQN (análogo a `scripts/diagnose_dqn_f0.py`) para inspeccionar:
- Sensibilidad a estados de alto riesgo.
- Posibles modos de fallo (parálisis, oscilaciones, exploración excesiva).
- Diferencias estructurales entre DQN-Control y Simbiosis.

Los hallazgos pueden añadirse como nota tecnica en `results/v11/ANEXO_TECNICO_v11.md` o en el preregistro de F3.

---

## Trazabilidad y reproducibilidad
- Todos los runs están registrados en `metadata.json` (incluyendo piloto GO/NO-GO y batch completo).
- Los datos crudos se almacenan en `raw/` con nombres informativos que incluyen grid, riesgo, seed y protocolo.
- Para la narrativa y reportes oficiales de v11 (con dataset canonico), ver `results/v11/README_REPRODUCIBLE_v11.md` y `results/v11/PUBLICACION_SERIE_V11.md`.
