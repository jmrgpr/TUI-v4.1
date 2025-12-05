# 🛑 ANÁLISIS CRÍTICO v10.x - Serie Bloqueada

**Fecha**: 2025-12-05  
**Status**: 🔴 **SERIE v10.x BLOQUEADA** - Problema arquitectural NO económico

---

## 📊 RESUMEN ITERACIONES

| Versión | step_cost | threshold | goal_reward | max_steps | spawn | Success | Rewards | Steps | Resources |
|---------|-----------|-----------|-------------|-----------|-------|---------|---------|-------|-----------|
| v10.7 | -0.25 | 2.0 | 0.0 | 30 | 0.30 | 0.0% | -11.85 | 22.5 | 0.98 |
| v10.8 | -0.15 | 2.0 | 10.0 | 30 | 0.40 | 0.0% | -31.70 | 30.0 | 0.98 |
| v10.9 | -0.25 | 1.0 | 20.0 | 20 | 0.40 | 0.0% | -28.87 | 19.96 | 0.67 |

**Observación crítica**: 3 iteraciones, 2400 episodios totales, **0% success CONSTANTE**.

---

## 🔍 ROOT CAUSE ARQUITECTURAL

### Hallazgo #1: Agent NO Explora Hacia Meta

**Evidencia**:
```
v10.7: tripwires 0.03, resources 0.98
v10.8: tripwires 0.04, resources 0.98
v10.9: tripwires 0.16, resources 0.67

Tripwires ~0.1 promedio → Agent NO se mueve activamente
Resources ~0.8 promedio → Recolecta ALGUNOS PERO no explora meta
```

**Diagnóstico**: Agent aprende comportamiento **estático** (camping).

### Hallazgo #2: Economía NO Es el Problema

**Evidencia v10.9**:
```
Config "óptima":
- goal_reward 20.0 (DOMINA penalties)
- step_cost -0.25 (balance drena)
- threshold_low 1.0 (menos brutal)
- spawn_rate 0.40 (resources disponibles)
- max_steps 20 (presión temporal)

Resultado: rewards -28.87, success 0%, resources 0.67 ❌
```

**Conclusión**: Incluso con economía "perfecta" teóricamente, agent NO converge.

### Hallazgo #3: DQN Converge a Estrategia Subóptima

**Evidencia**:
```
Epsilon: 1.0 → 0.01 en ~150-300 eps (convergencia rápida)
Success: 0% CONSTANTE en 500-1000 eps
Steps: 19.96-30.0 (máximo permitido)
Starvation v10.9: 54% (muere mitad episodios)
```

**Diagnóstico**: DQN converge a policy **"hacer nada hasta morir"**.

**Razón**: Sin reward shaping, DQN solo ve:
- Mover → step_cost negativo INMEDIATO
- Quedarse quieto → penalty_low acumulativo RETARDADO
- Alcanzar meta → goal_reward NUNCA (exploración insuficiente)

**Policy óptima local**: Minimizar step_cost → no moverse.

---

## 💡 INSIGHTS FUNDAMENTALES

### 1. Sparse Rewards Son INSUFICIENTES

**Problema**: goal_reward solo se obtiene alcanzando meta. En grid 6×6 con exploración random:
```
Probabilidad alcanzar meta por azar: ~1/36 = 2.8%
En 500 eps con epsilon 0.01: ~5 intentos random × 2.8% = 0.14 episodios

→ DQN NUNCA experimenta goal_reward en fase exploración
→ Policy converge SIN saber que goal existe
```

**Lección**: **Sparse rewards requieren shaped rewards o curriculum learning.**

### 2. Penalties Dominan Aprendizaje

**Problema**: Agent experimenta penalties CONSTANTEMENTE:
```
step_cost: -0.25 cada paso (100% episodios)
penalty_low: -1.0 cuando resources <1.0 (~50% pasos)
starvation: -2.5 al morir (54% episodios)

goal_reward: +20.0 NUNCA (0% episodios)

Ratio experiencia: 0 positiva / 1500 negativa = SOLO aprende evitar dolor
```

**Lección**: **Penalties sin shaped rewards → agent aprende "no hacer nada".**

### 3. Exploración Random NO Es Suficiente

**Problema**: Epsilon-greedy con decay 0.9995:
```
Epsilon 0.5 (exploración 50%): ~150 eps
Epsilon 0.1 (exploración 10%): ~450 eps
Epsilon 0.01 (exploración 1%): ~600 eps

En 500 eps: ~250 eps exploración efectiva
En grid 6×6: 36 estados × 10 steps promedio = 360 exploraciones necesarias

→ INSUFICIENTE para descubrir meta con probabilidad razonable
```

**Lección**: **Grid 6×6 requiere >1000 eps O shaped rewards para descubrimiento.**

---

## 🎯 OPCIONES FORWARD

### 🔴 Opción A: CERRAR v10.x (RECOMENDADO)

**Justificación**:
- 3 iteraciones, 2400 episodios, 0% success → problema NO es tunning
- Economía "perfecta" v10.9 falló → problema NO es balanceo
- DQN converge a subóptimo → problema ES arquitectura

**Plan**:
1. Documentar lecciones aprendidas v10.x
2. Declarar v10.x "Calibración economía + Exploración insuficiente"
3. Planificar v11 con **arquitectura diferente**

**v11 Propuesta**:
- **Curriculum learning**: 4×4 (trivial) → 6×6 (intermedio) → 8×8 (complejo)
- **Shaped rewards**: Distance-based bonus hacia meta
- **Exploration bonus**: Count-based (visitas a estados)
- **Pretrain**: Behavioral cloning con trayectorias óptimas

