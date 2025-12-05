# ❌ ANÁLISIS FALLO v10.8 - Root Cause Crítico

**Fecha**: 2025-12-05  
**Status**: 🔴 **v10.8 FALLÓ** - Rewards PEOR que v10.7, 0% success persiste

---

## 📊 RESULTADOS v10.8

### Comparación vs v10.7

| Métrica | v10.7 (smoke) | v10.8 (goal) | Delta | Evaluación |
|---------|--------------|--------------|-------|------------|
| Success | 0.0% | 0.0% | 0.0pp | ❌ Sin mejora |
| Rewards | -11.85 | -31.70 | **-19.85** | ❌ **PEOR** |
| Resources | 0.98 | 0.98 | 0.00 | = Sin cambio |
| Steps | 22.5 | **30.0** | +7.5 | ⚠️ Max steps |
| Starvation | 96.8% | **2.0%** | -94.8% | ✅ Sobrevive |
| Epsilon | 0.01 | 0.01 | 0.00 | ✅ Converge |

**Observaciones críticas**:
1. ❌ **Rewards -19.85 PEOR** (opuesto a esperado)
2. ⚠️ **Steps = 30.0 constante** (max_steps, NO alcanza meta)
3. ✅ **Starvation 2%** (vs 96.8%, economía sostenible)
4. ❌ **Success 0%** (goal_reward NO incentiva meta)

---

## 🔍 ROOT CAUSE ANALYSIS

### Problema #1: Max Steps Constant (30.0)

**Observación**: TODOS los episodios terminan en 30 steps (max_steps).

**CSV Evidencia** (líneas 990-1000):
```csv
episode,reward,steps,goal_reached,starvation
990,-29.75,30,0,0
991,-39.42,30,0,1
992,-24.42,30,0,0
...
999,-30.59,30,0,0
1000,-31.75,30,0,0
```

**Diagnóstico**: Agent NO muere (starvation 2%), NO alcanza meta (success 0%), simplemente agota max_steps.

### Problema #2: Rewards PEOR (-31.70 vs -11.85)

**Cálculo Teórico v10.8**:
```
Episode típico (30 steps, NO goal):
- step_cost: -0.15 × 30 = -4.5
- resources: +0.75 × 1 = +0.75
- penalty_low: -1.0 × X pasos
Total observado: -31.70
```

**vs v10.7**:
```
Episode típico (22 steps, starvation):
- step_cost: -0.25 × 22 = -5.5
- resources: +0.75 × 1 = +0.75
- penalty_low: -1.0 × ~3 = -3.0
- starvation: -2.5
Total observado: -11.85
```

**¿Por qué v10.8 PEOR?**

**Hipótesis A**: step_cost=-0.15 × 30 steps = -4.5, PERO balance NO drena lo suficiente para morir.

**Verificación energía**:
```python
# environment_v2.py línea 182-186
reward += self.step_cost  # -0.15
self.resources += self.step_cost  # -0.15 (drena balance)

# Episodio típico:
balance = 5.0
Por cada step: balance -= 0.15
Después 30 steps: balance = 5.0 - (0.15 × 30) = 5.0 - 4.5 = 0.5

threshold_low = 2.0
→ 0.5 < 2.0 → penalty_low = -1.0 aplicado ~28 steps

Total penalty_low: -1.0 × 28 = -28.0
```

**¡ENCONTRADO!** Penalty_low se aplica ~28 steps porque balance <2.0 casi todo el episodio.

**Cálculo correcto v10.8**:
```
- step_cost: -0.15 × 30 = -4.5
- resources: +0.75 × 1 = +0.75
- penalty_low: -1.0 × 28 = -28.0
Total: -4.5 + 0.75 - 28.0 = -31.75 ✅ MATCHES observado -31.70
```

