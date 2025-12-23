# Índice / Control Tower — Serie v11 (TUI v4.1)

**Última actualización:** 2025-12-23  
**Estado:** F0–F5 cerrados y auditados (v11 cerrado).

Este archivo existe para evitar “saltos” entre documentos. Aquí está qué es canónico, qué es histórico, y el orden recomendado de lectura.

## 1) Estado rápido por fases
- **F0_baseline:** cerrado (sanity check/pipeline).
- **F1_highrisk:** cerrado.
- **F2_redteam:** cerrado (stress adversarial sintético; no min-max).
- **F3:** cerrado (ablación `pgf_mix` + comparación justa; preregistrado y auditado).
- **F4:** cerrado (stakes run-level `B=3` + CFR; preregistrado y auditado).
- **F5:** cerrado (high-stakes `B=3`, endpoint primario `episodes_completed`; ver `results/v11/data/f5_preregistered_report_v11.md` y `results/v11/F5/F5_CLOSURE_REPORT.md`).

El mapa operativo actualizado vive en `results/v11/MEGA_PLAN_EVALUACION_v11.md`.

## 2) Fuente de verdad (si solo lees 5 archivos)
- **Manifiesto canónico CSV (sha256):** `results/v11/CANONICAL_DATASET_v11.md`
- **Manifiesto JSON (sha256 por run):** `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`
- **Pipeline reproducible v11:** `results/v11/README_REPRODUCIBLE_v11.md`
- **Reporte global vigente (incluye F5):** `results/v11/data/stats_report_v11.md`
- **Cierre F3:** `results/v11/F3/F3_CLOSURE_REPORT.md`
- **Cierre F4:** `results/v11/F4/F4_CLOSURE_REPORT.md`
- **Cierre F5:** `results/v11/F5/F5_CLOSURE_REPORT.md`

## 3) Qué leer según tu objetivo
### A) “Quiero reproducir números / regenerar artefactos”
1) `results/v11/README_REPRODUCIBLE_v11.md`  
2) `results/v11/CANONICAL_DATASET_v11.md` + `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`  
3) `results/v11/data/stats_report_v11.md`

### B) “Quiero la narrativa científica (F0–F2)”
Estos documentos cubren F0–F2 (son válidos para esa parte, pero no sustituyen F3):
- `results/v11/RESUMEN_EJECUTIVO_SERIE_V11.md`
- `results/v11/INFORME_CIENTIFICO_SERIE_V11.md`
- `results/v11/PUBLICACION_SERIE_V11.md`
- `results/v11/ANEXO_TECNICO_v11.md` (definiciones operacionales importantes)

### C) “Quiero el paquete peer-review proof de F3”
- **Preregistro canónico:** `results/v11/F3/PREREGISTRO_F3_v11.md`
- **Reporte preregistrado:** `results/v11/data/f3_preregistered_report_v11.md`
- **Log de desviaciones:** `results/v11/F3/F3_DEVIATIONS_LOG_v11.md`
- **Cierre formal:** `results/v11/F3/F3_CLOSURE_REPORT.md`

### D) “Quiero saber qué es F4 (y qué falta correr)”
- **Preregistro (canónico):** `results/v11/F4/PREREGISTRO_F4_v11.md`
- **Adenda 01 (stakes run-level + CFR):** `results/v11/F4/F4_ADENDA_01.md`
- **Reporte preregistrado (endpoint CFR + Holm):** `results/v11/data/f4_preregistered_report_v11.md`
- **Log de desviaciones:** `results/v11/F4/F4_DEVIATIONS_LOG_v11.md`
- **Cierre formal:** `results/v11/F4/F4_CLOSURE_REPORT.md`

### E) “Quiero saber qué es F5 (qué se corrió y dónde está)”
- **Preregistro (canónico):** `results/v11/F5/PREREGISTRO_F5_v11.md`
- **Log de desviaciones:** `results/v11/F5/F5_DEVIATIONS_LOG_v11.md`
- **Runner:** `results/v11/F5/run_F5_v11.py`
- **Organizador (raw → canónico):** `scripts/organize_F5_results.py`
- **Análisis preregistrado (endpoint `episodes_completed` + Holm):** `scripts/f5_preregistered_analysis_v11.py`
- **Reporte preregistrado:** `results/v11/data/f5_preregistered_report_v11.md`
- **Cierre formal:** `results/v11/F5/F5_CLOSURE_REPORT.md`

## 4) Documentos “históricos” para no confundirse
- `results/v11/stats_report_v11.md` es solo un puntero (deprecated) al reporte vigente en `results/v11/data/stats_report_v11.md`.
- `results/v11/episodic_metrics_v11.md` es solo un puntero (deprecated) a `results/v11/data/episodic_metrics_v11.md`.
- `results/v11/F3_PREREGISTRATION.md` es un borrador; el preregistro canónico está en `results/v11/F3/PREREGISTRO_F3_v11.md`.
- `results/v11/ANALISIS_PERSONAL_F1_F2_v11.md` es cualitativo y pre-F3 (no canónico).

## 5) Versionado vs “local-only” (para no inflar el repo)
- La **fuente canónica** para análisis son los `*_episodes.csv` listados en `results/v11/CANONICAL_DATASET_v11.md`.
- Los JSON por run se tratan como **datos brutos**; el repo ignora por defecto `results/**/*.json` (ver `.gitignore`), pero pueden existir JSON “históricos” ya versionados. Para auditoría, se publican hashes en `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`.
- Carpetas `raw/` y `archived/` existen para trazabilidad operativa, pero no se usan como input canónico.

## 6) Qué falta para “cerrar v11” (resumen operativo)
- v11 está cerrado: F0-F5 ejecutados, organizados y auditados; stats, master y manifiestos están regenerados.
