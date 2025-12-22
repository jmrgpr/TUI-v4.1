# F4 raw (no canónico)

Este directorio contiene salidas crudas generadas por `results/v11/F4/run_F4_v11.py`:

- JSON agregados por run (incluyen `control` + `simbiosis` y, si se activa, `dqn_control`).
- CSV agregados por run (filas por episodio y por agente).

Estos artefactos **no se versionan** (para evitar duplicación/bloat). Para publicar:

1) Ejecuta `python scripts/organize_F4_results.py` para generar la estructura canónica por agente en `results/v11/F4/F2_redteam/...`.
2) Versiona solo los CSV canónicos + documentos; los JSON quedan auditados vía hashes en `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`.
