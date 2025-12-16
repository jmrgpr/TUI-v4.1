## MEGA PLAN DE EVALUACIÓN TUI v11 — POST F2

### Estado y diagnóstico honesto (post-F2)

#### 1. Fases completadas
- [x] F0 (referencia): ejecutado y documentado (falta tabla agregada en informe)
- [x] F1 (alto riesgo): ejecutado y documentado (falta tabla agregada en informe)
- [x] F2 (redteam): ejecutado, tabla y análisis crítico incluidos

#### 2. Hallazgos clave y gaps
- Simbiosis/TUI no supera al control clásico en reward bajo redteam (F2)
- Robustez y métricas prudenciales requieren definición formal y justificación
- Baseline DQN/SOTA insuficiente: urge auditar o reemplazar por PPO/Safe RL
- Faltan análisis estadísticos reales (p-valores, IC95%, tests de significancia, Cohen's d)
- Faltan datos agregados y discusión narrativa de F0 y F1 en los informes
- La narrativa debe ser honesta: F2 revela vulnerabilidad estructural de Simbiosis/TUI

- [x] Agregar tablas y discusión de F0 y F1 en INFORME_CIENTIFICO y PUBLICACION
- [x] Definir formalmente "robustez" y otras métricas en ANEXO_TECNICO
- [x] Reescribir narrativa de F2 para reflejar trade-offs y vulnerabilidades
- [x] Incluir análisis estadístico inferencial mínimo (n, IC95%, effect size) en tablas clave — insertado y referenciado en `results/v11/stats_report_v11.md`
- [ ] Añadir métricas complementarias a robustez (mediana, IQR, % tripwires, CVaR, drawdown, violin/boxplots)
- [ ] Auditar baseline DQN; si no mejora, justificar o implementar PPO/Safe RL como baseline fuerte (o dejarlo como preregistro para F3)
- [ ] Planificar F3: escalado, nuevos baselines, métricas C/F/T, análisis u_proxy vs u_humans

#### 4. Planificación de fases siguientes
- F3: Escalado y SOTA, con nuevos baselines (PPO/Safe RL) y métricas de C/F/T, métricas complementarias y análisis estadístico completo
- F4: Análisis de alineación (u_proxy vs u_humans), correlación P_riesgo vs I_operativa
- Publicación: separar paper metodológico (infraestructura, reproducibilidad, trade-offs y modos de fallo) de validación teórica (solo cuando haya evidencia)

#### 5. Honestidad y comunicación


*Este plan reemplaza al roadmap original y guía la serie v11 hacia fases más alineadas, rigurosas y honestas, en línea con los peer reviews y la evidencia experimental.*

### Seguimiento inmediato (post-inserción)
### Cierre F2
- Estado: revisiones automáticas realizadas — estadística inferencial añadida, métricas por episodio calculadas, checks finales de seeds/outliers ejecutados.
- Resultado de checks: algunos archivos piloto/diagnóstico y debug (ej. `*_piloto50_*`, `test_debug_run_episodes.csv`) tienen menos episodios que la mediana; se listan en `results/v11/data/f2_final_checks.csv` (copia) y en `results/v11/f2_final_checks.md`. Los archivos problemáticos han sido movidos a `results/v11/archived/` (log: `results/v11/archived/moved_files_log.csv`).
- Acción recomendada: eliminar/ignorar archivos piloto/debug en agregados finales o documentarlos explícitamente. Si aceptas, marcaré F2 como cerrado y pasaré a preregistro PPO para F3.
*** End Patch***"/>
