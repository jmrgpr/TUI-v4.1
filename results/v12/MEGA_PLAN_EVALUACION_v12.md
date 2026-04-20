# MEGA PLAN DE EVALUACION - Serie v12 (diseño en curso)

Este documento es el **mapa de control** de la serie v12. Su objetivo es mantener el rigor “peer-review proof” replicando la disciplina de v11: preregistro → datos canónicos → análisis preregistrado → cierre formal, con trazabilidad por artefactos.

Contexto:
- v11 ya está cerrado (ver `results/v11/INDEX_SERIE_V11.md` y `results/v11/MEGA_PLAN_EVALUACION_v11.md`).
- v12 nace para (A) **generalizar** el hallazgo confirmatorio de robustez CFR y (B) **testear PGF directo** (P‑PGF‑1) sin mezclar `pgf_mix` con el principio PGF.

## 0) Principios invariantes (reglas de rigor)

1) **Evitar error de categoría:** `pgf_mix` es un knob (shaping lineal). PGF es una hipótesis causal sobre dinámica local de aprendizaje. v12 debe declarar explícitamente cuál de los dos está siendo evaluado.
2) **Una palanca causal por fase confirmatoria:** cada fase confirmatoria cambia **solo 1 dial** (p.ej. `B` o `red_team_prob`) respecto a la fase anterior.
3) **Headroom obligatorio en endpoints de cola/seguridad:** antes de claim confirmatorio con CFR, calibrar para que el control no esté saturado (objetivo operativo: `CFR_control` en ~0.3–0.8).
4) **Unidad primaria = run (seed × grid × grupo):** evitar pseudo-replicación por episodio; episodios se usan para métricas intra-run (descriptivo o preregistrado si aplica).
5) **Separar confirmatorio vs exploratorio:** cada fase debe tener family confirmatoria explícita (m, corrección, MESI) y un “espacio exploratorio” separado.
6) **Mantener constante A\*_t / proxies de alineación cuando se testea PGF:** en PGF, el término de aprendizaje útil multiplica `P^{eff}_t · S_t · (A^*_t · IPG_t)`. Si no se fija (o controla) `A^*_t`, el test no es atribuible a `P^{eff}_t`.

## 1) Objetivo v12 (en dos arcos)

### v12-A (primero): generalizar el hallazgo CFR (robustez high-stakes)

Claim mínimo/publicable: bajo una definición operacional de high-stakes (budget run-level) y adversarialidad fija, **Simbiosis reduce CFR vs Control** (sin afirmar universalidad ni mecanismo).

Estrategia: repetir el claim tipo F8 en ≥2 regímenes cercanos, cambiando una sola palanca por fase (p.ej. solo `B` o solo `red_team_prob`).

### v12-B (después): test PGF directo (P‑PGF‑1)

Predicción PGF a testear: dos grupos con igual “sorpresa” `S_t` pero distinto riesgo efectivo `P^{eff}_t` → el de mayor `P^{eff}_t` mejora F/T más rápido (pendiente).

Fuente teórica:
- `TUI/Teoria_Unificada_Inteligencia_v4.2.md` (ley local PGF).
- `TUI/Teoria_Inteligencia_Aplicada_IA_v4.2.md` (P‑PGF‑1: protocolo + falsación).

## 2) Estado por fases (v12)

- [ ] F0_baseline (sanity/pipeline bajo riesgo bajo; sin claims fuertes).
- [ ] F1_highrisk (baseline alto riesgo sin ataque; control de instrumentación).
- [ ] F2_redteam (baseline adversarial; dataset base para v12-A).
- [ ] F3 (piloto de headroom para CFR: seleccionar régimen con `CFR_control` no saturado).
- [ ] F4 (confirmatorio CFR: H1-only, m=1; replicación tipo F8 con headroom).
- [ ] F5 (generalización CFR: mismo diseño, cambiar 1 palanca causal).
- [ ] F6 (PGF directo: P‑PGF‑1; slope/pendiente en F/T con test de permutación).

## 3) Resumen de diseño por fase (definición operativa)

### F0_baseline (no confirmatoria)

