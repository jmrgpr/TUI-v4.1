# PREREGISTRO_REPAIR_VALIDATION_v11.md
**Serie:** v11 (post-errata)  
**Fase:** RV1 — Repair Validation (runner agent lifecycle + state-shape robustness)  
**Fecha de congelación:** 2025-12-23 (America/Puerto_Rico)  
**Estado:** PRE-EJECUCIÓN (congelado antes de correr RV1)  

---

## 0) Propósito (NO es un experimento “de teoría”)
Esta fase es **ingeniería validada con preregistro**. Su objetivo es confirmar que, tras el fix, el sistema **aprende a lo largo del run** (agente persistente entre episodios) y que el pipeline es estable (sin crashes por dimensiones de estado “corto”).

**No** se harán claims sobre “TUI funciona/no funciona” en RV1. RV1 solo habilita fases futuras (F7+).

---

## 1) Contexto y motivación
Se identificó y corrigió un bug conceptual en `runner.py`: el agente se reinstanciaba dentro del loop de episodios, produciendo un régimen *episodic-reset* sin aprendizaje acumulado.  
Tras corregirlo (agente instanciado una vez por run), surgieron desajustes de dimensión en estados `coords_only` / estados cortos; se hizo robusto con padding/truncation.

Los resultados de F0–F6 quedan documentados como *episodic-reset* (ver `results/v11/ERRATA_RUNNER_AGENT_LIFECYCLE.md`). Esta fase RV1 valida que el nuevo régimen es consistente.

---

## 2) Objetivos específicos (testables)
### O1 — Persistencia real del agente por run (invariante)
- El objeto agente/modelo **no cambia** entre episodios del mismo run.
- Señales internas de aprendizaje (p.ej. buffer/timesteps/updates) **crecen** a través de episodios.

### O2 — Robustez de shape del estado (invariante)
- No hay errores por mismatch de dimensión.
- Cualquier estado “corto” se normaliza determinísticamente por padding/truncation.

### O3 — Señal mínima de aprendizaje (criterio “go/no-go”)
En un entorno sin budget (low-stakes), debe observarse **mejora intra-run** (del inicio al final) en métricas ambientales o supervivencia, al menos en la mayoría de seeds.

---

## 3) Diseño experimental (mínimo y controlado)
### 3.1 Entorno y configuración
- Escenario: **F2 / hostil** (el mismo de v11).
- Modo stakes: **LOW** (sin terminación por budget) para permitir 200 episodios completos y ver aprendizaje.
- Episodios por run: **200**
- Grids: **{16}** (para minimizar varianza en validación)
- Seeds: **{42, 101, 13}** (3 seeds)

### 3.2 Agentes / condiciones
Se corren 2 condiciones (mínimo necesario para validar persistencia en ambos caminos):
- **C (Control-DQN)**
- **S0 (Simbiosis con pgf_mix=0.0)**

> Nota: `S2 (pgf_mix=0.2)` es opcional. Solo se ejecuta si C y S0 pasan invariantes; si se corre, se marca como “extensión no necesaria” (no cambia el criterio PASS/FAIL).

---

## 4) Endpoints y métricas
### 4.1 Endpoints “invariantes” (primarios para RV1)
**I1 — Agent lifecycle invariant**
- Evidencia: `agent_id` constante por run (misma identidad en todos los episodios).
- Evidencia: contadores de aprendizaje (ej. `timesteps`, `updates`, `buffer_size`) no se reinician por episodio.

**I2 — State shape invariant**
- Evidencia: no hay excepciones por dimensiones.
- Evidencia: `state_dim_final` constante por run (tras padding/trunc).

### 4.2 Endpoints de señal mínima de aprendizaje (secundarios, pero “go/no-go”)
**E1 — Mejora intra-run en reward_env_total (o proxy ambiental equivalente)**
- Definición por run:
  - `early_mean` = media de reward_env_total en episodios 1–50
  - `late_mean`  = media de reward_env_total en episodios 151–200
  - `Δlearn = late_mean - early_mean`

**E2 — Reducción de starvation rate (si aplica)**
- `starv_rate_early` = % episodios con starvation en 1–50
- `starv_rate_late`  = % episodios con starvation en 151–200
- `Δstarv = starv_rate_late - starv_rate_early` (esperado <= 0)

---

## 5) Criterios de éxito (PASS/FAIL)
### PASS si se cumple todo:
1) **I1 PASS:** `agent_id` constante y contadores crecen (en 3/3 seeds para C y S0).  
2) **I2 PASS:** sin errores de shape; `state_dim_final` constante por run (3/3 seeds para C y S0).  
3) **Señal mínima (E1):** al menos **2/3 seeds** muestran `Δlearn ≥ +MESI_RV`, donde  
   - **MESI_RV = +5% del |early_mean|**, o **+0.5** (lo que sea mayor).  

### FAIL si:
- cualquier invariante falla, o
- E1 no muestra señal mínima en 2/3 seeds (se considera que el setup aún no está listo para F7+).

---

## 6) Exclusiones (objetivas)
Un run se excluye solo si ocurre cualquiera:
- crash técnico reproducible (traceback)
- NaNs/inf en métricas primarias
- no completa logging mínimo de invariantes (agent_id, state_dim_final)

---

## 7) Plan de análisis (sin p-values)
RV1 es validación de ingeniería:
- Reporte por seed con tabla: `early_mean`, `late_mean`, `Δlearn`, invariantes I1/I2.
- Conclusión binaria: PASS/FAIL para “GO a F7+”.

No se hará inferencia confirmatoria (p-values / Holm) en RV1.

---

## 8) Artefactos requeridos
Guardar en `results/v11/RV1/`:
- `rv1_run_metrics.csv` (por-run)
- `rv1_invariants.json` (agent_id, dims, counters por episodio o por ventana)
- `RV1_CLOSURE_REPORT.md`
- `RV1_DEVIATIONS_LOG_v11.md` (si aplica)
- hashes SHA256 de CSV/JSON canónicos

---

## 9) Stop rules
- STOP inmediato si I1 o I2 falla en el primer seed de cualquier condición.
- STOP si se detecta reinicio de buffer/timesteps por episodio.

---

## 10) Decisión posterior
- Si RV1 = PASS → ejecutar F7 (calibrar B / recuperar headroom en CFR) bajo el nuevo régimen.
- Si RV1 = FAIL → corregir runner/estado/logging; no ejecutar fases confirmatorias.

