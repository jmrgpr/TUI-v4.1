# Informe Cientifico: Serie v11 (F0, F1, F2)

## 1. Alcance
Este informe resume la ejecucion y resultados de la serie v11 para tres fases:
- F0_baseline: referencia en riesgo bajo.
- F1_highrisk: alto riesgo sin ataque.
- F2_redteam: estres adversarial sintetico del entorno (no adversario min-max).

El objetivo principal es trazabilidad y coherencia entre lo ejecutado y lo reportado.

## 2. Fuente canonica y reproducibilidad
- Manifiesto canonico (rutas + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Regeneracion reproducible: `results/v11/README_REPRODUCIBLE_v11.md`
- Reporte estadistico vigente: `results/v11/data/stats_report_v11.md`
- Bootstrap (unidad primaria run/seed): `results/v11/data/bootstrap_stats_v11.md`
- Verificacion F2 != F1: `results/v11/data/f2_vs_f1_diff.md`

Nota: `results/v11/stats_report_v11.md` existe solo como compatibilidad historica y esta marcado como deprecated.

## 3. Metodologia (resumen)
- Unidades experimentales: runs por (grid, seed, agente) exportados como `*_episodes.csv` y su JSON asociado.
- En F2: `red_team=True` con `red_team_prob=0.1` (eventos adversos estocasticos en el entorno). No hay adversario que optimice contra la politica del agente.
- Analisis: se usan solo los archivos del dataset canonico (se excluyen copias en `archived/` y agregados en `raw/`).
- Metricas de recompensa:
  - `reward_total`: corresponde a la recompensa total exportada como `Recompensa` (puede incluir mezcla con PGF cuando `pgf_mix>0`).
  - `reward_env_total`: recompensa ambiental por episodio (sumatoria por step) estimada desde `reward_env_evol` en el JSON.
  Ver definiciones: `results/v11/ANEXO_TECNICO_v11.md`.

## 4. Resultados (dos metricas de recompensa)
Valores resumidos desde `results/v11/data/stats_report_v11.md` (n = numero de runs/archivos).

### 4.1 F0 (Referencia; risk_scale=0.5)
| Agente      | n | mean reward_total | mean reward_env_total |
|-------------|---|------------------|-----------------------|
| control     | 2 | -20.02           | -20.02                |
| dqn_control | 2 | -24.08           | -24.08                |
| simbiosis   | 2 |  14.87           | -22.66                |

### 4.2 F1 (Alto riesgo; risk_scale=1.2; red_team=False)
| Agente      | n  | mean reward_total | mean reward_env_total |
|-------------|----|------------------|-----------------------|
| control     | 10 | -56.83           | -56.83                |
| dqn_control | 10 | -60.03           | -60.03                |
| simbiosis   | 10 | -13.98           | -58.71                |

### 4.3 F2 (Estres adversarial sintetico; risk_scale=1.2; red_team=True; red_team_prob=0.1)
| Agente      | n  | mean reward_total | mean reward_env_total |
|-------------|----|------------------|-----------------------|
| control     | 10 | -71.48           | -71.48                |
| dqn_control | 10 | -70.45           | -70.45                |
| simbiosis   | 10 | -46.01           | -70.18                |

## 5. Inferencia (bootstrap)
La evidencia inferencial principal para F2 se reporta en `results/v11/data/bootstrap_stats_v11.md` y usa:
- Unidad primaria: promedio por archivo `*_episodes.csv` (equivalente a run/seed).
- Remuestreo no parametrico con reemplazo.

Esto evita suponer normalidad y reduce el riesgo de pseudo-replicacion por episodios.

## 6. Discusion (F2)
F2 degrada las metricas de recompensa respecto a F1, como se espera bajo perturbaciones.

Interpretacion por metrica:
- En `reward_total` (incluyendo PGF cuando aplica), `simbiosis` queda por encima de `control` y `dqn_control`.
- En `reward_env_total` (recompensa ambiental pura), `simbiosis` queda cercana a `control`/`dqn_control` y muestra una mejora pequena (≈ +1.29 vs `control` en F2).

Interpretacion metodologica: F2 es una prueba de estres adversarial sintetica (parametrizada por `red_team_prob` y probabilidades de tipo de evento). No debe presentarse como "red team min-max" sin implementar un adversario real.

## 7. Estado para F3
Con el dataset canonico, verificacion F2 != F1 y bootstrap por run/seed, la base experimental queda lista para F3: nuevos baselines, nuevos ataques sinteticos (o un adversario real), y metricas adicionales (CVaR, tripwires, shocks) a nivel run/seed.
