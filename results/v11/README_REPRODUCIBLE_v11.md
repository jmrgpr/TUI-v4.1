# Nota (2025-12-16): Los datos y scripts sueltos en `results/v11` han sido archivados en `results/v11/archived/`.
# El `results/master_results.csv` activo fue reemplazado por la versión limpia (`master_results_clean.csv`).

# Reproducible regeneration — Serie v11

Este README contiene los pasos y comandos exactos para regenerar los artefactos clave de la serie v11: reconstrucción del master, estadísticas descriptivas, bootstraps, validación y figuras. Sigue estos pasos desde la raíz del repositorio en Windows PowerShell con el entorno virtual activado.

Prerequisitos
- Activar entorno Python (se asume `.venv`):

```powershell
& ./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

1) Reconstruir master desde archivos de episodios

```powershell
python scripts/rebuild_master_from_episodes.py
# Resultado: `results/master_results_clean.csv`
```

2) Validar master contra fuentes

```powershell
python scripts/validate_master_sources_file.py results/master_results_clean.csv results/v11/data/validation_master_sources_clean.csv
# Resultado: `results/v11/data/validation_master_sources_clean.csv` (detalla match/ mismatch por fila)
```

3) Generar resumen estadístico a partir del master limpio

```powershell
python scripts/make_stats_from_master_clean.py
# Resultado: `results/v11/data/stats_summary_v11.csv`
```

4) Ejecutar bootstrap paramétrico (confirmatorio)

```powershell
python scripts/bootstrap_stats_v11.py
# Resultado: `results/v11/data/bootstrap_stats_v11.csv` y `.md`
```

5) Ejecutar bootstrap no paramétrico (desde episodios)

```powershell
python scripts/bootstrap_nonparam_from_episodes_v11.py
# Resultado: `results/v11/data/bootstrap_nonparam_from_episodes_v11.csv` and `.md`
```

6) Ejecutar bootstrap no paramétrico (desde master limpio)

```powershell
python scripts/bootstrap_nonparam_v11.py
# Resultado: `results/v11/data/bootstrap_nonparam_v11.csv` and `.md`
```

7) Generar figuras (box/violin) a partir del master limpio

```powershell
python scripts/plot_from_master.py
# Resultado: PNG/SVG en `results/v11/plots/`
```

8) Validaciones finales (sin NaNs)

```powershell
python scripts/check_no_nans.py
python scripts/validate_master_sources_file.py results/master_results_clean.csv results/v11/data/validation_master_sources_clean.csv
```

Notas importantes
- Todos los scripts prefieren `results/master_results_clean.csv` si existe. Si quieres regenerar desde consolidación antigua, elimina `results/master_results_clean.csv` y ejecuta `scripts/consolidate_results.py` según protocolo.
- Los grupos con `n<2` se excluyen automáticamente del bootstrap paramétrico y se documentan en `results/v11/data/stats_summary_v11.csv`.
- `results/v11/data/validation_master_sources_clean.csv` es la fuente canónica de trazabilidad; inclúyela en la revisión por pares.

Contacto
- Para cambios adicionales en la reproductibilidad o en la definición de columnas, abre un issue o solicita un patch en el repo.
