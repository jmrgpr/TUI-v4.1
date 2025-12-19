# F2_CLOSURE_REPORT - Serie v11 (TUI v4.1)

Estado: CERRADO (2025-12-17)

## Que es F2 (operacional)
F2 es una **prueba de estres adversarial sintetica**: activa `red_team=True` y perturba el entorno con eventos estocasticos por step (`red_team_prob=0.1`). No implementa un adversario min-max.

Por diseno, F2 esta orientado a **caracterizacion** (que cambia cuando el entorno es mas hostil), no a claims fuertes de "superioridad" de un agente.

## Dataset y trazabilidad (fuente canonica)
- Manifiesto canonico (rutas + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Regeneracion end-to-end: `results/v11/README_REPRODUCIBLE_v11.md`
- Validacion master vs fuentes: `results/v11/data/validation_master_sources_clean.csv`

## Metricas de recompensa (para evitar ambiguedad por shaping)
Se reportan dos metricas:
- `reward_total`: recompensa exportada en `*_episodes.csv` (para `simbiosis` puede incluir mezcla con PGF cuando `pgf_mix>0`).
- `reward_env_total`: recompensa ambiental por episodio (sumatoria por step) estimada desde `reward_env_evol` en el JSON del run.

Esto evita conclusiones infladas cuando existe reward shaping parcial.

## Hallazgos principales (descriptivos + trazables)

### H1: F2 degrada el desempeno vs F1 (esperado)
Ver diffs cuantitativos (incluye senales del ataque): `results/v11/data/f2_vs_f1_diff.md`.

En `reward_env_total`, degradacion (F2 - F1):
- `control`: -14.65 ( -56.83 -> -71.48 )
- `dqn_control`: -10.42 ( -60.03 -> -70.45 )
- `simbiosis`: -11.47 ( -58.71 -> -70.18 )

### H2: `reward_total` != `reward_env_total` cuando hay PGF
En F2 (risk_scale=1.2), `simbiosis` muestra un gap grande entre metricas:
- `reward_total`: -46.01
- `reward_env_total`: -70.18
- Gap: +24.17

Esto es evidencia de que **la metrica reportada importa** y debe explicitarse en cualquier publicacion.

### H3: F2 activa senales observables del stress test
`attack_enabled=True` y `red_team_prob=0.1` aparecen en los JSON canonicos, y cambian `avg_shocks`, `mean_surprise`, `avg_gap`, etc. Ver: `results/v11/data/f2_vs_f1_diff.md`.

## Evidencia estadistica (si se necesita, sin sobre-vender)
Para F2 vs `control`, bootstrap no parametrico por run/seed:
- Artefacto: `results/v11/data/bootstrap_stats_v11.md`
- Unidad primaria: `run_mean_by_file`
- Correccion multiple: Holm por metrica

## Artefactos vigentes de F2 (serie v11)
- Reporte estadistico (dual): `results/v11/data/stats_report_v11.md`
- Bootstrap (dual): `results/v11/data/bootstrap_stats_v11.md`
- Metricas episodicas (dual, run/seed): `results/v11/data/episodic_metrics_v11.md`
- Checks finales: `results/v11/data/f2_final_checks.md`

## Preguntas que F2 NO responde (motiva F3)
1) Ablacion PGF: efecto de `pgf_mix` sobre `reward_env_total` y sobre metricas de seguridad (tripwires/shocks/CVaR).
2) Comparacion justa de algoritmo: `simbiosis(pgf_mix=0.0)` vs baselines.
3) Baselines modernos: PPO/SAC/TD3 (si el claim apunta a SOTA).
4) Sensibilidad del stress test: curva de severidad por `red_team_prob` y/o adversario adaptativo (si se quiere "red teaming" fuerte).

## Transicion a F3
Protocolo propuesto: `results/v11/F3_PREREGISTRATION.md`.