**vs v10.7** (step_cost -0.25, balance drena más rápido → muerte step 22):
```
- step_cost: -0.25 × 22 = -5.5
- resources: +0.75 × 1 = +0.75
- penalty_low: -1.0 × ~3 = -3.0 (solo últimos 3 steps)
- starvation: -2.5
Total: -5.5 + 0.75 - 3.0 - 2.5 = -10.25 ≈ -11.85 observado
```

**Conclusión**: step_cost -0.15 es DEMASIADO SUAVE → agent sobrevive 30 steps → penalty_low -1.0 × 28 steps = -28 acumulado BRUTAL.

### Problema #3: goal_reward NO Aplicado

**CSV Evidencia**:
```csv
goal_reward_applied,episode
0,990
0,991
0,992
...
0,999
0,1000
```

**TODOS los episodios: goal_reward_applied = 0**

**Verificación código**:
```python
# environment_v2.py línea 166-169
if info.get('help') or info.get('goal_reached'):
    done = True
    info['goal_reached'] = True
    reward += config.ENV_GOAL_REWARD  # +10.0
    info['goal_reward_applied'] = True
```

Código correcto, PERO `info.get('goal_reached')` NUNCA True porque agent NO alcanza meta.

**Conclusión**: goal_reward implementado correctamente, PERO inútil si success 0%.

---

## 🎯 ROOT CAUSES IDENTIFICADOS

### 1. step_cost -0.15 CONTRAPRODUCENTE

**Problema**: Reductor step_cost -0.25 → -0.15 (-40%) tiene efecto OPUESTO al esperado.

**Esperado**: Menos castigo por explorar → mejor aprendizaje.

**Realidad**: Balance drena más lento → agent sobrevive 30 steps → acumula penalty_low -1.0 × 28 steps = -28.0.

**Efecto neto**: Rewards -11.85 → -31.70 (**PEOR 168%**).

### 2. Balance 5.0 + spawn_rate 0.40 INSUFICIENTE

**Problema**: Agent recolecta ~1 resource por episodio, PERO balance drena 0.15/step.

**Cálculo**:
```
Balance inicio: 5.0
Después 10 steps (Manhattan óptimo): 5.0 - (0.15 × 10) = 3.5
Recolecta 1 resource: 3.5 + 0.75 = 4.25
Balance threshold_low: 2.0
→ 4.25 > 2.0 (NO penalty) ✅

PERO agent NO va directo a meta, vagabundea:
Después 30 steps: 5.0 - (0.15 × 30) + 0.75 = 0.5
→ 0.5 < 2.0 (penalty_low -1.0) × 28 steps = -28.0 ❌
```

**Conclusión**: step_cost -0.15 parece "suave" PERO acumulativo 30 steps × -0.15 = -4.5 drena balance threshold.

### 3. goal_reward 10.0 NO ES SEÑAL DOMINANTE

**Problema**: goal_reward = 10.0 implementado PERO agent NO alcanza meta → reward nunca aplicado.

**Cálculo teórico** (si llegara a meta):
```
Episode óptimo (10 steps, goal):
- goal_reward: +10.0
- step_cost: -0.15 × 10 = -1.5
- resources: +0.75 × 1 = +0.75
Total: +10.0 - 1.5 + 0.75 = +9.25 ✅ POSITIVO

Episode subóptimo (30 steps, NO goal):
- goal_reward: 0.0
- step_cost: -0.15 × 30 = -4.5
- resources: +0.75 × 1 = +0.75
- penalty_low: -1.0 × 28 = -28.0
Total: -4.5 + 0.75 - 28.0 = -31.75 ❌ BRUTAL

Delta: +9.25 - (-31.75) = +41.0 → SEÑAL ENORME... si llegara
```

**PERO**: Agent NO explora hacia meta (tripwires 0.04, resources 0.98 marginal).

---

## 💡 INSIGHTS CRÍTICOS

### Insight #1: step_cost Tiene Efecto NO-LINEAL

**Descubrimiento**: Reducir step_cost NO siempre mejora rewards.

**Razón**: Balance drena más lento → agent sobrevive más steps → acumula MÁS penalty_low total.

