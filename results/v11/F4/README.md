# F4 (v11) — High-Stakes / Risk-Tension Test

F4 es un experimento puente (v11 → v12) diseñado para aislar una sola palanca causal nueva: **stakes / tensión de riesgo efectiva** en el entorno hostil (`F2_redteam`), y evaluar si:

- El “nicho” de robustez de `simbiosis` vs `control` se vuelve más nítido bajo stakes altos.
- `pgf_mix` (shaping lineal) solo aporta valor cuando el costo de catástrofe es alto.

## Estructura (peer-review proof)

- Outputs crudos (no canónicos): `results/v11/F4/raw/` (CSV agregados por run y JSON del runner; **no se versionan**).
- Outputs canónicos (se versionan CSV; JSON se audita por hashes):
  - `results/v11/F4/F2_redteam/stkL/`
  - `results/v11/F4/F2_redteam/stkH/`

Cada grupo mantiene el patrón por `grid{8,16}/riskhigh/{control,simbiosis,dqn_control(optional)}/`.

## Cómo ejecutar (cuando decidas correr F4)

1) Ejecutar runs crudos (genera JSON + CSV agregado por run):

```powershell
python results/v11/F4/run_F4_v11.py --dry-run
python results/v11/F4/run_F4_v11.py
```

2) Organizar a estructura canónica por agente (split del CSV agregado y JSON por agente):

```powershell
python scripts/organize_F4_results.py
```

3) Regenerar artefactos globales v11 (master, stats, manifiestos):

```powershell
python scripts/rebuild_master_from_episodes.py
python scripts/analisis_estadistico_v11.py
python scripts/generate_canonical_dataset_v11.py
python scripts/generate_canonical_dataset_extended_json_v11.py
```

## Documentos canónicos

- Preregistro: `results/v11/F4/PREREGISTRO_F4_v11.md`
- Deviations log: `results/v11/F4/F4_DEVIATIONS_LOG_v11.md`
