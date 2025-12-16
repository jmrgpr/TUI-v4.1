# MEGA_PLAN_EVALUACION_v11_POST_F2.md

## Estado actual y diagnóstico honesto (post-F2)

### 1. Fases completadas
- [x] F0 (referencia): ejecutado y documentado (falta tabla agregada en informe)
- [x] F1 (alto riesgo): ejecutado y documentado (falta tabla agregada en informe)
- [x] F2 (redteam): ejecutado, tabla y análisis crítico incluidos

### 2. Hallazgos clave y gaps
- Simbiosis/TUI no supera al control clásico en reward bajo redteam (F2)
- Robustez y métricas prudenciales requieren definición formal y justificación
- Baseline DQN/SOTA insuficiente: urge auditar o reemplazar por PPO/Safe RL
- Faltan análisis estadísticos reales (p-valores, IC95%, tests de significancia, Cohen's d)
- Faltan datos agregados y discusión narrativa de F0 y F1 en los informes
- La narrativa debe ser honesta: F2 revela vulnerabilidad estructural de Simbiosis/TUI

### 3. Acciones inmediatas
- [ ] Agregar tablas y discusión de F0 y F1 en INFORME_CIENTIFICO y PUBLICACION
- [ ] Definir formalmente "robustez" y otras métricas en ANEXO_TECNICO
- [ ] Reescribir narrativa de F2 para reflejar trade-offs y vulnerabilidades
- [ ] Incluir análisis estadístico mínimo en tablas clave (n, media, std, p, d)
- [ ] Auditar baseline DQN; si no mejora, implementar PPO como baseline fuerte
- [ ] Planificar F3: escalado, nuevos baselines, métricas C/F/T, análisis u_proxy vs u_humans

### 4. Planificación de fases siguientes
- F3: Escalado y SOTA, con nuevos baselines y métricas de C/F/T
- F4: Análisis de alineación (u_proxy vs u_humans), correlación P_riesgo vs I_operativa
- Publicación: separar paper metodológico (infraestructura, reproducibilidad) de validación teórica (solo cuando haya evidencia)

### 5. Honestidad y comunicación
- La serie v11 es un ejemplo de ciencia abierta y autocrítica
- No se afirma validación de TUI v4.1 hasta que los datos y análisis lo permitan
- Se documentan explícitamente los modos de fallo y vulnerabilidades detectadas

---

*Este plan reemplaza al roadmap original y guía la serie v11 hacia fases más alineadas, rigurosas y honestas, en línea con los peer reviews y la evidencia experimental.*
