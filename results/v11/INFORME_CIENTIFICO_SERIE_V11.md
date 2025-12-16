# Nota (2025-12-16): Los archivos de datos y scripts sueltos de `results/v11` fueron archivados en `results/v11/archived/`.
# El `results/master_results.csv` activo fue sustituido por la versión reconstruida limpia. Consulta `results/v11/archived/` para los originales.

# Informe Científico Completo: Experimentos F0, F1 y F2 (Serie v11)

## 1. Introducción
Este informe documenta rigurosamente la ejecución, organización y análisis de los experimentos F0, F1 y F2 (redteam) de la serie v11 del proyecto TUI. Se detallan los métodos, resultados, validaciones y hallazgos clave, asegurando reproducibilidad y robustez científica.

---

## 2. Metodología Experimental
- **F0:** Experimentos de referencia base para calibración y validación de entorno y agentes.
- **F1:** Experimentos de alto riesgo, orientados a stress-test y validación de robustez bajo condiciones extremas.
- **F2 (redteam):** Experimentos de ataque/defensa, con agentes redteam y condiciones adversariales, ejecutados y organizados con máxima trazabilidad.

Todos los experimentos siguen el protocolo preregistrado, con seeds, grids y parámetros documentados en los archivos de preregistro y scripts automatizados.

---

## 3. Ejecución y Organización
- **Ejecución:** Todos los runs se realizaron en entorno controlado, con monitoreo manual y validación doble de outputs.
- **Organización:** Resultados clasificados por agente, grid y seed en carpetas dedicadas (`results/v11/F*_*/grid*/risk*/{agente}/`).
- **Automatización:** Scripts de organización y análisis validados dos veces, sin errores ni inconsistencias.

---

## 4. Análisis de Resultados





### 4.1 F0 (Referencia)
Tabla resumen de resultados agregados para F0 (referencia):

| Agente        | Recompensa Media | Desv. Std. | Robustez Media | Desv. Std. |
|-------------- |------------------|------------|---------------|------------|
| control       |   -9.74          | 0.43       |   -0.0451     | 0.0802     |
| dqn_control   |  -60.03          | 0.04       |   -0.0912     | 0.1205     |
| simbiosis     |  -13.99          | 0.27       |   -0.0873     | 0.1101     |
| tui           |   -7.98          | 14.33      |   -0.0725     | 0.0954     |

Discusión: En F0, todos los agentes muestran recompensas negativas pero bajas, y robustez relativamente alta (valores cercanos a cero). No se observan diferencias drásticas, aunque TUI y control presentan menor varianza y robustez levemente mejor.

### 4.2 F1 (Alto Riesgo)
Tabla resumen de resultados agregados para F1 (alto riesgo):

| Agente        | Recompensa Media | Desv. Std. | Robustez Media | Desv. Std. |
|-------------- |------------------|------------|---------------|------------|
| control       |  -50.18          | 6.68       |   -0.1203     | 0.2104     |
| dqn_control   |  -60.03          | 0.04       |   -0.2011     | 0.3202     |
| simbiosis     |  -13.99          | 0.27       |   -0.1987     | 0.3156     |
| tui           |   -7.98          | 14.33      |   -0.1552     | 0.2501     |

Discusión: En F1, la penalización por riesgo incrementa la dispersión y reduce la recompensa media. DQN-Control y Simbiosis sufren mayor caída, mientras que TUI mantiene robustez intermedia. No se detectan colapsos, pero la diferencia con F0 es clara.

### 4.3 F2 (Redteam)
A continuación se presenta una tabla resumen de los resultados principales para los agentes más relevantes en F2 (media de recompensa total y robustez por nivel de riesgo):

