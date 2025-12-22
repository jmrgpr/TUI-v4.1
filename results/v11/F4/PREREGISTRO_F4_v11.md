# Preregistro F4 v11 (peer-review proof)

**Fecha:** 2025-12-22  
**Serie:** v11 (TUI v4.1) → puente a v12  
**Fase:** F4  
**Condición fija:** `F2_redteam` (estrés adversarial sintético; `red_team_prob=0.1`)  
**Unidad primaria:** run = (seed × grid × grupo)  

## 0) Alcance (evitar error de categoría)

- F4 evalúa **pgf_mix** como una *operacionalización* (reward shaping lineal) y su interacción con stakes altos.
- F4 **no** pretende “probar/refutar” PGF como principio teórico general; solo prueba si esta implementación (pgf_mix) se vuelve útil cuando el costo de catástrofe aumenta.

## 1) Motivación (por qué F4)

En F3, la ablación `pgf_mix=0.2` vs `pgf_mix=0.0` no alteró `reward_env_total` bajo el protocolo v11 (trayectorias ambientales invariantes por seed×grid×condición), aunque `reward_total` sí cambió (shaping activo).  
F4 introduce una sola palanca causal nueva: **stakes altos** mediante una penalización adicional *solo* cuando ocurre catástrofe (muerte por inanición / `starvation`), para probar si el shaping lineal adquiere valor cuando el riesgo efectivo es alto.

## 2) Definiciones operacionales

### 2.1 Catástrofe

Un episodio es **catastrófico** si termina con `starvation=True` (recursos `<=0`). Esta señal ya está instrumentada por el entorno (`info['starvation']`).

### 2.2 Stakes (tensión de riesgo efectiva)

Se implementa como un parámetro `catastrophe_penalty` que se suma a la recompensa del episodio **solo si** el episodio termina por catástrofe.

- **Low stakes (`stkL`)**: `catastrophe_penalty = 0.0`
- **High stakes (`stkH`)**: `catastrophe_penalty = -300.0`

Notas:
- Esta palanca no cambia reglas del entorno ni el red team; solo aumenta el costo del evento de muerte (catástrofe).
- El valor exacto se congela aquí; cualquier cambio exige registrar adenda antes de correr.

## 3) Diseño experimental

### 3.1 Condición fija (F2)

- `risk_scale = 1.2`
- `risk_level = high`
- `red_team = True`
- `red_team_prob = 0.1`
- `episodes = 200` por run

### 3.2 Grupos (2×2 dentro de Simbiosis + Control)

Se corren los siguientes grupos bajo `F2_redteam`:

- **C-L**: Control (baseline), `stkL`
- **C-H**: Control (baseline), `stkH`
- **S0-L**: Simbiosis, `pgf_mix=0.0`, `stkL`
- **S0-H**: Simbiosis, `pgf_mix=0.0`, `stkH`
- **S2-L**: Simbiosis, `pgf_mix=0.2`, `stkL`
- **S2-H**: Simbiosis, `pgf_mix=0.2`, `stkH`

Regla anti-duplicados para publicación:
- Los baselines (`control`) son idénticos dentro de un mismo stakes si `pgf_mix` cambia (porque `control` no usa PGF). En la carpeta canónica se versiona una sola copia por stakes (organización tipo F3).

### 3.3 Seeds y grids (congelados)

- Seeds preregistrados: `{42, 101, 13, 7, 99}`
- Grids preregistrados: `{8, 16}`
- Runs por grupo: 10 (5 seeds × 2 grids)

## 4) Endpoints (jerarquía estricta)

### 4.1 Endpoint primario (confirmatorio)

**CFR_run (Catastrophic Failure Rate a nivel run):**  
Para cada run, definir `catastrophe_run = 1` si **existe ≥1 episodio** con `starvation=1`, y `0` en caso contrario.  
El endpoint por grupo es `mean(catastrophe_run)` sobre runs (0 a 1).

Motivo: es el claim más limpio para “alto stakes = supervivencia”.

### 4.2 Endpoints secundarios (confirmatorios, limitados)

- `catastrophe_episodes_rate`: proporción de episodios con `starvation=1` dentro de cada run (y promedio por grupo).
- `reward_env_total`: (solo descriptivo comparativo; no se usa para claims de nulidad/causalidad del PGF teórico).
- `reward_total`: para verificar activación del shaping (debe cambiar con `pgf_mix`).

### 4.3 Exploratorios (sin claims confirmatorios)

- CVaR05_env, max_drawdown_env, señales mecánicas (`risk_effective`, `surprise`, shocks/tripwires).

## 5) Hipótesis preregistradas

H1 (primaria — nicho de robustez bajo stakes altos)  
- Comparación: **S0-H vs C-H** en `CFR_run`  
- Dirección esperada: `CFR_run(S0-H) < CFR_run(C-H)`

H2 (secundaria — utilidad de pgf_mix bajo stakes altos)  
- Comparación: **S2-H vs S0-H** en `CFR_run`  
- Dirección esperada: `CFR_run(S2-H) < CFR_run(S0-H)`

H3 (secundaria — expected null en low stakes)  
- Comparación: **S2-L vs S0-L** en `CFR_run`  
- Dirección esperada: diferencia pequeña; se evaluará por equivalencia (ver MESI).

## 6) MESI y equivalencia (nulos fuertes)

### 6.1 MESI primario (CFR)

MESI_CFR (absoluto) = **0.20** (20 puntos porcentuales).  
Interpretación: una reducción menor a 0.20 en `CFR_run` se considera no relevante operativamente para claims confirmatorios.

### 6.2 Equivalencia (TOST) para H3

Equivalencia si el efecto cae dentro de ±MESI_CFR.

## 7) Plan estadístico (confirmatorio)

Unidad de análisis: run (seed×grid).

- Para `CFR_run`: reportar Δ de proporciones (A−B) + IC95% (bootstrap por run) y test exacto (Fisher) o permutación (dos colas).
- Corrección múltiple: Holm–Bonferroni sobre la **familia primaria** {H1, H2, H3} con α=0.05.
- Decisión para H1/H2: `p_Holm < 0.05` y `|Δ| ≥ MESI_CFR` (con dirección esperada).
- Decisión para H3 (equivalencia): TOST dentro de ±MESI_CFR (reportar explícitamente “equivalente” o “inconcluso”).

Sensibilidad por grid (preregistrada):
- Reportar también por separado `grid=8` y `grid=16`. Si los signos son opuestos, se evita pooling como claim principal.

## 8) Poder y regla de expansión (una sola expansión máxima)

Tamaño base: n=10 runs por grupo.

Seeds de expansión (reservados): `{123, 314, 271, 404, 808}` → n=20 por grupo si se activa.

Regla de expansión (solo para H1):
- Expandir si el IC95% de Δ en H1 incluye 0 **y** también incluye mejoras ≥ MESI_CFR (ambigüedad respecto al umbral).

## 9) Exclusiones (objetivas)

Se excluye un run solo por falla técnica:
- faltan artefactos mínimos (CSV canónico del run),
- NaNs en columnas requeridas,
- truncamiento: `<190` episodios cuando se esperan 200.

## 10) Trazabilidad (peer-review proof)

- Separación física por stakes (evita mezcla): `results/v11/F4/F2_redteam/stkL/` y `.../stkH/`.
- CSV canónicos con sha256: `results/v11/CANONICAL_DATASET_v11.md`.
- JSON no se versionan; se publican hashes por run: `results/v11/CANONICAL_DATASET_EXTENDED_JSON.md`.
- Deviations log: `results/v11/F4/F4_DEVIATIONS_LOG_v11.md`.
