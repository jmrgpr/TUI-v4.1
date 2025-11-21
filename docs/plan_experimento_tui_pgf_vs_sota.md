# Plan científico integral / Scientific Plan: TUI + PGF vs SOTA (DQN, PPO, A2C)

## Objetivo del experimento (Fase 2) / Experiment Objective (Phase 2)
Comparar el desempeño de TUI+PGF frente a algoritmos SOTA (DQN, PPO, A2C) bajo escenarios de riesgo, evaluando robustez, reproducibilidad y trazabilidad mediante un pipeline totalmente automatizado.

Compare the performance of TUI+PGF against SOTA algorithms (DQN, PPO, A2C) under risk scenarios, evaluating robustness, reproducibility, and traceability through a fully automated pipeline.

## ¿Qué queremos probar? / What do we want to test?

- Superioridad o competitividad de TUI+PGF en métricas clave (PGF_neto, reward_total, robustez, variabilidad y tripwires).
- Reproducibilidad y trazabilidad total del pipeline a través de semillas múltiples y artefactos auditables.
- Automatización end-to-end, generando todos los outputs necesarios para análisis estadístico y publicación sin intervención manual.

- Superiority or competitiveness of TUI+PGF in key metrics (PGF_neto, total_reward, robustness, variability, and tripwires).
- Full reproducibility and traceability of the pipeline via multiple seeds and auditable artifacts.
- End-to-end automation, generating all outputs needed for statistical analysis and publication without manual intervention.
- **A1. Inventario de datasets**: reunir CSV de barridos risk_scale, semillas (42/123/456), episodios (200 y 500), grid PGF (kappa, lambda, mix). Estandarizar columnas: agent {TUI, DQN, PPO, A2C}, seed, episodes, risk_scale, kappa, lambda, mix, pgf_neto, tripwires, robustez, flexibilidad, reward_total.
- **A2. Métricas canónicas (fijas)**: PGF_neto; robustez; flexibilidad; tripwires; opcional reward_total, risk_cost. No cambiar definiciones durante el análisis; si se ajusta, marcar como post-hoc. Incluir fórmulas explícitas de robustez y flexibilidad en Métodos.
- **A3. Baselines SOTA claros**: hiperparámetros razonables (defaults documentados), mismo presupuesto computacional/episodios que TUI.
- **A4. Presupuesto computacional**: declarar en Métodos un criterio fijo: N episodios × T pasos máx por episodio, mismas evaluaciones cada K episodios y mismo número de updates por agente.
- **A5. Control de fairness**: incluir al menos un baseline SOTA “tuneado” (p.ej. PPO_tuned o DQN_tuned con 2–3 variantes razonables) y documentar sus hiperparámetros.

## Criterios de pase a Fase 3 (gates) / Criteria to advance to Phase 3 (gates)

- El pipeline corre sin errores críticos.
- Se genera un CSV maestro completo, con metadatos y trazabilidad por archivo/semilla/agente.
- Se observa señal preliminar de competitividad de TUI+PGF frente a SOTA (por PGF_neto y/o frontera recompensa-tripwires).
- Scripts y documentación quedan listos para reproducción por terceros.
- Repositorio GitHub limpio, versionado y sincronizado.

- The pipeline runs without critical errors.
- A complete master CSV is generated, with metadata and traceability by file/seed/agent.
- Preliminary signal of TUI+PGF competitiveness against SOTA is observed (by PGF_neto and/or reward-tripwires frontier).
- Scripts and documentation are ready for third-party reproduction.
- GitHub repository is clean, versioned, and synchronized.

## Fase B — Mejora en métricas relevantes (Claim 1)
- **B1. Comparativa por riesgo**: para cada risk_scale, comparar TUI vs SOTA en PGF_neto, tripwires, robustez, flexibilidad.
- **B2. Tablas**:
  - Resumen por riesgo y agente: risk_scale | agent | PGF_neto_mean | PGF_neto_std | tripwires_mean | robustez_mean | flexibilidad_mean.
  - Mejor agente por riesgo: quién maximiza PGF_neto y quién minimiza tripwires (discute trade-off).
