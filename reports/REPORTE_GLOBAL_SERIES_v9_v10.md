# REPORTE GLOBAL (Serie v9 y v10, sin ablation)

**Proyecto:** TUI-v4.1 – PGF / Gridworld RL  
**Serie:** v9 y v10 (experimentos centrales, sin incluir Fase 2 ablation)  
**Fecha:** 2025-12-08  
**Autor:** José M. Rivera García  
**Propósito:** Síntesis para publicación (hallazgos, métricas clave, riesgos, próximos pasos)

---

## 0. Alcance

- Incluye: resultados verificados de v9 (curriculum de shaping) y v10 (adaptive trivial y v10_viable con curriculum y transfer).  
- Excluye: Ablation Fase 1/2, sweeps previos y series v11+ (solo referencias mínimas).  
- Fuentes primarias:  
  - v9: `results/pgf_v9/REPORTE_FINAL_v9.md`  
  - v10 (adaptive trivial): `results/pgf_v10/reportes/REPORTE_FINAL_v10.md`  
  - v10_viable: `results/pgf_v10_viable/reportes/REPORTE_FINAL_v10_viable.md`  
  - Global previo: `reports/REPORTE_GLOBAL_2025-11-24.md`

---

## 1. Resumen Ejecutivo

- **v9 (curriculum de shaping en 4×4)**: Evidencia preliminar (N=3) sugiere que un curriculum de intensidad de shaping (s=0→0.25→0.5→1.0) puede mitigar over-alignment en entornos pequeños. 2/3 seeds alcanzan paridad con control; 1/3 colapsa. Efecto medio (d≈0.66) pero potencia estadística baja (18%) → requiere réplica con N≈10.
- **v10 (adaptive trivial 8×8)**: Entorno fácil (balance 8.0); Adaptive, Fixed y Control convergen a ~100% success. Curriculum/adaptive no aportan en condiciones triviales. Hallazgo metodológico: cuando el entorno no presiona, el curriculum es redundante.
- **v10_viable (curriculum + transfer 4×4→6×6→8×8)**: Pipeline completo con economía viable; todos los gates superados. Resultados: 4×4 success_last_100 ≈93%; 6×6 ≈68%; 8×8 ≈87%. Transfer efectivo (primer éxito 8×8 en episodio 1), escalabilidad validada.
- **Conclusión global**: Curriculum y transfer son útiles en entornos con presión moderada (v10_viable), redundantes en entornos triviales (v10). El shaping de PGF en v9 muestra señales prometedoras pero necesita mayor N para confirmar.

---

## 2. Metodología (común)

- Entorno: `ResourceDensityEnv` (grid con recursos dinámicos, tripwires, shocks, distractores).  
- Economía v10/v10_viable: initial_resources=8.0, step_cost=-0.15, spawn_rate=0.40, goal_reward=20.0.  
- Agente: DQN con replay y target network (LEARNING_RATE, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY, BATCH_SIZE, MEMORY_SIZE, HIDDEN_DIM) según `run_curriculum_complete_viable.py`.  
- Métricas: success_rate_total, success_last_100, first_success_episode, convergence_episode, gates por fase (80/20/10 en curriculum).

---

## 3. Resultados por Serie

### 3.1 v9 (Curriculum de shaping, grid 4×4, N=3)
- Diseño: curriculum de shaping s=0→0.25→0.5→1.0 vs directo s=1.0 vs control s=0.0; 300 episodios totales.  
- Hallazgos:  
  - 2/3 seeds alcanzan éxito comparable al control (reward ~116, success 100%); 1/3 colapsa en etapa final.  
  - Efecto medio (d≈0.66) y potencia 18% → evidencia preliminar, no concluyente.  
- Riesgo: N insuficiente; resultados no significativos estadísticamente (ICs amplios).  
- Fuente: `results/pgf_v9/REPORTE_FINAL_v9.md`.

### 3.2 v10 (Adaptive curriculum trivial 8×8, entorno fácil)
- Diseño: adaptive vs fixed vs control en 8×8 con economía balance=8.0.  
- Resultados: ~100% success en todas las estrategias; ratios ~1.0; gates superados trivialmente.  
- Conclusión: curriculum/adaptive redundantes cuando el entorno es poco exigente.  
- Fuente: `results/pgf_v10/reportes/REPORTE_FINAL_v10.md`.

