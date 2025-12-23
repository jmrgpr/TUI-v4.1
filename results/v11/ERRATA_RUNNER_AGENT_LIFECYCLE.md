# ERRATA (v11) — Ciclo de vida del agente en `sim/runner.py`

**Fecha:** 2025-12-23  
**Serie:** v11 (TUI v4.1)  
**Estado:** Nota post‑cierre (no reabre fases)

## Resumen

Se detectó un punto crítico de implementación en `sim/runner.py` dentro de `run_experiment(...)`:

- El agente (`Agent` y/o `DQNAgent`) se **instanciaba dentro** del loop `for ep in range(episodes):`.
- Esto implica que, para `episodes>1`, **cada episodio crea un agente nuevo**, reiniciando:
  - política/Q‑table (`Agent.policy`) o red/pesos/buffer (`DQNAgent`)
  - schedules (por ejemplo, `epsilon` en DQN)
  - memoria/estado del agente entre episodios

## Implicación (qué significa para v11)

- Los resultados y artefactos de v11 (F0–F6) siguen siendo **auditables** (CSV canónicos + hashes + scripts).
- Pero cualquier interpretación que asuma **aprendizaje acumulativo a través de los 200 episodios de un run** queda limitada: el comportamiento observado corresponde a un régimen tipo **episodic‑reset** (aprendizaje dentro del episodio/steps, pero no acumulado entre episodios).

Esto puede afectar especialmente fases high‑stakes (F4–F6), donde se esperaba que el agente pudiera **mejorar supervivencia** a medida que avanzan los episodios.

## Qué no se hace (por rigor)

- No se reescriben ni “corrigen” resultados ya cerrados (F0–F6).
- No se re‑etiquetan outputs canónicos existentes.
- Esta errata solo documenta el hallazgo para evitar overclaim en peer review.

## Qué sigue (roadmap)

Antes de ejecutar una fase adicional (p.ej. F7), se recomienda:

1) Corregir el ciclo de vida del agente (instanciar una vez por run).
2) Hacer una micro‑fase de validación (“repair validation”) que demuestre que:
   - el agente persiste entre episodios (no se reinstancia),
   - alguna señal de aprendizaje (p.ej. métricas o supervivencia) puede cambiar a través de episodios.
3) Re‑plantear calibraciones (por ejemplo `red_team_prob` o budget `B`) bajo el nuevo régimen.

## Referencias

- Código: `sim/runner.py` (función `run_experiment`).
- Control Tower: `results/v11/INDEX_SERIE_V11.md`
- Roadmap: `results/v11/MEGA_PLAN_EVALUACION_v11.md`

