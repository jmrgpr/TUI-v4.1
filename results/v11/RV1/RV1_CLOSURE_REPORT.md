# RV1_CLOSURE_REPORT — Repair Validation (v11 post-errata)

**Serie:** v11 (post-errata)  
**Fase:** RV1 — Repair Validation  
**Fecha de cierre:** 2025-12-23 (America/Puerto_Rico)  
**Estado:** FAIL

## 1) Resumen ejecutivo

- Objetivo: validar persistencia del agente por run + robustez de shape + señal mínima de aprendizaje intra-run.
- Decisión: **NO-GO (FAIL)**.
- Invariantes: I1(all)=PASS, I2(all)=PASS.
- Señal mínima E1 (>=2/3 seeds por condición): C=0/3, S0=0/3 ⇒ FAIL.

## 2) Setup congelado (según preregistro)

- episodes=200, grid=16, seeds=[42, 101, 13]
- risk_scale=1.2, risk_level=high, red_team_prob=0.03
- stakes=LOW (sin budget)
- condiciones: C (Control-DQN), S0 (Simbiosis pgf_mix=0.0)

## 3) Artefactos

- Metrics (canónico): `results/v11/RV1/rv1_run_metrics.csv` (sha256=2da042871fb10b42845432b1995f7ca46a2653a4bcd6e920f2f314236846b8e0)
- Invariants (canónico): `results/v11/RV1/rv1_invariants.json` (sha256=e5ac61ece84b4c024344f60ce1221af45e3928368746927531d383bf6689de57)
- Raw (local-only): `results/v11/RV1/raw`

## 4) Siguiente paso

- Si PASS: se habilita re-intentar una fase confirmatoria (F7+) bajo el nuevo régimen (agente persistente).
- Si FAIL: no ejecutar F7; corregir instrumentación/runner y repetir RV1.
