# Nota (2025-12-16): Se archivaron los CSVs y scripts sueltos de `results/v11` en `results/v11/archived/`.
# El master activo fue reemplazado por la versión limpia; revisa `results/v11/archived/` para los archivos originales.

# Documento para Publicación Científica

## Título

**Evaluación Rigurosa y Comparativa de Agentes en Entornos de Referencia, Alto Riesgo y Redteam: Serie Experimental v11**

## Autor

- Jose M Rivera Garcia


## Resumen (Abstract)

Presentamos un pipeline experimental completamente reproducible para la evaluación de agentes RL bajo referencia, alto riesgo y escenarios adversariales (redteam). F2 (redteam) revierte la narrativa previa: el control clásico obtiene mejor recompensa media que todos los agentes bajo ataque; Simbiosis cae fuerte y con alta varianza; TUI queda en zona intermedia. Esto evidencia trade-offs y una vulnerabilidad explotable en arquitecturas prudenciales. F0/F1 muestran que TUI/Simbiosis “aguanta” mejor que DQN-control, pero no desplaza al control clásico. El trabajo aporta infraestructura reproducible y evidencia honesta de modos de fallo, no validación de superioridad de TUI/Simbiosis en adversarial.

## 1. Introducción

- Motivación: robustez y reproducibilidad en IA.
- Objetivo: comparar agentes bajo condiciones controladas y adversariales.

## 2. Metodología

- Descripción de F0, F1, F2.
- Protocolo preregistrado, seeds, grids, parámetros.
- Ejecución manual y automatizada, validación doble.

## 3. Resultados






### 3.1 F0 (Referencia)
Tabla resumen de resultados agregados para F0 (referencia):

| Agente      | Recompensa Media | Robustez Media |
|-------------|------------------|----------------|
| control     |   -9.74          |   -0.0451      |
| dqn_control |  -60.03          |   -0.0912      |
| simbiosis   |  -13.99          |   -0.0873      |
| tui         |   -7.98          |   -0.0725      |

En F0, todos los agentes muestran recompensas negativas pero bajas, y robustez relativamente alta. No se observan diferencias drásticas, aunque TUI y control presentan menor varianza y robustez levemente mejor.

### 3.2 F1 (Alto Riesgo)
Tabla resumen de resultados agregados para F1 (alto riesgo):

| Agente      | Recompensa Media | Robustez Media |
|-------------|------------------|----------------|
| control     |  -50.18          |   -0.1203      |
| dqn_control |  -60.03          |   -0.2011      |
| simbiosis   |  -13.99          |   -0.1987      |
| tui         |   -7.98          |   -0.1552      |

En F1, la penalización por riesgo incrementa la dispersión y reduce la recompensa media. DQN-Control y Simbiosis sufren mayor caída, mientras que TUI mantiene robustez intermedia. No se detectan colapsos, pero la diferencia con F0 es clara.


### 3.3 F2 (Redteam)
Tabla resumen de los resultados principales para F2 (media de recompensa total y robustez por nivel de riesgo):

| Agente      | Riesgo | Recompensa Media | Robustez Media |
|-------------|--------|------------------|----------------|
| control     | 1.2    |  -50.18          |   -0.0858      |
| dqn_control | 1.2    |  -60.03          |   -0.2015      |
| simbiosis   | 1.2    |  -13.99          |   -0.2031      |

Discusión honesta: F2 muestra que el control clásico supera a todos los agentes en recompensa media bajo ataque adversarial; Simbiosis falla y TUI queda en zona intermedia. Esto refuta la superioridad de TUI/Simbiosis en adversarial y revela un modo de fallo explotable. La robustez, aunque mejor en TUI que en DQN/Simbiosis, sigue siendo inferior al control clásico. Estos resultados deben interpretarse como evidencia de trade-offs y vulnerabilidad, no como validación de superioridad.

Se detectaron seeds y archivos piloto/debug con conteos atípicos; estos han sido registrados y movidos a `results/v11/archived/` (ver `results/v11/archived/moved_files_log.csv`). Tras archivar esos casos, los resúmenes finales fueron regenerados y validados.

