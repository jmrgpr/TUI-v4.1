# Preregistro Fase 3 – PGF Offline (Serie v10, TUI-v4.1)

**Fecha:** 2025-12-08  
**Alcance:** Análisis offline de PGF/I_op sobre episodios existentes (sin entrenamiento nuevo).

## 1. Contexto
- Fase 1 (Multi-seed v10): curriculum viable y economía estable en 4×4→6×6→8×8.
- Fase 2 (Ablation de componentes): baseline 8×8 robusto; regularización mejora; reward_extra inestable; shaping (PGF como reward) colapsa; PGF se usará solo como métrica offline.

## 2. Objetivo
Cuantificar cómo se comportan I_op y PGF sobre episodios ya generados en v10_viable (y opcionalmente multi-seed), respondiendo:
1) ¿Correlaciona PGF con probabilidad de éxito (goal_reached) y overhead vs Manhattan?  
2) ¿Existe una “firma PGF” de políticas sanas vs políticas colapsadas?

## 3. Datos y alcance
- Fuente principal: `results/pgf_v10_viable/resultados/phase*_*.csv` (4×4, 6×6, 8×8).
- Opcional: episodios de Fase 1 multi-seed si están consolidados.
- No se entrena nada nuevo; solo enriquecimiento y análisis offline.

## 4. Procedimiento
1) Enriquecer episodios con I_op y PGF usando `scripts/compute_pgf_offline_v10.py`.
   - Salida en `results/pgf_v10_pgf_offline/datos_enriquecidos/phaseX_with_pgf.csv`.
2) Análisis:
   - Distribución de PGF en episodios exitosos vs fallidos.
   - Correlación PGF ↔ overhead.
   - Evolución PGF por episodio (rolling).
   - Resumen en `results/pgf_v10_pgf_offline/analisis/pgf_vs_success_summary.csv`.
3) Figuras:
   - Histogramas PGF (con/ sin goal).
   - Scatter PGF vs overhead.
   - Curvas PGF medio por episodio.
4) Reporte:
   - `results/pgf_v10_pgf_offline/REPORTE_PGF_OFFLINE_v10.md` con resultados, interpretación y limitaciones.

## 5. Hipótesis (antes de ver datos)
- H1: PGF de episodios exitosos se concentra en rangos intermedios (ni extremos de riesgo/costo).
- H2: Menor overhead correlaciona con PGF en rango estable.
- H3: En escenarios con breakthrough, PGF medio muestra transición estable (no puro ruido).

## 6. Criterios de cierre
- CSV enriquecidos con I_op/PGF para todas las fases de v10_viable.
- Análisis cuantitativo de correlación PGF ↔ éxito/overhead.
- `REPORTE_PGF_OFFLINE_v10.md` redactado (aunque H1–H3 se refuten).
