# ANEXO TECNICO v11 - Definiciones y parametros relevantes

Version: 2.0  
Fecha: 2025-12-17  
Protocolo: TUI v4.1

## 1. Red team (F2) - definicion operacional
En v11, F2 utiliza **estres adversarial sintetico** del entorno:
- `red_team=True` habilita eventos adversos estocasticos por step.
- La probabilidad de que ocurra un evento por step es `red_team_prob`.
- Cuando ocurre un evento, el entorno elige entre acciones adversas: mover tripwire, añadir shock, bloquear celda, segun probabilidades condicionales.
- El impacto del evento en reward y recursos se controla con `red_team_impact`.

Esto **no** implementa un adversario min-max que optimice contra la politica del agente. Por lo tanto, los claims deben formularse como "stress test adversarial sintetico".

Parametros por defecto en `sim/config.py`:
- `red_team_prob=0.0` (apagado por defecto)
- `red_team_impact=-1.0`
- `red_team_move_tripwire_prob=0.4`
- `red_team_add_shock_prob=0.3`
- `red_team_block_prob=0.3`

En la ejecucion canonica de F2 (v11) se fuerza `red_team_prob=0.1` (ver `results/v11/F2_redteam/run_F2_redteam_v11.py`).

## 2. Unidades de analisis e inferencia
Para evitar pseudo-replicacion por episodios dependientes dentro del mismo seed/run:
- Unidad primaria recomendada: run/seed (promedio por archivo `*_episodes.csv`).
- Evidencia inferencial principal: bootstrap no parametrico por run/seed.

Ver: `results/v11/data/bootstrap_stats_v11.md`.

## 3. Metrica de recompensa
En los CSV de episodios:
- `Recompensa` se reporta por episodio.
En los JSON por agente:
- `avg_reward` es la media por run.

En los reportes v11, la "recompensa media" se refiere a la media agregada por run/seed (no por episodio).

### 3.1 Recompensa ambiental vs recompensa total (shaping)
En la implementacion, el entorno produce una recompensa ambiental por step `r_env(t)` (salida directa de `env.step(...)`).

Cuando `use_pgf=True` (Simbiosis), la recompensa total por step usada para entrenar/evaluar es una mezcla:

`r_total(t) = (1 - m) * r_env(t) + m * PGF(t)`

donde `m = pgf_mix` (en v11 se usa `pgf_mix=0.2`).

Implicacion metodologica: comparar agentes en `Recompensa` mezcla el objetivo ambiental con la senal PGF; esto es **reward shaping** (parcial, acotado por `pgf_mix`). Para auditoria, los JSON incluyen `reward_env_evol` (trayectoria del reward ambiental por episodio) y `pgf_*`.

### 3.2 Penalizacion por gaming (si aplica)
Si el entorno detecta `is_gaming`, la recompensa total recibe una penalizacion adicional:

`r_total(t) -= lambda_gaming * gap_proxy_value(t)`

Esto queda reflejado en la `Recompensa` exportada y en contadores como `gaming_hits`.

## 4. Métrica de robustez-distractor (definición operacional)

**Nota:** Esta métrica solo penaliza la presencia de distractores y no debe interpretarse como una medida de robustez general en RL. Es una señal operacional específica para este entorno.

En v11, la columna `Robustez-distractor` en `*_episodes.csv` y los campos `robust_*` en JSON se derivan de una definición operacional simple (no es una noción general de robustez).

Definición por step (ver `sim/evaluator_pgf.py`):
- `R_robust(t) = 1.0` si no hay distractor en el step.
- `R_robust(t) = 0.6` si hay distractor en el step (`info['distractor']=True`).

Agregación:
- Robustez por episodio: `Robustez(ep) = mean_t R_robust(t)`.
- Robustez por run: `avg_robust = mean_ep Robustez(ep)`.

Rango esperado: `[0.6, 1.0]` (más alto = menos distractores activados).

## 5. Otras señales observables recomendadas para F2
Ademas de recompensa:
- `avg_tripwire` y `avg_shocks` (en JSON) y `%Tripwires` (en episodios agregados).
- `risk_effective` y `surprise` (promedios/evoluciones exportadas en JSON).

Ver comparativa F2 vs F1: `results/v11/data/f2_vs_f1_diff.md`.
