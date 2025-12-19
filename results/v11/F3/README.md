# F3 — peer-review proof (v11)

F3 es la fase preregistrada para convertir las limitaciones observadas en F2 en comparaciones causales testeables, manteniendo comparabilidad con v11 y trazabilidad (unidad primaria = run/seed).

## Documentos canónicos
- Preregistro completo: `results/v11/F3/PREREGISTRO_F3_v11.md`
- Log de desviaciones (antes de analizar): `results/v11/F3/F3_DEVIATIONS_LOG_v11.md`
- Manifiesto CSV (hashes): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto JSON (hashes, sin subir JSON): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`

## Estructura (misma convención que F2, separada por condición)
- `raw/F1_highrisk/` y `raw/F2_redteam/`: salidas agregadas por (grid, seed) para facilitar trazabilidad.
- `F1_highrisk/grid{8,16}/riskhigh/{control,simbiosis,dqn_control}/`: dataset por agente/seed (condición F1).
- `F2_redteam/grid{8,16}/riskhigh/{control,simbiosis,dqn_control}/`: dataset por agente/seed (condición F2).
- `analysis/`: análisis preregistrado (scripts/notebooks y outputs de verificación).

## Nota sobre JSON
Los JSON por run son considerados datos brutos y no se versionan por tamaño; se publican sus hashes en `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md` para permitir verificación independiente de derivaciones como `reward_env_total`.
