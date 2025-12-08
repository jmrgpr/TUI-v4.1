# FASE 2 COMPLETADA – Ablation de Componentes v10

**Fecha:** 2025-12-08  
**Resumen:** Fase 2 ejecutada en 8×8 con variantes oficiales: baseline, with_regularization, with_rewardextra, with_shaping, with_curriculum (seeds 42/13/101). Variantes hyper_* tratadas como exploratorias.

## Resultados clave
- Baseline: success_last_100 ≈ 0.84 (robusto).
- +Regularización: ≈ 0.95 (mejora estable).
- +RewardExtra: ≈ 0.56 (inestable, peor que baseline).
- +Shaping (PGF como reward): 0% en las 3 seeds (colapso).
- Curriculum aislado: solo seed 101 completó 4×4→6×6→8×8; seeds 13/42 abortaron en 4×4 (gate fallido).

## Decisiones
- Adoptar regularización en el stack estable.
- No adoptar reward_extra.
- Descartar PGF como reward directo; usar PGF solo como métrica offline/analítica.
- Curriculum: documentar fragilidad y abortos por seed.
- Hyper_* se mantienen como exploratorio (apéndice).

## Artefactos
- CSV oficial: `results/pgf_v10_ablation/analisis_comparativo/ablation_componentes_summary_v10.csv`
- Reporte F2: `results/pgf_v10_ablation/REPORTE_ABLATION_COMPONENTES_v10.md`

## Próximo paso
- Fase 3 (PGF offline): enriquecer episodios con I_op/PGF y analizar correlaciones (ver preregistro Fase 3).
