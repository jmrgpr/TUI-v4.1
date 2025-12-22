# Informe Cientifico: Serie v11 (F0, F1, F2)

> Nota (2025-12-22): este informe cubre solo F0–F2. F3 ya fue ejecutado y cerrado (ver `results/v11/F3/README.md` y `results/v11/data/f3_preregistered_report_v11.md`). F4 está preregistrado y pendiente (ver `results/v11/F4/README.md`). Guía general: `results/v11/INDEX_SERIE_V11.md`.

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

### Definición formal de PGF y ejemplo numérico

En Simbiosis, la recompensa total por step se calcula como:

$$
r_{total}(t) = (1 - m) \cdot r_{env}(t) + m \cdot PGF(t)
$$

donde $m = pgf\_mix$ (en v11, $pgf\_mix = 0.2$).

**Ejemplo real (F2, risk_scale=1.2):**
- Simbiosis (pgf_mix=0.2):  
  - reward_total = **-46.01**
  - reward_env_total = **-70.18**
  - Gap por PGF = **+24.17** puntos

Por tanto, **reward_env_total** es la métrica primaria para comparaciones justas entre agentes, ya que reward_total puede inflarse artificialmente por el shaping.

## 4. Resultados (dos metricas de recompensa)
Valores resumidos desde `results/v11/data/stats_report_v11.md` (n = numero de runs/archivos).

### 4.1 F0 (Referencia descriptiva / sanity check; risk_scale=0.5)
| Agente      | n | mean reward_total | mean reward_env_total |
|-------------|---|------------------|-----------------------|
| control     | 2 | -20.02           | -20.02                |
| dqn_control | 2 | -24.08           | -24.08                |
| simbiosis   | 2 |  14.87           | -22.66                |

Nota: F0 se reporta solo como referencia descriptiva (sanity check); n=2 es insuficiente para inferencias estadísticas o comparaciones entre agentes.

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

**v11 demuestra el efecto del componente prudencial (PGF) en la métrica mezclada (`reward_total`), pero no demuestra superioridad algorítmica en reward ambiental bajo estrés. Las comparaciones justas deben hacerse siempre sobre `reward_env_total`.**

Interpretacion metodologica: F2 es una prueba de estres adversarial sintetica (parametrizada por `red_team_prob` y probabilidades de tipo de evento). No debe presentarse como "red team min-max" sin implementar un adversario real.

## 7. Estado al cierre de F2 (previo a F3)
F2 queda **operacionalmente cerrado** como fase de caracterizacion:
- Dataset canonico verificado: `results/v11/CANONICAL_DATASET_v11.md`
- F2 != F1 demostrado: `results/v11/data/f2_vs_f1_diff.md`
- Metricas duales reportadas (`reward_total` / `reward_env_total`) para auditar shaping
- Bootstrap por run/seed para F2 vs control: `results/v11/data/bootstrap_stats_v11.md`

Documentacion de cierre: `results/v11/F2_CLOSURE_REPORT.md`.

F3 se justificó para responder preguntas causales y comparaciones justas (ablación de `pgf_mix`, `simbiosis(pgf_mix=0.0)`, etc.). El preregistro canónico y el cierre de F3 están en `results/v11/F3/PREREGISTRO_F3_v11.md` y `results/v11/F3/F3_CLOSURE_REPORT.md` (el borrador histórico se conserva en `results/v11/F3_PREREGISTRATION.md`).

## Apéndice: Resultados F2 estratificados por grid_size

A continuación se reportan las medias de reward_total y reward_env_total por agente y tamaño de grid en F2 (risk_scale=1.2, red_team=True):

| Agente      | grid_size | n  | mean reward_total | mean reward_env_total |
|-------------|-----------|----|-------------------|----------------------|
| control     | 8x8       | 5  | -71.72            | -71.72               |
| control     | 16x16     | 5  | -70.83            | -70.83               |
| dqn_control | 8x8       | 5  | -71.38            | -71.38               |
| dqn_control | 16x16     | 5  | -70.51            | -70.51               |
| simbiosis   | 8x8       | 5  | -49.62            | -70.68               |
| simbiosis   | 16x16     | 5  | -42.75            | -69.68               |

Notas:
- n = número de runs por agente y grid_size.
- Las medias se calcularon a partir de master_results_clean.csv, agrupando por agente y grid_size (extraído del path del archivo).
- Se observa que el gap entre reward_total y reward_env_total en Simbiosis es consistente en ambos tamaños de grid, y que la diferencia entre grids es menor que la diferencia entre agentes.
