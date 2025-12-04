# ANÁLISIS CRÍTICO: Validación Multi-Grid Falló (0% Success)

**Fecha:** 2025-12-04  
**Status:** ⚠️ **FIXES TÉCNICOS OK, PERO ECONOMÍA INVIABLE**

---

## 🔴 Problema Identificado

### Datos Validación (results/validation_all_grids_post_fixes/)

| Grid  | Success | Starvation | Resources | Tripwires | Reward  | Steps |
|-------|---------|------------|-----------|-----------|---------|-------|
| 6×6   | 0.0%    | 100%       | 0.0       | 0.0       | -154 a -167 | 14-16 |
| 8×8   | 0.0%    | 100%       | 0.0       | 0.0       | -160 a -185 | 15-18 |
| 16×16 | 0.0%    | 100%       | 0.0       | 0.0       | -156 a -192 | 19-24 |

**Observaciones críticas:**
1. ✅ max_steps parametrizado correcto (30, 42, 90)
2. ✅ Starvation 100% confirma FIX #3 (step_cost drena resources)
3. ❌ **0 resources recolectados** → agente no explora
4. ❌ **0 tripwires activados** → agente paralizado
5. ❌ **Epsilon final 0.367** → política no progresa

---

## 🔍 Root Cause Analysis

### Breakdown Rewards Típico (6×6, 16 steps, reward=-164)

```python
# Configuración 6×6
initial_balance = 4.0
threshold_low = 5.0  # ENV_RESOURCE_THRESHOLD_LOW
penalty_low = -10.0  # ENV_PENALTY_LOW_RESOURCES
step_cost = -0.25
```

**Cálculo step-by-step:**
```
Step 0: resources = 4.0 → resources < 5.0 → penalty -10.0 aplicada
Step 1: resources = 4.0 - 0.25 = 3.75 → penalty -10.0 aplicada
Step 2: resources = 3.75 - 0.25 = 3.50 → penalty -10.0 aplicada
...
Step 16: resources = 0.0 → starvation=True, done=True

Rewards acumulados:
- step_cost: 16 × -0.25 = -4.0
- penalty_low_resources: 16 × -10.0 = -160.0  ⚠️ BRUTAL
- risk_penalty_low terminal: -25.0
- TOTAL: -4 - 160 - 25 = -189 (observado: -164)
```

### ⚠️ **El Problema: Penalty Continua Desde Step 1**

**Condición:** `if self.resources < config.ENV_RESOURCE_THRESHOLD_LOW` (línea 172 environment.py)

Con `initial_balance=4.0` y `threshold_low=5.0`:
- Agente SIEMPRE bajo threshold desde inicio
- **Penalty -10.0 aplicada CADA step** (160× más que step_cost)
- Señal reward extremadamente negativa → DQN aprende "NO MOVERSE"
- Epsilon decay no ayuda: acción random o learned = ambas castigan -10/step

**Comparación penalties:**
```
step_cost:              -0.25 por step (economía base)
penalty_low_resources:  -10.0 por step (40× más fuerte!)
penalty_tripwire:       -0.5 por hit (recién corregido de -0.01)
risk_penalty:           -25 terminal (1× al final)
```

---

## 💡 Solución Propuesta

### Opción A: Reducir Penalty Drásticamente (RECOMENDADO)
```python
# config.py línea 59
ENV_PENALTY_LOW_RESOURCES = -1.0  # Era -10.0 (10× menos)
```

**Justificación:**
- Mantiene señal "resources bajos = malo"
- Permite exploración antes de morir
- Balance: -0.25 step_cost vs -1.0 penalty = 4:1 ratio (razonable)

### Opción B: Subir Threshold Low (COMPLEMENTARIO)
```python
# config.py línea 55
ENV_RESOURCE_THRESHOLD_LOW = 2.0  # Era 5.0
```

**Justificación:**
- Con balance inicial 4.0, agente tiene ~8 steps antes de entrar zona crítica
- Permite recolectar 1-2 resources antes de penalty constante

### Opción C: Ajustar Balance Inicial (PALIATIVO)
```python
# Validación 6×6
INITIAL_BALANCE = 6.0  # Era 4.0
# Balance post-viaje = 6.0 + 0.75 - 10×0.25 = 4.25 (85% margen)
# BUT: Con threshold_low=5.0, sigue bajo desde inicio
```

**Justificación:**
- Menos efectivo si threshold_low=5.0 sigue alto
- Mejor combinado con Opción A o B

---

## 🎯 Fix Recomendado (Combo A + B)

```python
# sim/config.py

# Línea 55: Threshold bajo = emergencia económica real
ENV_RESOURCE_THRESHOLD_LOW = 2.0  # Era 5.0 (40% resources iniciales)

# Línea 59: Penalty proporcional, no brutal
ENV_PENALTY_LOW_RESOURCES = -1.0  # Era -10.0 (10× menos)
```

**Impacto esperado 6×6 (balance=4.0):**
```
Steps 0-8: resources 4.0 → 2.0 (NO penalty, explora libremente)
Step 8: resources < 2.0 → penalty -1.0 activa (señal suave)
Steps 9-16: acumula -1.0 × 8 = -8.0 (vs -160 previo)

Nuevo breakdown reward:
- step_cost: 16 × -0.25 = -4.0
- penalty_low: 8 × -1.0 = -8.0 (solo últimos 8 steps)
- risk_penalty: -25.0
- TOTAL: -37 (vs -189 previo) ✅ VIABLE PARA APRENDIZAJE
```

---

## 📊 Smoke Test Propuesto

Después de aplicar fix:

```bash
# Test 6×6 rápido (100 eps, 1 min)
python scripts/run_validation_6x6_post_penalty_fix.py
```

**Gates esperados:**
- Success rate: 10-30% (mínimo aprendizaje)
- Resources collected: >0.5 promedio
- Tripwires hit: >0.5 promedio (señal exploración)
- Starvation: 70-90% (economía aún exigente)
- Rewards: -20 a -40 rango (viable DQN)

---

## 🔄 Próximos Pasos

### Inmediato
1. ✅ Aplicar FIX penalty + threshold (Opción A + B)
2. ⏳ Smoke test 6×6 (100 eps, ~1 min)
3. ⏳ Si gates pasan → validar 8×8, 16×16
4. ⏳ Comitear "FIX #5: ENV_PENALTY_LOW_RESOURCES viable"

### Post-Fix
5. Crear v10.7 experimentos con economía REAL y penalty calibrada
6. Test mode v10.7 (~5-10 min) validar gates discriminativos
7. Batch v10.7 si gates pasan
8. Instrumentación PGF

---

## 📝 Lecciones Aprendidas

1. **Validación técnica ≠ Validación científica**
   - Fixes CÓDIGO aplicados correctamente ✅
   - Pero economía hace experimento INVIABLE ❌

2. **Penalties desbalanceadas matan aprendizaje**
   - step_cost: -0.25 (base económica)
   - penalty_low: -10.0 (40× más!) → DQN aprende "no moverse"
   - Ratio penalties debe ser proporcional impacto

3. **Threshold vs Balance inicial crítico**
   - threshold_low=5.0 con balance=4.0 → penalty DESDE step 0
   - Debe haber ventana exploración libre antes de zona crítica

4. **Smoke tests deben validar COMPORTAMIENTO**
   - No solo "código no crashea"
   - Verificar: resources_collected > 0, tripwires > 0, exploration activa

---

**STATUS:** ⏳ Pendiente aplicar FIX #5 penalty + smoke test 6×6
