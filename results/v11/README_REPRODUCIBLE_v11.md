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

7) Verificar que F2 difiere de F1

```powershell
python scripts/diff_check_f2_vs_f1.py
# Salida: `results/v11/data/f2_vs_f1_diff.md`
```

8) (Opcional) Graficos a partir del master

```powershell
python scripts/plot_from_master.py
# Salida: PNG/SVG en `results/v11/plots/`
```

9) Validaciones finales

```powershell
python scripts/final_checks_f2.py
python scripts/check_no_nans.py
python scripts/validate_master_sources_file.py results/master_results_clean.csv results/v11/data/validation_master_sources_clean.csv
```

Notas importantes
- Si editas los JSON de `F2_redteam`, vuelve a ejecutar `scripts/update_f2_metadata_fields.py` para propagar `phase/attack_*` antes de regenerar el manifiesto.
- `results/v11/CANONICAL_DATASET_v11.md` es la fuente definitiva de qué CSV se usan en los analisis; compara los hashes si regresas datos.
- `results/v11/data/stats_report_v11.md` y `results/v11/data/f2_vs_f1_diff.md` documentan la diferencia de F2 y sirven de respaldo al peer review.

Contacto
- Para cambios en la trazabilidad o en la definicion de columnas, abre un issue o solicita un patch en el repo.