### 3.3 v10_viable (Curriculum + transfer 4×4→6×6→8×8)
- Diseño: curriculum completo con transferencia de pesos entre fases, gates 80/20/10.  
- Resultados (tabla reporte):  
  - 4×4: success_rate_total ≈79.6%; success_last_100 ≈93%; gate 80% → pasado.  
  - 6×6: success_rate_total ≈27.4%; success_last_100 ≈68%; gate 20% → pasado.  
  - 8×8: success_rate_total ≈61.3%; success_last_100 ≈87%; gate 10% → pasado.  
  - Transfer: primer éxito 8×8 en episodio 1 (transfer efectivo).  
- Conclusión: pipeline viable, escalabilidad validada en economía v10.  
- Fuente: `results/pgf_v10_viable/reportes/REPORTE_FINAL_v10_viable.md`.

---

## 4. Limitaciones y Riesgos
- v9: N=3 → potencia 18%; resultados preliminares, no significativos formalmente.  
- v10: entorno demasiado fácil; no estresa curriculum ni transfer.  
- v10_viable: single-seed (42) en curriculum completo; falta multi-seed para robustez.  
- No hay validación causal amplia ni red-team real; sólo simulaciones controladas.

---

## 5. Recomendaciones
- Replicar v9 con N≥10 para confirmar efecto del curriculum de shaping.  
- Para entornos tipo v10 (fáciles): curriculum no aporta; concentrar esfuerzos en escenarios con presión real.  
- Extender v10_viable a multi-seed (≥3) para consolidar evidencia de curriculum+transfer.  
- Documentar ablation Fase 2 (en curso) para decidir qué componentes (shaping, reward_extra, curriculum, transfer, regularización) se mantienen para v11.  
- Mantener reproducibilidad: usar los parámetros fijados en `run_curriculum_complete_viable.py` y preregistros correspondientes.

---

## 6. Referencias de archivos
- v9: `results/pgf_v9/REPORTE_FINAL_v9.md`, `results/pgf_v9/PREREGISTRO_v9.md`, `results/pgf_v9/README.md`.  
- v10: `results/pgf_v10/reportes/REPORTE_FINAL_v10.md`, `results/pgf_v10/PREREGISTRO_v10.md`.  
- v10_viable: `results/pgf_v10_viable/reportes/REPORTE_FINAL_v10_viable.md`, `results/pgf_v10_viable/PREREGISTRO_v10_viable.md`.  
- Global previo: `reports/REPORTE_GLOBAL_2025-11-24.md`.

---

## 7. Nota sobre ablation (Fase 2)
La ablation por componentes (shaping, reward_extra, curriculum, transfer, regularización) está preregistrada en `results/pgf_v10_ablation/PREREGISTRO_ABLATION_COMPONENTES_v10.md` y en ejecución; sus resultados se integrarán en un reporte aparte cuando finalicen los runs.

---

## Opinión científica sobre los resultados de ablation v10

### 1. Regularización
La regularización (weight decay y dropout) mejora o iguala el desempeño del RL puro. En todos los seeds, el éxito final y en los últimos 100 episodios es igual o superior al baseline. Esto indica que la regularización es un componente robusto y recomendable para producción.

### 2. Shaping
El shaping, tal como está implementado, perjudica el aprendizaje: todos los seeds fallan el gate y el éxito es prácticamente nulo. Esto sugiere que el diseño actual del shaping introduce una señal de recompensa que interfiere negativamente con la política óptima. Recomiendo revisar el mecanismo y su escala.

### 3. RewardExtra
El reward extra aporta, pero no supera a la regularización ni al baseline. Su éxito es moderado y consistente, pero no destaca como solución óptima. Puede ser útil en combinación, pero no como único componente.

### 4. Curriculum
El curriculum muestra alta varianza entre seeds: solo uno pasa el gate, los otros abortan en 4x4. Esto indica que el curriculum puede ser útil en ciertos casos, pero su robustez depende fuertemente de la inicialización y la secuencia de tareas. Recomiendo analizar más a fondo la configuración y los criterios de avance.

### 5. Hyperparametrización
Los barridos de hiperparámetros (shaping/rewardextra) pueden superar el baseline si se ajustan correctamente. Esto demuestra que la optimización fina de parámetros es clave para maximizar el desempeño, pero requiere validación cruzada y análisis de sensibilidad.

### 6. Baseline RL puro
El RL puro 8x8 es un baseline fuerte y estable, con éxito alto y baja varianza entre seeds. Es una referencia válida para comparar cualquier mejora.

---

## Recomendaciones científicas
- Mantener regularización como componente estándar.
- Rediseñar el shaping para evitar interferencias negativas.
- Analizar la varianza y robustez del curriculum.
- Priorizar la optimización de hiperparámetros en futuras fases.
- Usar el RL puro como baseline para toda comparación.

---

*Análisis científico generado por GitHub Copilot el 8/12/2025.*