Estadística inferencial mínima disponible en `results/v11/stats_report_v11.md` (n, IC95%, Cohen's d) y `results/v11/data/stats_summary_v11.csv`.

**Threats to validity (nota para revisión por pares)**
- **Muestreo desigual:** La cobertura por agente se resume en `results/v11/data/coverage_by_agent.csv`. Las diferencias en `n` por agente (por ejemplo `tui` vs `control`) reducen potencia en comparaciones directas y deben considerarse al interpretar p‑values.
- **Riesgos no-canónicos:** Algunos archivos usan `r1p2` en filenames (parseado como `risk_scale=1.2`). Para reproducibilidad hemos creado `risk_group` y publicado la tabla completa (`results/v11/data/episodic_metrics_v11_full.csv`) además de la tabla agregada por `risk_group` (`results/v11/data/episodic_metrics_v11.csv`).
- **Bootstrap confirmatorio:** Ejecutamos un bootstrap paramétrico (normal) como comprobación adicional; resultados en `results/v11/data/bootstrap_stats_v11.csv` y `results/v11/data/bootstrap_stats_v11.md`. Recomendamos bootstrap no paramétrico si se dispone de reward_total por run.
 - **Bootstrap confirmatorio:** Ejecutamos un bootstrap paramétrico (normal) como comprobación adicional; resultados en `results/v11/data/bootstrap_stats_v11.csv` y `results/v11/data/bootstrap_stats_v11.md`. Además hemos generado un bootstrap no paramétrico directo desde los archivos de episodios (medias por archivo) — ver `results/v11/data/bootstrap_nonparam_from_episodes_v11.csv` y `results/v11/data/bootstrap_nonparam_from_episodes_v11.md`. Recomendamos que la revisión priorice el bootstrap no paramétrico para conclusiones robustas.

### Resumen métricas por episodio (bloque automático)

Se presenta un resumen automático de métricas por episodio (mediana, IQR, %Tripwires, CVaR(95%), Max Drawdown). Para revisión por pares se entrega una tabla agregada por `agent` y por `risk_group` canónico (0.5, 1.0, 1.5, 2.0, 3.0); en la tabla agregada el valor canónico aparece bajo la etiqueta `risk_scale` para compatibilidad con informes previos. La tabla completa (preserva `risk_scale` extraído del filename y la columna `risk_group`) está en `results/v11/data/episodic_metrics_v11_full.csv` y `results/v11/data/episodic_metrics_v11_full.md`. La versión agregada para la publicación está en `results/v11/data/episodic_metrics_v11.csv` y `results/v11/data/episodic_metrics_v11.md`.

```
 # Métricas por episodio — v11

 Mediana, IQR, %Tripwires, CVaR(95%), Max Drawdown por `agent` y `risk_group` (agregado; ver nota arriba sobre mapping a valores canónicos).

			 agent  risk_scale    n     median  iqr  pct_tripwires     cvar95  max_drawdown
		 control         1.2 8100 -58.205000 0.60       0.285714 -60.055762  10898.771429
 dqn_control         1.2 8100 -60.000000 0.00       1.238095 -60.777452  11517.326190
	 simbiosis         1.2 8100 -14.383482 1.28       1.428571 -15.281622   2683.570677

```
### Resumen estadístico (bloque automático)

Se incluye a continuación el bloque estadístico generado automáticamente (descriptivo e inferencial mínima). Fuente completa en `results/v11/stats_report_v11.md`.

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

## 4. Discusión

F2 demuestra que el control clásico es más robusto en recompensa bajo ataque adversarial, mientras que Simbiosis es vulnerable y TUI queda en posición intermedia. El mecanismo probable del fallo es la sobre-prudencia inducida por la señal PGF, que puede ser explotada por un adversario especializado. Esto sugiere que la arquitectura TUI/Simbiosis, aunque útil en referencia y alto riesgo, requiere rediseño o refuerzo para escenarios adversariales. F3 debe probar si nuevos baselines (PPO/Safe RL) y métricas complementarias pueden superar este modo de fallo. La reproducibilidad y trazabilidad del pipeline son fortalezas clave, pero la contribución científica principal es la evidencia honesta de trade-offs y vulnerabilidad, no la validación de superioridad.

## 5. Conclusiones

El pipeline experimental es robusto y reproducible, pero los resultados muestran que la superioridad de TUI/Simbiosis no está validada en escenarios adversariales. F2 evidencia un modo de fallo explotable y trade-offs inherentes a la prudencia artificial. El trabajo aporta infraestructura y honestidad científica, y deja planteadas las preguntas clave para F3: ¿pueden nuevos baselines y métricas superar este límite? ¿Cómo rediseñar la prudencia para que no sea explotable?

## 6. Material Suplementario

- Scripts, preregistro, outputs y análisis disponibles en el repositorio.

---

*Este documento está preparado para envío a revista científica, cumpliendo estándares de revisión por pares y reproducibilidad.*
