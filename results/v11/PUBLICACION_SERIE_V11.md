# Documento para Publicacion Cientifica (v11)

## Titulo
Evaluacion reproducible de agentes bajo referencia, alto riesgo y estres adversarial sintetico: serie v11 (TUI v4.1)

## Resumen (Abstract)
Presentamos un pipeline reproducible para evaluar agentes bajo tres fases: F0 (referencia), F1 (alto riesgo) y F2 (estres adversarial sintetico). En F2 se activa `red_team=True` y se inyectan eventos adversos estocasticos en el entorno con `red_team_prob=0.1` (no adversario min-max). Reportamos un dataset canonico con hashes, verificaciones de consistencia y estadistica inferencial por bootstrap no parametrico con unidad primaria run/seed. Para evitar ambiguedad por reward shaping, reportamos dos metricas: `reward_total` (recompensa exportada; puede incluir mezcla con PGF en Simbiosis) y `reward_env_total` (recompensa ambiental pura estimada desde JSON). En esta serie, Simbiosis mejora fuertemente `reward_total` y muestra solo una mejora pequena en `reward_env_total`, por lo que las conclusiones deben interpretarse como evidencia sobre el objetivo prudencial (PGF) y no como superioridad general en reward ambiental.

Advertencia: La métrica "robustez-distractor (operacional)" se reporta únicamente como indicador operacional bajo el protocolo experimental de v11. No debe interpretarse como una medida de robustez general o extrapolable fuera del contexto de este experimento. Su rango esperado y limitaciones están detallados en el anexo técnico.

## Artefactos reproducibles (fuente canonica)
- Dataset canonico y hashes: `results/v11/CANONICAL_DATASET_v11.md`
- Reporte estadistico vigente: `results/v11/data/stats_report_v11.md`
- Bootstrap por run/seed: `results/v11/data/bootstrap_stats_v11.md`
- Check de que F2 != F1: `results/v11/data/f2_vs_f1_diff.md`
- Pasos de regeneracion: `results/v11/README_REPRODUCIBLE_v11.md`

## Resultados principales (dos metricas de recompensa)
Valores resumidos desde `results/v11/data/stats_report_v11.md` (n = numero de runs/archivos por agente y fase).

### F0 (Referencia descriptiva / sanity check; risk_scale=0.5; red_team=False)
| Agente      | n | mean reward_total | mean reward_env_total |
|-------------|---|------------------|-----------------------|
| control     | 2 | -20.02           | -20.02                |
| dqn_control | 2 | -24.08           | -24.08                |
| simbiosis   | 2 |  14.87           | -22.66                |

Nota: F0 se reporta solo como referencia descriptiva (sanity check); n=2 es insuficiente para inferencias estadísticas o comparaciones entre agentes.

### F1 (Alto riesgo; risk_scale=1.2; red_team=False)
| Agente      | n  | mean reward_total | mean reward_env_total |
|-------------|----|------------------|-----------------------|
| control     | 10 | -56.83           | -56.83                |
| dqn_control | 10 | -60.03           | -60.03                |
| simbiosis   | 10 | -13.98           | -58.71                |

### F2 (Estres adversarial sintetico; risk_scale=1.2; red_team=True; red_team_prob=0.1)
| Agente      | n  | mean reward_total | mean reward_env_total |
|-------------|----|------------------|-----------------------|
| control     | 10 | -71.48           | -71.48                |
| dqn_control | 10 | -70.45           | -70.45                |
| simbiosis   | 10 | -46.01           | -70.18                |

## Discusion (F2)
F2 activa perturbaciones adversariales del entorno (shocks/tripwires/bloqueos) con probabilidad por step `red_team_prob`. Esto debe interpretarse como una prueba de estres sintetica, no como un red teaming con adversario que optimiza contra la politica del agente.

Interpretacion por metrica:
- En `reward_total` (incluyendo PGF cuando aplica), Simbiosis queda por encima de `control` y `dqn_control`.
- En `reward_env_total` (recompensa ambiental), Simbiosis queda cercana a `control`/`dqn_control` y muestra una mejora pequena (≈ +1.29 vs `control` en F2).

Por tanto, el principal hallazgo empirico de v11 es que la mezcla prudencial (PGF) cambia el objetivo medido (`reward_total`), pero no demuestra superioridad sobre el reward ambiental bajo estres.

**v11 demuestra el efecto del componente prudencial (PGF) en la métrica mezclada (`reward_total`), pero no demuestra superioridad algorítmica en reward ambiental bajo estrés. Las comparaciones justas deben hacerse siempre sobre `reward_env_total`.**

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

## Estadistica e inferencia
La evidencia inferencial principal se apoya en bootstrap no parametrico por run/seed (unidad primaria = promedio por archivo `*_episodes.csv`) y se reporta en `results/v11/data/bootstrap_stats_v11.md`. Esta eleccion evita asumir normalidad y reduce el riesgo de pseudo-replicacion por episodios dependientes.

## Amenazas a la validez
- F2 es un estres adversarial sintetico; no implementa adversario min-max.
- `reward_total` puede incluir mezcla PGF cuando `pgf_mix>0` (reward shaping parcial). Para auditoria, `reward_env_total` se estima desde JSON. Ver `results/v11/ANEXO_TECNICO_v11.md` y `results/v11/data/stats_report_v11.md`.
- El pipeline depende de la definicion de `red_team_prob` y otros parametros del entorno; estos quedan trazados en los JSON de cada run.
- Para auditoria, las copias archivadas se conservan en `results/v11/archived`, pero el analisis usa solo el dataset canonico.

## Conclusiones
La serie v11 queda reproducible con un dataset canonico verificable, y F2 queda operacionalmente cerrado (F2 != F1 y la activacion del modo adversarial es observable). Esto habilita F3 sobre una base consistente: nuevos baselines, nuevas metricas de seguridad y/o variantes del ataque sintetico.
