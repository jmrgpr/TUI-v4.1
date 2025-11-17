# Tracking y Bitácora TUI v4.2

Este documento registra todos los avances, decisiones, experimentos, tests y resultados de la Fase v4.2 del proyecto TUI.

## Estructura sugerida
- **Fecha**
- **Acción/Commit**
- **Descripción breve**
- **Archivos modificados**
- **Resultado/Test**
- **Observaciones**

---

## Ejemplo de entrada

**2025-11-17  [17:00]**
- Creación de rama `feature/tui-v4.2-refactorizacion-metodologica` y carpeta `v4.2jobs`.
- Registro del plan de acción definitivo para TUI v4.2.
- El plan sigue la revisión científica y el consenso metodológico externo, que identificó dos problemas críticos: (1) baseline injusto (Q-learning vs. DQN) y (2) arquitectura de "agente oráculo" (PGF calculado internamente).
- Se adopta el plan integrado por su valor metodológico y por asegurar reproducibilidad, robustez y trazabilidad científica.
- Razón: Dos análisis independientes coinciden en los fallos y soluciones, lo que da certeza absoluta sobre el camino correcto. El hito de visualización (video 1x3 agentes) se añade para maximizar el impacto y la comunicación científica.
- Estado inicial: Workspace limpio, cobertura ≥98%, documentación y auditoría actualizadas, repositorio privado.

---

**2025-11-17  [17:00]**
- Inicio formal de la Fase I: Refactorización metodológica y baseline justo.
- Próximo paso: Implementar Agente DQN-Control y crear test de inacción esperada.

---

## Extracto del Reporte de Revisión Científica y Plan de Acción Estratégico

**Para:** Investigador Principal del Proyecto TUI
**De:** Asociado de Investigación Científica (Peer Reviewer)
**Fecha:** 17 de noviembre de 2025
**Asunto:** Evaluación de análisis externos y consolidación del plan de acción definitivo para TUI v4.2.

La evaluación externa confirma los dos problemas críticos: (1) baseline injusto (Q-learning vs. DQN) y (2) arquitectura de "agente oráculo" (PGF calculado internamente). Dos análisis independientes coinciden en los fallos y soluciones, dando certeza absoluta sobre los próximos pasos. El hito de visualización (video 1x3 agentes) se añade para maximizar el impacto y la comunicación científica.

**Plan de Acción Definitivo:**
- FASE I: Refactorización metodológica (baseline justo, eliminar oráculo, reproducibilidad multi-seed)
- FASE II: Ejecución y análisis de datos (validación de hipótesis, barrido de risk_scale, análisis de tensión del riesgo)
- FASE III: Diseminación y publicación (video comparativo, redacción y publicación del paper)
- FASE IV: Investigación futura (experimento de emergencia, validación teórica)

Este plan transforma la prueba de concepto en una validación científica robusta y lista para publicación y revisión por pares.

---

<<<<<<< HEAD
## Bitácora de cambios recientes (2025-11-18)

**2025-11-18  [18:00]**
- Refactorización final y merge a `main`.
- Eliminado código muerto (Agent.__init__ duplicado) en `sim/prototipo_rl_simbiosis.py`.
- Añadidos tests de integración con subprocess para CLI y cobertura de ramas visualización, export, plot y risk_sweep.
- Reforzada cobertura de `reprogram_purpose` y métodos de serialización de policy.
- Cobertura final: 98% en `sim/prototipo_rl_simbiosis.py` y 96-100% en módulos principales.
- Todos los tests pasan correctamente (316/316).
- Documentación y README actualizados para reflejar estructura profesional y auditoría de exportación.
- Merge exitoso de rama `feature/tui-v4.2-refactorizacion-metodologica` a `main` y push remoto.
- Estado: Listo para publicación y auditoría científica internacional.

=======
>>>>>>> 66a6632 (Subida de avances: baseline DQN-Control, reorganización, test y cobertura 95%. Listo para refuerzo a 98%.)
