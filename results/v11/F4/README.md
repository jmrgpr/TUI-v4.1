# F4 (v11) — Stakes run-level (B=3) + CFR

F4 es un experimento puente (v11 → v12) que fija `F2_redteam` y cambia solo **stakes/riesgo efectivo** a nivel run mediante un **presupuesto de catástrofes** `B` (Adenda 01).

## Estructura (alineada a F3)

- Preregistro y auditoría:
  - `results/v11/F4/PREREGISTRO_F4_v11.md`
  - `results/v11/F4/F4_ADENDA_01.md`
  - `results/v11/F4/F4_DEVIATIONS_LOG_v11.md`
- Outputs crudos (no canónicos; no versionar): `results/v11/F4/raw/`
- Outputs canónicos (versionar CSV; JSON solo por hashes):
  - `results/v11/F4/F2_redteam/stkL/` (low-stakes)
  - `results/v11/F4/F2_redteam/stkH/` (high-stakes, budget `B=3`)

Cada grupo mantiene el patrón por `grid{8,16}/riskhigh/{control,simbiosis}/`.

## Cómo ejecutar

1) Ejecutar runs crudos (genera JSON + CSV agregado por run):

```powershell
python results/v11/F4/run_F4_v11.py --dry-run
python results/v11/F4/run_F4_v11.py
```

Nota: `run_F4_v11.py` imprime **40 comandos** (stakes × grid × seed × `pgf_mix`). Eso es esperado porque cada corrida ejecuta **`control` + `simbiosis`**; tras `scripts/organize_F4_results.py` se obtienen **60 CSV canónicos** (6 grupos × 10 runs) según `results/v11/F4/PREREGISTRO_F4_v11.md`.

2) Organizar a estructura canónica por agente (split del CSV agregado + JSON por agente):

```powershell
python scripts/organize_F4_results.py
```

3) Ejecutar análisis preregistrado F4 (endpoint CFR + Holm):

```powershell
python scripts/f4_preregistered_analysis_v11.py
```

4) Regenerar artefactos globales v11 (master, stats, manifiestos):

```powershell
python scripts/rebuild_master_from_episodes.py
python scripts/analisis_estadistico_v11.py
python scripts/generate_canonical_dataset_v11.py
python scripts/generate_canonical_dataset_extended_json_v11.py
```
