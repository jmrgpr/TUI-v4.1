# F2_redteam — Red Team sintetico (v11)

## Que es (operacional)
F2 activa `red_team=True` en el entorno y fuerza perturbaciones estocasticas por step (no es un adversario min-max).

Implementacion actual (v11):
- Probabilidad de evento adverso por step: `red_team_prob` (en v11 se usa `0.1`).
- Tipo de evento (cuando ocurre): mover tripwire / añadir shock / bloquear celda.
- Impacto directo: aplica `red_team_impact` al reward y a los recursos (default `-1.0`).

Nota: esto es una **prueba de estres adversarial sintetica**. No implementa un "agente oponente" que optimice contra la politica del agente; por tanto, evita claims fuertes de "red teaming" estilo RL min-max.

## Objetivo
Evaluar resiliencia bajo perturbaciones adversariales activas, comparando:
- `control`
- `simbiosis`
- `dqn_control`

## Parametros v11 (segun preregistro)
- `risk_scale = 1.2`
- `risk_level = high`
- `red_team = True`
- `red_team_prob = 0.1`
- `pgf_mix = 0.2`
- `episodes = 200`
- `grids = {8, 16}`
- `seeds = {42, 101, 13, 7, 99}`

## Estructura de carpetas
- `raw/`: salida agregada por (grid, seed) con los 3 agentes en un solo CSV/JSON.
- `grid8/riskhigh/{control,simbiosis,dqn_control}/`: **dataset canonico** (1 CSV/JSON por agente y seed).
- `grid16/riskhigh/{control,simbiosis,dqn_control}/`: idem.
- `analysis/`: scripts de analisis rapido.

El manifiesto canonico (hashes y rutas) esta en `results/v11/CANONICAL_DATASET_v11.md`.

## Como ejecutar
Desde la raiz del repo:

```powershell
python results/v11/F2_redteam/run_F2_redteam_v11.py
python scripts/organize_F2_redteam_results.py
python scripts/update_f2_metadata_fields.py
python scripts/bootstrap_stats_v11.py
python scripts/analisis_estadistico_v11.py
python scripts/diff_check_f2_vs_f1.py
```

## Artefactos clave
- `results/v11/data/bootstrap_stats_v11.md`
- `results/v11/data/stats_report_v11.md`
- `results/v11/data/f2_vs_f1_diff.md`
