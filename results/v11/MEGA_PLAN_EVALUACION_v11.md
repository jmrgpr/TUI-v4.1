# MEGA PLAN DE EVALUACION - Serie v11 (post F2)

Este documento resume el estado real de la serie v11 despues de cerrar operacionalmente F2 y alinear pipeline/datos/reportes.

## 1) Fases completadas (v11)
- [x] F0 (baseline): ejecutado y presente en dataset canonico.
- [x] F1 (alto riesgo): ejecutado y presente en dataset canonico.
- [x] F2 (stress test adversarial sintetico): ejecutado con `red_team` activo y trazabilidad en JSON.

## 2) Hallazgos y gaps metodologicos
- F2 no es un "red teaming" min-max: es un stress test parametrico con perturbaciones estocasticas; los claims deben reflejarlo.
- En F2 todos los agentes empeoran vs F1 (esperable); el ranking por reward puede cambiar y la degradacion es una senal clave.
- Baselines: `control` y `dqn_control` no son SOTA; si se quiere hacer claims fuertes, F3 debe incluir PPO/SAC/TD3 (o Safe-RL).
- Estadistica: la unidad primaria debe ser seed/run (evitar p-values por episodio); bootstrap por clusters recomendado.

## 3) Checklist (cerrado vs pendiente)
- [x] Dataset canonico con hashes: `results/v11/CANONICAL_DATASET_v11.md`.
- [x] Pipeline reproducible (master limpio + reportes): `results/v11/README_REPRODUCIBLE_v11.md`.
- [x] Reporte estadistico vigente: `results/v11/data/stats_report_v11.md`.
- [x] Evidencia de que F2 != F1: `results/v11/data/f2_vs_f1_diff.md`.
- [x] Checks F2 (runs/outliers) sobre canonico: `results/v11/data/f2_final_checks.md`.
- [ ] Definir formalmente la metrica "robustez" en el cuerpo del reporte (formula e interpretacion).
- [ ] Agregar metricas complementarias (mediana/IQR, % tripwires, CVaR, violin/boxplots) si se busca publicacion formal.
- [ ] Baseline fuerte (PPO/SAC/TD3 o Safe-RL) como preregistro y ejecucion en F3.

## 4) Plan de fases siguientes
- F3: escalado + baseline fuerte + ablations (por ejemplo `pgf_mix`), con estadistica por seed/run.
- F4: analisis de alineacion (u_proxy vs u_humans) y trade-offs bajo riesgo/adversidad.

## 5) Cierre operacional de F2
- F2 se considera "cerrado" si `attack_enabled=true` en los JSON canonicos y `results/v11/data/f2_vs_f1_diff.md` muestra diferencias observables (tripwires/shocks/surprise/risk_effective).
- Archivos piloto/debug y copias redundantes se conservan en `results/v11/archived/` (log: `results/v11/archived/moved_files_log.csv`) y no entran en el master limpio.