- **B3. Gráficos core**: PGF_neto vs riesgo; tripwires vs riesgo; robustez vs riesgo; flexibilidad vs riesgo (líneas por agente).
- **B4. Criterio de éxito**: ventaja si ocurre (al menos uno): TUI > SOTA en PGF_neto con diferencia estadística; o TUI ≈ SOTA en PGF_neto pero con menos tripwires/mayor robustez; o TUI domina frontera recompensa-riesgo.
- **B5. Reportar casos neutros/negativos**: sub-sección con rangos donde TUI no supera o es neutral, para evitar cherry-picking.

### Micro-mejora A: Definición cuantitativa de “competitivo o superior” / Quantitative definition of “competitive or superior”
“Consideraremos TUI+PGF competitivo si su PGF_neto medio está dentro de 1 desviación estándar del mejor SOTA en ≥X niveles de riesgo (X = 30% de risk_scales evaluados, o ≥2 niveles si hay pocos riesgos). Consideraremos TUI+PGF superior si excede al mejor SOTA con p < 0.05 (por risk_scale) usando test estadístico apropiado y corrección Holm-Bonferroni.”

“We will consider TUI+PGF competitive if its mean PGF_neto is within 1 standard deviation of the best SOTA in ≥X risk levels (X = 30% of evaluated risk_scales, or ≥2 levels if few risks). TUI+PGF will be considered superior if it exceeds the best SOTA with p < 0.05 (per risk_scale) using an appropriate statistical test and Holm-Bonferroni correction.”

### Micro-mejora B: Definición de “error crítico” / Definition of “critical error”
“Error crítico = fallo que impide producir el CSV maestro o invalida la comparabilidad (ej.: falta de seeds, riesgos incompletos, crash en un agente). Fallos no críticos = warnings, plots omitidos, o artefactos secundarios faltantes.”

“Critical error = failure that prevents producing the master CSV or invalidates comparability (e.g., missing seeds, incomplete risks, agent crash). Non-critical failures = warnings, omitted plots, or missing secondary artifacts.”

### Preflight GO/NO-GO checklist (5 minutos antes del batch grande) / Preflight GO/NO-GO checklist (5 minutes before big batch)

- Plan firmado y documentado (PROTOCOL/PREREG). / Signed and documented plan (PROTOCOL/PREREG).
- Pipeline automático (YAML/runner/script) listo. / Automatic pipeline (YAML/runner/script) ready.
- Rutas limpias, sin hardcoding. / Clean paths, no hardcoding.
- Smoke test previo con 1 seed × 1 riesgo × pocos episodios. / Prior smoke test with 1 seed × 1 risk × few episodes.
- CSV maestro verificado (columnas + metadatos). / Master CSV verified (columns + metadata).
- Baselines SOTA incluyen default + tuned light. / SOTA baselines include default + light tuning.
- Guardado de top-k configs PGF, no solo top-1. / Saving top-k PGF configs, not just top-1.
- Repo sincronizado y limpio. / Repo synchronized and clean.

## Fase C — Reproducibilidad (Claim 2)
- **C1. Semillas**: repetir B con seeds 42/123/456; incluir estadística.
- **C2. Estadística mínima**: media ± sd, IC95% (bootstrap o t), tamaño de efecto (Cohen d o Cliff) para PGF_neto y tripwires por riesgo/agente. Declarar test de significancia (p.ej. Mann-Whitney U por riesgo) y corrección por múltiples comparaciones (Holm-Bonferroni o FDR).
- **C3. Gráficos**: boxplots (o violin) de PGF_neto y tripwires por seed y agente.
- **C4. Claim**: “La media y desviación estándar de PGF_neto y tripwires para TUI y SOTA son consistentes entre semillas, indicando estabilidad del efecto.”

