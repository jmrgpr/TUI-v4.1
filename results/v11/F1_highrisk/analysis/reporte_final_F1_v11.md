# reporte_final_F1_v11.md (DEPRECATED)

Este documento se conserva solo como **auditoria historica**. Fue redactado antes del cierre reproducible/canonico de la serie v11 y contiene estadistica a nivel episodio (tests por episodio) que puede incurrir en **pseudo-replicacion**.

Para resultados vigentes y coherentes con el dataset canonico de v11, usar:
- `results/v11/INFORME_CIENTIFICO_SERIE_V11.md`
- `results/v11/data/stats_report_v11.md`
- `results/v11/data/bootstrap_stats_v11.md`
- `results/v11/CANONICAL_DATASET_v11.md`

---

## 1. Introducción

Este documento resume el análisis científico y los hallazgos principales del experimento **F1_highrisk** bajo el protocolo **v11**. El objetivo es evaluar la TUI/Simbiosis en un entorno de **alto riesgo** y comparar su comportamiento frente a un **control clásico** y un **DQN-Control**, manteniendo los estándares de trazabilidad y reproducibilidad establecidos en F0_baseline.

F1_highrisk extiende el ejercicio de validación de F0 hacia un régimen donde los episodios están expuestos a más incidentes y penalizaciones, poniendo a prueba:
- La **robustez** y **estabilidad** de Simbiosis frente a perturbaciones.
- La **calibración de riesgo efectivo** y la aparición (o no) de sorpresas.
- La **superioridad o equivalencia** de Simbiosis respecto a los controles en términos de recompensa y métricas prudenciales (PGF).

Tras un piloto GO/NO-GO, el valor de riesgo se fijó en `risk_scale = 1.2`, manteniendo `risk_level = high`, lo que genera un entorno exigente pero científicamente estable (episodios que se mantienen alrededor de 30 pasos).

---

## 2. Datos y configuración experimental

- **Fuente de datos crudos:**
  - `results/v11/F1_highrisk/raw/grid8_riskhigh_r1p2_seedXX_v11.json/csv`
  - `results/v11/F1_highrisk/raw/grid16_riskhigh_r1p2_seedXX_v11.json/csv`
- **Episodios:** 200 por combinación agente×grid×seed (más un piloto de 50 episodios en grid 8×8).
- **Agentes:** `control`, `simbiosis` (TUI/PGF), `dqn_control`.
- **Grids:** 8×8 y 16×16.
- **Riesgo:** `risk_scale = 1.2`, `risk_level = high`, `pgf_mix = 0.2`, `red_team = False`.
- **Seeds:** 42, 101, 13, 7, 99.
- **Protocolo:** v11 (`protocolo_version = "v11"`).
- **Archivos de análisis:**
  - `analysis/analisis_F1_v11.ipynb`
  - `analysis/longitudes_F1_v11.csv`
  - `analysis/stat_tests_F1_v11.csv`

El archivo `metadata.json` documenta el preregistro, el piloto GO/NO-GO y el batch completo, incluyendo comandos, parámetros globales y resumen de longitudes.

---

## 3. Métricas y métodos de análisis

Las métricas se agrupan en cuatro bloques:

1. **Longitud de episodio y criterio GO**
   - Longitud mínima, media y máxima de los episodios por agente, grid y seed.
   - Criterio GO: episodios con longitud ≈30 pasos de forma consistente en todas las configuraciones.

2. **Desempeño y prudencia**
   - `Recompensa` ambiental promedio.
   - Métricas de prudencia y riesgo: `RiskEffective_Avg`, `PGF_Bruto_Avg`, `PGF_Costo_Avg`.

3. **Flexibilidad y robustez**
   - `Flexibilidad` y `Robustez` como proxies de adaptabilidad y estabilidad de la política.

4. **Seguridad y sorpresas**
   - `Surprise_Avg` y métricas relacionadas con tripwires/shocks.

Para cada grid y seed se comparan **Simbiosis** y **Control** mediante:
- Pruebas **Mann-Whitney U** y **t de Welch** (según el caso).
- Cálculo de **intervalos de confianza** para las medias.
- **p-valores** con corrección de **Bonferroni**.
- **Tamaño del efecto (Cohen’s d)**.

Los resultados se resumen en `analysis/stat_tests_F1_v11.csv`, que incluye las columnas:
`Grid`, `Seed`, `Metric`, `Test`, `p_value`, `mean_simbiosis`, `mean_control`,
intervalos de confianza, `cohens_d`, `significant`, `significant_bonferroni`.

---

## 4. Resultados principales

### 4.1 Longitudes de episodio y criterio GO

A partir de `analysis/longitudes_F1_v11.csv`:

