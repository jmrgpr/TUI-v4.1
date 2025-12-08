# PREREGISTRO_PGF_OFFLINE_v10

## Objetivo
Analizar el impacto de PGF/I_op calculados offline sobre los episodios y resultados de v10 (especialmente 6×6 y 8×8), correlacionando PGF con éxito, overhead y breakthrough.

## Motivación
La ablation de componentes v10 demuestra que el shaping PGF directo es perjudicial para el aprendizaje RL. Por tanto, PGF se reposiciona como métrica instrumental/evaluadora en Fase 3.

## Diseño experimental
- Fórmula operacional de I_op y PGF (aproximada, documentada en este preregistro).
- Enriquecer los CSV de episodios con columnas PGF/I_op offline.
- Analizar correlaciones:
  - PGF vs success
  - PGF vs pasos (overhead)
  - PGF antes/después del breakthrough
- Usar datos de:
  - `results/pgf_v10_viable/resultados/phase2_6x6_*.csv`
  - `results/pgf_v10_viable/resultados/phase3_8x8_*.csv`
  - Equivalentes de B_direct y multiseed si es relevante.

## Protocolo
- Script: `scripts/compute_pgf_offline_v10.py`
- Output: CSV enriquecidos en `results/pgf_v10_pgf_offline/datos_enriquecidos/phase*_with_pgf.csv`
- Análisis y figuras en `results/pgf_v10_pgf_offline/analisis_correlaciones/` y `results/pgf_v10_pgf_offline/figuras/`
- Reporte final: `REPORTE_PGF_OFFLINE_v10.md`

## Estado
- Preregistro creado y alineado con los resultados de Fase 2.
- Fase 2 marcada como completada en el plan global.
- PGF/I_op reposicionados como métricas evaluadoras, no shaping directo.

---
*Preregistro generado automáticamente el 8/12/2025 por GitHub Copilot, integrando el análisis y conclusiones de Fase 2.*
