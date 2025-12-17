# Resumen Ejecutivo: Serie v11 (F0, F1, F2)

## Objetivo
Evaluar desempeno y comportamiento bajo referencia (F0), alto riesgo (F1) y estres adversarial sintetico (F2) bajo el protocolo v11.

## Fuente canonica
- Dataset canonico (hashes + rutas): `results/v11/CANONICAL_DATASET_v11.md`
- Reporte estadistico vigente: `results/v11/data/stats_report_v11.md`
- Bootstrap (unidad primaria = run/seed por archivo): `results/v11/data/bootstrap_stats_v11.md`
- Verificacion de que F2 != F1: `results/v11/data/f2_vs_f1_diff.md`

## Resultados (media de recompensa por fase)
Valores resumidos desde `results/v11/data/stats_summary_v11.csv`.

### F0 (Referencia, risk_scale=0.5, red_team=False)
| Agente      | n (runs) | Recompensa media |
|-------------|----------|------------------|
| control     | 2        | -20.02           |
| dqn_control | 2        | -24.08           |
| simbiosis   | 2        |  14.87           |

### F1 (Alto riesgo, risk_scale=1.2, red_team=False)
| Agente      | n (runs) | Recompensa media |
|-------------|----------|------------------|
| control     | 10       | -56.83           |
| dqn_control | 10       | -60.03           |
| simbiosis   | 10       | -13.98           |

### F2 (Estres adversarial sintetico, risk_scale=1.2, red_team=True, red_team_prob=0.1)
| Agente      | n (runs) | Recompensa media |
|-------------|----------|------------------|
| control     | 10       | -71.48           |
| dqn_control | 10       | -70.45           |
| simbiosis   | 10       | -46.01           |

## Lectura rapida (F2)
- F2 aplica perturbaciones estocasticas del entorno (no adversario min-max). La configuracion efectiva queda registrada en cada JSON (campos `config.red_team_prob`, etc.).
- En esta ejecucion canonicamente regenerada, F2 degrada la recompensa de todos los agentes; `simbiosis` queda por encima de `control` y `dqn_control` en recompensa media.
- Evidencia inferencial principal: bootstrap no parametrico por run/seed en `results/v11/data/bootstrap_stats_v11.md`.
- Nota de interpretacion: la "Recompensa" es la recompensa total exportada (`Recompensa`), que para `simbiosis` puede incluir mezcla PGF cuando `pgf_mix>0` (ver `results/v11/ANEXO_TECNICO_v11.md`).

## Estado
La documentacion y los artefactos canonicamente regenerados estan alineados y listos para usar como base de F3.