### 🟡 Opción B: v10.10 Último Intento

**Cambios DRÁSTICOS**:
```python
# Shaped reward: distancia a meta
distance_to_goal = manhattan_distance(agent_pos, goal_pos)
reward += 0.1 × (distance_prev - distance_current)  # Acercarse bonus

# Exploration bonus
state_visits[state] += 1
reward += 1.0 / sqrt(state_visits[state])  # Novelty bonus

# Aumentar goal_reward
ENV_GOAL_REWARD = 50.0  # vs 20.0 (2.5× más)

# Grid 4×4 simplificado
GRID_SIZE = 4  # vs 6 (36 → 16 estados)
```

**Gates v10.10** (500 eps, 4×4):
- Success >25% (4×4 más simple)
- Rewards >+10 últimos 100 eps
- Agent alcanza meta ≥1 vez primeros 200 eps

**Riesgo**: SI v10.10 falla → mismo problema persiste.

### 🟢 Opción C: Iniciar v11 Directamente

**Enfoque**: Curriculum learning riguroso.

**Fase 1: 4×4 Trivial** (200 eps):
- Grid 4×4, Manhattan=4, max_steps=8
- goal_reward=30, spawn_rate=0.50
- Gate: Success >50%

**Fase 2: 6×6 Transfer** (500 eps):
- Grid 6×6, load weights de 4×4
- goal_reward=20, spawn_rate=0.40
- Gate: Success >20%

**Fase 3: 8×8 Completo** (1000 eps):
- Grid 8×8, load weights de 6×6
- goal_reward=15, spawn_rate=0.35
- Gate: Success >10%

---

## 📝 LECCIONES APRENDIDAS v10.x

### 1. Sparse Rewards + Random Exploration = Fallo

**Error**: Asumimos epsilon-greedy suficiente para descubrir meta.

**Realidad**: Probabilidad descubrimiento ~0.14 episodios en 500 eps.

**Lección**: **Sparse rewards requieren shaped rewards O curriculum O demos.**

### 2. Economía Balanceada ≠ Aprendizaje

**Error**: Enfocamos en tunear step_cost, threshold_low, spawn_rate.

**Realidad**: Economía "perfecta" v10.9 falló con 0% success.

**Lección**: **Economía viable NO garantiza descubrimiento objetivo.**

### 3. DQN Converge A Mínimo Local

**Error**: Asumimos más episodios → mejor convergencia.

**Realidad**: DQN converge rápido (epsilon 0.01 en 300 eps) a "hacer nada".

**Lección**: **Convergencia rápida SIN reward shaping = mínimo local.**

### 4. Tunning Hiperparámetros Tiene Límite

**Error**: Iteramos v10.7 → v10.8 → v10.9 tunneando economía.

**Realidad**: 3 iteraciones, TODOS 0% success → problema NO es parámetros.

**Lección**: **Si 3+ iteraciones fallan, problema ES arquitectura.**

### 5. Grid 6×6 NO Es "Simple"

**Error**: Asumimos 6×6 (36 estados) es "toy problem".

**Realidad**: 36 estados × 10 steps × 4 acciones = 1440 experiencias necesarias.

**Lección**: **"Simple" para humanos ≠ "simple" para DQN random exploration.**

---

## 🎯 DECISIÓN FINAL

### Recomendación: **CERRAR v10.x + INICIAR v11 Curriculum**

**Razones**:
1. 3 iteraciones, 0% success CONSTANTE → problema NO económico
2. v10.9 economía "perfecta" falló → no hay más parámetros tunear
3. Root cause arquitectural: sparse rewards + random exploration
4. Curriculum learning addressing problema directamente

**Plan inmediato**:
1. Documentar v10.x lecciones aprendidas
2. Comitear análisis crítico
3. Diseñar arquitectura v11:
   - Curriculum 4×4 → 6×6 → 8×8
   - Shaped rewards (distance-based)
   - Exploration bonus (count-based)
4. Implementar Fase 1 (4×4 trivial)
5. Gate: Success >50% en 200 eps

**SI v11 Fase 1 falla**: Considerar:
- Behavioral cloning (imitation learning)
- PPO (on-policy más estable)
- Reward engineering más agresivo
- Problema fundamental con task design

---

## 📊 TABLA COMPARATIVA FINAL

| Aspecto | v10.7 | v10.8 | v10.9 | v11 Propuesta |
|---------|-------|-------|-------|---------------|
| **Arquitectura** | DQN vanilla | DQN vanilla | DQN vanilla | DQN + Curriculum |
| **Rewards** | Sparse | Sparse | Sparse | Shaped |
| **Exploration** | ε-greedy | ε-greedy | ε-greedy | ε-greedy + Bonus |
| **Grid** | 6×6 | 6×6 | 6×6 | 4×4 → 6×6 → 8×8 |
| **Success** | 0% | 0% | 0% | TBD |
| **Diagnóstico** | Sin goal_reward | Economía contraproducente | Economía OK, arquitectura NO | Arquitectura nueva |

---

## 🔗 DOCUMENTOS RELACIONADOS

- `SMOKE_TEST_1000_EPS_ANALISIS.md` - v10.7 análisis detallado
- `VALIDACION_AUDITORIA_v10.7_CONFIRMADA.md` - Usuario confirmó análisis
- `ANALISIS_FALLO_v10.8.md` - Root cause step_cost NO-lineal
- `results/smoke_test_v10.9_rapid/` - Datos 500 eps v10.9

**Commit**: Pendiente análisis crítico v10.x serie bloqueada
