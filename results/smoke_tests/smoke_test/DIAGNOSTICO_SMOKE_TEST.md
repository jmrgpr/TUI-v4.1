# DIAGNÓSTICO CRÍTICO SMOKE TEST
**Fecha:** 1 de diciembre 2025  
**Estado:** PROBLEMA CRÍTICO IDENTIFICADO

## RESUMEN EJECUTIVO

Los datos reales en `results/smoke_test/` muestran un **fallo completo** de los agentes `simbiosis` y `tui`:
- **0/2000 episodios con reward >0** (seeds 123 y 456)
- Medias: -88.31 y -83.91
- Los agentes `control` (tabular) y `dqn_control` (DQN) funcionan perfectamente

## DATOS REALES VERIFICADOS

### Archivo: dqn_control_easy_seed123_episodes.csv (3001 líneas)
- `control`: media=316.91, 1000/1000 >0 ✅
- `simbiosis`: media=-88.31, 0/1000 >0 ❌
- `dqn_control`: media=91.68, 1000/1000 >0 ✅

### Archivo: dqn_control_easy_seed456_episodes.csv (3001 líneas)
- `control`: media=324.80, 1000/1000 >0 ✅
- `simbiosis`: media=-83.91, 0/1000 >0 ❌
- `dqn_control`: media=108.98, 1000/1000 >0 ✅

### Archivo: tui_pgf_easy_seed123_episodes.csv (3001 líneas)
- `control`: media=316.91, 1000/1000 >0 ✅
- `simbiosis`: media=-88.31, 0/1000 >0 ❌
- `tui`: media=-88.31, 0/1000 >0 ❌

### Archivo: tui_pgf_easy_seed456_episodes.csv (3001 líneas)
- `control`: media=324.80, 1000/1000 >0 ✅
- `simbiosis`: media=-83.91, 0/1000 >0 ❌
- `tui`: media=-83.91, 0/1000 >0 ❌

## BUG IDENTIFICADO EN CÓDIGO

### Ubicación: `sim/runner.py` líneas 198-202

```python
r_pgf = metrics['PGF'] * mixed + reward_env * (1.0 - mixed) if use_pgf else reward_env

if use_dqn and agent_name == "DQN-Control":
    reward_env = min(reward_env, 0.0)  # <--- FUERZA REWARDS ≤0
    r_pgf = min(r_pgf, 0.0)
```

**Problema:** Este código debería bloquear "DQN-Control", PERO los datos muestran que "DQN-Control" aprende bien y "simbiosis/tui" fallan.

### Hipótesis de causa raíz

Los agentes `simbiosis` y `tui` usan `use_pgf=True`, lo que significa:
```python
r_pgf = metrics['PGF'] * mixed + reward_env * (1.0 - mixed)
```

Con `pgf_mix=1.0` (default):
```python
r_pgf = metrics['PGF'] * 1.0 + reward_env * 0.0 = metrics['PGF']
```

**El agente aprende SOLO con PGF, ignorando reward_env completamente.**

### Verificación necesaria

1. ¿Qué valores tiene `metrics['PGF']` en los episodios fallidos?
2. ¿Está `PGF_Bruto` y `PGF_Costo` calculándose correctamente?
3. ¿Hay un problema en `evaluator_pgf.py` que genera PGF siempre negativo?

## ANÁLISIS DE MÉTRICAS PGF EN CSV

Revisando el CSV `tui_pgf_easy_seed123_episodes.csv`:
- Columnas: `PGF_Bruto_Avg`, `PGF_Costo_Avg`
- Para agente `simbiosis` episodio 1: `0.0, 0.0` → PGF_Neto = 0.0
- Para agente `tui` episodio 1: `0.0, 0.0` → PGF_Neto = 0.0

**PROBLEMA CRÍTICO:** Si PGF es 0.0 en la mayoría de los pasos, el agente NO recibe señal de aprendizaje.

## DISCREPANCIA DOCUMENTACIÓN vs REALIDAD

La documentación en `RESULTADOS_TUNING_DQN.md` reporta:
- DQN-Control: medias 115/107/117, 66% success (2000/3000)
- TUI/PGF: medias 44/47/52, 33% success (1000/3000)

**PERO** los datos reales muestran:
- DQN-Control: medias 92-109, 100% success (2000/2000)
- Simbiosis/TUI: medias -84 a -88, 0% success (0/2000)

**Conclusión:** La tabla en la documentación es una PROYECCIÓN, no resultados reales medidos.

## IMPACTO EN TEORÍA TUI

**CRÍTICO:** No podemos validar TUI vs DQN hasta resolver este problema.

Los agentes con lógica PGF (`use_pgf=True`) están completamente bloqueados. Esto invalida cualquier comparación TUI vs Control en este smoke test.

## PLAN DE ACCIÓN URGENTE

### PASO 1: Diagnosticar cálculo PGF
- Revisar `evaluator_pgf.py` líneas donde se calcula `PGF_Bruto` y `PGF_Costo`
- Verificar si `delta_P` (cambio en riesgo) está siempre en 0
- Confirmar valores de `kappa` y `lambda_c`

### PASO 2: Verificar delta_P en entorno benigno
El problema puede ser que en entorno 3×3 benigno (sin tripwires/shocks):
- `delta_P = 0` en casi todos los pasos
- Por tanto `PGF_Bruto = kappa * delta_P * A_t ≈ 0`
- Y `PGF_Neto = 0 - lambda_c * delta_C_t` → NEGATIVO por el costo

**Hipótesis:** En entorno benigno, PGF es sistemáticamente negativo porque no hay reducción de riesgo.

### PASO 3: Soluciones propuestas

**Opción A: Ajustar pgf_mix**
- Probar `pgf_mix=0.5` o `0.8` para mezclar PGF con reward_env
- Esto permitiría aprendizaje incluso si PGF es débil

**Opción B: Rediseñar PGF para entorno benigno**
- Incluir recompensa base cuando `delta_P ≈ 0`
- Ajustar `lambda_c` para reducir penalización por costos

**Opción C: Usar entorno con riesgo real**
- Activar tripwires/shocks para generar `delta_P > 0`
- El smoke test actual es DEMASIADO benigno para validar PGF

### PASO 4: Experimentos de validación

1. **EXP_DEBUG_01:** Correr simbiosis con `pgf_mix=0.0` (solo reward_env)
   - Debería funcionar como control
   - Confirma que el problema es PGF, no el agente

2. **EXP_DEBUG_02:** Correr simbiosis con `pgf_mix=0.5` (mix 50/50)
   - Ver si aprende con señal híbrida

3. **EXP_DEBUG_03:** Analizar CSV de un run simbiosis
   - Imprimir valores de `PGF_Bruto`, `PGF_Costo`, `PGF_Neto` por paso
   - Confirmar si son todos ≤0

## CONCLUSIÓN

El smoke test actual tiene un **fallo fundamental**: el entorno 3×3 benigno NO genera suficiente señal PGF para que los agentes simbiosis/tui aprendan.

**Prioridad 1:** Desbloquear agentes simbiosis/tui ajustando `pgf_mix` o rediseñando PGF para entorno benigno.

**Prioridad 2:** Actualizar documentación para reflejar datos reales, no proyecciones.

**Prioridad 3:** Rediseñar protocolo de smoke test para incluir riesgo mínimo que active PGF.

---

**SIGUIENTE PASO:** Revisar `evaluator_pgf.py` para entender cálculo exacto de PGF y confirmar hipótesis.
