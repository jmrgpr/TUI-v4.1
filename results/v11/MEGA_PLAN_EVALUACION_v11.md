# MEGA PLAN DE EVALUACION - Serie v11 (post F3 / pre F4)

Este documento es el **mapa de control** de la serie v11 y resume: (i) qué fases están cerradas, (ii) qué cambió con F3, y (iii) qué queda para cerrar v11 con F4.

Si necesitas una guía rápida de “qué leer primero”, ver: `results/v11/INDEX_SERIE_V11.md`.

## 1) Estado por fases (v11)
- [x] F0 (baseline): ejecutado y presente en dataset canónico.
- [x] F1 (alto riesgo): ejecutado y presente en dataset canónico.
- [x] F2 (stress test adversarial sintético): ejecutado con `red_team=True` y trazabilidad en JSON.
- [x] F3 (causal / ablations / comparación justa): **cerrado** y auditado (ver `results/v11/F3/F3_CLOSURE_REPORT.md`).
- [ ] F4 (stakes run-level + CFR): **preregistrado y congelado**, pero **no ejecutado aún** (ver `results/v11/F4/PREREGISTRO_F4_v11.md` y `results/v11/F4/F4_ADENDA_01.md`).

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
- [ ] Ejecutar F4 (runs) y producir outputs canónicos.
- [ ] Cierre formal F4 (closure report + stats/prueba preregistrada + manifiestos actualizados).
- [ ] (Opcional) Baseline “SOTA” (PPO/SAC/TD3 o Safe-RL) si el claim apunta a comparar con literatura; no es requisito para cerrar v11 si el claim es “nicho/robustez bajo stress”.

## 5) Qué significa “cerrar v11” (criterio operativo)
v11 queda cerrado cuando:
- F0–F3 están cerradas y auditables (ya lo están), y
- F4 queda **(a)** ejecutado y cerrado **o** **(b)** explícitamente diferido (con una nota formal en `results/v11/F4/F4_DEVIATIONS_LOG_v11.md` indicando “no ejecutado”).

En caso (a), el cierre mínimo de F4 debe incluir:
- Outputs canónicos en `results/v11/F4/F2_redteam/stk{L,H}/` (CSV versionados).
- Manifiestos regenerados: `results/v11/CANONICAL_DATASET_v11.md` y `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`.
- Master + stats regenerados: `results/master_results_clean.csv`, `results/v11/data/stats_report_v11.md`.
- Un `F4_CLOSURE_REPORT.md` citando artefactos exactos.
