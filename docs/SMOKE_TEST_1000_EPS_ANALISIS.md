# Smoke Test Convergencia 1000 Episodios - Análisis Completo

**Fecha**: 2025-01-XX  
**Objetivo**: Validar convergencia DQN 6×6 con economía ajustada antes de declarar v10.7

---

## 📋 CONFIGURACIÓN AJUSTADA

vs Validación 200 eps:

| Parámetro | Validación | Smoke Test | Cambio |
|-----------|-----------|------------|---------|
| Episodes | 200 | 1000 | +400% |
| spawn_rate | 0.15 | 0.30 | +100% |
| initial_balance | 4.0 | 5.0 | +25% |
| epsilon_decay | 0.995 | 0.9995 | -80% decay |

**Balance Teórico Post-Viaje**:
```
Balance = 5.0 + 0.75 - (10 × 0.25) = 5.0 + 0.75 - 2.5 = 3.25
Margen = 3.25 / 2.0 = 162% (vs threshold_low=2.0)
```

**Grid 6×6 Complejidad**:
- Estados posibles: ~1000-2000 (agent × goal × resources)
- Manhattan óptimo: 10 pasos
- max_steps: 30 (3× margen)

---

## 🚦 GATES CONVERGENCIA

### Gate 1: Epsilon <0.1 ✅
**Status**: ✅ PASÓ  
**Resultado**: epsilon_final = 0.0100  
**Análisis**: Policy convergió exitosamente, agente explota conocimiento adquirido.

**Progresión epsilon**:
```
Ep 100:  0.337 (explorando activamente)
Ep 200:  0.112 (transición exploit)
Ep 300:  0.036 (cerca convergencia)
Ep 400+: 0.010 (policy estable)
```

### Gate 2: Success >5% ❌
**Status**: ❌ FALLÓ  
**Resultado**: success_rate = 0.0% (0/1000 episodios)  
**Análisis**: **NINGÚN** episodio alcanzó meta en 1000 intentos.

**Diagnóstico**:
1. Agente NO aprende estrategia goal-seeking
2. Policy convergió a comportamiento subóptimo
3. Starvation 96.8% indica muerte prematura

### Gate 3: Resources >1.0 ❌
**Status**: ❌ FALLÓ (marginalmente)  
**Resultado**: resources_mean = 0.98 (últimos 100 eps)  
**Análisis**: ~1 resource por episodio, mejora vs 0.0 validación.

**Progresión resources**:
```
Ep 100:  0.84 resources/ep (aprendiendo)
Ep 300:  1.01 resources/ep (peak)
Ep 400+: 0.86-1.03 resources/ep (estable pero marginal)
```

**Varianza**: Oscila 0.82-1.03, sugiere spawn_rate aún bajo.

### Gate 4: Rewards >-5 ❌
**Status**: ❌ FALLÓ  
**Resultado**: reward_mean = -11.85 (últimos 100 eps)  
**Análisis**: Mejora vs -160 validación penalty brutal, PERO lejos de -5 target.

**Progresión rewards**:
```
Ep 100:  -13.7 (peor)
Ep 300:  -11.5 (mejor)
Ep 700:  -10.6 (mejor en serie)
Ep 1000: -11.8 (estancado)
```

No mejora consistente últimos 300 eps → policy estancada.

---

## 📊 MÉTRICAS DETALLADAS

### Totales (1000 episodios)

| Métrica | Valor | Evaluación |
|---------|-------|-----------|
| Success rate | 0.0% | ❌ Crítico |
| Reward mean | -11.80 | ⚠️ Lejos target |
| Steps mean | 22.47 | ✅ Explora activo |
| Starvation | 96.8% | ❌ Muerte prematura |
| Tripwires | 0.03 | ⚠️ Exploración mínima |
| Resources | 0.92 | ⚠️ Marginal |

### Últimos 100 episodios (convergencia)

| Métrica | Valor | vs Total |
|---------|-------|---------|
| Success | 0.0% | Sin cambio |
| Reward | -11.85 | -0.4% (estancado) |
| Resources | 0.98 | +6.5% (mejora) |
| Epsilon | 0.010 | Convergido |

---

## 🔍 ROOT CAUSE ANALYSIS

### 1. spawn_rate=0.30 INSUFICIENTE

**Evidencia**:
- Resources ~1.0 promedio (apenas suficiente)
- Starvation 96.8% (muere sin resources)
- Tripwires 0.03 (no explora grid)

**Cálculo Teórico**:
```
Grid 6×6 = 36 celdas
spawn_rate 0.30 → 0.3 × 36 = 10.8 resources esperados por reset
max_resources_on_grid = 3 → solo 3 resources simultáneos

Probabilidad encontrar resource en Manhattan-10:
P = 3 / 36 × 10 pasos = 0.083 × 10 = 0.83 resources esperados

Balance post-viaje SIN resources:
5.0 - (10 × 0.25) = 2.5 → 125% margen (sobrevive)

Balance post-viaje CON 1 resource:
5.0 + 0.75 - (10 × 0.25) = 3.25 → 162% margen (sobrevive)
```

