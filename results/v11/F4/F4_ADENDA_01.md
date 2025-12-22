# F4 Adenda 01 — Stakes run-level + CFR (budget-exhaustion)

**Fecha:** 2025-12-22  
**Referencia:** `results/v11/F4/PREREGISTRO_F4_v11.md` (secciones 2–9)  
**Estado:** congelado antes de ejecución  

## 1) Motivación

Se reemplaza el enfoque de “penalización numérica” por un mecanismo de **riesgo efectivo a nivel run** para evitar que el agente amortice catástrofes estadísticamente en un entorno reseteable.

## 2) Redefinición operacional de stakes

### Low-stakes (baseline v11)

- El run ejecuta 200 episodios independientemente del número de catástrofes.
- Las catástrofes solo afectan el episodio donde ocurren (no hay corte del run).

### High-stakes (run-level budget)

- Cada run tiene un **presupuesto de catástrofes** `B`.
- `B` primario: **3**
- Regla: al acumular `B` catástrofes, el run termina inmediatamente.
- No se imputan episodios faltantes para endpoints continuos; se registran métricas observadas y `episodes_completed`.

### Definición canónica de catástrofe (para v11/F4)

Catástrofe = episodio termina con `starvation=True` (muerte por recursos `<=0`).  
Esto coincide con lo que expone el entorno vía `info["starvation"]` cuando `done=True`.

## 3) Endpoint primario actualizado

Endpoint primario: **CFR (budget-exhaustion)** = proporción de runs con `catastrophes_total >= B`.

Endpoints secundarios:
- `episodes_completed`
- `catastrophe_episodes_rate`
- `CVaR05_env` (sobre episodios observados, reportando N)
- `reward_env_total` y `reward_total` (secundarios/descriptivos)

## 4) Hipótesis actualizadas

- H1: en high-stakes (`B=3`), Simbiosis/TUI tendrá CFR menor que Control.
- H2: interacción stakes×arquitectura: la diferencia Simbiosis vs Control en CFR será mayor en high-stakes que en low-stakes.
- H3: en high-stakes, `pgf_mix=0.2` reducirá CFR frente a `pgf_mix=0.0` dentro de Simbiosis.

## 5) MESI para CFR

MESI primario para CFR: **ΔCFR ≥ 0.20** (reducción absoluta mínima).

## 6) Plan estadístico para CFR

- Test primario comparaciones binarias: Fisher exact (n pequeño).
- Corrección múltiple: Holm–Bonferroni para familia confirmatoria (H1–H3).
- IC95%: proporciones y ΔCFR.

## 7) Sensibilidad del budget

Si se desea sensibilidad del umbral `B`, debe registrarse como **exploratoria** y/o como fase separada (p.ej. F4b), dado que cambiar `B` altera la dinámica (terminación temprana) en high-stakes.

## 8) Regla de expansión

Si H1 queda ambiguo respecto a MESI (IC95% incluye 0 y también incluye mejoras ≥ MESI), se expande a n=20 por grupo usando seeds preregistrados de expansión.
