# Resumen Ejecutivo: Serie v11 (F0–F8 + RV1/RV2)

> Última actualización: 2025-12-24. Guía general: `results/v11/INDEX_SERIE_V11.md`.

## Objetivo (v11)
Evaluar agentes en (i) referencia, (ii) alto riesgo, (iii) estrés adversarial, y luego cerrar preguntas causales sobre `pgf_mix` (shaping) y robustez bajo stakes, con trazabilidad reproducible (CSV canónicos + hashes; JSON auditados por hashes).

## Fuente canónica (siempre)
- Dataset canónico (CSV + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto extendido (JSON + sha256): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`
- Reporte global vigente (descriptivo): `results/v11/data/stats_report_v11.md`
- Paquetes preregistrados: `results/v11/data/f3_preregistered_report_v11.md`, `results/v11/data/f7_preregistered_report_v11.md`, `results/v11/data/f8_preregistered_report_v11.md`

## Hallazgos clave (confirmatorios / preregistrados)
### 1) `pgf_mix` como shaping lineal no muestra efecto ambiental (F3)
- La ablación `pgf_mix=0.2` vs `pgf_mix=0.0` en `reward_env_total` arrojó Δ=0 con p≈0.99 (Holm=1): no hay evidencia de que `pgf_mix` cambie desempeño ambiental bajo este protocolo. Ver `results/v11/data/f3_preregistered_report_v11.md`.
- Comparación “justa” (Simbiosis con `pgf_mix=0.0`) sugiere trade-off: pierde vs `control` en F1 y gana vs `control` en F2 (ver mismo reporte).

### 2) Robustez bajo stakes high-stakes (post‑errata): Simbiosis reduce fallos catastróficos (F8)
- F7 calibró el budget (`B*`) para des‑saturar CFR y mostró señal direccional pero quedó INCONCLUSIVE por Holm (ver `results/v11/data/f7_preregistered_report_v11.md`).
- F8 replicó H1-only (sin Holm; family m=1) con `B=40` y `red_team_prob=0.03` y cerró **PASS**:
  - `CFR`: Control = 1.000 vs Simbiosis (m=0.0) = 0.400; Δ=-0.600; p=1.19209e-07. Ver `results/v11/data/f8_preregistered_report_v11.md`.

## Nota post‑cierre (muy importante)
Se documentó una errata de implementación: en `sim/runner.py` el agente se reinstanciaba por episodio, lo que limita interpretaciones de aprendizaje acumulado entre episodios en F0–F6. Ver `results/v11/ERRATA_RUNNER_AGENT_LIFECYCLE.md`. Tras el fix, RV2 cerró PASS/GO y habilitó F7/F8 bajo agente persistente.

## Estado
La serie v11 queda cerrada y auditada (F0–F8 + errata + RV1/RV2). El “veredicto sin dudas” para high-stakes CFR está en F8 (PASS).
