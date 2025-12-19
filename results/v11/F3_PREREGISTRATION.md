# F3_PREREGISTRATION (DRAFT) - Serie v11 (TUI v4.1)

Nota (2025-12-19): el preregistro canónico “peer-review proof” de F3 vive en `results/v11/F3/PREREGISTRO_F3_v11.md`.
Este archivo se mantiene como borrador histórico.

Este documento propone un preregistro para F3 (borrador). Su objetivo es convertir las limitaciones de F2 en preguntas causales testeables, manteniendo trazabilidad y comparabilidad con v11.

## Principio
- Unidad primaria: run/seed (no episodios).
- Metrica primaria recomendada: `reward_env_total` (comparable entre agentes).
- `reward_total` se reporta como metrica secundaria cuando `pgf_mix>0` (explicitar shaping).

## Preguntas (pre-registradas)

### P1: Ablacion PGF (efecto de `pgf_mix`)
Objetivo: estimar como cambia (i) `reward_env_total` y (ii) metricas de riesgo/cola al variar `pgf_mix`.

Diseno sugerido:
- Agente: `simbiosis`
- Factor: `pgf_mix` en una grilla discreta (ej. {0.0, 0.1, 0.2, 0.35, 0.5})
- Condiciones: F1_highrisk y F2_redteam
- Seeds: reutilizar {42, 101, 13, 7, 99} para comparabilidad; agregar seeds nuevos solo si se preregistra.

Metricas:
- Primaria: `reward_env_total`
- Secundarias: `reward_total`, degradacion (F2 - F1) en `reward_env_total`, tripwires/shocks/surprise, CVaR05 (env) y max_drawdown (env).

### P2: Comparacion justa (sin shaping)
Objetivo: responder si `simbiosis` (algoritmo) mejora sobre baselines cuando se elimina shaping.

Diseno sugerido:
- Agentes: `simbiosis(pgf_mix=0.0)`, `control`, `dqn_control`
- Condiciones: F1_highrisk y F2_redteam
- n: aumentar respecto a v11 si el efecto esperado es pequeno (decidir con piloto y preregistro)

Metrica primaria:
- `reward_env_total`

### P3 (opcional): Baseline moderno (PPO/SAC)
Objetivo: situar los resultados frente a un baseline RL mas estable.

Nota: implementar PPO/SAC puede requerir wrappers adicionales del entorno. Si se incluye, preregistrar libreria/version, hiperparametros y protocolo de entrenamiento.

### P4 (opcional): Severidad del stress test
Objetivo: validar que `red_team_prob` modula severidad de manera monotona y no artefactual.

Diseno sugerido:

## Efecto mínimo de interés (MESI)
- Para `reward_env_total`, el MESI se define heurísticamente como una diferencia de al menos 5% respecto al baseline control, basada en la variabilidad observada en v11.
- Para `reward_total`, el MESI se define como una diferencia de al menos 10% respecto al baseline control, dado el mayor rango de valores posibles.
- Para métricas de riesgo (CVaR05, max_drawdown), el MESI se define como una diferencia absoluta de al menos 2 unidades respecto al baseline.

Estos valores son orientativos y pueden ajustarse en función de la varianza observada en los datos piloto.

## Regla de expansión de n (seeds)
- El aumento de n (número de seeds) solo se considerará si la varianza o los intervalos de confianza (IC95%) de la métrica primaria (`reward_env_total`) resultan demasiado amplios para detectar el MESI definido, independientemente de la dirección del efecto observado.
- Cualquier expansión de n debe preregistrarse antes de analizar los resultados completos y documentarse en F3_deviations_log.md.

## Comparaciones y métricas pre-registradas

- Comparaciones primarias:
  - P1: Efecto de pgf_mix sobre reward_env_total en Simbiosis (F1 y F2)
  - P2: Simbiosis(pgf_mix=0.0) vs control y dqn_control en reward_env_total (F1 y F2)
- Comparaciones secundarias/exploratorias:
  - P1: Efecto de pgf_mix sobre reward_total, CVaR05, max_drawdown, tripwires, shocks
  - P3: Simbiosis vs PPO/SAC (si se implementa)
  - P4: Efecto de red_team_prob sobre reward_env_total y señales observables
- Corrección múltiple:
  - Se aplicará corrección Holm-Bonferroni a todas las comparaciones primarias sobre reward_env_total.
  - Comparaciones secundarias se reportan como exploratorias, sin corrección estricta.

## Analisis (pre-registrado)
- Reportar medias + IC95% por bootstrap a nivel run/seed.
- Definir comparaciones primarias vs exploratorias.
- Correccion multiple: Holm (o preregistrar alternativa).

## Estructura de salida (sugerida)
Mantener el mismo patron de carpetas que v11 (por fase / grid / riesgo / agente / seed) para reusar scripts existentes.

## Desviaciones
Registrar cualquier desviacion en un log versionado (ej. `results/v11/F3_deviations_log.md`) antes de reportar resultados.

## Criterios de exclusión y stopping rule

- Se excluirán runs con archivos corruptos, NaNs en métricas primarias, runs truncados o con menos del 95% de episodios esperados.
- Cualquier exclusión será documentada en F3_deviations_log.md antes del análisis.
- Stopping rule: se detendrá la recolección de datos cuando se alcance el n preregistrado por grupo/fase, salvo que el análisis intermedio justifique aumentar n (debe preregistrarse antes de analizar resultados).

## Definición exacta de métricas de riesgo
- CVaR05: promedio del 5% peor de reward_env_total por run (cola izquierda de la distribución de episodios).
- max_drawdown: máxima caída acumulada de reward_env_total por run (diferencia máxima entre un pico local y el mínimo posterior en la serie temporal de episodios).

## Plan de reporte mínimo
- Tablas: medias, IC95% y n por agente, fase y grid_size para reward_env_total (primaria) y reward_total (secundaria).
- Figura obligatoria: degradación F2−F1 en reward_env_total por agente y grid_size.
- Todas las exclusiones y desviaciones documentadas en F3_deviations_log.md.

- Nota: la definición canónica de la family primaria (M y comparaciones) está fijada en `results/v11/F3/PREREGISTRO_F3_v11.md`. Este borrador no debe usarse para auditoría.
