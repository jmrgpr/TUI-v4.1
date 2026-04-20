# Plan Operativo v12 (Fase por Fase)

## Objetivo
Convertir `results/v12/` de scaffold a serie cerrada, reproducible y auditable.

## Regla base de ejecucion
Cada fase se cierra con 5 entregables minimos:
1. Preregistro congelado.
2. Outputs canonicos (`*_episodes.csv`) versionados.
3. Hashes y manifiesto de brutos (JSON no versionado).
4. Analisis preregistrado con reporte de fase.
5. Closure report con decision GO/NO-GO.

## Estandar sugerido de naming
- CSV canonico: `grid{N}_risk{L}_seed{S}_{fase}_v12_episodes.csv`
- JSON bruto: mismo prefijo, extension `.json`
- Metricas run-level: `{fase}_run_metrics_v12.csv`
- Reporte fase: `{fase}_preregistered_report_v12.md`

## F0_baseline
Proposito:
- Validar instrumentacion y pipeline.

Checklist:
- Runner F0 v12 creado.
- Seeds y episodios definidos en preregistro.
- Carpetas `grid8/`, `grid16/`, `raw/`, `analysis/` usadas de forma consistente.
- GO tecnico (sin claims confirmatorios).

## F1_highrisk
Proposito:
- Baseline en riesgo alto sin red team.

Checklist:
- Runner F1 v12.
- Reporte descriptivo + control de calidad de columnas.
- Sin claims causales fuertes.

## F2_redteam
Proposito:
- Baseline adversarial para arco v12-A.

Checklist:
- Runner F2 v12 (ya existe; revisar version final).
- Dataset base completo por seed y grid.
- Reporte de integridad y consistencia.

## F3 (piloto headroom CFR)
Proposito:
- Elegir regimen con `CFR_control` no saturado.

Checklist:
- Candidatos preregistrados.
- Tabla de seleccion publicada (`f3_pilot_selection_v12.*`).
- Justificacion de seleccion antes de F4.

## F4 (confirmatorio CFR, H1-only)
Proposito:
- Replicar claim robustez CFR en regimen seleccionado.

Checklist:
- Family confirmatoria explicita (m=1).
- Test pareado preregistrado.
- MESI y criterio de decision explicitos.
- Cierre formal F4.

## F5 (generalizacion CFR)
Proposito:
- Generalizar con una sola palanca causal modificada.

Checklist:
- Cambio unico documentado vs F4.
- H1 primaria unica.
- Cierre formal F5.

## F6 (PGF directo, P-PGF-1)
Proposito:
- Test causal directo de pendiente de mejora bajo manip de `P_eff`.

Checklist:
- Control explicito de sorpresa/dificultad (`S_t`).
- Control o fijacion de factores de alineacion operativa.
- Test de permutacion preregistrado.
- Cierre formal F6 con falsacion soportada.

## Scripts minimos a crear para v12
- `results/v12/F0_baseline/run_F0_baseline_v12.py`
- `results/v12/F1_highrisk/run_F1_highrisk_v12.py`
- `results/v12/F3/run_F3_v12.py`
- `results/v12/F4/run_F4_v12.py`
- `results/v12/F5/run_F5_v12.py`
- `results/v12/F6/run_F6_v12.py`

- `scripts/organize_F0_results_v12.py` ... `organize_F6_results_v12.py`
- `scripts/f4_preregistered_analysis_v12.py`
- `scripts/f5_preregistered_analysis_v12.py`
- `scripts/f6_preregistered_analysis_v12.py`
- `scripts/generate_canonical_dataset_v12.py`
- `scripts/generate_canonical_dataset_extended_json_v12.py`
- `scripts/make_stats_from_master_clean_v12.py`

## Politica de backup (obligatoria)
- `raw/*.csv` y JSON fuera de git, pero con backup redundante (2 ubicaciones).
- Guardar manifest de backup por fecha.
- No borrar crudos hasta cierre oficial de serie.

## Definicion de terminado (DoD) por fase
Una fase esta terminada si cualquier tercero puede:
1. Encontrar preregistro,
2. localizar CSV canonicos,
3. verificar hashes,
4. ejecutar analisis,
5. reproducir conclusion de fase.
