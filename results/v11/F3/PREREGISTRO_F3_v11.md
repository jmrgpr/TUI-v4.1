# Preregistro F3 v11 (peer-review proof)

**Fecha:** 2025-12-19  
**Serie:** v11 (TUI v4.1)  
**Fase:** F3  
**Unidad primaria:** archivo por run (seed × grid)  
**Métrica primaria:** `reward_env_total`  

## 1) Motivación (por qué F3)
F2 mostró que `reward_total` puede reflejar reward shaping (mezcla PGF), y que comparaciones “justas” entre agentes requieren priorizar `reward_env_total` (derivado del JSON del run vía `reward_env_evol`). F3 preregistra comparaciones y reglas de auditoría para responder:
1) qué parte del efecto observado se debe a PGF (`pgf_mix`) vs al algoritmo, y
2) si existe mejora algorítmica cuando `pgf_mix=0.0` (sin shaping).

## 2) Preguntas e hipótesis (pre-registradas)

### P1 — Ablación PGF (impacto causal de `pgf_mix`)
**Pregunta:** En Simbiosis, ¿cambia `reward_env_total` al pasar de `pgf_mix=0.0` a `pgf_mix=0.2` bajo F1 y bajo F2?

**Hipótesis (2-sided):**
- H1a (F1): Δ(`reward_env_total`) ≠ 0 entre `pgf_mix=0.2` vs `pgf_mix=0.0`.
- H1b (F2): Δ(`reward_env_total`) ≠ 0 entre `pgf_mix=0.2` vs `pgf_mix=0.0`.

### P2 — Comparación justa (sin shaping)
**Pregunta:** Con `pgf_mix=0.0`, ¿Simbiosis mejora `reward_env_total` frente a `control` y `dqn_control` bajo F1 y bajo F2?

**Hipótesis (2-sided):**
- H2a (F1): `simbiosis(pgf_mix=0.0)` difiere de `control` en `reward_env_total`.
- H2b (F1): `simbiosis(pgf_mix=0.0)` difiere de `dqn_control` en `reward_env_total`.
- H2c (F2): `simbiosis(pgf_mix=0.0)` difiere de `control` en `reward_env_total`.
- H2d (F2): `simbiosis(pgf_mix=0.0)` difiere de `dqn_control` en `reward_env_total`.

## 3) Diseño experimental (pre-registrado)

### Agentes
- `control`
- `dqn_control`
- `simbiosis` con `pgf_mix ∈ {0.0, 0.2}` (comparaciones primarias)

### Condiciones (compatibles con v11)
- Condición F1 (alto riesgo): `risk_scale=1.2`, `risk_level=high`, `red_team=False`
- Condición F2 (estrés adversarial sintético): `risk_scale=1.2`, `risk_level=high`, `red_team=True`, `red_team_prob=0.1`

### Seeds y grids
- Seeds preregistrados: `{42, 101, 13, 7, 99}`
- Grids preregistrados: `{8, 16}`

### Episodios
- `episodes = 200` por ejecución (misma convención de v11).

### Unidad primaria y pooling
- Unidad primaria = un archivo por (seed, grid, agente, condición).
- **Pooling primario:** se reporta análisis principal “pooled” sobre `grid ∈ {8,16}` (n = seeds × grids por grupo/condición).
- **Sensibilidad (secundaria):** replicar el análisis por grid (8 y 16) como chequeo de robustez, sin cambiar conclusiones primarias.

## 4) Métricas (definiciones operacionales)

### Primaria
- `reward_env_total`: recompensa ambiental “pura”, derivada del JSON del run (campo `reward_env_evol`).

### Secundarias (reportadas, no primarias)
- `reward_total` (puede incluir mezcla PGF; se reporta siempre con disclaimer de shaping).
- Señales observables de estrés/ataque (según instrumentación del entorno): `avg_tripwire`, `avg_shocks`, `risk_effective`, `surprise` (y/o equivalentes disponibles).

### Métricas de cola/seguridad (secundarias)
- `CVaR05_env`: promedio del 5% peor de la distribución episodios de `reward_env` por run.
- `max_drawdown_env`: máxima caída acumulada en la serie temporal de `reward_env` por run.

Nota: en F3 estas métricas se consideran **exploratorias** (sin umbral confirmatorio preregistrado y sin claims primarios). Si se quieren usar para conclusiones confirmatorias en futuras series, se debe preregistrar un MESI específico y corrección múltiple.

