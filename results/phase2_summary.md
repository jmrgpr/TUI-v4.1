# Resultado experimento fase 2 (TUI + PGF vs SOTA)

## Resumen ejecutivo
- Pipeline técnico: **OK**. Barridos default/tuning (seeds 42/123/456), rerun 500 eps, SOTA y consolidación completados sin errores críticos; `results/master_results.csv` y `results/experiment_log.txt` generados.
- Métricas principales (PGF_neto, tripwires, reward):
  - **DQN-Control** domina en recompensa y empata/ligeramente supera en PGF_neto/tripwires frente a TUI+PGF.
  - **TUI+PGF (tuning)** mejora vs default (de parálisis a comportamiento competitivo) y muestra menos tripwires que DQN-Control en riesgo alto, a costa de recompensa.
  - **PPO** aparece con reward/accidentes no comparables (posible “quedarse quieto”); no concluyente.
- Claims científicos: soportan prudencia (menos accidentes en alto riesgo con TUI tuning), pero no hay superioridad general en recompensa/PGF_neto. Faltan métricas secundarias para robustez/flexibilidad.

## Hallazgos clave
- Tuning PGF (kappa=2.0, lambda=0.05, mix=0.8) es crítico: TUI pasa de recompensa ~-25 (parálisis) a ~-2.5 (riesgo bajo) y reduce tripwires en riesgo alto.
- DQN-Control mantiene mejor trade-off recompensa–riesgo global; TUI tuning solo gana en “menos accidentes” bajo riesgo 3.0.
- PPO en este master no es baseline fiable (reward 371 en riesgo 0.5 y 0 tripwires en altos riesgos). Requiere export homogénea.

## Limitaciones del master actual
- Columnas `robustez` y `flexibilidad` están en NaN → no se puede evaluar esos claims.
- No se capturó metadata de configuración (default vs tuning vs rerun 500), ni episodes/kappa/lambda/mix por fila.
- risk_scale depende del nombre del archivo; si falta “riskX” queda None.
- SOTA incompleto: A2C no aparece; PPO exportado con escala dudosa.

## Próximos pasos recomendados
1) Reconsolidar con más metadata:
   - Leer risk_scale desde columna si está disponible; incluir episodes/kappa/lambda/mix y flags de config (default/tuning/rerun500).
   - Incluir robustez y flexibilidad si están en los CSV fuente.
2) Homogeneizar SOTA:
   - Exportar PPO/A2C/DQN con la misma definición de reward/tripwires y un CSV por seed/riesgo.
3) Re-consolidar y reanalizar:
   - Volver a generar tablas/gráficos (PGF_neto/tripwires vs riesgo, mejor agente por riesgo, frontera recompensa–tripwires).
   - Aplicar tests (Mann-Whitney + Holm/FDR) y tamaños de efecto para PGF_neto/tripwires.
4) Si se busca validar PGF:
   - Ablation TUI sin PGF vs TUI con PGF.
   - Ajustes PGF menos severos (aflojar lambda/mix) para ver si mejora recompensa sin perder prudencia.

## Archivos relevantes
- `results/master_results.csv` (datos consolidados actuales).
- `results/experiment_log.txt` (log de ejecución).
- `notebooks/analysis_phase2.ipynb` (genera tablas/gráficos en `reports/phase2/`).
