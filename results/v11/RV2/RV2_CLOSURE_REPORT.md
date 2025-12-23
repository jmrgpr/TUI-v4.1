# RV2_CLOSURE_REPORT — Repair Validation (v11 post-errata)

**Serie:** v11 (post-errata)  
**Fase:** RV2 — Repair Validation (GO/NO-GO por invariantes)  
**Fecha de cierre:** YYYY-MM-DD (America/Puerto_Rico)  
**Estado:** DRAFT (completar al finalizar RV2)

---

## 1) Resumen ejecutivo

- **Objetivo:** validar que el sistema está listo para F7+ verificando invariantes I1/I2.
- **Resultado:** PASS / FAIL (completar).
- **Desviaciones:** ver `results/v11/RV2/RV2_DEVIATIONS_LOG_v11.md`.

---

## 2) Setup congelado (según preregistro)

- `episodes=200`, `grid=16`, `seeds={42,101,13}`
- `risk_scale=1.2`, `risk_level=high`, `red_team_prob=0.03`
- stakes LOW (sin budget)
- condiciones: C (Control-DQN), S0 (Simbiosis pgf_mix=0.0)

---

## 3) Invariantes (I1/I2)

Completar con evidencia de:
- `agent_id` constante por run
- contadores (`memory_size`, `_learn_steps`, `epsilon`) no reinician por episodio
- sin errores de dimensión; `state_dim` constante

Artefactos:
- `results/v11/RV2/rv2_invariants.json`
- `results/v11/RV2/rv2_run_metrics.csv`

---

## 4) Descriptivos (E1/E2)

Reportar (sin gating):
- `Δlearn` (early vs late)
- `Δstarv` (starvation early vs late)

---

## 5) Decisión GO/NO-GO

- PASS/GO → habilita F7+ bajo el nuevo régimen (agente persistente).
- FAIL/NO-GO → no ejecutar F7; corregir y repetir RV2.