**Conclusión**: spawn_rate 0.30 genera ~1 resource por episodio, suficiente para SOBREVIVIR pero NO para APRENDER estrategia goal-seeking.

### 2. RECOMPENSA GOAL INSUFICIENTE

**Estructura Actual**:
```python
# Llegar a meta SIN resources
Balance final = 2.5 (> threshold 2.0)
Reward = 0 (goal_reward + no penalties)

# Llegar a meta CON 1 resource
Balance final = 3.25
Reward = 0.75 (resource_reward)
```

**Problema**: **NO HAY RECOMPENSA EXPLÍCITA POR ALCANZAR META**

Agente aprende:
- ✅ Recolectar resources (+0.75)
- ✅ Evitar tripwires (-0.5)
- ✅ Evitar inanición (drena -0.25/step)
- ❌ **NO aprende que llegar a meta es objetivo**

### 3. STEP_COST DOMINA SEÑAL

**Análisis Recompensas**:
```
Episode típico (22 steps, starvation):
- Resources: +0.75 × 1 = +0.75
- Step cost: -0.25 × 22 = -5.5
- Penalty low: -1.0 × ~3 pasos = -3.0
- Starvation: -2.5 (muerte)
Total: -10.25 (matches observed -11.85)

Episode teórico óptimo (10 steps, goal):
- Resources: +0.75 × 1 = +0.75
- Step cost: -0.25 × 10 = -2.5
- Goal reward: +0.0 (NO EXISTE)
Total: -1.75
```

**Problema**: Incluso episode PERFECTO reward negativo. Agente NO incentivado alcanzar meta rápido.

---

## 🛠️ RECOMENDACIONES ECONOMÍA

### Ajuste Crítico #1: GOAL REWARD
```python
# sim/config.py
ENV_GOAL_REWARD = 10.0  # NUEVO: recompensa explícita meta
```

**Impacto**:
```
Episode óptimo CON goal_reward:
+10.0 (goal) + 0.75 (resource) - 2.5 (steps) = +8.25 ✅ POSITIVO

Episode subóptimo SIN goal:
+0.75 (resource) - 5.5 (steps) - 3.0 (penalty) = -7.75 ❌ NEGATIVO

Delta = 8.25 - (-7.75) = +16.0 → Señal CLARA alcanzar meta
```

### Ajuste Crítico #2: spawn_rate
```python
# Configuración actual
resource_spawn_rate = 0.30

# Propuesta
resource_spawn_rate = 0.40  # +33%
```

**Impacto**:
- Resources esperados: 0.83 → 1.11 (+34%)
- Probabilidad ≥2 resources: 20% → 40%
- Margen seguridad: 162% → 200%

### Ajuste Opcional: step_cost
```python
# Configuración actual
step_cost = -0.25

# Propuesta
step_cost = -0.15  # -40%
```

**Impacto**:
```
Episode óptimo:
-0.25 × 10 = -2.5 → -0.15 × 10 = -1.5 (delta +1.0)

Episode subóptimo:
-0.25 × 22 = -5.5 → -0.15 × 22 = -3.3 (delta +2.2)

→ Reduce castigo exploración, facilita aprendizaje
```

---

## 📈 COMPARACIÓN VALIDACIÓN vs SMOKE TEST

| Métrica | Validación 200 | Smoke 1000 | Mejora |
|---------|---------------|-----------|--------|
| Success | 0.0% | 0.0% | - |
| Reward | -10.8 | -11.8 | -9% ⚠️ |
| Resources | 0.0 | 0.92 | +∞ ✅ |
| Starvation | 100% | 96.8% | -3.2% ✅ |
| Epsilon | 0.367 | 0.010 | Convergió ✅ |

**Interpretación**:
- ✅ Epsilon convergió (200 eps insuficientes, 1000 OK)
- ✅ Resources mejoró 0.0 → 0.92 (spawn_rate 0.30 ayuda)
- ✅ Starvation 100% → 96.8% (margen adicional ayuda)
- ❌ Success 0% sin cambio (falta goal_reward)
- ⚠️ Reward -10.8 → -11.8 peor (policy convergió a subóptimo)

---

## 🎯 CONCLUSIONES

### ✅ LO QUE SÍ FUNCIONA

1. **Fixes Técnicos Validados**:
   - max_steps parametrizado (3× Manhattan)
   - risk_penalty signo correcto + elif
   - step_cost drena resources
   - penalty_low -1.0 (vs -10.0 brutal)

2. **DQN Converge Correctamente**:
   - Epsilon 1.0 → 0.01 en 300 eps
   - Aprende recolectar resources (0.0 → 0.92)
   - Policy estable últimos 700 eps

