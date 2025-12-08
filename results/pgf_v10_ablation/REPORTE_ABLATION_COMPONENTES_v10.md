# REPORTE_ABLATION_COMPONENTES_v10.md

## Resumen Ejecutivo
FASE 2 compara el RL puro 8×8 (baseline) contra variantes que encienden un único componente. Variantes oficiales: baseline, with_regularization, with_rewardextra, with_shaping, with_curriculum. Las variantes hyper_* se consideran exploratorias (apéndice).

## Tabla comparativa (8×8, seeds 42/13/101)

| Variante             | Seed | Success Total | Últimos 100 | Gate | 1er Éxito | Reg | Shaping | RewardExtra | Curriculum |
|----------------------|------|---------------|-------------|------|-----------|-----|---------|-------------|------------|
| baseline             | 42   | 0.806         | 0.85        | Sí   | 11        | No  | No      | No          | No         |
| baseline             | 13   | 0.756         | 0.86        | Sí   | 24        | No  | No      | No          | No         |
| baseline             | 101  | 0.775         | 0.81        | Sí   | 74        | No  | No      | No          | No         |
| with_regularization  | 42   | 0.787         | 0.90        | Sí   | 9         | Sí  | No      | No          | No         |
| with_regularization  | 13   | 0.757         | 0.97        | Sí   | 6         | Sí  | No      | No          | No         |
| with_regularization  | 101  | 0.819         | 0.97        | Sí   | 2         | Sí  | No      | No          | No         |
| with_rewardextra     | 42   | 0.501         | 0.74        | Sí   | 13        | No  | No      | Sí          | No         |
| with_rewardextra     | 13   | 0.522         | 0.21        | Sí   | 5         | No  | No      | Sí          | No         |
| with_rewardextra     | 101  | 0.637         | 0.73        | Sí   | 136       | No  | No      | Sí          | No         |
| with_shaping         | 42   | 0.018         | 0.00        | No   | 4         | No  | Sí      | No          | No         |
| with_shaping         | 13   | 0.000         | 0.00        | No   | -         | No  | Sí      | No          | No         |
| with_shaping         | 101  | 0.000         | 0.00        | No   | -         | No  | Sí      | No          | No         |
| with_curriculum      | 101  | 0.614         | 0.81        | Sí   | 1         | No  | No      | No          | Sí         |
| with_curriculum      | 13   | NA            | NA          | No   | -         | No  | No      | No          | Sí         |
| with_curriculum      | 42   | NA            | NA          | No   | -         | No  | No      | No          | Sí         |
| hyper_shaping*       | 42   | 0.812         | 0.95        | Sí   | 12        | No  | No      | No          | No         |
| hyper_shaping*       | 13   | 0.675         | 0.82        | Sí   | 44        | No  | No      | No          | No         |
| hyper_shaping*       | 101  | 0.798         | 0.92        | Sí   | 7         | No  | No      | No          | No         |
| hyper_rewardextra*   | 42   | 0.835         | 1.00        | Sí   | 19        | No  | No      | No          | No         |
| hyper_rewardextra*   | 13   | 0.735         | 0.79        | Sí   | 4         | No  | No      | No          | No         |
| hyper_rewardextra*   | 101  | 0.665         | 0.77        | Sí   | 3         | No  | No      | No          | No         |

Notas:
- with_curriculum: seeds 13 y 42 abortaron en 4×4 (gate fallido), solo seed 101 llegó a 8×8.
- with_shaping: colapso a success=0 en las 3 seeds.
- *hyper_*: sweeps exploratorios; no forman parte del núcleo.

## Conclusiones y decisiones
- **Baseline RL puro**: robusto (≈0.84 success_last_100).
- **Regularización**: mejora el éxito y la estabilidad → adoptar en el stack estándar.
- **RewardExtra**: inestable y por debajo de baseline → no adoptar.
- **Shaping (PGF como reward)**: colapso sistemático → descartar en v10; PGF se usará solo como métrica offline (no como reward).
- **Curriculum aislado**: frágil; abortos en 4×4 se documentan como resultado válido.
- **Hyper_***: se reportan como exploratorio/apéndice, no en la comparación principal.

## Recomendaciones
- Mantener regularización por defecto.
- No usar PGF como reward; reservar PGF para análisis offline (Fase 3/v11).
- No integrar reward_extra en el stack estable.
- Curriculum: usar con cautela y documentar gates/abortos por seed.

## Reproducibilidad
- Datos en `results/pgf_v10_ablation/component_*/seeds/seed_*/...summary_*.csv`.
- CSV oficial: `results/pgf_v10_ablation/analisis_comparativo/ablation_componentes_summary_v10.csv` (incluye notas de abortos/colapsos).
- Runner y preregistro: `scripts/run_ablation_componentes_v10.py`, `PREREGISTRO_ABLATION_COMPONENTES_v10.md`.