## Fase D — Generalidad del ajuste PGF (Claim 3)
- **D1. Múltiples combinaciones**: evaluar varias (kappa, lambda, mix) en varios riesgos.
- **D2. Gráficos hiperparámetros**: heatmaps de PGF_neto (ejes kappa/lambda) por mix; PGF_neto y tripwires vs riesgo para top-N combinaciones.
- **D3. Criterio**: tendencia positiva repetida (no un pico aislado): “el ajuste PGF mejora la frontera recompensa-tripwires en riesgos altos y bajos”.

## Fase E — No overfitting (Claim 4)
- **E1. Robustez a parámetros**: varias configs PGF rinden bien; no depende de un set mágico.
- **E2. Evidencia**: distribución de resultados del grid (hist/box PGF_neto y tripwires); re-run de la mejor config con más episodios (500) para estabilidad.
- **E3. Criterio**: si la mejor config se mantiene al cambiar seed, subir episodios o variar riesgo, no es tuning oportunista.
- **E4. Control de leak**: si se elige mejor config del grid, verificar top-k en reruns o en un subset de riesgos distinto para mostrar generalidad.

## Fase F — Análisis comparativo profundo (Claim 5)
- **F1. Frontera recompensa-riesgo**: scatter reward_total vs tripwires por riesgo (color por agente); opcional convex hull/curva frontera.
- **F2. Interpretación**: por qué SOTA colapsa (si ocurre) en alto riesgo? por qué TUI mantiene acción prudencial? rol de PGF (penalización, tensión, memoria).
- **F3. Claim ejemplo**: “TUI logra menor tripwires con PGF_neto competitivo, mostrando mayor robustez ante riesgos extremos sin colapso conductual.”

## Estructura sugerida del reporte
1. Resumen ejecutivo (1 página): ¿TUI supera a SOTA? ¿en qué métricas/rango de riesgo? ¿cuál es la frontera dominante?
2. Métodos: entorno y riesgo, algoritmos, métricas, presupuesto experimental, seeds/episodios, grid PGF.
3. Resultados: 3.1 Mejora (Fase B); 3.2 Reproducibilidad (Fase C); 3.3 Generalidad PGF (Fase D); 3.4 No overfit (Fase E); 3.5 Frontera (Fase F).
4. Discusión: interpretación, comparación con literatura, limitaciones, qué falta para validar fuerte.
5. Conclusión: ¿escalas a Fase 3? condiciones exactas donde TUI aporta valor.
6. Apéndices: tablas completas por seed, configuraciones, links a CSV y scripts.

## Checklist de acciones (ejecución)
1) **Recolección y consolidación**: reunir CSV; escribir master con columnas estándar (agent, seed, episodes, risk_scale, kappa, lambda, mix, pgf_neto, tripwires, robustez, flexibilidad, reward_total).
2) **Ejecución**:
   - Default PGF (seeds 42/123/456, 200 ep).
   - Tuning PGF (p.ej. kappa=2.0, lambda=0.05, mix=0.8, mismas seeds/ep).
   - Mejor config re-run con 500 ep (descartar overfit).
   - SOTA (`run_sota_comparison.py`) para PPO/A2C/DQN en mismos risk_scale.
3) **Análisis y visuales**:
   - Tablas core por riesgo/agente; tabla de mejor agente por riesgo.
   - Gráficos: líneas vs riesgo (PGF_neto, tripwires, robustez, flexibilidad); boxplots por seed (PGF_neto, tripwires); scatter reward vs tripwires; heatmaps grid PGF si aplica.
   - Estadística: IC95% y tamaño de efecto para PGF_neto y tripwires por riesgo.