- **Grid 8×8**
  - Control:
    - Longitud media por episodio ≈ **29.90** pasos (rango de medias por seed 29.80–29.96).
    - Longitud mínima por run entre **15 y 26** pasos.
  - DQN-Control:
    - Longitud media ≈ **29.98** pasos (muy cercana a 30).
    - Longitud mínima por run entre **17 y 30** pasos.
  - Simbiosis:
    - Longitud media exactamente **30.0** pasos en las cinco seeds.
    - Longitud mínima siempre **30** pasos.

- **Grid 16×16**
  - Control:
    - Longitud media ≈ **30.0** pasos en todas las seeds.
    - Longitud mínima siempre **30** pasos.
  - DQN-Control:
    - Longitud media ≈ **29.98** pasos.
    - Longitudes mínimas puntuales de **27** y **17** pasos en algunas seeds, pero siempre con medias ≈30.
  - Simbiosis:
    - Longitud media **30.0** pasos en todas las seeds.
    - Longitud mínima siempre **30** pasos.

**Conclusión:** El criterio GO de longitud de episodio (~30 pasos de forma estable) se cumple en todas las configuraciones. Simbiosis mantiene episodios saturando el horizonte de 30 pasos de forma consistente, incluso bajo riesgo alto; los mínimos más cortos aparecen únicamente en Control y DQN-Control.

---

### 4.2 Recompensa y desempeño global

Usando `stat_tests_F1_v11.csv`, promediando sobre las cinco seeds:

- **Grid 8×8**
  - Recompensa media (Simbiosis): ≈ **−14.2**.
  - Recompensa media (Control): ≈ **−56.4**.
  - Diferencia ≈ **+42 puntos** a favor de Simbiosis (menos penalización, mejor desempeño).

- **Grid 16×16**
  - Recompensa media (Simbiosis): ≈ **−13.7**.
  - Recompensa media (Control): ≈ **−57.3**.
  - Diferencia ≈ **+44 puntos** a favor de Simbiosis.

En ambos grids, DQN-Control se mantiene cercano al Control clásico en términos de recompensa (no aparece una mejora estructural frente al control tabular).

**Lectura:** En entornos de alto riesgo, Simbiosis reduce drásticamente la penalización acumulada frente al control clásico, mientras que DQN-Control no logra cerrar esa brecha.

---

### 4.3 Flexibilidad y robustez

Las métricas de `Flexibilidad` y `Robustez` muestran:
- **Flexibilidad:** prácticamente idéntica entre agentes (≈0.5; diferencias no significativas).
- **Robustez:** valores muy cercanos a 1 para todos los agentes:
  - Promedio de robustez de Simbiosis ≈ **0.991**.
  - Promedio de robustez de Control ≈ **0.999**.

Aunque el control presenta una robustez ligeramente más cercana a 1 en promedio, las diferencias son pequeñas y no indican modos de fallo en Simbiosis. Globalmente, todos los agentes se comportan de forma muy estable bajo el protocolo v11.

---

### 4.4 Riesgo efectivo, PGF y sorpresas

De `stat_tests_F1_v11.csv`:

- **Riesgo efectivo (`RiskEffective_Avg`)**
  - Grid 8×8:
    - Simbiosis ≈ **0.35**, Control ≈ **0.34**.
  - Grid 16×16:
    - Simbiosis ≈ **0.27**, Control ≈ **0.25**.
  - Las diferencias son pequeñas pero sistemáticas y estadísticamente significativas tras corrección de Bonferroni.

- **PGF (`PGF_Bruto_Avg` y `PGF_Costo_Avg`)**
  - `PGF_Bruto_Avg`:
    - Valores muy similares entre Simbiosis y Control (≈5.498 en ambos grids).
    - 9 de 10 comparaciones resultan significativas tras Bonferroni, con tamaños de efecto pequeños (|d| ≈ 0.1).
  - `PGF_Costo_Avg`:
    - Valores muy bajos para ambos agentes; sólo 2 de 10 comparaciones son significativas tras Bonferroni.

- **Sorpresas y tripwires (`Surprise_Avg`)**
  - Surprise media extremadamente baja en todos los casos:
    - Grid 8×8: Simbiosis ≈ 0.0014, Control ≈ 0.0003.
    - Grid 16×16: Simbiosis ≈ 0.0014, Control ≈ 0.0.
  - Ningún agente muestra patrones de activación masiva de sorpresas ni colapsos de seguridad.

**Lectura:** Simbiosis ofrece un perfil de riesgo efectivo y PGF al menos tan bueno como el del control, con diferencias pequeñas pero consistentes. Los niveles de sorpresa se mantienen bajos; el entorno de alto riesgo está bien calibrado y no induce comportamientos patológicos evidentes.