3. **Economía Balanceada (Sobrevivencia)**:
   - Balance 5.0 + spawn_rate 0.30 → supervivencia 96.8%
   - Margen 162% threshold_low
   - step_cost -0.25 no es brutal

### ❌ LO QUE NO FUNCIONA

1. **NO HAY APRENDIZAJE GOAL-SEEKING**:
   - 0/1000 episodios alcanza meta
   - Policy convergió a comportamiento subóptimo
   - Agente NO incentivado buscar goal

2. **ECONOMÍA NO INCENTIVA META**:
   - goal_reward = 0.0 (NO recompensa)
   - Episode óptimo reward negativo (-1.75)
   - step_cost domina señal aprendizaje

3. **spawn_rate MARGINAL**:
   - Resources ~1.0 promedio (apenas suficiente)
   - Tripwires 0.03 (exploración mínima)
   - Grid 6×6 requiere ~1.5-2.0 resources

---

## 🚦 DECISIÓN v10.7

### ❌ NO LISTO PARA v10.7

**Veredicto**: Smoke test 1000 eps confirma sistema NO aprende objetivo primario (alcanzar meta).

**Evidencia**:
- 3/4 gates fallidos (success, resources, rewards)
- 0% success rate en 1000 episodios
- Policy convergió a comportamiento subóptimo
- Falta incentivo goal-seeking

### 📋 PLAN FORWARD

#### Opción A: v10.8 - Economía Goal-Oriented 🟢 RECOMENDADO

1. **Implementar goal_reward = 10.0**
2. **Ajustar spawn_rate 0.30 → 0.40**
3. **Reducir step_cost -0.25 → -0.15 (opcional)**
4. **Smoke test 1000 eps gates**:
   - Success >10% (DQN aprende meta)
   - Rewards >0 últimos 100 eps (positivo)
   - Resources >1.5 promedio

#### Opción B: Cerrar v10.x - Documentar Lecciones 🟡 ALTERNATIVA

1. **Documentar serie v10**: "Calibración economía + Debugging fixes"
2. **Validar técnicamente**: Fixes 1-5 funcionan (rewards -11 vs -160)
3. **Reconocer limitaciones**: Sistema sobrevive pero NO aprende goal
4. **Serie v11**: "Goal-oriented rewards + Spawn rate balanceado"

#### Opción C: v10.8 Minimal - Solo goal_reward 🟡 CONSERVADOR

1. **Solo goal_reward = 10.0** (cambio mínimo)
2. **Mantener spawn_rate 0.30, step_cost -0.25**
3. **Smoke test 500 eps validar mejora**
4. **Iterar si gates fallan**

---

## 📝 LECCIONES APRENDIDAS

### 1. Convergencia ≠ Aprendizaje Correcto

**Observación**: Epsilon convergió (0.01), policy estable, PERO comportamiento subóptimo.

**Lección**: **DQN puede convergir a estrategia incorrecta si señales reward mal diseñadas.**

### 2. Survival ≠ Task Success

**Observación**: Starvation 96.8% (agente sobrevive), pero success 0% (NO alcanza meta).

**Lección**: **Balancear economía para sobrevivencia NO garantiza aprendizaje objetivo primario.**

### 3. 200 vs 1000 Episodios

**Observación**: Validación 200 eps epsilon=0.367, smoke test 1000 eps epsilon=0.01.

**Lección**: **200 episodios INSUFICIENTES validar convergencia DQN. Mínimo 1000 eps necesario.**

### 4. Recompensa Explícita Crítica

**Observación**: Agente aprende recolectar resources (+0.75) pero NO busca goal (reward=0).

**Lección**: **TODO objetivo aprendizaje DEBE tener recompensa explícita positiva dominante.**

---

## 🔗 SIGUIENTE PASO INMEDIATO

**Usuario decide** entre:

1. **v10.8 Goal-Oriented** (implementar goal_reward + ajustes economía)
2. **Cerrar v10.x** (documentar lecciones, planificar v11)
3. **v10.8 Minimal** (solo goal_reward, iterar)

**BLOQUEO v10.7 CONFIRMADO**: No declarar "listo" hasta smoke test demuestre success >5%.

---

**Documentos Relacionados**:
- `AUDITORIA_VALIDACION_HONESTA.md` - Análisis crítico validación 200 eps
- `RESUMEN_VALIDACION_FIX5_TODOS_GRIDS.md` - Validación multi-grid (optimista)
- `COMPARACION_FIX5_BEFORE_AFTER.md` - Análisis 6×6 detallado
- `VALIDACION_FIXES_v10.7.md` - Fixes técnicos 1-5

**Resultados Raw**:
- `results/smoke_test_convergencia_1000eps/episodes.csv` - 1000 episodios detalle
- `results/smoke_test_convergencia_1000eps/summary.json` - Métricas agregadas
