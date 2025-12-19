# F0_baseline — Referencia (v11)

**Propósito:** validar instrumentación y pipeline bajo riesgo bajo.  
**Nota:** F0 no se usa para claims fuertes de performance (n pequeño).

## Diseño experimental
- Entorno: `SimbiosisEnv`
- Agentes: `control`, `dqn_control`, `simbiosis`
- Grids: 8×8 y 16×16
- `risk_scale=0.5` (`risk_level=low`)
- `red_team=False`
- Semilla: 42
- Episodios: 100 por run

## Dataset canónico vs `raw/`
- El dataset canónico (por agente y por run) vive en `grid8/risklow/...` y `grid16/risklow/...`.
- `raw/` contiene salidas agregadas/duplicadas y se excluye de los análisis canónicos.
- Manifiesto con hashes y rutas: `results/v11/CANONICAL_DATASET_v11.md`.

## Nota sobre recompensas (crítico para reviews)
En v11 se reportan dos métricas:
- `reward_total`: recompensa exportada por el entorno; puede incluir mezcla con PGF cuando `pgf_mix>0`.
- `reward_env_total`: recompensa ambiental pura por episodio (estimada desde `reward_env_evol` en los JSON).

Para comparaciones entre agentes, prioriza `reward_env_total` y métricas prudenciales; usa `reward_total` solo con disclaimers explícitos.

## Artefactos vigentes (serie v11)
- Pipeline reproducible: `results/v11/README_REPRODUCIBLE_v11.md`
- Reporte estadístico (dual): `results/v11/data/stats_report_v11.md`
- Bootstrap por run/seed: `results/v11/data/bootstrap_stats_v11.md`
- Métricas episódicas (dual): `results/v11/data/episodic_metrics_v11.md`
- Informe/publicación: `results/v11/INFORME_CIENTIFICO_SERIE_V11.md`, `results/v11/PUBLICACION_SERIE_V11.md`

## Cómo ejecutar (si necesitas re-correr F0)
```powershell
python results/v11/F0_baseline/run_F0_baseline_v11.py
python scripts/organize_F0_baseline_results.py
```
