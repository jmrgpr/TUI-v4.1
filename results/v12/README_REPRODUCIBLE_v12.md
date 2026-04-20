# Regeneración reproducible — Serie v12 (WIP)

Este README documenta el pipeline reproducible para v12. Se mantiene el mismo criterio que v11: separación estricta entre datos canónicos (CSV) y datos brutos (JSON no versionado).

Estado actual: documento “WIP” (v12 aún no ejecutada).

## Prerrequisitos

```powershell
& ./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

## Pipeline (cuando exista data v12)

1) Ejecutar fases (F0–F6) generando outputs bajo `results/v12/`.
2) Generar manifiestos canónicos con hashes:
   - `results/v12/CANONICAL_DATASET_v12.md`
   - `results/v12/CANONICAL_DATASET_EXTENDED_JSON.md`
3) Construir master limpio desde los `*_episodes.csv` y generar reporte estadístico v12 (análogo a v11).

Notas:
- En v11 existen scripts versionados para master/stats/manifiestos (ver `results/v11/README_REPRODUCIBLE_v11.md`). Para v12 se recomienda crear wrappers `*_v12.py` que no mezclen series.

