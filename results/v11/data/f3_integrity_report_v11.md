# F3 integrity checks (v11)

- CSVs organizados encontrados (excluye `raw/`): 80 (esperado=80)
- Por pgf_mix: m0.0=60 (esperado=60), m0.2=20 (esperado=20)
- CSVs agregados en raw/: 40 (informativo; no canónico)
- Episodios esperados por archivo: 200 (umbral truncamiento < 190)

## Lectura de CSV
- Archivos no legibles: 0
- Archivos truncados (<190 filas): 0
- Archivos con warning (>= 190 y < 200 filas): 0

## Master reconsolidado
- `results/master_results_clean.csv` existe: True
- Filas master (total): 146
- Filas master (F3): 80
