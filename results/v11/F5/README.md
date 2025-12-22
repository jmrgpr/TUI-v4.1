# F5 (v11) — High-stakes (B=3) con endpoint primario `episodes_completed`

F5 existe para resolver el **ceiling effect** observado en F4: con `B=3`, el endpoint confirmatorio **CFR** saturó en 1.0 en todos los grupos.  
En F5 se mantiene el mismo setup high-stakes (`B=3`) y se cambia el endpoint confirmatorio a **`episodes_completed`** (tiempo-hasta-agotar-budget).

## Estructura (alineada a F3/F4)

- Preregistro y auditoría:
  - `results/v11/F5/PREREGISTRO_F5_v11.md`
  - `results/v11/F5/F5_DEVIATIONS_LOG_v11.md`
  - `results/v11/F5/F5_CLOSURE_REPORT.md` (se completa al cerrar)
- Outputs crudos (no canónicos; no versionar): `results/v11/F5/raw/`
- Outputs canónicos (versionar CSV; JSON solo por hashes):
  - `results/v11/F5/F2_redteam/stkH/` (high-stakes, budget `B=3`)

## Cómo ejecutar

1) Ejecutar runs crudos (genera JSON + CSV agregado por run):

```powershell
python results/v11/F5/run_F5_v11.py --dry-run
python results/v11/F5/run_F5_v11.py
```

Nota: `run_F5_v11.py` imprime **20 comandos** (grid × seed × `pgf_mix`). Eso es esperado porque cada corrida ejecuta **`control` + `simbiosis`**; tras `scripts/organize_F5_results.py` se obtienen **30 CSV canónicos** (3 grupos × 10 runs) según `results/v11/F5/PREREGISTRO_F5_v11.md`.

2) Organizar a estructura canónica por agente (split del CSV agregado + JSON por agente):

```powershell
python scripts/organize_F5_results.py
```

3) Ejecutar análisis preregistrado F5 (endpoint `episodes_completed` + Holm):

```powershell
python scripts/f5_preregistered_analysis_v11.py
```

4) (Opcional) Regenerar artefactos globales v11 (master, stats, manifiestos):

```powershell
python scripts/rebuild_master_from_episodes.py
python scripts/analisis_estadistico_v11.py
python scripts/generate_canonical_dataset_v11.py
python scripts/generate_canonical_dataset_extended_json_v11.py
```