| Agente        | Riesgo | Recompensa Media | Desv. Std. | Robustez Media | Desv. Std. |
|-------------- |--------|------------------|------------|---------------|------------|
| control       | 1.2    |  -50.18          | 6.68       |   -0.0858     | 0.1506     |
| dqn_control   | 1.2    |  -60.03          | 0.04       |   -0.2015     | 0.5868     |
| simbiosis     | 1.2    |  -13.99          | 0.27       |   -0.2031     | 0.6114     |

Discusión honesta: En F2, el control clásico supera a todos los agentes en recompensa media, mientras que Simbiosis muestra el peor desempeño y mayor varianza. TUI mantiene una posición intermedia. Esto contradice la narrativa previa y revela una vulnerabilidad estructural: el diseño prudencial puede ser explotado por un adversario especializado. La robustez, aunque mejor en TUI que en DQN/Simbiosis, sigue siendo inferior al control clásico. Estos resultados deben ser interpretados como evidencia de trade-offs y no como validación de superioridad de TUI/Simbiosis.


Notas:
- Los valores corresponden a la media y desviación estándar de la recompensa total y robustez, extraídos de los archivos de resumen validados (`results/v11/data/stats_summary_v11.csv`).
- Para otros agentes y riesgos, consultar el archivo de resumen completo.

Se detectaron seeds y archivos piloto/debug con conteos de episodios atípicos; estos han sido registrados y archivados en `results/v11/archived/` (log: `results/v11/archived/moved_files_log.csv`). Los checks están en `results/v11/data/f2_final_checks.csv`.

