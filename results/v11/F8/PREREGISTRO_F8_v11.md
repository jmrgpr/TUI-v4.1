# PREREGISTRO_F8_v11 — Replicación “quirúrgica” (H1-only) para cierre de v11 (CFR, high-stakes `B*=40`)

**Versión:** 1.0 (congelada)  
**Fecha:** 2025-12-23  
**Serie:** v11 (post-errata; agente persistente)  
**Fase:** F8  
**Motivo:** en F7 se recuperó headroom real del endpoint CFR con `B*=40`, y H1 mostró señal consistente (ΔCFR≤-0.20) pero quedó “INCONCLUSIVE” por corrección Holm al incluir H3 (con m=2, Holm para el p más pequeño equivale a ~p×2: 0.03125→0.0625). F8 replica **solo** el claim primario de arquitectura (H1) con mayor n y una única familia confirmatoria (m=1) para cerrar v11 sin ambigüedad metodológica.

## 0) Alcance (evitar error de categoría)

- F8 evalúa **arquitectura** (Control vs Simbiosis/TUI) bajo stakes run-level usando CFR.
- F8 **no** pretende “probar/refutar” PGF como principio teórico general.
- `pgf_mix` no es claim confirmatorio en F8 (se trata como fuera de alcance / exploratorio si se ejecuta).

## 1) Definiciones operacionales (congeladas)

### 1.1 Catástrofe

Un episodio cuenta como catástrofe si termina con `done=True` y el entorno marca `info["starvation"] == True` (recursos <= 0).  
En `*_episodes.csv` se registra como columna `Starvation` (1/0).

### 1.2 High-stakes (riesgo efectivo run-level)

- Cada run tiene un presupuesto de catástrofes `B`.
- `episodes_target = 200` si el budget no se agota.
- Al acumular `B` catástrofes, el run termina inmediatamente.
- No se imputan episodios faltantes.

### 1.3 Indicador budget-exhaustion (para CFR)

`budget_exhausted = True` si el run termina por alcanzar `B` catástrofes antes de `episodes_target`.

### 1.4 Endpoint CFR (primario)

`CFR = mean(budget_exhausted)` a nivel run.  
Rango: [0, 1]. Menor = mejor.

## 2) Condición fija (sin nuevos diales)

Se mantiene la condición que ya evitó ceiling en F7:

- `condition = F2_redteam`
- `risk_scale = 1.2`
- `risk_level = high`
- `red_team = True`
- `red_team_prob = 0.03` (congelado)
- `B = 40` (congelado; “B*” de F7)

## 3) Diseño experimental

### 3.1 Grupos confirmatorios (H1-only)

- `C-H`: Control
- `S0-H`: Simbiosis, `pgf_mix=0.0`

> Nota: si se corre `pgf_mix=0.2` para obtener `S2-H`, se reporta como **exploratorio** y no entra en la familia confirmatoria.

### 3.2 Grids

`grids = {8, 16}` (pooled primario; sensibilidad por grid descriptiva).

### 3.3 Seeds y tamaño muestral

Unidad: run = seed×grid.

**Base (confirmatorio):**
- Seeds base (20): `{601..620}`  
- Runs por grupo: 20 seeds × 2 grids = **40 runs** por grupo.

**Expansión (una sola, preregistrada):**
- Seeds reservadas (10): `{621..630}`  
- Runs extra por grupo: 10 seeds × 2 grids = **+20 runs** por grupo → total **60 runs** por grupo.

## 4) Endpoints (jerarquía estricta)

### 4.1 Primario (confirmatorio)

- **CFR** por grupo.

### 4.2 Secundarios (no confirmatorios)

- `episodes_completed`
- `catastrophes_total`
- `catastrophe_episodes_rate`
- recompensas (solo descriptivo)

## 5) Hipótesis preregistradas (familia confirmatoria)

**H1 (única confirmatoria):** bajo high-stakes `B=40`, Simbiosis sin shaping falla menos que Control.

- Comparación: `S0-H` vs `C-H` en CFR  
- Dirección: `CFR(S0-H) < CFR(C-H)`

## 6) MESI (mínimo efecto relevante)

`MESI_CFR` (absoluto): `|ΔCFR| ≥ 0.20` (20 puntos porcentuales).  
Interpretación: diferencias < 0.20 se consideran no relevantes operativamente para claims confirmatorios.

## 7) Plan estadístico (confirmatorio)

Unidad: run (seed×grid).  
Emparejamiento: por seed×grid (misma semilla y grid para comparar grupos).

Test confirmatorio (H1):

- **McNemar exacto (2-sided)** sobre el indicador binario `budget_exhausted`, emparejado por seed×grid.

Se reporta además:

- `ΔCFR = mean(S0-H) - mean(C-H)` e IC95% por bootstrap sobre pares (descriptivo).

Corrección múltiple:

- No aplica (familia confirmatoria m=1).

Regla de decisión:

- **PASS** si `p < 0.05` y `ΔCFR ≤ -MESI_CFR` (dirección esperada).  
- Si no, se declara **INCONCLUSIVE** (sin forzar narrativa).

Sensibilidad por grid (no confirmatoria):

- Reportar CFR separado para grid=8 y grid=16.
- Si el signo difiere, evitar pooling como claim principal (se reporta como limitación).

## 8) Power plan + regla de expansión (una sola)

Racional: F7 (n=20 por grupo) mostró ΔCFR≈-0.30 con `p=0.03125` pero quedó “INCONCLUSIVE” por Holm al incluir H3. F8 incrementa n y usa H1-only para aumentar potencia y evitar el “casi-sí”.

Se activa expansión a n=60 por grupo (usando seeds reservadas) si, con n=40 por grupo:
- `ΔCFR` está en dirección esperada (`ΔCFR ≤ -0.15`) pero `p ≥ 0.05`, y
- no hay evidencia de fallo técnico sistemático.

## 9) Exclusiones (objetivas)

Se excluye un run solo por falla técnica:
- faltan artefactos mínimos, o
- NaNs/columnas requeridas ausentes en outputs.

Terminación por budget (high-stakes) **no** es exclusión; es parte del endpoint.

## 10) Trazabilidad (peer-review proof)

- Raw (local-only): `results/v11/F8/raw/`
- Organización canónica: `scripts/organize_F8_results.py` → `results/v11/F8/F2_redteam/stkH/rt*/grid{8,16}/riskhigh/{control,simbiosis}/`
- Log de desviaciones: `results/v11/F8/F8_DEVIATIONS_LOG_v11.md`
- Reporte preregistrado: `scripts/f8_preregistered_analysis_v11.py` → `results/v11/data/`