## 5) Comparaciones primarias y corrección múltiple

### Family primaria (para control de error familiar)
Se define una única familia primaria sobre `reward_env_total` con **M = 6** comparaciones:
1. F1: `simbiosis(m=0.0)` vs `control`
2. F1: `simbiosis(m=0.0)` vs `dqn_control`
3. F2: `simbiosis(m=0.0)` vs `control`
4. F2: `simbiosis(m=0.0)` vs `dqn_control`
5. F1: `simbiosis(m=0.2)` vs `simbiosis(m=0.0)`
6. F2: `simbiosis(m=0.2)` vs `simbiosis(m=0.0)`

**Corrección:** Holm–Bonferroni, α = 0.05, 2-sided.

Todas las demás comparaciones (otros `pgf_mix`, otros endpoints) se reportan como secundarias/exploratorias (sin claims de significancia primaria).

## 6) Plan de análisis (pre-registrado)
- Estadísticos por grupo/condición: media y IC95% por bootstrap a nivel run (unidad primaria).
- Efecto: diferencia de medias (Δ) en `reward_env_total` con IC95%.
- p-valores: reportar p ajustado Holm (family primaria).
- Reporte mínimo: tablas pooled + tablas por grid (sensibilidad).

Implementación reproducible:
- Script: `scripts/f3_preregistered_analysis_v11.py`
- Salidas: `results/v11/data/f3_preregistered_report_v11.md` y `results/v11/data/f3_preregistered_stats_v11.csv`

## 7) MESI (efecto mínimo de interés) y regla de expansión de n
- MESI para `reward_env_total` (pooled): diferencia absoluta ≥ 5% del baseline `control` (referencia F1/F2).
- Si el IC95% de la métrica primaria es demasiado ancho para decidir el MESI, se permite expansión de n (nuevas seeds).
- Cualquier expansión debe registrarse **antes** de ver resultados completos, en `results/v11/F3/F3_DEVIATIONS_LOG_v11.md`.

## 8) Criterios de exclusión y stopping rule
Se excluyen runs únicamente por fallas técnicas:
- archivos corruptos/incompletos,
- NaNs en métrica primaria,
- runs truncados (menos de **190** episodios cuando el esperado es 200).

Stopping rule: se detiene al completar el n preregistrado por condición/grupo, salvo expansión preregistrada.

## 9) Trazabilidad y data availability (peer-review proof)
- CSV canónicos (hash sha256): `results/v11/CANONICAL_DATASET_v11.md`.
- JSON de runs NO se versionan por tamaño; se publica un manifiesto de hashes sha256 (sin subir JSON) para verificación independiente: `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`.
- Para F3, se debe regenerar y publicar el manifiesto extendido al cerrar la fase.

## 10) Estructura de salida (convención)
Mantener la estructura de F2 y separar físicamente por condición para evitar mezcla de outputs:
- `results/v11/F3/raw/F1_highrisk/` y `results/v11/F3/raw/F2_redteam/` (agregados por grid/seed).
- `results/v11/F3/F1_highrisk/grid{8,16}/riskhigh/{control,simbiosis,dqn_control}/` (por agente/seed).
- `results/v11/F3/F2_redteam/grid{8,16}/riskhigh/{control,simbiosis,dqn_control}/` (por agente/seed).
- `results/v11/F3/analysis/` (reportes/figuras; preferiblemente ignorar outputs pesados).

## 11) Regla de sensibilidad por grid (preregistrada)
El análisis primario es pooled (grids 8+16). Como sensibilidad se reporta por grid. Si los efectos por grid muestran **signos opuestos** para una comparación primaria, se reportan ambos grids por separado y se evita pooling para esa comparación (posible interacción grid×tratamiento).

## 12) Nota metodológica sobre la ablación PGF (clarificación)
`reward_env_total` está definido como recompensa ambiental derivada de `reward_env_evol` (JSON). Por diseño, el término PGF (`pgf_mix`) afecta directamente la métrica mezclada `reward_total` (shaping), pero **no** altera directamente `reward_env_total` salvo por efectos indirectos vía cambios de política. Por tanto, un resultado nulo en la ablación sobre `reward_env_total` es plausible y no implica que `pgf_mix` no se haya aplicado; debe corroborarse con sanity checks (config `pgf_mix` en JSON y cambios en `reward_total`), publicados en `results/v11/data/f3_preregistered_report_v11.md`.
