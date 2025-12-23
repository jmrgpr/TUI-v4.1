# PREREGISTRO_RV2_v11 — Repair Validation (GO/NO-GO por invariantes)

**Serie:** v11 (post-errata)  
**Fase:** RV2 — Repair Validation (invariantes como gating)  
**Fecha de congelación:** 2025-12-23 (America/Puerto_Rico)  
**Estado:** PRE-EJECUCIÓN (congelado antes de correr RV2)  

---

## 0) Propósito
RV2 es una fase de **ingeniería preregistrada**. Su objetivo es confirmar que, tras el fix del ciclo de vida del agente (persistencia por run) y la robustez de shape de estado DQN, el sistema es lo suficientemente estable para re-intentar fases confirmatorias (F7+).

RV2 **no** hace claims sobre la teoría TUI/PGF.

---

## 1) Diferencia clave vs RV1

RV1 cerró FAIL porque el criterio E1 (“señal mínima de mejora intra-run en reward”) no se observó, pese a que las invariantes I1/I2 fueron PASS.

En RV2, el criterio GO/NO-GO se basa **solo en invariantes** (I1/I2). E1/E2 se reportan como descriptivos.

---

## 2) Setup congelado

### 2.1 Entorno (fijo)
- `grid_size = 16`
- `episodes = 200`
- `seeds = {42, 101, 13}`
- `stakes_mode = "low"` (sin budget)
- `risk_scale = 1.2`
- `risk_level = "high"`
- `red_team = True`
- `red_team_prob = 0.03`
- `red_team_impact = -1.0`
- `red_team_move_tripwire_prob = 0.4`
- `red_team_add_shock_prob = 0.3`
- `red_team_block_prob = 0.3`
- `state_mode = "abstract"`

### 2.2 Condiciones (2)
- **C (Control-DQN):** `use_dqn=True`, `use_pgf=False`, `pgf_mix=0.0`
- **S0 (Simbiosis):** `use_dqn=True`, `use_pgf=True`, `pgf_mix=0.0`

---

## 3) Endpoints

### 3.1 Invariantes (confirmatorios / gating)

**I1 — Agent lifecycle invariant**
- `agent_id` constante por run (misma identidad en todos los episodios).
- contadores DQN (`memory_size`, `_learn_steps`, `epsilon`) no se reinician por episodio (tendencia no decreciente global).

**I2 — State shape invariant**
- sin excepciones por mismatch de dimensión.
- `state_dim` constante (instrumentación del runner).

### 3.2 Descriptivos (no gating)
Se reportan por seed y condición:
- E1: `Δlearn = late_mean(total_rewards[151–200]) − early_mean(total_rewards[1–50])`
- E2: `Δstarv = starv_rate_late − starv_rate_early`

---

## 4) Criterio GO/NO-GO (PASS/FAIL)

**PASS/GO** si:
- I1 PASS en **3/3 seeds** para **C** y **S0**, y
- I2 PASS en **3/3 seeds** para **C** y **S0**.

**FAIL/NO-GO** si falla cualquier invariante (y se aplica STOP temprano).

---

## 5) Stop rules

- STOP inmediato si I1 o I2 falla en el primer seed de cualquier condición.

---

## 6) Artefactos requeridos

Guardar en `results/v11/RV2/`:
- `rv2_run_metrics.csv`
- `rv2_invariants.json`
- `RV2_CLOSURE_REPORT.md`
- `RV2_DEVIATIONS_LOG_v11.md` (si aplica)

