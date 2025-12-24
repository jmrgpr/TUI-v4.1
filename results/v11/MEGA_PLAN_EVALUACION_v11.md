# MEGA PLAN DE EVALUACION - Serie v11 (post F8; cierre completado)

Este documento es el **mapa de control** de la serie v11 y resume: (i) qué fases están cerradas, (ii) qué cambió con F3/F4/F5, y (iii) la extensión F6 (diseñada para resolver el ceiling effect de CFR sin reabrir F4/F5).

**ERRATA (post‑cierre):** se documentó una limitación de implementación sobre el ciclo de vida del agente (reinicio por episodio) que puede afectar interpretaciones de “aprendizaje entre episodios”. Ver `results/v11/ERRATA_RUNNER_AGENT_LIFECYCLE.md`.

Si necesitas una guía rápida de “qué leer primero”, ver: `results/v11/INDEX_SERIE_V11.md`.

## 1) Estado por fases (v11)
- [x] F0 (baseline): ejecutado y presente en dataset canónico.
- [x] F1 (alto riesgo): ejecutado y presente en dataset canónico.
- [x] F2 (stress test adversarial sintético): ejecutado con `red_team=True` y trazabilidad en JSON.
- [x] F3 (causal / ablations / comparación justa): **cerrado** y auditado (ver `results/v11/F3/F3_CLOSURE_REPORT.md`).
- [x] F4 (stakes run-level + CFR): ejecutado, auditado y con cierre formal (ver `results/v11/F4/F4_CLOSURE_REPORT.md`).
- [x] F5 (high-stakes `B=3`, endpoint `episodes_completed`): ejecutado, auditado y con cierre formal (ver `results/v11/F5/F5_CLOSURE_REPORT.md`).
- [x] F6 (calibración `red_team_prob` para CFR con `B=3`): ejecutado, auditado y con cierre formal (ver `results/v11/F6/F6_CLOSURE_REPORT.md`).
- [x] F7 (budget calibration `B` → `B*` para des‑saturar CFR): ejecutado y cerrado (ver `results/v11/F7/F7_CLOSURE_REPORT.md`).
- [x] F8 (replicación H1-only para cierre de CFR sin Holm): ejecutado y cerrado (**PASS**) (ver `results/v11/F8/F8_CLOSURE_REPORT.md` y `results/v11/data/f8_preregistered_report_v11.md`).

## 2) Qué cambió con los hallazgos nuevos (impacto sobre el plan)
Cambios que afectan directamente al MEGA_PLAN original (post-F2):

1) **PGF ≠ `pgf_mix` (error de categoría evitado)**
- F3 evalúa `pgf_mix` como **operacionalización** (reward shaping lineal). No “prueba/refuta” el principio teórico PGF.
- Hallazgo clave: `pgf_mix` altera `reward_total` (shaping activo), pero **no altera `reward_env_total`** en el protocolo v11 (trayectorias ambientales invariantes por pares seed×grid×condición). Esto se documenta en `results/v11/F3/F3_CLOSURE_REPORT.md`.

2) **El hallazgo principal de v11 ya no es “mejor reward promedio”, sino “trade-off eficiencia vs robustez”**
- En F1 (sin ataque) aparece un coste/ineficiencia relativa frente a `control`.
- En F2 (con stress adversarial), Simbiosis/TUI muestra señales de ventaja operativa bajo ataque (dependiendo de métrica, ver F3 preregistrado).

3) **F4 se redefinió**
- El MEGA_PLAN post-F2 decía “alineación u_proxy vs u_humans”.
- Con F3, el siguiente test falsable y limpio es **subir stakes/riesgo efectivo** sin introducir 5 mecanismos nuevos: F4 fija `F2_redteam` y define stakes **a nivel run** con un presupuesto de catástrofes `B=3`, usando **CFR** como endpoint primario (ver `results/v11/F4/PREREGISTRO_F4_v11.md`).

4) **“Robustez” ya tiene definiciones operacionales**
- “Robustez-distractor” (operacional, no general) quedó definida formalmente en `results/v11/ANEXO_TECNICO_v11.md`.
- F3 ya incluye métricas de cola (`CVaR05_env`, `max_drawdown_env`) como secundarias/exploratorias (ver `results/v11/F3/PREREGISTRO_F3_v11.md`).
- F4 eleva la robustez a **endpoint primario** vía CFR (budget-exhaustion).

