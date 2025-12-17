# Analisis personal (actualizado) sobre F1_highrisk y F2_redteam - v11

Este texto es una lectura cualitativa para acompañar los artefactos canonicos. No reemplaza los reportes generados por pipeline.

Referencias canonicas:
- `results/v11/data/stats_report_v11.md`
- `results/v11/data/stats_summary_v11.csv`
- `results/v11/data/f2_vs_f1_diff.md`
- `results/v11/CANONICAL_DATASET_v11.md`

## F1_highrisk (sin ataque)
- En F1 se evalua rendimiento bajo riesgo alto sin perturbaciones adversariales activas.
- En el dataset canonico, el ranking por reward medio favorece a `simbiosis` frente a `control` y `dqn_control` (ver `results/v11/data/stats_report_v11.md`).

## F2_redteam (stress test adversarial sintetico)
Definicion operacional (v11):
- F2 activa `red_team=True` y perturbaciones estocasticas por step (no hay adversario min-max).
- Los parametros del ataque quedan trazados en cada JSON (`attack_enabled`, `attack_type`, `attack_params`).

Lectura de resultados:
- F2 reduce el reward medio de todos los agentes respecto a F1, lo cual es consistente con un entorno mas hostil.
- El ranking por reward en F2 puede mantenerse o cambiar, pero lo mas importante es medir la **degradacion** (F2 - F1) y las senales observables del ataque (tripwires/shocks/surprise/risk_effective), que se documentan en `results/v11/data/f2_vs_f1_diff.md`.
- En el dataset canonico actual, `simbiosis` sigue mostrando mejor reward medio que `control`, pero su degradacion relativa (vs F1) es mayor; esto sugiere trade-offs y posibles fragilidades bajo stress adversarial.

## Nota de honestidad metodologica
La serie v11 tiene trazabilidad fuerte, pero si se quiere publicar con claims robustos, F3 deberia:
- Usar unidad primaria por seed/run (evitar independencia falsa por episodio).
- Incluir un baseline RL mas estable (PPO/SAC/TD3 o Safe-RL).
- Definir formalmente "robustez" y metricas prudenciales (formula e interpretacion).