4) **Interpretación y reporte**: redactar con la estructura anterior; llenar checklist de éxito Fase 2.
5) **Checklist operativo detallado (resumen)**:
   - Recolección y consolidación: reunir todos los CSV (barridos, semillas, episodios, grid); master con columnas indicadas; estandarizar nombres y campos faltantes.
   - Ejecución de experimentos: 3 barridos consistentes (default PGF seeds 42/123/456 200 ep; tuning PGF kappa=2.0 lambda=0.05 mix=0.8 mismas seeds/ep; mejor config re-run 500 ep). Correr SOTA (run_sota_comparison.py) para PPO/A2C/DQN en mismos risk_scale y guardar summaries.
   - Análisis y visualización: tablas core; “mejor agente por riesgo”; líneas vs riesgo; boxplots por seed; scatter recompensa vs tripwires (frontera); heatmaps kappa/lambda por mix si haces grid; estadística mínima (IC95% y tamaño de efecto Cohen/Cliff para PGF_neto y tripwires por riesgo).
   - Interpretación y reporte: seguir estructura (Resumen, Métodos, Resultados, Discusión, Conclusión, Apéndices); completar checklist de éxito (TUI domina alguna métrica o frontera, reproducible en >=3 seeds, tendencia PGF positiva, no depende de un solo set, rerun 500 ep estable, discusión explica mecanismos) y decidir si escalar a Fase 3.
6) **Preflight obligatorio**: antes de cada corrida, verificar que los CSV esperados no existan duplicados/mezclados y registrar hash de la configuración (p.ej. plan_hash = sha256 de un archivo de plan/parámetros).
7) **Artefactos por corrida**: guardar outputs en carpeta única por corrida (p.ej. `artifacts/run_{seed}_{episodes}_{risk}`) para trazabilidad.

## Checklist de acciones resumido (texto original solicitado)
1. Recolección y consolidación de datos  
   - Reunir todos los CSV generados (barridos, semillas, episodios, grid search).  
   - Consolidar datos en un CSV maestro con columnas: agent, seed, episodes, risk_scale, kappa, lambda, mix, pgf_neto, tripwires, robustez, flexibilidad, reward_total.  
   - Estandarizar nombres de columnas y agregar campos faltantes.
2. Ejecución de experimentos  
   - Ejecutar tres barridos consistentes:  
     * Default PGF (seeds 42/123/456, 200 episodios)  
     * Tuning PGF (kappa=2.0, lambda=0.05, mix=0.8, mismas seeds/episodios)  
     * Mejor config re-run con 500 episodios (descartar overfit)  
   - Correr SOTA (`run_sota_comparison.py`) para PPO/A2C/DQN en los mismos risk_scale y guardar summaries.
3. Análisis y visualización automatizada  
   - Generar tablas core: por riesgo y agente (media/SD de PGF_neto, tripwires, robustez, flexibilidad) y “mejor agente por riesgo” (PGF_neto y tripwires).  
   - Graficar: líneas vs riesgo (PGF_neto, tripwires, robustez, flexibilidad); boxplots por seed (PGF_neto y tripwires); scatter recompensa vs tripwires (frontera); heatmaps grid PGF (kappa/lambda por mix) si haces el grid.  
   - Calcular estadística mínima: IC95% (bootstrap o t-interval) y tamaño de efecto (Cohen’s d o Cliff’s delta) para PGF_neto y tripwires por riesgo.
4. Interpretación y reporte  
   - Redactar el reporte según la estructura propuesta (Resumen, Métodos, Resultados, Discusión, Conclusión, Apéndices).  
   - Completar el checklist de éxito de Fase 2:  
     * ¿TUI domina alguna métrica clave o la frontera recompensa-tripwires?  
     * ¿Diferencia reproducible en ≥3 semillas?  
     * ¿Tendencia PGF positiva en varios riesgos?  
     * ¿No depende de un solo set de parámetros?  
     * ¿Re-run con 500 episodios confirma estabilidad?  
     * ¿Discusión explica mecanismos, no solo números?  
   - Marcar cuántos puntos PASS y decidir si se escala a Fase 3.

## Checklist de éxito Fase 2 (marcar PASS/FAIL)
- TUI domina al menos 1 métrica clave o la frontera recompensa-tripwires.
- Diferencia reproducible en >=3 semillas.
- Tendencia PGF positiva en varios riesgos.
- No depende de un solo set de parámetros.
- Re-run con 500 episodios confirma estabilidad.
- La discusión explica mecanismos (no solo números).

Decisión: si >=5/6 PASS -> escalar a Fase 3. 3-4/6 -> Fase 2.5 (más seeds/episodios). <=2/6 -> revisar hipótesis o diseño experimental.
