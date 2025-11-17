
# PREREGISTRO_FASE4_SCALABILITY_v10.md

**Objetivo:**
Evaluar la escalabilidad del stack v10 (DQN + economía v10 + regularización + RL puro) en grids más grandes (16×16) bajo dos configuraciones (sin y con regularización), usando dos semillas (42, 101) y 3000 episodios por experimento.

**Pipeline oficial:**
- Script ejecutado: `scripts/run_fase4_scalabilidad_v10.py`
- Experimentos: 2 configs × 2 seeds × 3000 episodios
- Resultados generados y auditados en las carpetas designadas

**Gate de éxito:**
- 16×16: >20% success en últimos 100 episodios con overhead decente.
- Si no se alcanza, documentar frontera de v10 y motivar v11.

**Métricas:**
- success, steps, overhead, PGF, I_op.

**Resultados y análisis:**
- CSVs por experimento en `results/pgf_v10_scalabilidad/`
- Consolidación y análisis en `analisis_scalability/consolidado_fase4_v10.md`
- Reporte técnico y log de auditoría actualizados

**Meta:**
- Definir hasta dónde llega v10 antes de pasar a v11.
