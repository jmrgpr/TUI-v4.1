
# Resultados / Results

Esta carpeta centraliza todos los resultados experimentales: archivos csv, json, png, etc.

This folder centralizes all experimental results: csv, json, png files, etc.

## Organización y protocolo (actualizado 19/11/2025)

- Todos los resultados de Fase 2 se guardan en `results/fase2/` con nombres únicos por semilla y risk_scale.
- El runner `run_fase2.py` automatiza la ejecución de las 60 corridas.
- El script `merge_summaries.py` une los resúmenes por semilla en un solo archivo global.
- Ejemplo de uso:
	```powershell
	python run_fase2.py
	python merge_summaries.py
	```
- No mezclar código fuente ni notebooks aquí.
- Do not mix source code or notebooks here.