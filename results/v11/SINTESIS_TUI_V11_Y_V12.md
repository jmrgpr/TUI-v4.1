# Síntesis v11 → v12 (TUI v4.2): qué apoya, qué no, y qué sigue

**Fecha:** 2025-12-24  
**Serie:** v11 (TUI v4.1) + marco teórico de referencia TUI v4.2  
**Fuente de verdad (artefactos):** `results/v11/INDEX_SERIE_V11.md`

---

## 1) Qué “es” v11 (en una frase)

v11 es una serie **reproducible y preregistrada** que separa (i) desempeño ambiental (`reward_env_total`) de (ii) reward mezclado con shaping (`reward_total`), y termina con un cierre confirmatorio de robustez bajo *high-stakes* medido por **CFR** (F8).

---

## 2) Qué dice v11 sobre PGF/TUI (sin error de categoría)

### 2.1 PGF (teoría) ≠ `pgf_mix` (operacionalización v11)

- En TUI v4.2, el **PGF** formaliza una **ley local de aprendizaje** donde el cambio en inteligencia útil depende del producto de riesgo efectivo, sorpresa y alignment: ver `TUI/Teoria_Unificada_Inteligencia_v4.2.md` (§1.8; riesgo efectivo `P^{eff}_t`).
- En v11, `pgf_mix` es un **knob de reward shaping lineal** sobre `reward_total` (operacionalización parcial). Por diseño, puede cambiar `reward_total` sin cambiar `reward_env_total`.

**Implicación:** v11 puede **falsar/apoyar** la utilidad de `pgf_mix` *como implementación*, pero no “probar/refutar” PGF como principio general.

### 2.2 Resultado v11 sobre `pgf_mix`: efecto ambiental nulo bajo este protocolo (F3)

- F3 (preregistrado) muestra que la ablación `pgf_mix=0.2` vs `pgf_mix=0.0` en `reward_env_total` dio **Δ=0** con p≈0.99 (Holm=1): ver `results/v11/data/f3_preregistered_report_v11.md`.
- Esto descarta que **esta** implementación (shaping lineal) tenga un efecto causal detectable en la métrica ambiental primaria, bajo el protocolo v11.

Lectura compatible con TUI: sin un “riesgo efectivo” que cambie decisiones/gradientes (PGF), el shaping puede ser ignorado o no afectar la política medida por `reward_env_total`.

---

## 3) Qué hallazgo queda “cerrado sin dudas” en v11 (F8)

### 3.1 Hallazgo confirmatorio: robustez bajo high-stakes (CFR)

Tras resolver el ceiling effect (B=3) y documentar la errata del ciclo de vida del agente (F0–F6), se ejecutó un arco post‑errata:

- **F7**: calibración de budget `B*` para des‑saturar CFR (señal direccional; INCONCLUSIVE por Holm): `results/v11/data/f7_preregistered_report_v11.md`.
- **F8**: replicación **H1-only** (family m=1, sin Holm) con `B=40` y `red_team_prob=0.03`, que cierra el claim confirmatorio:
  - Control CFR=1.000 vs Simbiosis (`pgf_mix=0.0`) CFR=0.400; Δ=-0.600; p=1.19209e-07 ⇒ **PASS**.
  - Ver `results/v11/data/f8_preregistered_report_v11.md` y `results/v11/F8/F8_CLOSURE_REPORT.md`.

**Interpretación mínima (lo que sí puedes afirmar):**
Bajo esta definición operacional de *high-stakes* (budget `B=40` sobre catástrofes=starvation) y este régimen adversarial, **Simbiosis reduce de forma grande y estadísticamente clara** la tasa de fallos catastróficos vs Control.

### 3.2 Qué NO queda demostrado por v11

- No queda demostrado que `pgf_mix=0.2` sea útil (F3 y F7 no apoyan H3; F8 no evalúa H3).
- No queda demostrado que el efecto sea “universal” fuera del entorno/protocolo (solo que existe en este dominio).
- No queda demostrado mecanismo (por qué baja CFR): v11 es cierre causal/confirmatorio del efecto, no una descomposición mecanística.

---

## 4) Limitaciones críticas (ya documentadas)

- **Errata de lifecycle:** F0–F6 reflejan régimen *episodic-reset* (agente reinstanciado por episodio), lo que limita claims sobre “aprendizaje acumulado entre episodios”. Ver `results/v11/ERRATA_RUNNER_AGENT_LIFECYCLE.md`.
- **Riesgo “proxy” vs físico:** el *risk-effective* aquí es operacional (budget run-level), no riesgo físico irreversible; conecta con PGF por analogía experimental, no como validación de H1 en organismos.
- **Definición de catástrofe:** catástrofe=starvation es una elección operacional; si starvation está dominada por dinámica basal del entorno, limita la interpretación causal del “ataque”.

---

## 5) Qué procede para v12 (recomendación pragmática)

### 5.1 Objetivo v12 (elige uno como primario)

**Opción A (recomendada): Generalización del hallazgo de robustez (CFR)**
- Repetir el claim de F8 en ≥2 regímenes cercanos (p.ej. `B∈{30,50}` o `red_team_prob∈{0.02,0.04}`) con preregistro y calibración de headroom.
- Agregar un baseline *capacity-matched* para aislar “arquitectura vs tamaño”.

**Opción B: Probar predicciones PGF más directas (riesgo efectivo modula tasa de aprendizaje)**
- Diseñar un experimento que manipule `P^{eff}` de forma monotónica y mida pendientes (learning curves) o métricas F/T, como sugieren predicciones PGF (ver `TUI/Teoria_Inteligencia_Aplicada_IA_v4.2.md` P‑PGF‑1).

### 5.2 Reglas de diseño (para que v12 sea “peer-review proof”)

- Cambiar **una palanca causal** por fase (evita “monstruos”).
- Definir MESI y endpoints primarios de cola/seguridad si se van a usar para claims (no solo reportarlos).
- Mantener la disciplina de v11: preregistro → pipeline canónico → análisis preregistrado → cierre.

---

## 6) Lectura recomendada (orden)

1) `results/v11/INDEX_SERIE_V11.md`  
2) `results/v11/data/f3_preregistered_report_v11.md` (qué pasa con `pgf_mix` y comparación justa)  
3) `results/v11/ERRATA_RUNNER_AGENT_LIFECYCLE.md` + `results/v11/RV2/RV2_CLOSURE_REPORT.md`  
4) `results/v11/data/f8_preregistered_report_v11.md` (veredicto high-stakes CFR)  
5) `TUI/Teoria_Unificada_Inteligencia_v4.2.md` (§1.8 PGF) y `TUI/Teoria_Inteligencia_Aplicada_IA_v4.2.md` (Camino C + predicciones PGF)

