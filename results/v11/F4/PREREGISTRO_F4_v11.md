# Preregistro F4 v11 (peer-review proof)

**Versión:** 1.1 (Adenda 01 integrada)  
**Fecha:** 2025-12-22  
**Serie:** v11 (TUI v4.1) → puente a v12  
**Fase:** F4  
**Condición fija:** `F2_redteam` (estrés adversarial sintético; `red_team_prob=0.1`)  
**Unidad primaria:** run = (seed × grid × grupo)  

## 0) Alcance (evitar error de categoría)

- F4 evalúa `pgf_mix` como **operacionalización** (reward shaping lineal) y su interacción con stakes/“riesgo efectivo”.
- F4 no pretende “probar/refutar” PGF como principio teórico general; solo prueba si esta implementación de shaping se vuelve útil bajo stakes altos.

Documento de cambios: `results/v11/F4/F4_ADENDA_01.md`.

## 1) Motivación

En F3, la ablación `pgf_mix=0.2` vs `pgf_mix=0.0` no alteró `reward_env_total` bajo el protocolo v11 (trayectorias ambientales invariantes por seed×grid×condición), aunque `reward_total` sí cambió (shaping activo).  
F4 introduce una sola palanca causal nueva: **stakes a nivel run** (presupuesto de catástrofes) para evitar que un entorno reseteable “amortice” catástrofes a lo largo de 200 episodios.

## 2) Definiciones operacionales

### 2.1 Catástrofe

Una catástrofe ocurre cuando un episodio termina con `starvation=True` (recursos `<=0`).  
Esta señal está instrumentada por el entorno vía `info["starvation"]` cuando `done=True`.

### 2.2 Stakes (riesgo efectivo a nivel run)

Se define un **presupuesto de catástrofes** `B` por run:

- **Low-stakes (baseline v11):** el run ejecuta `episodes_target=200` episodios independientemente del número de catástrofes (no hay corte por budget).
- **High-stakes (run-level budget):** al acumular `B` catástrofes, el run termina inmediatamente.

Parámetros congelados:
- `B = 3` (presupuesto primario).
- `episodes_target = 200` (si el budget no se agota).

No se imputan episodios faltantes en endpoints continuos; se reporta explícitamente `episodes_completed`.

## 3) Diseño experimental (F4)

### 3.1 Condición fija (F2)

- `risk_scale = 1.2`
- `risk_level = high`
- `red_team = True`
- `red_team_prob = 0.1`
- `episodes_target = 200` por run

### 3.2 Grupos (Control vs Simbiosis, con y sin pgf_mix)

Se corren los siguientes grupos bajo `F2_redteam`:

- **C-L:** `control`, low-stakes
- **C-H:** `control`, high-stakes (`B=3`)
- **S0-L:** `simbiosis`, `pgf_mix=0.0`, low-stakes
- **S0-H:** `simbiosis`, `pgf_mix=0.0`, high-stakes (`B=3`)
- **S2-L:** `simbiosis`, `pgf_mix=0.2`, low-stakes
- **S2-H:** `simbiosis`, `pgf_mix=0.2`, high-stakes (`B=3`)

Regla anti-duplicados para publicación (igual que F3):
- Los baselines (`control`) son idénticos dentro de un mismo stakes si `pgf_mix` cambia (porque `control` no usa PGF). En la carpeta canónica se versiona una sola copia por stakes.

### 3.3 Seeds y grids (congelados)

- Seeds preregistrados: `{42, 101, 13, 7, 99}`
- Grids preregistrados: `{8, 16}`
- Runs por grupo: 10 (5 seeds × 2 grids)

## 4) Endpoints (jerarquía estricta)

### 4.1 Endpoint primario (confirmatorio): CFR (budget-exhaustion)

Para cada run, calcular:
- `catastrophes_total`: número de episodios con `starvation=1`.
- `budget_exhausted`: indicador `catastrophes_total >= B` (con `B=3`).

**CFR** (Catastrophic Failure Rate) por grupo = `mean(budget_exhausted)` sobre runs.

