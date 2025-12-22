# F5 / F2_redteam (canónico)

Esta carpeta contiene los outputs **canónicos** de F5 (solo high-stakes):

- `stkH/`: high-stakes (run-level budget `B=3`; `episodes_completed` puede ser <200 por terminación por budget).

Los CSV `*_episodes.csv` se versionan; los JSON asociados no se versionan por tamaño y se auditan vía hashes en `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`.

Nota: los runs crudos se generan con `sim.prototipo_rl_simbiosis`, que ejecuta `control`+`simbiosis` en una sola corrida; el conteo final de runs por grupo se refleja en los CSV canónicos tras `scripts/organize_F5_results.py`.

