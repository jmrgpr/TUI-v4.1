# PREREGISTRO_TUI_PGF_v10

## Fase 3 – Ablation TUI/PGF con run_ablation_quick.py (Serie v10, TUI-v4.1)

**Fecha:** 2025-12-08
**Autor:** José M. Rivera García
**Repositorio:** TUI-v4.1

### Scripts clave
- scripts/experimentos_previos/run_ablation_quick.py
- sim/prototipo_rl_simbiosis.py
- evaluator_pgf.py
- scripts/consolidate_results.py

---

## 1. Contexto y motivación
Las Fases 0–2 demostraron que el RL puro y la regularización son robustos, mientras que el shaping PGF directo es perjudicial. PGF se reposiciona como métrica instrumental/evaluadora. Fase 3 pregunta: ¿qué pasa si PGF guía la decisión (TUI-style) vs tui_only?

## 2. Preguntas de investigación
- Q1: ¿PGF (tui_pgf_light/heavy) modifica sistemáticamente el comportamiento frente a tui_only al variar risk_scale?
- Q2: ¿Existe trade-off prudencia vs recompensa al activar PGF?
- Q3: ¿Diferencias consistentes entre tui_pgf_light y tui_pgf_heavy?
- Q4: ¿Robustez a la seed?

## 3. Diseño experimental
- Configs: tui_only, tui_pgf_light, tui_pgf_heavy (parámetros fijos)
- Seeds: [42, 123, 456]
- Risk_scales: [0.5, 1.0, 1.5, 2.0, 3.0]
- Episodios: 200 por corrida
- Output: CSVs por seed/config/risk_scale en results/sweep/fase2_instrumented/
- Consolidación: scripts/consolidate_results.py → CSV maestro + figuras

## 4. Variables y métricas
- Independientes: config, seed, risk_scale
- Dependientes: reward_total, eventos de riesgo, episodios seguros, etc.

## 5. Hipótesis
- H1: PGF reduce eventos graves en risk_scale altos
- H2: Trade-off prudencia vs reward
- H3: heavy < light en eventos graves, pero penaliza más reward
- H4: Robustez a la seed

## 6. Plan de análisis
- Consolidar resultados y comparar configs por seed/risk_scale
- Tablas y gráficos comparativos
- Evaluar H1–H4 cualitativamente
- Reporte: results/pgf_tui_ablation/REPORTE_TUI_PGF_v10.md

## 7. Criterios de éxito
- Ejecutar las 45 corridas
- Consolidar en CSV maestro + figuras
- Responder honestamente a H1–H4
- Claridad, reproducibilidad y conexión con teoría TUI/PGF

## 8. Comandos pre-definidos
- Smoke test: `python scripts/experimentos_previos/run_ablation_quick.py --test`
- Corrida completa: `python scripts/experimentos_previos/run_ablation_quick.py`
- Consolidación: `python scripts/consolidate_results.py`

---
*Preregistro generado automáticamente el 8/12/2025 por GitHub Copilot, integrando y validando el aporte recibido.*
