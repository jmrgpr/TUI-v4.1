# PREREGISTRO_F7_v11 — Budget calibration para des‑saturar CFR (high‑stakes)

**Versión:** 1.0 (congelada)  
**Fecha:** 2025-12-23  
**Serie:** v11 (post‑errata; agente persistente)  
**Fase:** F7  
**Motivo:** en F4/F6 el endpoint confirmatorio **CFR** saturó (≈1.0) bajo high‑stakes `B=3`. Tras corregir el ciclo de vida del agente (ver `results/v11/ERRATA_RUNNER_AGENT_LIFECYCLE.md`) y validar invariantes (RV2 PASS), F7 calibra **solo** el budget `B` para recuperar espacio de discriminación del CFR.

## 0) Alcance (evitar error de categoría)

- F7 evalúa arquitectura (Control vs Simbiosis/TUI) y `pgf_mix` como **operacionalización** (reward shaping lineal) bajo stakes run‑level.
- F7 **no** pretende “probar/refutar” PGF como principio teórico general.
- F7 existe por ceiling effect del endpoint CFR; no re‑abre F4–F6.

## 1) Definiciones operacionales (congeladas)

### 1.1 Catástrofe

Una catástrofe ocurre cuando un episodio termina con `done=True` y el entorno marca `info["starvation"] == True` (recursos <= 0).  
En `*_episodes.csv` se registra como columna `Starvation` (1/0).

### 1.2 High‑stakes (riesgo efectivo run‑level)

- Cada run tiene un presupuesto de catástrofes `B`.
- `episodes_target = 200` si el budget no se agota.
- Al acumular `B` catástrofes, el run termina inmediatamente.
- No se imputan episodios faltantes.

### 1.3 Indicador budget‑exhaustion (para CFR)

`budget_exhausted = True` si el run termina por alcanzar `B` catástrofes antes de `episodes_target`.

### 1.4 Endpoint CFR (primario en F7)

`CFR = mean(budget_exhausted)` a nivel run.  
Rango: [0, 1]. Menor = mejor (menor tasa de fracaso por budget).

## 2) Único factor nuevo en F7: budget `B` (calibrado)

Se calibra **solo** el budget `B`, manteniendo fija la severidad adversarial:

- `condition = F2_redteam`
- `risk_scale = 1.2`
- `risk_level = high`
- `red_team = True`
- `red_team_prob = 0.03` (congelado; valor conservador usado en RV2 y en el tie‑break de F6)

## 3) Diseño experimental (dos etapas)

### 3.1 Etapa A — Piloto de calibración de `B` (no confirmatoria)

**Objetivo:** elegir `B*` tal que `CFR_control(B*)` sea **no trivial** (ideal ~0.5; rango objetivo `[0.3, 0.7]`).

- Grupo en piloto: solo Control (`C-H`)
- Stakes: high (budget) con `B` variable
- Grid piloto: `grid=16`
- Seeds piloto (no reutilizados luego): `{9001, 9002, 9003, 9004, 9005}`
- Candidatos preregistrados: `B ∈ {3, 5, 10, 20, 40}`
- Runs por candidato: 5 (1 grid × 5 seeds)
- Total piloto: 5 candidatos × 5 runs = 25 runs

**Regla de selección de `B*` (determinística):**

1) Calcular `CFR_control(B)` en los 5 runs del piloto.  
2) Elegir el `B` cuyo `CFR_control(B)` esté más cerca de 0.5 y dentro de `[0.3, 0.7]`.  
3) Si ningún `B` cae en `[0.3, 0.7]`, elegir el `B` con `CFR_control(B)` más cercano a 0.5.  
4) Si hay empate, elegir el `B` más pequeño (más estricto).

**Criterio de STOP (preflight):**

Si para todos los candidatos `B`, `CFR_control(B)=1.0` (ceiling estructural), **STOP** y no proceder a confirmatorio. Esto indica que hay que redefinir catástrofe, horizonte o severidad basal.

**Salida del piloto (versionada):**

- JSON canónico de selección: `results/v11/F7/analysis/f7_pilot_selection_v11.json`
- Tabla piloto: `results/v11/data/f7_pilot_table_v11.csv`
- Reporte del piloto: `results/v11/data/f7_pilot_selection_v11.md`

