# F0_baseline — Referencia / sanity (v12)

**Propósito:** validar instrumentación y pipeline bajo riesgo bajo (sanity check).  
**Nota:** F0 no se usa para claims fuertes de performance (n pequeño por diseño).

## Diseño (borrador)
- Entorno: `SimbiosisEnv`
- Agentes: `control`, `dqn_control`, `simbiosis`
- Grids: 8 y 16
- `risk_scale=0.5` (`risk_level=low`)
- `red_team=False`
- Seeds: (a definir; mínimo seed=42)
- Episodios: (a definir; v11 usó 100)

## Dataset canónico vs `raw/`
- Dataset canónico: `grid8/` y `grid16/` (CSV `*_episodes.csv`).
- `raw/`: trazabilidad operativa (no input canónico).

## Artefactos v12
- Control tower: `results/v12/INDEX_SERIE_V12.md`
- Mega plan: `results/v12/MEGA_PLAN_EVALUACION_v12.md`

