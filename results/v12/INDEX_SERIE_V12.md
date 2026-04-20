# Índice / Control Tower — Serie v12 (TUI v4.1)

**Última actualización:** 2025-12-24  
**Estado:** diseño en curso (sin fases ejecutadas aún)

Este archivo existe para evitar saltos entre documentos. Indica qué es canónico, el orden recomendado de lectura y el estado por fase.

## 1) Estado rápido por fases
- **F0_baseline:** pendiente.
- **F1_highrisk:** pendiente.
- **F2_redteam:** pendiente.
- **F3:** pendiente (piloto headroom CFR).
- **F4:** pendiente (confirmatorio CFR, H1-only).
- **F5:** pendiente (generalización CFR).
- **F6:** pendiente (PGF directo, P‑PGF‑1).

Mapa operativo: `results/v12/MEGA_PLAN_EVALUACION_v12.md`.

## 2) Fuente de verdad (cuando exista)
- **Manifiesto canónico CSV (sha256):** `results/v12/CANONICAL_DATASET_v12.md`
- **Manifiesto extendido JSON (sha256 por run):** `results/v12/CANONICAL_DATASET_EXTENDED_JSON.md`
- **Pipeline reproducible v12:** `results/v12/README_REPRODUCIBLE_v12.md`
- **Reporte global vigente:** `results/v12/data/stats_report_v12.md`

## 3) Orden recomendado de lectura
1) `results/v12/MEGA_PLAN_EVALUACION_v12.md`
2) `results/v11/SINTESIS_TUI_V11_Y_V12.md` (criterio de diseño y alcance)
3) `TUI/Teoria_Unificada_Inteligencia_v4.2.md` + `TUI/Teoria_Inteligencia_Aplicada_IA_v4.2.md` (PGF/P‑PGF‑1)

## 4) Versionado vs “local-only”
- La fuente canónica para análisis son CSV `*_episodes.csv` versionados bajo `results/v12/`.
- Los JSON por run se tratan como datos brutos: no se versionan; se publican hashes en el manifiesto extendido.
- Carpetas `raw/` existen para trazabilidad operativa; no deben ser input canónico.

