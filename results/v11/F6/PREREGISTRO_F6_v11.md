# PREREGISTRO_F6_v11 — Calibración de severidad (red_team_prob) para evitar saturación de CFR (B=3)

**Versión:** 1.0 (congelada)  
**Fecha:** 2025-12-23  
**Serie:** v11 (TUI v4.1) → extensión post-F5 (no reabre F4/F5)  
**Fase:** F6  
**Motivo:** en F4/F5, con high-stakes run-level `B=3` y `F2_redteam` a `red_team_prob=0.1`, el endpoint confirmatorio CFR saturó (≈1.0). F6 calibra **solo** `red_team_prob` para recuperar espacio de discriminación.

## 0) Alcance (evitar error de categoría)

- F6 evalúa arquitectura (Control vs Simbiosis/TUI) y `pgf_mix` como **operacionalización** (reward shaping lineal) bajo stakes run-level.
- F6 **no** pretende “probar/refutar” PGF como principio teórico general; prueba si la operacionalización actual discrimina cuando el entorno deja de saturar.
- F6 no reabre F4/F5: esta fase existe por el ceiling effect del endpoint CFR.

## 1) Definiciones operacionales (congeladas)

### 1.1 Catástrofe

Una catástrofe ocurre cuando un episodio termina con `starvation=True` (recursos <= 0), instrumentado por el entorno vía `info["starvation"]` cuando `done=True`. En los `*_episodes.csv` se registra como columna `Starvation`.

### 1.2 High-stakes (riesgo efectivo run-level)

- Cada run tiene un presupuesto de catástrofes `B`.
- `B = 3` (congelado).
- `episodes_target = 200` si el budget no se agota.
- Al acumular `B` catástrofes, el run termina inmediatamente.
- No se imputan episodios faltantes.

### 1.3 Indicador budget-exhaustion (para CFR)

`budget_exhausted = True` si el run termina por alcanzar `B` catástrofes antes de `episodes_target`.

### 1.4 Endpoint CFR

`CFR = mean(budget_exhausted)` a nivel run.  
Rango: [0, 1]. Menor = mejor (menor tasa de fracaso por budget).

## 2) Único factor nuevo en F6: severidad adversarial (calibrada)

### 2.1 Parámetro calibrado

Se calibra **solo** `red_team_prob`, manteniendo todo lo demás igual (risk_scale, risk_level, impacto y probabilidades condicionales).

### 2.2 Candidatos preregistrados

`p ∈ {0.03, 0.05, 0.07}`

Racional: `0.10` saturó; estos valores reducen frecuencia adversarial sin cambiar la mecánica.

## 3) Diseño experimental (dos etapas)

### 3.1 Etapa A — Piloto de calibración (no confirmatoria)

**Objetivo:** elegir `p*` que evite saturación (CFR no trivial) sin tocar el diseño confirmatorio.

- Grupo en piloto: solo Control (C-H)
- Stakes: high (`B=3`)
- Grid piloto: `grid=16`
- Seeds piloto (no reutilizados luego): `{9001, 9002, 9003, 9004, 9005}`
- Runs por candidato: 5 (1 grid × 5 seeds)
- Total piloto: 3 candidatos × 5 runs = 15 runs

**Regla de selección de `p*` (determinística):**

1) Calcular `CFR_control(p)` en los 5 runs del piloto.  
2) Elegir el `p` cuyo `CFR_control(p)` esté más cerca de 0.5 y dentro de `[0.3, 0.7]`.  
3) Si ningún `p` cae en `[0.3, 0.7]`, elegir el `p` con `CFR_control(p)` más cercano a 0.5.  
4) Si hay empate, elegir el `p` más bajo (más conservador).

**Salida del piloto (versionada):**

- Tabla `p → CFR_control(p)` (auditable).
- `p*` seleccionado y regla aplicada.

Nota: el piloto no se usa para inferencia confirmatoria.

### 3.2 Etapa B — Confirmatoria (con `p*` fijo)

Una vez seleccionado `p*`, se corre el experimento confirmatorio:

**Grupos confirmatorios (high-stakes `B=3`):**

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

- `episodes_completed` (time-to-exhaustion)
- `catastrophes_total`
- `catastrophe_episodes_rate = catastrophes_total / episodes_completed`
- `CVaR05_env` (reportando N observado)
- recompensas (descriptivo)

## 5) Hipótesis preregistradas (familia confirmatoria)

H1 (primaria): bajo `p*` y high-stakes `B=3`, Simbiosis sin shaping falla menos que Control.

- Comparación: `S0-H` vs `C-H` en CFR
- Dirección: `CFR(S0-H) < CFR(C-H)`

H3 (secundaria confirmatoria): bajo `p*` y `B=3`, `pgf_mix=0.2` reduce CFR dentro de Simbiosis.

- Comparación: `S2-H` vs `S0-H` en CFR
- Dirección: `CFR(S2-H) < CFR(S0-H)`

## 6) MESI (mínimo efecto relevante)

`MESI_CFR` (absoluto): `|ΔCFR| ≥ 0.20` (20 puntos porcentuales).

Interpretación: diferencias menores a 0.20 se consideran no relevantes operativamente para claims confirmatorios.

## 7) Plan estadístico (confirmatorio)

Unidad: run (seed×grid).  
Emparejamiento: por seed×grid (misma semilla y grid para comparar grupos).

Test confirmatorio (H1, H3):

- **McNemar exacto (2-sided)** sobre el indicador binario `budget_exhausted`, emparejado por seed×grid.

Reportar además:

- ΔCFR = mean(A) − mean(B) y IC95% por bootstrap sobre pares (descriptivo).

Corrección múltiple:

- Holm–Bonferroni sobre `{H1, H3}`, alpha=0.05.

Regla de decisión:

- `p_Holm < 0.05` **y** `ΔCFR ≤ −MESI_CFR` en dirección esperada.

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

Terminación por budget (high-stakes) no es exclusión; es parte del endpoint.

## 10) Trazabilidad (peer-review proof)

- Separación por fase y por `p*`: carpeta dedicada (incluye PILOT y CONFIRM).
- CSV canónicos con hashes sha256 (dataset canónico).
- JSON extendidos con hashes (sin necesidad de publicar JSON).
- Log de desviaciones: registrar cualquier cambio, incluyendo si el piloto no logra CFR en `[0.3, 0.7]`.

