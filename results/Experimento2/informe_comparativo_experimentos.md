# Informe comparativo - Exp2 (TUI-v4.1) y SOTA

Fecha: 2025-11-25  
Fuente de datos: `results/master_results.csv` (tras consolidar `results/sweep/fase2_full` y `results/sota/*`, excluyendo `sota_all_global_summary.csv`).

## Cobertura de agentes y metadatos
- Agentes presentes: `control`, `dqn_control`, `simbiosis`, `tui`, `a2c`, `dqn`, `ppo`.
- Riesgos: 0.5, 1.0, 1.5, 2.0, 3.0.
- Seeds: 42, 123, 456 para control/dqn_control/simbiosis/tui. Las filas SOTA (ppo/a2c/dqn) vienen sin `seed`, `risk_level` ni `red_team` (metadatos faltantes).
- Métricas `robustez` y `flexibilidad`: vacías (NaN) en el master actual; no están exportadas en los CSV.

## Estadísticos rápidos (medias globales por agente)
- Tripwires (baja = mejor): control ≈0.0127 < tui ≈0.0331 < dqn ≈0.0340 < ppo ≈0.0850 < dqn_control ≈0.1039 < simbiosis ≈0.1126. (a2c tiene solo 10 filas resumen, tripwires=0).
- Reward_total (media): ppo ≈197.7, dqn ≈173.0, control ≈-3.58, tui ≈-11.47, dqn_control ≈-9.88, simbiosis ≈-26.27, a2c ≈-0.02 (resumen).
- PGF_neto (media): dqn ≈-0.075 > control ≈-0.087 > ppo ≈-0.094 > tui ≈-0.160 > dqn_control ≈-0.206 > simbiosis ≈-0.215. (a2c ≈0, resumen).

## Limitaciones del dataset actual
- SOTA (ppo/a2c/dqn) están consolidados como resúmenes por riesgo sin `seed`, `risk_level` ni episodios/steps; no son comparables 1:1 con los episodios TUI/control.
- `robustez`/`flexibilidad` no se exportaron en los CSV, por eso están vacías.
- `risk_level` y `red_team` no vienen en los CSV (quedan NaN en el master).
- Advertencia de pandas: seed con tipos mixtos (float/NaN) al leer el master.

## Recomendaciones de análisis

## Problemas detectados y soluciones propuestas

**1. Falta de metadatos en SOTA:** Los agentes SOTA no incluyen `seed`, `risk_level` ni episodios, lo que dificulta comparaciones directas.
	- *Solución:* Reexportar los CSV de SOTA con estos metadatos y reconsolidar el master.

**2. Métricas vacías:** `robustez` y `flexibilidad` no están presentes en los CSV.
	- *Solución:* Modificar el pipeline para exportar estas métricas en los resultados.

**3. Advertencias de pandas:** Tipos mixtos en la columna `seed`.
	- *Solución:* Normalizar el tipo de dato de `seed` antes de consolidar.

**4. Comparabilidad limitada:** Los resúmenes SOTA no permiten análisis por semilla/riesgo.
	- *Solución:* Analizar SOTA por separado o mejorar la exportación de datos.

## Recomendaciones de análisis
- Para análisis inmediato: filtrar por agentes `control`, `dqn_control`, `simbiosis`, `tui` y comparar `reward_total`, `tripwires`, `pgf_neto` por `risk_scale` y `seed`.
- Si se desea comparar SOTA: reexportar CSV SOTA incluyendo `seed`, `risk_level`, `red_team` y, si es posible, episodios por seed; luego reconsolidar.
- Generar visualizaciones (boxplots/lines) a partir del master filtrado, o ajustar el notebook `analysis_phase2.ipynb` para leer `results/master_results.csv`.
- Normalizar `seed` a entero/string al consolidar para evitar `DtypeWarning`.
## Siguientes pasos sugeridos
1) Decidir si se reexportan SOTA con metadatos completos; si no, analizarlos aparte como resúmenes por riesgo.
2) Generar gráficos/tablas por agente y riesgo para `reward_total`, `tripwires`, `pgf_neto` con los datos TUI/control/dqn_control/simbiosis (y SOTA si se reexportan).
3) Si se necesitan `robustez`/`flexibilidad`, incluirlas en los CSV de salida del pipeline antes de reconsolidar.
4) Documentar en `experiment_log.txt` cualquier reexportación o reconsolidado adicional.

---
*Este informe ha sido revisado y optimizado el 25/11/2025. Para detalles completos, consultar el notebook de análisis y los archivos de resultados en el repositorio.*
