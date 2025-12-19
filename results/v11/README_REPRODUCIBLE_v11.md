# Nota (2025-12-16): Los datos y scripts sueltos en `results/v11` han sido archivados en `results/v11/archived/`.
# El `results/master_results.csv` activo fue reemplazado por la version limpia (`master_results_clean.csv`).

# Regeneracion reproducible - Serie v11

Este README enumera los pasos concretos para regenerar los artefactos de la serie v11: reconstruccion del master, validacion, estadisticas, bootstrap, manifiesto canonico y comparativas F1 vs F2. Ejecuta cada comando desde la raiz del repo en PowerShell con `.venv` activado.

Prerequisitos
- Activar el entorno Python (se asume `.venv`):

```powershell
& ./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

1) Reconstruir el master a partir de los episodios

```powershell
python scripts/rebuild_master_from_episodes.py
# Salida: `results/master_results_clean.csv`
```

2) Validar el master contra las fuentes

```powershell
python scripts/validate_master_sources_file.py results/master_results_clean.csv results/v11/data/validation_master_sources_clean.csv
# Salida: `results/v11/data/validation_master_sources_clean.csv`
```

3) Generar resumen estadistico y reporte

```powershell
python scripts/analisis_estadistico_v11.py
# Salida: `results/v11/data/stats_summary_v11.csv`, `results/v11/data/stats_report_v11.md`
```

4) Bootstrap no parametrico (cluster por seed/run)

```powershell
python scripts/bootstrap_stats_v11.py
# Salida: `results/v11/data/bootstrap_stats_v11.*`
```

5) (Opcional) Recalcular los bootstraps auxiliares

```powershell
python scripts/bootstrap_nonparam_from_episodes_v11.py
python scripts/bootstrap_nonparam_v11.py
# Salidas: `results/v11/data/bootstrap_nonparam_from_episodes_v11.*` y `results/v11/data/bootstrap_nonparam_v11.*`
```

6) Generar el manifiesto canonico con hashes

```powershell
python scripts/generate_canonical_dataset_v11.py
# Salida: `results/v11/CANONICAL_DATASET_v11.md`
```

7) Métricas episódicas (agregado por run/seed)

```powershell
python scripts/episodic_metrics_v11.py
# Salida: `results/v11/data/episodic_metrics_v11.md` y `results/v11/data/episodic_metrics_v11_full.md`
```

8) Verificar que F2 difiere de F1

```powershell
python scripts/diff_check_f2_vs_f1.py
# Salida: `results/v11/data/f2_vs_f1_diff.md`
```

9) (Opcional) Graficos a partir del master

```powershell
python scripts/plot_from_master.py
# Salida: PNG/SVG en `results/v11/plots/`
```

10) Validaciones finales

```powershell
python scripts/final_checks_f2.py
python scripts/check_no_nans.py
python scripts/validate_master_sources_file.py results/master_results_clean.csv results/v11/data/validation_master_sources_clean.csv
```

## Metadatos de entorno y versiones (congelado)

- Python: 3.9.x
- OS: Windows 10 Pro x64
- CPU: Intel(R) Core(TM) i7-10850H CPU @ 2.70GHz
- RAM: 32 GB (34,065,440,768 bytes)
- GPU: NVIDIA Quadro T1000, Intel(R) UHD Graphics
- Commit repo: 988dbbf3d73e4b14e82049cf7c547750e0f669d1
- requirements.lock: ver archivo `results/v11/requirements.lock` generado por `pip freeze`


Notas importantes
- `results/master_results_clean.csv` incluye `reward_total` (desde `*_episodes.csv`) y `reward_env_total` (estimado desde el JSON del run via `reward_env_evol`).
- `reward_env_total` depende de los archivos JSON generados por cada run. Para reproducibilidad completa y verificación independiente, se requiere acceso a estos JSON fuente. El manifiesto canónico actual solo incluye hashes de los CSV; los hashes de los JSON no están incluidos (ver CANONICAL_DATASET_v11.md para aclaración formal).
- `results/v11/data/stats_report_v11.md` reporta ambas métricas (`reward_total` y `reward_env_total`) para evitar ambigüedad por reward shaping.

# NOTA: Este README solo contiene la sección canónica (congelada) de metadatos y pasos reproducibles para v11. Cualquier plantilla o ejemplo para futuros experimentos debe mantenerse fuera de este archivo para evitar confusión o conflicto de metadatos.
- Si editas los JSON de `F2_redteam`, vuelve a ejecutar `scripts/update_f2_metadata_fields.py` para propagar `phase/attack_*` antes de regenerar el manifiesto.
- `results/v11/CANONICAL_DATASET_v11.md` es la fuente definitiva de qué CSV se usan en los analisis; compara los hashes si regresas datos.
- `results/v11/data/stats_report_v11.md` y `results/v11/data/f2_vs_f1_diff.md` documentan la diferencia de F2 y sirven de respaldo al peer review.

Contacto
- Para cambios en la trazabilidad o en la definicion de columnas, abre un issue o solicita un patch en el repo.
