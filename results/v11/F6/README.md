# F6 (v11) — Calibración de severidad para evitar saturación de CFR (B=3)

F6 existe para resolver lo que F4/F5 dejaron claro **sin spin**: con high-stakes run-level `B=3` y `F2_redteam` a `red_team_prob=0.1`, el endpoint confirmatorio **CFR** saturó (≈1.0) y no discrimina.

En F6 se mantiene **high-stakes `B=3`** y se calibra **solo** `red_team_prob` mediante un **piloto preregistrado** (no confirmatorio) para seleccionar un `p*` que evite saturación (CFR control ≈ 0.5). Luego se corre la etapa confirmatoria con `p*` fijo.

## Estructura (alineada a F4/F5)

- Preregistro y auditoría:
  - `results/v11/F6/PREREGISTRO_F6_v11.md`
  - `results/v11/F6/F6_DEVIATIONS_LOG_v11.md`
  - `results/v11/F6/F6_CLOSURE_REPORT.md` (se completa al cerrar)
- Outputs crudos (no canónicos; no versionar): `results/v11/F6/raw/`
- Outputs canónicos (versionar CSV; JSON solo por hashes):
  - Confirmatorio: `results/v11/F6/F2_redteam/stkH/rt*/grid{8,16}/riskhigh/{control,simbiosis}/`
- Piloto (calibración; no confirmatorio):
  - Reporte/tabla: `results/v11/data/f6_pilot_selection_v11.md` y `results/v11/data/f6_pilot_table_v11.csv`

## Cómo ejecutar

1) Preflight (ver plan sin ejecutar):

```powershell
python results/v11/F6/run_F6_v11.py --dry-run
```

2) Ejecutar piloto + selección de `p*` + confirmatorio (raw):

```powershell
python results/v11/F6/run_F6_v11.py
```

3) Organizar a estructura canónica por agente (split del CSV agregado + JSON por agente):

```powershell
python scripts/organize_F6_results.py
```

4) Ejecutar análisis preregistrado F6 (endpoint CFR + McNemar exact + Holm):

```powershell
python scripts/f6_preregistered_analysis_v11.py
```

5) (Opcional) Regenerar artefactos globales v11 (master, stats, manifiestos):

```powershell
python scripts/rebuild_master_from_episodes.py
python scripts/analisis_estadistico_v11.py
python scripts/generate_canonical_dataset_v11.py
python scripts/generate_canonical_dataset_extended_json_v11.py
```

