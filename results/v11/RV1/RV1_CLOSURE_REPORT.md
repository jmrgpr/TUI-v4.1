# RV1_CLOSURE_REPORT — Repair Validation (v11 post-errata)

**Serie:** v11 (post-errata)  
**Fase:** RV1 — Repair Validation  
**Fecha de cierre:** YYYY-MM-DD (America/Puerto_Rico)  
**Estado:** DRAFT (completar al finalizar RV1)

---

## 1) Resumen ejecutivo

- **Objetivo:** validar que el fix de `sim/runner.py` habilita aprendizaje acumulativo por run (agente persistente) y robustez de shapes DQN antes de ejecutar fases confirmatorias (F7+).
- **Resultado:** PASS / FAIL (completar).
- **Stop rules activadas:** SI / NO (completar).
- **Desviaciones:** ver `results/v11/RV1/RV1_DEVIATIONS_LOG_v11.md`.

---

## 2) Setup congelado (según preregistro)

- Episodios por run: 200
- Grid: 16
- Seeds: {42, 101, 13}
- Stakes: LOW (sin budget)
- Condiciones: C (Control-DQN) y S0 (Simbiosis pgf_mix=0.0)

---

## 3) Invariantes (I1/I2)

Completar con evidencia de:
- `agent_id` constante por run
- contadores que crecen (p.ej. buffer/timesteps/updates)
- ausencia de errores de dimensión
- `state_dim_final` constante

Referencias:
- `results/v11/RV1/rv1_invariants.json` (cuando exista)

---

## 4) Señal mínima de aprendizaje (E1/E2)

Completar tabla por seed y condición:
- early_mean (1–50)
- late_mean (151–200)
- Δlearn
- starvation early/late (si aplica)

Referencias:
- `results/v11/RV1/rv1_run_metrics.csv` (cuando exista)

---

## 5) Decisión GO/NO-GO

- **PASS/GO** (si aplica): habilita ejecutar F7 (calibración de B / headroom de CFR) bajo el nuevo régimen.
- **FAIL/NO-GO** (si aplica): no ejecutar F7; corregir instrumentación/runner y repetir RV1.