Objetivo:
- Validar que la instrumentación y el pipeline producen outputs canónicos auditables.
- Establecer referencia “riesgo bajo” (no adversarial).

Resultado esperado:
- GO técnico (datos completos, columnas correctas, sin fallos).

### F1_highrisk (no confirmatoria)

Objetivo:
- Establecer referencia en `risk_level=high` sin red team (control de estabilidad del entorno).

Resultado esperado:
- GO técnico + descriptivos (no claims confirmatorios).

### F2_redteam (no confirmatoria)

Objetivo:
- Establecer baseline adversarial (stress test) sobre el cual se construyen fases high-stakes/CFR.

Resultado esperado:
- Dataset base + trazabilidad (no claims confirmatorios por sí sola).

### F3 (piloto headroom CFR; no confirmatorio)

Objetivo:
- Seleccionar un régimen (p.ej. `B` y/o `red_team_prob`) que deje **headroom** para CFR.

Regla recomendada (a preregistrar):
- Elegir el régimen que deje `CFR_control` dentro de [0.3, 0.8] (o el más cercano si no existe), con empate → régimen más conservador (menor severidad).

Salida esperada:
- `results/v12/data/f3_pilot_selection_v12.md` + tabla `*.csv` con CFR por candidato (pilot).

### F4 (confirmatorio CFR; H1-only)

Objetivo:
- Replicar el claim tipo F8 en el régimen seleccionado en F3.

Recomendación para mantener “sin dudas”:
- Family confirmatoria m=1 (sin Holm), H1-only (S0-H vs C-H).
- Mantener pairing por (seed, grid) y usar test pareado preregistrado (p.ej. McNemar exact).
- MESI_CFR explícito (reusar 0.20 salvo razón fuerte para cambiar).

Salida esperada:
- `results/v12/data/f4_preregistered_report_v12.md` + `F4_CLOSURE_REPORT.md` citando artefactos exactos.

### F5 (confirmatorio CFR; generalización)

Objetivo:
- Generalizar el hallazgo cambiando **una sola** palanca causal (ejemplos):
  - Mantener `red_team_prob` fijo y variar `B` (p.ej. 30 vs 40 vs 50 en fases separadas), o
  - Mantener `B` fijo y variar `red_team_prob` (p.ej. 0.02 vs 0.03 vs 0.04).

Regla de rigor:
- Una fase = un solo cambio = una sola H1 primaria.

### F6 (PGF directo; P‑PGF‑1)

Objetivo:
- Testear causalmente el efecto de `P^{eff}_t` sobre la pendiente de mejora (F/T).

Diseño mínimo (a preregistrar):
- Igualar `S_t` (misma dificultad/distribución) entre grupos.
- Mantener constante (o controlar) `A^*_t` y proxies de alineación operativa.
- Manipular `P^{eff}_t` de forma monótona (alto vs bajo) sin introducir diales extra.
- Medir pendiente de una métrica F/T operacional (o proxy explícito si F/T no existe aún en el entorno) durante ~1000 episodios.
- Falsación: si pendientes indistinguibles (p>0.05 en permutación) → no se apoya PGF bajo esa operacionalización.

## 4) Artefactos canónicos v12 (fuente de verdad)

Estos artefactos se consideran fuente de verdad una vez generados:
- Manifiesto canónico CSV (sha256): `results/v12/CANONICAL_DATASET_v12.md`
- Manifiesto extendido JSON (sha256 por run): `results/v12/CANONICAL_DATASET_EXTENDED_JSON.md`
- Pipeline reproducible: `results/v12/README_REPRODUCIBLE_v12.md`
- Reporte estadístico global vigente: `results/v12/data/stats_report_v12.md`
- Control tower: `results/v12/INDEX_SERIE_V12.md`

## 5) Checklist “phase closed” (plantilla)

Una fase queda cerrada cuando (mínimo):
- Preregistro congelado (versión + fecha) y deviations log actualizado.
- Outputs canónicos (CSV `*_episodes.csv`) versionados en la carpeta de fase.
- JSON no versionado; hashes publicados en manifiesto extendido.
- Reporte preregistrado publicado en `results/v12/data/` (si aplica).
- Closure report citando artefactos exactos (paths/hashes).