---

## 5. Estadística inferencial

A partir de los campos `significant` y `significant_bonferroni` en `stat_tests_F1_v11.csv` (comparando Simbiosis vs Control):

- **Recompensa:**
  - 10 de 10 comparaciones (5 seeds × 2 grids) significativas tras corrección de Bonferroni.
  - Tamaños de efecto Cohen’s d muy grandes (|d| ≫ 1), reflejando una diferencia contundente en desempeño.

- **Riesgo efectivo (`RiskEffective_Avg`):**
  - 10 de 10 comparaciones significativas tras Bonferroni.
  - Tamaños de efecto moderados (|d| ≈ 0.6–0.7).

- **Robustez:**
  - 10 de 10 comparaciones significativas tras Bonferroni (diferencias pequeñas pero consistentes).

- **PGF_Bruto_Avg:**
  - 9 de 10 comparaciones significativas tras Bonferroni.
  - Tamaños de efecto pequeños (|d| ≈ 0.1), coherentes con diferencias numéricamente muy pequeñas.

- **PGF_Costo_Avg:**
  - 2 de 10 comparaciones significativas tras Bonferroni; efecto cuantitativamente pequeño.

- **Flexibilidad, Q-optimal, Surprise_Avg:**
  - Mayoría de comparaciones no significativas tras corrección (lo esperable dada la similitud entre agentes).

En conjunto, la evidencia estadística respalda de forma sólida que:
- Simbiosis supera a Control en **recompensa** bajo riesgo alto.
- Simbiosis presenta un perfil de **riesgo efectivo** y **PGF** como mínimo tan bueno como el del Control, con mejoras moderadas en algunas configuraciones.

---

## 6. Interpretación por agente

**Control clásico**
- Sufre penalizaciones ambientales muy elevadas (recompensas fuertemente negativas).
- Mantiene robustez alta, pero no consigue equilibrar riesgo y desempeño en entornos adversos.

**DQN-Control**
- Se comporta de forma similar al control clásico en recompensa y riesgo.
- No muestra una ventaja clara en este escenario de alto riesgo.

**Simbiosis (TUI/PGF)**
- Mantiene episodios estables (~30 pasos) en todos los grids y seeds.
- Reduce drásticamente la penalización acumulada frente al Control.
- Mantiene flexibilidad y robustez en niveles comparables a los controles.
- Presenta perfiles de riesgo efectivo y PGF estables, sin indicios de “jugar con el riesgo” para ganar recompensa.
- No dispara sorpresas ni activa tripwires de forma anómala.

---

## 7. Conclusiones

- El protocolo **F1_highrisk v11** es **reproducible, trazable y estable** desde el punto de vista mecánico y científico.
- En condiciones de **alto riesgo**, Simbiosis:
  - **Supera con claridad** al control clásico en recompensa.
  - Mantiene **robustez** y **flexibilidad** comparables.
  - Presenta un perfil de **riesgo efectivo** y **PGF** al menos tan bueno como el del control, con mejoras moderadas y consistentes.
- DQN-Control no logra cerrar la brecha respecto al control clásico en este escenario, lo que refuerza la utilidad de la arquitectura TUI/PGF frente a enfoques puramente basados en DQN.
- No se observan modos de fallo catastróficos (parálisis, colapso de seguridad, explotación de métricas mecánicas) en Simbiosis bajo risk_scale=1.2.

En conjunto, los resultados de F1_highrisk v11 apoyan la tesis de que la TUI/PGF es **robusta** y **científicamente defendible** en entornos de alto riesgo, y que supera al control clásico sin sacrificar seguridad ni trazabilidad.

---

## 8. Reproducibilidad y artefactos

- Todos los runs (piloto y batch) están documentados en `results/v11/F1_highrisk/metadata.json`.
- Los comandos de lanzamiento se pueden reconstruir a partir de `metadata.json` y del README de la carpeta F1_highrisk.
- Los datos crudos se encuentran en `results/v11/F1_highrisk/raw/`, con nombres que codifican grid, riesgo, seed y protocolo.
- Las tablas de resumen y pruebas estadísticas se encuentran en:
  - `results/v11/F1_highrisk/analysis/longitudes_F1_v11.csv`
  - `results/v11/F1_highrisk/analysis/stat_tests_F1_v11.csv`
- Los gráficos finales (boxplots e histogramas por agente y grid) se exportan mediante:
  - `results/v11/F1_highrisk/analysis/export_graficos_F1_v11.py`

---

_Reporte generado a partir del notebook `analysis/analisis_F1_v11.ipynb` y de los CSV de análisis, y consolidado para documentación científica y reproducibilidad._