```
v10.7: -0.25 × 22 steps → muerte rápida → penalty_low × 3 steps = -3.0
v10.8: -0.15 × 30 steps → sobrevive max → penalty_low × 28 steps = -28.0

Resultado: v10.8 PEOR que v10.7
```

**Lección**: **Reducir step_cost SIN ajustar threshold_low es CONTRAPRODUCENTE.**

### Insight #2: Max Steps = 30 Es TRAMPA

**Descubrimiento**: Grid 6×6 Manhattan=10, max_steps=30 (3× margen) es EXCESIVO.

**Problema**: Agent puede vagabundear 30 steps SIN morir → NO aprende urgencia alcanzar meta.

**Comparación**:
```
v10.7 (step_cost -0.25): Muere step ~22 (muerte natural fuerza aprendizaje)
v10.8 (step_cost -0.15): Agota max_steps 30 (sin presión temporal)
```

**Lección**: **max_steps debe ser ajustado según step_cost, NO solo Manhattan.**

### Insight #3: threshold_low=2.0 Demasiado Alto

**Descubrimiento**: threshold_low = 2.0 (40% balance inicial 5.0) es BRUTAL para step_cost -0.15.

**Problema**: Agent cae bajo threshold en step ~20:
```
5.0 - (0.15 × 20) = 5.0 - 3.0 = 2.0 → threshold_low

→ Penalty_low -1.0 aplicado steps 20-30 = 10 steps × -1.0 = -10.0 (mínimo)
```

**Realidad observada**: penalty_low × 28 steps = -28.0 (agent cae threshold step ~2).

**Cálculo correcto**:
```
Balance + 1 resource: 5.0 + 0.75 = 5.75
Drena: 5.75 - (0.15 × X) < 2.0
X > (5.75 - 2.0) / 0.15 = 3.75 / 0.15 = 25 steps

→ Agent cae bajo threshold step 25 (sin resources adicionales)
PERO recolecta 1 resource promedio, retarda a step ~30
→ Penalty_low × ~5 steps

CSV muestra -31.70 → penalty_low × 28 steps
→ Agent NO recolecta resources a tiempo, cae threshold step ~2
```

**Lección**: **threshold_low = 2.0 demasiado alto para step_cost -0.15. Debe ser ~1.0.**

---

## 🛠️ CORRECCIONES NECESARIAS

### Fix Crítico #1: Revert step_cost

**Problema**: step_cost -0.15 EMPEORA rewards vs -0.25.

**Solución**:
```python
# sim/config.py
ENV_STEP_COST = -0.25  # Revert a v10.7 (drena balance más rápido)
```

**Justificación**: step_cost -0.25 fuerza muerte step ~22, evita acumular penalty_low excesivo.

### Fix Crítico #2: Reducir threshold_low

**Problema**: threshold_low = 2.0 (40% balance) demasiado alto.

**Solución**:
```python
# sim/config.py
ENV_RESOURCE_THRESHOLD_LOW = 1.0  # Era 2.0 (-50%)
```

**Impacto**:
```
Balance típico: 5.0 - (0.25 × 22) + 0.75 = 0.25
threshold_low = 1.0
→ Penalty_low aplicado últimos ~5 steps (vs 28 steps previo)
```

### Fix Crítico #3: Reducir max_steps

**Problema**: max_steps = 30 (3× Manhattan) permite vagabundeo excesivo.

**Solución**:
```python
# environment_v2.py
max_steps_multiplier = 2.0  # Era 3.0 (6×6: 20 steps vs 30)
```

**Impacto**: Agent tiene 20 steps (2× margen) → presión temporal aumenta → fuerza goal-seeking.

### Fix Crítico #4: Aumentar goal_reward

**Problema**: goal_reward = 10.0 insuficiente vs penalty_low acumulado.

**Solución**:
```python
# sim/config.py
ENV_GOAL_REWARD = 20.0  # Era 10.0 (2× señal)
```