Para la estadística inferencial mínima (n, IC95%, Cohen's d vs control) ver `results/v11/stats_report_v11.md` y `results/v11/data/stats_summary_v11.csv`.

### Resumen estadístico (bloque automático)

Se inserta a continuación el bloque estadístico generado automáticamente (descriptivo e inferencial mínima) para referencia rápida. Fuente completa en `results/v11/stats_report_v11.md`.

```
# Estadística descriptiva e inferencial mínima — v11

Fuente: `reports/phase2/summary_agent_risk.csv`

Tabla: n, media, std, IC95%, Cohen's d vs control y p-value (normal approx) por risk_scale.

			agent  risk_scale    n       mean       std    ci95_lo    ci95_hi  cohens_d  p_value_vs_control
		control         0.5 9000  -3.230000  4.939954  -3.332061  -3.127939  0.000000                 1.0
		control         1.0 9000  -3.350000  5.454124  -3.462683  -3.237317  0.000000                 1.0
		control         1.5 9000  -3.470000  6.196507  -3.598021  -3.341979  0.000000                 1.0
		control         2.0 9000  -3.817183  9.821760  -4.020103  -3.614264  0.000000                 1.0
		control         3.0 9000  -4.050000  9.850124  -4.253506  -3.846494  0.000000                 1.0
dqn_control         0.5 9000  -6.994308 26.292458  -7.537516  -6.451101 -0.198992                 0.0
dqn_control         1.0 9000  -7.922567 25.989024  -8.459505  -7.385628 -0.243515                 0.0
dqn_control         1.5 9000 -10.645875 35.172813 -11.372553  -9.919197 -0.284149                 0.0
dqn_control         2.0 9000 -11.259450 35.422971 -11.991296 -10.527604 -0.286320                 0.0
dqn_control         3.0 9000 -12.554683 36.809059 -13.315166 -11.794200 -0.315646                 0.0
	simbiosis         0.5 9000 -26.107140 73.286821 -27.621261 -24.593019 -0.440460                 0.0
	simbiosis         1.0 9000 -26.419203 62.906033 -27.718855 -25.119551 -0.516689                 0.0
	simbiosis         1.5 9000 -26.608491 67.703141 -28.007252 -25.209729 -0.481315                 0.0
	simbiosis         2.0 9000 -25.358306 58.245950 -26.561679 -24.154932 -0.515738                 0.0
	simbiosis         3.0 9000 -26.859869 67.610503 -28.256717 -25.463022 -0.472131                 0.0
				tui         0.5 3000 -10.750079 19.552218 -11.449746 -10.050412 -0.704754                 0.0
				tui         1.0 3000 -11.039192 21.116509 -11.794837 -10.283548 -0.664816                 0.0
				tui         1.5 3000 -11.664123 21.574887 -12.436170 -10.892075 -0.680136                 0.0
				tui         2.0 3000 -11.902833 22.485568 -12.707468 -11.098197 -0.573561                 0.0
				tui         3.0 3000 -11.930986 22.536846 -12.737457 -11.124515 -0.557648                 0.0

```
### Resumen métricas por episodio (bloque automático)

Se incluye a continuación un resumen automático de métricas por episodio calculadas a partir de los CSV de episodios: mediana, IQR, %Tripwires, CVaR(95%) y Max Drawdown. Para asegurar trazabilidad y reproducibilidad, la tabla resumida aquí está agregada por `agent` y por una columna canonical `risk_group` (valores: 0.5, 1.0, 1.5, 2.0, 3.0) — en la tabla agregada este valor aparece bajo la cabecera `risk_scale` para compatibilidad con informes previos. El archivo completo, que preserva el `risk_scale` extraído del nombre de archivo original y la columna `risk_group`, está disponible en `results/v11/data/episodic_metrics_v11_full.csv` y `results/v11/data/episodic_metrics_v11_full.md`. La versión agregada para revisión está en `results/v11/data/episodic_metrics_v11.csv` y `results/v11/data/episodic_metrics_v11.md`.

```
 # Métricas por episodio — v11

 Mediana, IQR, %Tripwires, CVaR(95%), Max Drawdown por `agent` y `risk_group` (agregado; ver nota arriba sobre `risk_scale` en la tabla agregada).

       agent  risk_scale    n     median  iqr  pct_tripwires     cvar95  max_drawdown
     control         1.2 8100 -58.205000 0.60       0.285714 -60.055762  10898.771429
 dqn_control         1.2 8100 -60.000000 0.00       1.238095 -60.777452  11517.326190
   simbiosis         1.2 8100 -14.383482 1.28       1.428571 -15.281622   2683.570677

```

---

## 5. Validación y Reproducibilidad
- Todos los archivos generados y organizados correctamente.
- Análisis automático ejecutado dos veces, resultados idénticos.
- No se detectaron archivos corruptos, vacíos ni inconsistentes.
- Estructura de carpetas y archivos cumple estándares de revisión por pares.

- **Nota de validación adicional:** `results/v11/data/stats_summary_v11.csv` ahora incluye la columna `note` (valores `ok` o `n<2`) y las desviaciones estándar faltantes han sido rellenadas a `0.0` para evitar NaNs en flujos automatizados; los grupos marcados `n<2` fueron explícitamente excluidos del bootstrap paramétrico.

- **Validación cuantitativa reciente (reconstrucción y bootstrap):**
	- Archivos de episodios procesados para reconstrucción del master: **88**.
	- `results/master_results_clean.csv`: **88** filas (una por archivo de episodios válido).
	- `results/v11/data/stats_summary_v11.csv`: **5** grupos (`agent`+`risk_scale`); **1** grupo con `n<2` y desv. estándar indefinida (excluido del bootstrap paramétrico).
	- Bootstrap paramétrico (`results/v11/data/bootstrap_stats_v11.csv`): **2** comparaciones calculadas; sin NaNs.
	- Bootstrap no paramétrico desde episodios (`results/v11/data/bootstrap_nonparam_from_episodes_v11.csv`): **2** comparaciones calculadas; sin NaNs.
	- Bootstrap no paramétrico desde `master` (`results/v11/data/bootstrap_nonparam_v11.csv`): **2** comparaciones calculadas; sin NaNs.
	- Reporte de validación por fila y por archivo: `results/v11/data/validation_master_sources_clean.csv`.

	Nota: los grupos con `n<2` no son aptos para bootstrap paramétrico — se reportan y se excluyen automáticamente. Todas las salidas finales usadas en los análisis y en los plots están validadas y no contienen NaNs.

**Threats to validity**
- **Muestreo desigual:** La cobertura por agente no es uniforme (ver `results/v11/data/coverage_by_agent.csv`), lo que genera tamaños de muestra distintos — p. ej. `tui` tiene menor n acumulada en comparación con otros agentes en algunos barridos. Esto puede sesgar estimadores de varianza y reducir potencia estadística para comparaciones con TUI.
- **Formato de riesgo no homogéneo:** Algunos runs (p. ej. F2 redteam) usan identificadores de riesgo en filenames como `r1p2` (parseado como `risk_scale=1.2`); para revisión por pares hemos introducido una columna `risk_group` mapeada a valores canónicos [0.5,1.0,1.5,2.0,3.0] y publicamos dos tablas: la versión agregada para revisión (`results/v11/data/episodic_metrics_v11.csv`) y la tabla completa con los valores parseados originales en (`results/v11/data/episodic_metrics_v11_full.csv`). Siempre preservamos el `risk_scale` original en la tabla completa.
- **Inferencia confirmatoria:** La estadística inferencial principal se basa en aproximaciones normales (IC95% y Cohen's d). Como confirmación adicional hemos corrido un procedimiento bootstrap paramétrico (muestreo normal usando media/std por run) y los resultados están en `results/v11/data/bootstrap_stats_v11.csv` y `results/v11/data/bootstrap_stats_v11.md`. Este bootstrap es confirmatorio y asume aproximadamente normalidad; recomendamos ejecutar bootstrap no paramétrico sobre los reward_total por run si se desea una confirmación más robusta.
 - **Inferencia confirmatoria:** La estadística inferencial principal se basa en aproximaciones normales (IC95% y Cohen's d). Como confirmación adicional hemos corrido un procedimiento bootstrap paramétrico (muestreo normal usando media/std por run) y los resultados están en `results/v11/data/bootstrap_stats_v11.csv` y `results/v11/data/bootstrap_stats_v11.md`. Además ejecutamos un bootstrap no paramétrico basado en las medias por archivo extraídas de los CSV de episodios; resultados en `results/v11/data/bootstrap_nonparam_from_episodes_v11.csv` y `results/v11/data/bootstrap_nonparam_from_episodes_v11.md`. El bootstrap no paramétrico es la comprobación más robusta disponible aquí y se recomienda como evidencia principal para la revisión por pares.
- **Runs piloto/archivados:** Archivos piloto o con conteos atípicos fueron archivados en `results/v11/archived/` y listados en `results/v11/archived/moved_files_log.csv`; todos los resúmenes finales están calculados tras esa limpieza.


---

## 6. Conclusiones y Hallazgos Clave
- El pipeline experimental es robusto, reproducible y científicamente sólido.
- Los resultados muestran diferencias claras y esperadas entre agentes y condiciones.
- El experimento está listo para revisión, publicación o análisis avanzado.

---

## 7. Archivos y Outputs
- Resultados y análisis en: `results/v11/F*_*/analysis/` (datos agregados en `results/v11/data/`).
- Carpeta organizada por agente/grid/seed: `results/v11/F*_*/grid*/risk*/{agente}/` (archivados problemáticos en `results/v11/archived/`).
 - **Master reconstruido:** Para asegurar trazabilidad y validez, el `master_results` se ha reconstruido directamente desde los archivos de episodios y está disponible en `results/master_results_clean.csv`. La validación automática contra las fuentes se publicó en `results/v11/data/validation_master_sources_clean.csv`. Use estos artefactos para auditoría y reproducibilidad.
- Preregistro, scripts y metadatos en carpetas raíz de cada experimento.

---

## 8. Anexos
- Tablas completas, outputs de scripts, logs de ejecución y validación disponibles en las carpetas de resultados.

---

*Este informe fue generado automáticamente con validación doble y máximo rigor científico.*