Nota: en high-stakes, `budget_exhausted` implica terminación por budget. En low-stakes, `budget_exhausted` se interpreta como “agotaría el budget” dentro de 200 episodios (sin cortar el run).

### 4.2 Endpoints secundarios

- `episodes_completed`: episodios ejecutados en el run (≤200; variable en high-stakes).
- `catastrophe_episodes_rate`: `catastrophes_total / episodes_completed`.
- `CVaR05_env`: calculado sobre episodios observados; se reporta explícitamente `episodes_completed` usado.
- `reward_env_total` y `reward_total`: secundarios/descriptivos.

## 5) Hipótesis preregistradas (familia confirmatoria)

H1 (primaria): en high-stakes (`B=3`), Simbiosis (sin shaping) es más robusta que Control.  
- Comparación: **S0-H vs C-H** en CFR  
- Dirección esperada: `CFR(S0-H) < CFR(C-H)`

H2 (interacción): la diferencia Simbiosis vs Control en CFR es mayor en high-stakes que en low-stakes.  
- Contraste: `(CFR(S0-H) − CFR(C-H)) < (CFR(S0-L) − CFR(C-L))`

H3 (secundaria): en high-stakes (`B=3`), `pgf_mix=0.2` reduce CFR dentro de Simbiosis.  
- Comparación: **S2-H vs S0-H** en CFR  
- Dirección esperada: `CFR(S2-H) < CFR(S0-H)`

## 6) MESI para CFR

MESI_CFR (absoluto) = **0.20** (20 puntos porcentuales).  
Interpretación: una reducción menor a 0.20 en CFR se considera no relevante operativamente para claims confirmatorios.

Se reportará adicionalmente la reducción relativa como descriptivo/exploratorio.

## 7) Plan estadístico (confirmatorio)

Unidad de análisis: run (seed×grid).

- Para comparaciones binarias (H1, H3): Fisher exact (2-sided) + ΔCFR con IC95%.
- Para H2 (interacción): estimar el contraste por diferencia-de-diferencias y reportar IC95% por bootstrap a nivel run; el p-value se obtiene por permutación simple (re-etiquetado por grupo dentro de cada stakes), o se marca como “inconcluso” si no se implementa sin ambigüedad.
- Corrección múltiple: Holm–Bonferroni sobre {H1, H2, H3}, α=0.05.
- Regla de decisión (H1/H3): `p_Holm < 0.05` y `|ΔCFR| ≥ MESI_CFR` (con dirección esperada).

Sensibilidad por grid (preregistrada):
- Reportar también `grid=8` y `grid=16`. Si los signos son opuestos, se evita pooling como claim principal.

## 8) Regla de expansión de n (una sola expansión máxima)

Tamaño base: n=10 runs por grupo.  
Seeds de expansión (reservados): `{123, 314, 271, 404, 808}` → n=20 por grupo.

Regla de expansión (solo H1):
- Expandir si el IC95% de `ΔCFR(H1)` incluye 0 **y** también incluye efectos favorables ≥ MESI_CFR (ambigüedad respecto al umbral).

## 9) Exclusiones (objetivas)

Se excluye un run solo por falla técnica:
- faltan artefactos mínimos (CSV canónico del run),
- NaNs en columnas requeridas.

Importante:
- En **low-stakes**, `episodes_completed` debe ser 200; si es menor por fallo técnico, se registra como excluido y se re-ejecuta.
- En **high-stakes**, `episodes_completed` puede ser <200 por budget; esto **no es truncamiento técnico**.

## 10) Trazabilidad (peer-review proof)

- Separación física por stakes: `results/v11/F4/F2_redteam/stkL/` y `results/v11/F4/F2_redteam/stkH/`.
- CSV canónicos con sha256: `results/v11/CANONICAL_DATASET_v11.md`.
- JSON no se versionan; se publican hashes por run: `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`.
- Deviations log: `results/v11/F4/F4_DEVIATIONS_LOG_v11.md`.
