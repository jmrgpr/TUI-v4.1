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

## 4. Otras señales observables recomendadas para F2
Ademas de recompensa:
- `avg_tripwire` y `avg_shocks` (en JSON) y `%Tripwires` (en episodios agregados).
- `risk_effective` y `surprise` (promedios/evoluciones exportadas en JSON).

Ver comparativa F2 vs F1: `results/v11/data/f2_vs_f1_diff.md`.