Nota: el piloto no se usa para inferencia confirmatoria.

### 3.2 Etapa B — Confirmatoria (con `B*` fijo)

Una vez seleccionado `B*`, se corre el experimento confirmatorio:

**Grupos confirmatorios (high‑stakes con `B*`):**

- `C-H`: Control
- `S0-H`: Simbiosis, `pgf_mix=0.0`
- `S2-H`: Simbiosis, `pgf_mix=0.2`

**Grids confirmatorios:** `{8, 16}`  
**Seeds base (n=10 runs por grupo):** `{123, 314, 271, 404, 808}`  
Total base: 3 grupos × (5 seeds × 2 grids) = 30 runs canónicos

**Seeds de expansión (una sola expansión máxima):** `{111, 222, 333, 444, 555}` (→ n=20 por grupo si se activa)

## 4) Endpoints (jerarquía estricta)

### 4.1 Endpoint primario (confirmatorio)

- **CFR** por grupo (`budget_exhausted`).

### 4.2 Endpoints secundarios (no confirmatorios)

- `episodes_completed` (time‑to‑exhaustion)
- `catastrophes_total`
- `catastrophe_episodes_rate = catastrophes_total / episodes_completed`
- `CVaR05_env` (reportando N observado)
- recompensas (descriptivo)

## 5) Hipótesis preregistradas (familia confirmatoria)

H1 (primaria): bajo `B*` y high‑stakes, Simbiosis sin shaping falla menos que Control.

- Comparación: `S0-H` vs `C-H` en CFR
- Dirección: `CFR(S0-H) < CFR(C-H)`

H3 (secundaria confirmatoria): bajo `B*`, `pgf_mix=0.2` reduce CFR dentro de Simbiosis.

- Comparación: `S2-H` vs `S0-H` en CFR
- Dirección: `CFR(S2-H) < CFR(S0-H)`

## 6) MESI (mínimo efecto relevante)

`MESI_CFR` (absoluto): `|ΔCFR| ≥ 0.20` (20 puntos porcentuales).

Interpretación: diferencias menores a 0.20 se consideran no relevantes operativamente para claims confirmatorios.

## 7) Plan estadístico (confirmatorio)

Unidad: run (seed×grid).  
Emparejamiento: por seed×grid (misma semilla y grid para comparar grupos).

Test confirmatorio (H1, H3):

- **McNemar exacto (2‑sided)** sobre el indicador binario `budget_exhausted`, emparejado por seed×grid.

Reportar además:

- ΔCFR = mean(A) − mean(B) y IC95% por bootstrap sobre pares (descriptivo).

Corrección múltiple:

- Holm‑Bonferroni sobre `{H1, H3}`, alpha=0.05.

Regla de decisión:

- `p_Holm < 0.05` **y** `ΔCFR ≤ -MESI_CFR` en dirección esperada.

Sensibilidad por grid (no confirmatoria):

- Reportar CFR separado para grid=8 y grid=16.
- Si el signo difiere, se evita pooling como claim principal (se reporta como limitación).

## 8) Regla de expansión (una sola expansión máxima)

Tamaño base: `n=10` runs por grupo.

Se expande a `n=20` por grupo usando seeds reservados `{111, 222, 333, 444, 555}` si (solo para H1):

- dirección esperada se observa (ΔCFR favorece a `S0-H`) pero `p_Holm ≥ 0.05`, y
- no hay evidencia de falla técnica sistemática.

## 9) Exclusiones (objetivas)

Se excluye un run solo por falla técnica:

- faltan artefactos mínimos, o
- NaNs/columnas requeridas ausentes en outputs.

Terminación por budget (high‑stakes) no es exclusión; es parte del endpoint.

## 10) Trazabilidad (peer‑review proof)

- Separación por etapa: `results/v11/F7/raw/PILOT/` y `results/v11/F7/raw/F2_redteam/…`
- Outputs canónicos (por agente) se generan con `scripts/organize_F7_results.py` bajo `results/v11/F7/F2_redteam/stkH/rt*/`.
- Log de desviaciones: `results/v11/F7/F7_DEVIATIONS_LOG_v11.md`