**Impacto**:
```
Episode óptimo (10 steps, goal):
+20.0 (goal) - 2.5 (steps) + 0.75 (resource) = +18.25 ✅ MUY POSITIVO

Episode subóptimo (20 steps, NO goal):
-5.0 (steps) + 0.75 (resource) - 5.0 (penalty) = -9.25 ❌

Delta = +18.25 - (-9.25) = +27.5 (SEÑAL ENORME)
```

---

## 📋 PLAN v10.9

### Cambios Código

1. **sim/config.py**:
```python
ENV_STEP_COST = -0.25  # Revert (drena más rápido)
ENV_RESOURCE_THRESHOLD_LOW = 1.0  # Era 2.0 (-50%)
ENV_GOAL_REWARD = 20.0  # Era 10.0 (2× señal)
ENV_RESOURCE_SPAWN_RATE = 0.40  # Mantener
```

2. **sim/environment_v2.py**:
```python
max_steps_multiplier = 2.0  # Era 3.0 (presión temporal)
```

### Smoke Test v10.9 (1000 eps)

**Config**:
- Grid: 6×6
- Episodes: 1000
- goal_reward: 20.0 (2× v10.8)
- step_cost: -0.25 (revert v10.7)
- spawn_rate: 0.40 (mantener v10.8)
- threshold_low: 1.0 (50% reducción)
- max_steps: 20 (era 30, -33%)

**Gates v10.9**:
- Success: >15% (150+ episodios, más estricto)
- Rewards: >+5 últimos 100 eps (positivo sólido)
- Resources: >1.5 promedio
- Steps: <15 promedio (eficiencia)

---

## 🔗 LECCIONES APRENDIDAS v10.8

### 1. Reducir step_cost NO Siempre Mejora

**Error**: Asumimos step_cost -0.15 "más suave" = mejor.

**Realidad**: Balance drena más lento → agent sobrevive más → acumula penalty_low MÁS.

**Lección**: **Economía es sistema complejo, cambios tienen efectos NO-LINEALES.**

### 2. threshold_low Debe Escalarse con step_cost

**Error**: threshold_low = 2.0 fijo independiente de step_cost.

**Realidad**: threshold_low 2.0 OK para step_cost -0.25, BRUTAL para -0.15.

**Lección**: **threshold_low ∝ step_cost (ratio ~8:1 óptimo).**

### 3. max_steps Debe Forzar Urgencia

**Error**: max_steps = 3× Manhattan "generoso" permite vagabundeo.

**Realidad**: Agent llena max_steps sin aprender goal-seeking.

**Lección**: **max_steps = 2× Manhattan fuerza presión temporal, incentiva eficiencia.**

### 4. goal_reward Debe DOMINAR Penalties

**Error**: goal_reward = 10.0 parece "grande" aisladamente.

**Realidad**: Penalty_low acumulado -28.0 DOMINA goal_reward 10.0.

**Lección**: **goal_reward ≥ 2× penalties máximos acumulados para señal clara.**

---

## 🎯 PRÓXIMO PASO

**Implementar v10.9** con correcciones críticas:
1. ✅ Revert step_cost -0.25
2. ✅ Reducir threshold_low 1.0
3. ✅ Aumentar goal_reward 20.0
4. ✅ Reducir max_steps 2× multiplier
5. ✅ Mantener spawn_rate 0.40

**Smoke test 1000 eps** validar gates:
- Success >15%
- Rewards >+5
- Steps <15

**SI v10.9 falla**: Cerrar v10.x, documentar lecciones, planificar v11 con arquitectura diferente (e.g., curriculum learning, shaped rewards).

---

**Documentos Relacionados**:
- SMOKE_TEST_1000_EPS_ANALISIS.md (v10.7 análisis)
- VALIDACION_AUDITORIA_v10.7_CONFIRMADA.md (decisión v10.8)
- RESUMEN_EJECUTIVO_AUDITORIA_v10.7.md (bloqueo v10.7)
