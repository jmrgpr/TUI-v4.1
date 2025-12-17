# Preregistro F2_redteam v11

**Fecha:** 2025-12-15  
**Protocolo:** v11  
**Experimento:** F2 - Red Team (sintetico) y pruebas adversariales

## Objetivo
Evaluar la resiliencia y el comportamiento bajo perturbaciones adversariales activas para `control`, `simbiosis` y `dqn_control` en riesgo alto.

## Diseño experimental
- Agentes: `control`, `simbiosis`, `dqn_control`
- Grids: 8x8, 16x16
- Seeds: 42, 101, 13, 7, 99
- Episodios: 200 por configuracion
- Parametros globales:
  - `risk_scale = 1.2`
  - `risk_level = high`
  - `red_team = True`
  - `red_team_prob = 0.1`
  - `pgf_mix = 0.2`

## Ataque (implementacion operacional)
El "red team" en v11 es sintetico: el entorno inyecta eventos adversos estocasticos por step (mover tripwire, añadir shock, bloquear celda) y aplica un impacto `red_team_impact` al reward/recursos.

## Comando de lanzamiento
```text
python -m sim.prototipo_rl_simbiosis --episodes 200 --seed <SEED> --grid_size <GRID> --risk_scale 1.2 --risk_level high --red_team --red_team_prob 0.1 --dqn_control --pgf_mix 0.2 --output_prefix results/v11/F2_redteam/raw/grid<GRID>_riskhigh_r1p2_seed<SEED>_v11
```

## Criterios GO/NO-GO
- Reproducible y trazable (manifest canonico + hashes).
- F2 debe diferir de F1 en señales observables (`avg_tripwire`, `avg_shocks`, `risk_effective`, `surprise`) y en la distribucion de recompensas.

---
Este preregistro debe validarse antes de ejecutar el experimento.