5) **F5 se crea para resolver el “ceiling effect” de F4**
- En F4, con `B=3`, el endpoint confirmatorio CFR saturó (CFR=1.0 en todos los grupos), dejando H1/H2/H3 inconclusas.
- F5 mantiene high-stakes `B=3` (misma definición de catástrofe) y cambia el endpoint confirmatorio a `episodes_completed` (tiempo-hasta-agotar-budget).
- Ver: `results/v11/F4/F4_CLOSURE_REPORT.md` y `results/v11/F5/PREREGISTRO_F5_v11.md`.

6) **Resultado de F5 (y qué deja resuelto vs abierto)**
- F5 evitó el ceiling effect del endpoint CFR, pero mantuvo CFR=1 como secundario (budget agotado en todos los runs).
- Endpoint primario `episodes_completed` mostró diferencias pooled: S0-H vs C-H mean diff=4.5 episodios (p Holm=0.046875), pero el punto estimado no supera MESI_EC=5, por lo que la decisión confirmatoria queda **INCONCLUSIVE** (ver `results/v11/data/f5_preregistered_report_v11.md`).
- `pgf_mix=0.2` vs `pgf_mix=0.0` no mostró efecto en el endpoint primario (diff=0; ver H3 en `results/v11/data/f5_preregistered_report_v11.md`).

7) **F6 (por qué existe y qué intenta resolver)**
- F4 mostró ceiling effect con CFR bajo `B=3` y `red_team_prob=0.1` (CFR≈1.0 en todos los grupos).
- F5 evitó el ceiling effect cambiando endpoint a `episodes_completed`, pero la decisión confirmatoria quedó inconclusa por MESI (Δ=4.5 < 5).
- F6 vuelve a CFR como endpoint primario, pero calibra **solo** `red_team_prob` mediante un piloto preregistrado para seleccionar un `p*` tal que el CFR de Control quede ~0.5 (evita saturación y deja espacio de discriminación).
- Ver preregistro: `results/v11/F6/PREREGISTRO_F6_v11.md`.

8) **Resultado de F6**
- El piloto no logró evitar saturación: `CFR_control(p)=1.0` para `{0.03, 0.05, 0.07}`, por lo que `p*` quedó en `0.03` por la regla de desempate (ver `results/v11/data/f6_pilot_selection_v11.md`).
- En confirmatorio, CFR volvió a saturar en `1.0` en todos los grupos (C-H, S0-H, S2-H) ⇒ H1/H3 **INCONCLUSIVE** (ver `results/v11/data/f6_preregistered_report_v11.md`).
- Señal descriptiva: `episodes_completed` es mayor en Simbiosis que en Control, pero no es claim confirmatorio en F6 (ver `results/v11/F6/F6_CLOSURE_REPORT.md`).

 9) **ERRATA (ciclo de vida del agente) y ajuste del roadmap**
- Se detectó post‑cierre que `sim/runner.py` instanciaba el agente dentro del loop de episodios (`for ep in range(episodes)`), lo que implica un régimen tipo **episodic‑reset** (sin aprendizaje acumulado entre episodios).
- Esto **no invalida** la auditabilidad de los artefactos (CSV/hashes), pero **sí limita** claims sobre “aprendizaje a través de 200 episodios”.
- Roadmap ajustado (hecho): se corrigió el runner; RV1 cerró **FAIL/NO-GO**; RV2 cerró **PASS/GO**; F7 se ejecutó bajo agente persistente; F8 se ejecutó como replicación H1-only y cerró **PASS** (CFR) sin Holm.

