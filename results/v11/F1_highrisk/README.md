# Experimento F1_v11 — High Risk

Este experimento pone a prueba la TUI/Simbiosis en condiciones de alto riesgo, siguiendo la estructura y trazabilidad de F0_baseline.

## Estructura de carpetas
- `grid8/riskhigh/{control,simbiosis,dqn_control}/`
- `grid16/riskhigh/{control,simbiosis,dqn_control}/`
- `raw/`, `analysis/`, `metadata.json`, `README.md`

## Objetivo
Evaluar la robustez, seguridad y alineación de la TUI/PGF bajo condiciones adversas (riesgo alto, incidentes frecuentes).

## Preregistro
Ver `PREREGISTRO_F1_v11.md` para detalles completos del diseño experimental, hipótesis y criterios de evaluación.

---

## Estado y plan de ejecución
- Fase 1A (piloto GO/NO-GO):
  - run archivado: `archivados/grid8_riskhigh_seed42_piloto50_v11.*` (prefijo original, sobreescrituras previas; no usar).
  - run limpio (GO): prefijo `grid8_riskhigh_r1p2_seed42_piloto50_v11` con risk_scale=1.2, seed 42, 50 episodios, grid 8×8. Longitudes ~30 pasos (criterio cumplido).
- Fase 1B (batch): con Fase 1A GO, lanzar 5 seeds (42, 101, 13, 7, 99), 200 episodios (subir a 500 si la varianza es alta) en grids 8×8 y 16×16, con `risk_scale=1.2` y prefijos separados por seed/grid.
- Sin red team en F1; F2 reservará red_team=True y ataques adversariales.

## Comando piloto (Fase 1A)
```
python -m sim.prototipo_rl_simbiosis ^
  --episodes 50 ^
  --seed 42 ^
  --grid_size 8 ^
  --risk_scale 1.5 ^
  --risk_level high ^
  --dqn_control ^
  --pgf_mix 0.2 ^
  --output_prefix results/v11/F1_highrisk/raw/grid8_riskhigh_seed42_piloto50_v11
```

## Notas de trazabilidad
- Documentar en `metadata.json` cada ejecución (seed, episodios, grid, risk_scale, comando, resultado GO/NO-GO).
- Guardar todos los JSON/CSV en `raw/` con sufijos informativos (piloto/batch).
- Actualizar este README con el estado tras cada fase.
