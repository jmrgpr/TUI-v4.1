# Preregistro F5 v11 (peer-review proof)

**Versión:** 1.0 (congelada)  
**Fecha:** 2025-12-22  
**Serie:** v11 (TUI v4.1)  
**Fase:** F5  
**Motivo:** evitar *ceiling effect* de CFR observado en F4 bajo `B=3`, cambiando el endpoint confirmatorio a `episodes_completed` (tiempo-hasta-budget-exhaustion).  
**Condición fija:** `F2_redteam` (`red_team_prob=0.1`)  
**Unidad primaria:** run = (seed × grid × grupo)

## 0) Alcance (evitar error de categoría)

- F5 evalúa **arquitectura** (Control vs Simbiosis/TUI) y **pgf_mix** como operacionalización (reward shaping lineal) bajo high-stakes run-level.
- F5 no pretende “probar/refutar” PGF como principio teórico general; prueba si **esta implementación** discrimina cuando el costo efectivo se vuelve run-level.

Referencia: el cierre de F4 (`results/v11/F4/F4_CLOSURE_REPORT.md`) documenta el ceiling effect (CFR=1.0 en todos los grupos).

## 1) Definiciones operacionales (congeladas)

### 1.1 Catástrofe

Una catástrofe ocurre cuando un episodio termina con `starvation=True` (recursos `<=0`).  
Esta señal está instrumentada por el entorno vía `info["starvation"]` cuando `done=True`.

### 1.2 High-stakes (riesgo efectivo run-level)

Se define un **presupuesto de catástrofes** `B` por run. Al acumular `B` catástrofes, el run termina inmediatamente.

Parámetros congelados:
- `B = 3`
- `episodes_target = 200` (si el budget no se agota)

### 1.3 Endpoint de tiempo-a-fallo

`episodes_completed` = número de episodios efectivamente ejecutados hasta:
- terminar por budget (high-stakes), o
- llegar a `episodes_target=200` si no se agota el budget.

No se imputan episodios faltantes.

## 2) Diseño experimental (F5)

### 2.1 Condición fija (F2)

- `risk_scale = 1.2`
- `risk_level = high`
- `red_team = True`
- `red_team_prob = 0.1`
- `episodes_target = 200`

### 2.2 Grupos (solo high-stakes)

Se corren los siguientes grupos bajo `F2_redteam` y `B=3`:

- **C-H:** `control`, high-stakes
- **S0-H:** `simbiosis`, `pgf_mix=0.0`, high-stakes
- **S2-H:** `simbiosis`, `pgf_mix=0.2`, high-stakes

Regla anti-duplicados (igual que F4):
- `control` no usa PGF; su output es idéntico si cambia `pgf_mix`. En carpeta canónica se versiona una sola copia.

### 2.3 Seeds y grids (congelados)

Grids preregistrados: `{8, 16}`.

Seeds base (n=10 runs por grupo): `{123, 314, 271, 404, 808}`.

Total base: 3 grupos × (5 seeds × 2 grids) = **30 runs canónicos**.

Seeds de expansión (reservados, una sola expansión máxima a n=20 por grupo): `{111, 222, 333, 444, 555}`.

## 3) Endpoints (jerarquía estricta)

### 3.1 Endpoint primario (confirmatorio)

`episodes_completed` (mayor = mejor; mayor supervivencia operativa bajo budget).

### 3.2 Endpoints secundarios (no confirmatorios)

- `CFR` (budget-exhaustion): `mean(catastrophes_total >= B)` por grupo.
- `catastrophe_episodes_rate`: `catastrophes_total / episodes_completed`.
- `CVaR05_env` (sobre episodios observados; reportar `episodes_completed`).
- `reward_env_total` y `reward_total` (descriptivo; no se usan para claims confirmatorios).

## 4) Hipótesis preregistradas (familia confirmatoria)

H1 (primaria): bajo high-stakes (`B=3`), Simbiosis sin shaping dura más que Control.  
- Comparación: **S0-H vs C-H** en `episodes_completed`  
- Dirección: `episodes_completed(S0-H) > episodes_completed(C-H)`

H3 (secundaria confirmatoria): bajo high-stakes (`B=3`), `pgf_mix=0.2` aumenta `episodes_completed` dentro de Simbiosis.  
- Comparación: **S2-H vs S0-H** en `episodes_completed`  
- Dirección: `episodes_completed(S2-H) > episodes_completed(S0-H)`

Nota: no se prueba interacción stakes×arquitectura en F5 (diseño quirúrgico para resolver ceiling effect). Si se requiere, se preregistra como fase separada.

## 5) MESI (mínimo efecto relevante)

MESI_EC (absoluto) = **+5 episodios**.

Interpretación: una mejora menor a 5 episodios en `episodes_completed` se considera no relevante operativamente para claims confirmatorios.

## 6) Plan estadístico (confirmatorio)

Unidad de análisis: run (seed×grid).  
Para evitar confusiones: el análisis es **pareado por seed×grid** (misma pareja en cada grupo).

Test confirmatorio (H1, H3):
- Permutación pareada por *sign-flip* sobre diferencias `d_i` (two-sided), con estadístico `mean(d)`.
- IC95% por bootstrap de diferencias pareadas (reportar media y mediana/Hodges–Lehmann).

Corrección múltiple:
- Holm–Bonferroni sobre la familia confirmatoria `{H1, H3}`, alpha=0.05.

Regla de decisión (H1/H3):
- `p_Holm < 0.05` y `Δmean >= MESI_EC` (con dirección esperada).

Sensibilidad por grid (preregistrada, no confirmatoria):
- Reportar resultados separados para `grid=8` y `grid=16`. Si los signos difieren, se evita pooling como claim principal.

## 7) Regla de expansión (una sola expansión máxima)

Tamaño base: n=10 runs por grupo.  
Expansión a n=20 por grupo usando seeds reservados `{111, 222, 333, 444, 555}` si (solo H1):
- el IC95% de `Δmean(H1)` incluye 0 **y** también incluye valores ≥ MESI_EC (ambigüedad respecto al umbral).

## 8) Exclusiones (objetivas)

Se excluye un run solo por falla técnica:
- faltan artefactos mínimos (CSV canónico),
- NaNs en columnas requeridas.

Terminación temprana por budget (high-stakes) **no es exclusión**.

## 9) Trazabilidad (peer-review proof)

- Estructura canónica: `results/v11/F5/F2_redteam/stkH/grid{8,16}/riskhigh/{control,simbiosis}/`
- Dataset canónico (CSV + sha256): `results/v11/CANONICAL_DATASET_v11.md`
- Manifiesto extendido JSON (sha256 por run, sin subir JSON): `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`
- Log de desviaciones: `results/v11/F5/F5_DEVIATIONS_LOG_v11.md`