## 3) Artefactos canónicos (fuente de verdad)
- Dataset canónico (CSV + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto de JSON (sha256 por run): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`
- Pipeline reproducible (master + stats + manifiestos): `results/v11/README_REPRODUCIBLE_v11.md`
- Reporte estadístico global vigente: `results/v11/data/stats_report_v11.md`
- Cierre F2: `results/v11/F2_CLOSURE_REPORT.md`
- Paquete F3 (preregistro + reporte + cierre):
  - `results/v11/F3/PREREGISTRO_F3_v11.md`
  - `results/v11/data/f3_preregistered_report_v11.md`
  - `results/v11/F3/F3_CLOSURE_REPORT.md`

## 4) Checklist (cerrado vs pendiente)
- [x] Dataset canónico con hashes (incluye F3): `results/v11/CANONICAL_DATASET_v11.md`.
- [x] Reporte global vigente (incluye F3): `results/v11/data/stats_report_v11.md`.
- [x] Preregistro + cierre F3 “peer-review proof”.
- [x] Definiciones operacionales de métricas clave (shaping, robustez-distractor, colas): `results/v11/ANEXO_TECNICO_v11.md`, `results/v11/F3/PREREGISTRO_F3_v11.md`.
- [x] Ejecutar F4 (runs) y producir outputs canónicos.
- [x] Cierre formal F4 (closure report + análisis preregistrado + manifiestos/stats actualizados).
- [x] Ejecutar F5 (runs) y producir outputs canónicos.
- [x] Cierre formal F5 (closure report + análisis preregistrado + manifiestos/stats actualizados).
- [x] Ejecutar F6 (piloto → p* → confirmatorio) y producir outputs canónicos.
- [x] Cierre formal F6 (closure report + análisis preregistrado + manifiestos/stats actualizados).
- [x] RV1 (Repair Validation post‑errata): ejecutado y cerrado (**FAIL/NO-GO**) — invariantes OK, pero sin señal mínima de mejora intra-run en reward (ver `results/v11/RV1/RV1_CLOSURE_REPORT.md`).
- [x] RV2 (Repair Validation post‑errata; invariantes como gating): ejecutado y cerrado (**PASS/GO**) (ver `results/v11/RV2/RV2_CLOSURE_REPORT.md`).
- [x] F7 (budget calibration `B` → `B*` para des‑saturar CFR): ejecutado y cerrado (ver `results/v11/F7/F7_CLOSURE_REPORT.md`).
- [x] F8 (replicación H1-only para cierre CFR sin Holm): ejecutado y cerrado (**PASS**) (ver `results/v11/F8/F8_CLOSURE_REPORT.md` y `results/v11/data/f8_preregistered_report_v11.md`).
- [ ] (Opcional) Baseline “SOTA” (PPO/SAC/TD3 o Safe-RL) si el claim apunta a comparar con literatura; no es requisito para cerrar v11 si el claim es “nicho/robustez bajo stress”.

## 5) Qué significa “cerrar v11” (criterio operativo)
v11 queda cerrado cuando:
- F0–F4 están cerradas y auditables (ya lo están), y
- F5 queda **(a)** ejecutado y cerrado **o** **(b)** explícitamente diferido (con una nota formal en `results/v11/F5/F5_DEVIATIONS_LOG_v11.md` indicando “no ejecutado”).

Para un cierre “sin dudas” del arco **high-stakes CFR** (post‑errata):
- F7 deja headroom real (B*), pero el veredicto puede quedar INCONCLUSIVE por potencia/multiplicidad.
- F8 existe para cerrar **H1** (S0-H vs C-H) como claim confirmatorio H1-only; ya está ejecutado y cerrado (**PASS**) (ver `results/v11/F8/F8_CLOSURE_REPORT.md`).

En caso (a), el cierre mínimo de F4 debe incluir:
- Outputs canónicos en `results/v11/F4/F2_redteam/stk{L,H}/` (CSV versionados).
- Manifiestos regenerados: `results/v11/CANONICAL_DATASET_v11.md` y `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`.
- Master + stats regenerados: `results/master_results_clean.csv`, `results/v11/data/stats_report_v11.md`.
- Un `F4_CLOSURE_REPORT.md` citando artefactos exactos.

En caso (a), el cierre mínimo de F5 debe incluir:
- Outputs canónicos en `results/v11/F5/F2_redteam/stkH/` (CSV versionados).
- Reporte preregistrado F5 en `results/v11/data/` y un `F5_CLOSURE_REPORT.md` citando artefactos exactos.
- Manifiestos y stats regenerados (master + reportes + hashes).

Estado actual: F0–F8 cerrados y auditables; errata documentada; RV1 cerrado (FAIL/NO-GO); RV2 cerrado (PASS/GO).
