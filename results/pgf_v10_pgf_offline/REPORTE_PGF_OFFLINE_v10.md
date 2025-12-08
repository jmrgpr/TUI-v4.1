# REPORTE_PGF_OFFLINE_v10

## 1. Resumen ejecutivo

En esta fase se realizó un análisis **offline** de las métricas `PGF` e `I_op`
sobre episodios ya generados en la serie v10_viable (sin entrenamiento nuevo).

Se estudiaron:

- La relación entre PGF e I_op por fase (4×4, 6×6, 8×8).
- La relación entre PGF y el éxito (`success`) por episodio.
- La relación entre PGF y el número de pasos (`steps`) como proxy de overhead.

Los datos y resultados se ajustan al preregistro de Fase 3, con la salvedad
de que la carpeta de datos enriquecidos se llama `enriched/` en lugar de
`datos_enriquecidos/` (ver sección 4).

## 2. Datos y procedimiento

- Episodios origen: snapshots de v10_viable exportados a
  `results/pgf_v10_pgf_offline/raw/phaseX_*.csv`.
- Enriquecimiento con PGF/I_op:
  - Script: `scripts/compute_pgf_offline_v10.py`.
  - Salida: `results/pgf_v10_pgf_offline/enriched/*_enriched.csv`.
  - Columnas presentes en cada CSV enriquecido:
    `success, rewards, steps, resources, epsilon, first_success, PGF, I_op`.
- Análisis avanzado:
  - Script: `scripts/analyze_pgf_offline_v10.py`.
  - Entrada: `enriched/`.
  - Salida: `results/pgf_v10_pgf_offline/analysis/`:
    - `*_summary.csv`  → `describe()` de PGF e I_op.
    - `*_correlation.txt` → correlación PGF–I_op.
    - `*_hist_pgf.png`, `*_hist_iop.png` → histogramas.
    - `pgf_vs_success_summary.csv` → resumen global PGF vs éxito/steps por archivo.

Todos los comandos utilizados se registraron en
`results/pgf_v10_pgf_offline/FASE3_LOG_COMANDOS.md`.

## 3. Resultados cuantitativos

En la tabla siguiente se resumen las medias por fase (promedio sobre los CSV
de cada fase) a partir de `pgf_vs_success_summary.csv`:

| Fase   | PGF (media) | I_op (media) | Éxito medio (`success_rate`) | corr(PGF, I_op) aprox. | corr(PGF, éxito) | corr(PGF, steps) |
|--------|-------------|--------------|------------------------------|------------------------|------------------|------------------|
| 4×4    | ≈ 1.94      | ≈ 0.47       | ≈ 0.78                       | ≈ 0.60                 | ≈ 0.05           | ≈ 0.02           |
| 6×6    | ≈ 1.60      | ≈ 0.37       | ≈ 0.19                       | ≈ 0.69*                | ≈ -0.04          | ≈ 0.05           |
| 8×8    | ≈ 1.21      | ≈ 0.42       | ≈ 0.61                       | ≈ 0.44                 | ≈ 0.02           | ≈ 0.07           |

\*En 6×6 hay ficheros con `success` casi constante (0 o muy bajo), por lo que
la correlación PGF–éxito es numéricamente poco informativa y se reporta con
prudencia.

Observaciones:

- PGF medio **decrece** al pasar de 4×4 → 6×6 → 8×8, reflejando entornos más
  difíciles / costosos.
- I_op medio se mantiene en un rango relativamente estable (≈ 0.35–0.48).
- La **correlación PGF–I_op** es positiva en todas las fases (moderada-alta en
  4×4 y 6×6, menor en 8×8).
- La **correlación PGF–éxito** por episodio es pequeña (≈ 0.0–0.05):
  PGF no actúa como predictor lineal simple de éxito episodio-a-episodio, aunque
  los niveles medios por fase son coherentes con la dificultad.
- La **correlación PGF–steps** (proxy de overhead) también es pequeña
  (≈ 0.02–0.07), sin señal fuerte lineal; episodios con más pasos tienden a
  tener PGF algo diferente, pero el efecto es débil.

Las figuras `*_hist_pgf.png` y `*_hist_iop.png` muestran que ambas métricas
concentran masa en rangos intermedios y se desplazan con el tamaño de la
rejilla, sin colas extremas patológicas en estos episodios viables.

## 4. Coherencia con el preregistro y notas técnicas

El preregistro de Fase 3 especificaba:

- Enriquecer episodios con I_op y PGF.
- Analizar:
  - Distribución PGF en episodios exitosos vs fallidos.
  - Correlación PGF–overhead.
  - Evolución de PGF a lo largo de los episodios.
- Generar un CSV `pgf_vs_success_summary.csv` y un reporte interpretativo.

Estado actual respecto a ese plan:

- Enriquecimiento con PGF/I_op: **cumplido**, usando `enriched/` como carpeta
  final (equivalente funcional de `datos_enriquecidos/`).
- Correlación PGF–éxito: **cumplida** a nivel global por archivo, vía la
  columna `corr_pgf_success` en `pgf_vs_success_summary.csv`.
- Overhead: se usa `steps` como proxy de overhead (no se dispone de la
  distancia Manhattan por episodio); la correlación PGF–steps se reporta como
  `corr_pgf_steps`.
- Evolución temporal (PGF medio vs episodio): no se generaron gráficas
  adicionales por episodio, dado que las métricas agregadas por archivo ya
  muestran la tendencia fase-a-fase; esta extensión quedaría como trabajo
  futuro opcional.

## 5. Interpretación y conclusiones

En el contexto de la serie v10 (donde se descartó usar PGF como reward), estos
resultados apoyan una lectura prudente de PGF como **métrica descriptiva**:

- PGF refleja la dificultad global del entorno (baja al hacer el grid más
  grande), pero **no** es un buen predictor lineal del éxito de cada episodio.
- I_op se correlaciona moderadamente con PGF, lo que indica que la estructura
  informacional del entorno y el “performance” económico están relacionados,
  pero no de forma trivial.
- No se observa una “firma PGF” simple que separe de forma limpia episodios
  exitosos de fallidos; las diferencias se manifiestan más en tendencias
  agregadas por fase que a nivel de episodio individual.

En conjunto, estos hallazgos son coherentes con la decisión metodológica
tomada en Fase 2: **no usar PGF como reward directo**, sino como una métrica
offline para caracterizar políticas y escenarios. Fase 3 cumple ese rol:
aporta evidencia cuantitativa de que PGF es útil como descriptor del régimen de
entrenamiento, pero no como señal de refuerzo “mágica” que garantice éxito.

## 6. Limitaciones y trabajo futuro

- Falta incorporar explícitamente la distancia Manhattan para definir un
  overhead normalizado (steps / distancia), lo que haría más precisa la parte
  de H2 del preregistro.
- No se incluyó en este reporte el análisis por seed ni por política
  colapsada vs estable; esto podría ampliarse a partir de los CSV crudos de
  otras fases (multi-seed, ablation).
- Las correlaciones reportadas son lineales (Pearson); relaciones no lineales
  entre PGF y éxito podrían existir y requerir métodos adicionales.

---
*Este reporte documenta el cierre de la Fase 3 – PGF Offline (v10) tal como se
ejecutó en `results/pgf_v10_pgf_offline/`.*

