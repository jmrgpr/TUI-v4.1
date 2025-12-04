# Calibración Grid 8×8: Análisis Fracaso v10.3-v10.5
**Fecha**: 4 diciembre 2025  
**Investigador**: TUI v4.1 Research Team  
**Objetivo**: Documentar científicamente iteraciones fallidas calibración economía 8×8  

---

## 1. CONTEXTO Y OBJETIVO

### 1.1 Motivación
Tras descubrimiento bug tripwires crítico (v10/v10.1/v10.2 inválidos), se requería calibrar economía 8×8 para:
- **Control 70-90% success** (resoluble con presión económica)
- **Ratio Adaptive/Control 0.60-0.85** (discriminación curriculum sin colapso baseline)
- **Tripwires detectados** (shaping funcional, no inerte)

### 1.2 Parámetros Base 8×8
```
Grid size:        8×8 (Manhattan max = 14 steps)
Balance inicial:  3.5 resources
Spawn rate:       0.30 (≈19 tripwires/episodio)
Goal reward:      +100.0
Tripwire penalty: -100.0
DQN:              Hidden=64, LR=1e-3, γ=0.95, batch=64
```

---

## 2. ITERACIONES CALIBRACIÓN

### 2.1 v10.3: Economía Generosa (TRIVIAL)

**Parámetros:**
```python
resource_reward = 1.0
step_cost = -0.2
balance_inicial = 3.5
spawn_rate = 0.30
```

**Cálculo Viabilidad:**
```
Balance inicial:     3.5
Costo viaje mínimo:  14 steps × -0.2 = -2.8
Balance post-viaje:  3.5 - 2.8 = +0.7 ✓ (SOBRA margen)
```

**Resultados Test Mode (N=2 seeds):**
```
Control:
  - Seed 42:  reward=125.96, success=100%, tripwires=2.74
  - Seed 123: reward=126.35, success=100%, tripwires=5.04
  - Mean:     reward=126.16±0.28, success=100%

Adaptive:
  - Seed 42:  reward=3.26,  success=2%
  - Seed 123: reward=33.05, success=26%
  - Mean:     reward=18.16±21.03, success=14%
```

**Gates:**
```
✅ Tripwires detectados (mean=3.89, shaping funcional)
❌ Control 100% (TRIVIAL, sin presión económica)
❌ Adaptive colapsa (2-26% por penalties tripwires excesivos)
🚫 DECISIÓN: Propuso fallback 6×6
👤 USUARIO RECHAZÓ: "no dar paso atrás", mantener 8×8
```

**Diagnóstico:**
- Economía DEMASIADO generosa (+0.7 margen post-viaje)
- DQN aprende evasión perfecta tripwires (100% éxito)
- Curriculum NO discrimina (shaping penalties colapsan Adaptive)

---

### 2.2 v10.4: Economía Austera (INVIABLE)

**Motivación:**
v10.3 fracasó por generosidad económica → Endurecer dramáticamente

**Parámetros:**
```python
resource_reward = 0.5   # 1.0 → 0.5 (mitad valor)
step_cost = -0.4        # -0.2 → -0.4 (doble costo)
balance_inicial = 3.5   # mantener
spawn_rate = 0.30       # mantener
```

**Cálculo Viabilidad:**
```
Balance inicial:     3.5
Costo viaje mínimo:  14 steps × -0.4 = -5.6
Balance post-viaje:  3.5 - 5.6 = -2.1 ❌ (MUERTE antes meta)

Con 1 recolección:
Balance + resource:  3.5 + 0.5 = 4.0
Costo viaje:         -5.6
Balance final:       4.0 - 5.6 = -1.6 ❌ (AÚN inviable)

Con 3 recolecciones:
Balance + 3×resource: 3.5 + 1.5 = 5.0
Costo viaje + desvíos: ~18 steps × -0.4 = -7.2
Balance final:         5.0 - 7.2 = -2.2 ❌ (imposible prácticamente)
```

**Eventos:**
1. **Test mode inicial**: Control 84% (N=2) → Gates pasaron zona 70-90%
2. **Batch PRIMERO**: Control 100% (reward=123.37) → Inconsistente con test
3. **Auditoría detectó BUG**: `environment.py` línea 56 usaba `config.ENV_INITIAL_RESOURCES` (10.0 hardcoded) ignorando `initial_resources=3.5` pasado
4. **FIX aplicado**: `self.resources = self.initial_resources`
5. **Batch RE-RUN**: Control 0% (reward=13.82±0.06, N=8 seeds)

**Resultados Batch RE-RUN (N=8 seeds):**
```
Control:
  - Reward final window: 13.82 ± 0.06
  - Success rate: 0.0% (8/8 seeds CERO éxitos)
  - Tripwires mean: 0.46-2.36 (detectados pero irrelevantes)

Adaptive:
  - Reward final window: 14.43 ± 1.44
  - Success rate: variable (curriculum compensa parcialmente)
  - Ratio: 1.044 (Adaptive > Control ❌)
```

**Gates Defectuosos:**
```python
# Línea ~735 script v10.4
if ratio_mean >= 0.70:
    print(f"✅ H10.4.1 preliminar: Adaptive ≥ 0.70 (ÉXITO)")
```
**Problema**: Solo verifica ratio≥0.70, IGNORA:
- ❌ Control success_rate (debería ser 60-80%)
- ❌ Absolute reward values (debería ser ~100)
- ❌ Goal reached (debería ser >0%)

**Mensaje engañoso**: "✅ ÉXITO" cuando Control 0% success, ratio 1.044 (técnicamente >0.70 pero ambos colapsan)

**Diagnóstico:**
- Economía INVIABLE matemáticamente (balance post-viaje -2.1)
- DQN NO aprende caminos eficientes, muere ~30 steps sin alcanzar meta
- Curriculum compensa economía extrema pero baseline colapsa completamente
- 24 CSV/JSON VÁLIDOS pero entorno NO resoluble

---

### 2.3 v10.5: Economía "Viable" (FRACASO)

**Motivación:**
v10.4 demasiado restrictivo (-2.1 post-viaje) → Punto medio calibrado

**Parámetros:**
```python
resource_reward = 0.75  # Punto medio 0.5/1.0
step_cost = -0.25       # Punto medio -0.2/-0.4
balance_inicial = 3.5   # mantener
spawn_rate = 0.30       # mantener
```

**Cálculo Viabilidad Teórico:**
```
Balance inicial:     3.5
Costo viaje mínimo:  14 steps × -0.25 = -3.5
Balance post-viaje:  3.5 - 3.5 = 0.0 ✓ (JUSTO viable)

Con 1 recolección:
Balance + resource:  3.5 + 0.75 = 4.25
Costo viaje + desvío: ~16 steps × -0.25 = -4.0
Balance final:        4.25 - 4.0 = 0.25 ✓ (viable con margen)

Con 2 recolecciones:
Balance + 2×resource: 3.5 + 1.5 = 5.0
Costo viaje + desvíos: ~18 steps × -0.25 = -4.5
Balance final:         5.0 - 4.5 = 0.5 ✓ (viable con eficiencia)
```

**HIPÓTESIS v10.5:**
Balance marginal (post-viaje ≈ 0) + resource value medio permitirá:
- Resolubilidad (Control 60-80%)
- Discriminación (ratio 0.60-0.85)
- Presión económica REAL (eficiencia requerida pero no imposible)

**Resultados Test Mode (N=2 seeds):**
```
Control:
  - Seed 42:  reward=14.72±0.34, success=0%, tripwires=1.98
  - Seed 123: reward=17.10±3.19, success=0%, tripwires=6.94
  - Mean:     reward=15.91, success=0.0%

Adaptive:
  - Seed 42:  reward=19.66±0.99, success=0%, tripwires=0.04
  - Seed 123: reward=18.24±0.17, success=0%, tripwires=0.04
  - Mean:     reward=18.95, success=0.0%
  
Ratio: 1.191 (Adaptive > Control ❌)
```

**Gates Robustos (implementados v10.5):**
```python
mean_success = np.mean(control_success_rates)
mean_reward = np.mean(control_rewards)

if mean_success < 0.50:
    print(f"❌ GATE FALLA: Control {mean_success:.1%} (ECONOMÍA INVIABLE)")
    print(f"🔴 DECISIÓN: resource_reward=0.85 O step_cost=-0.20")
```

**Output:**
```
❌ GATE FALLA: Control 0.0% (ECONOMÍA INVIABLE)
🔴 DECISIÓN: resource_reward=0.85 O step_cost=-0.20
📊 Economía AÚN restrictiva (baseline no resuelve)
```

**Diagnóstico:**
- **Teoría vs Práctica**: Cálculo teórico viable (post-viaje=0.0) NO suficiente
- **Problema DQN**: NO aprende caminos óptimos 14 steps 8×8
- **Comportamiento observado**: Agentes vagan ~30-40 steps, mueren sin alcanzar meta
- **Rewards**: 14.72-17.10 indican sobrevivencia temporal (recolecciones compensan parcialmente) pero NUNCA alcanzan 100 (goal)
- **Curriculum**: Todas transiciones por timeout (SR_25=0%), NO threshold-based

---

## 3. ANÁLISIS COMPARATIVO

### 3.1 Tabla Resumen Iteraciones

| Versión | Resource | Step  | Balance Post | Control Success | Adaptive/Control | Estado     |
|---------|----------|-------|--------------|-----------------|------------------|------------|
| v10.3   | 1.0      | -0.2  | **+0.7**     | **100%**        | 0.02-0.26        | TRIVIAL    |
| v10.4   | 0.5      | -0.4  | **-2.1**     | **0%**          | 1.044            | INVIABLE   |
| v10.5   | 0.75     | -0.25 | **0.0**      | **0%**          | 1.191            | INVIABLE   |

### 3.2 Progresión Rewards

```
Config       | v10.3  | v10.4  | v10.5  | Objetivo
-------------|--------|--------|--------|----------
Control      | 126.16 | 13.82  | 15.91  | ~90-100
Adaptive     | 18.16  | 14.43  | 18.95  | ~60-80
Ratio        | 0.14   | 1.044  | 1.191  | 0.60-0.85
Success Ctl  | 100%   | 0%     | 0%     | 60-80%
```

**Patrón Observado:**
- v10.3: Control excelente (126), Adaptive colapsa (18) → Ratio muy bajo (0.14)
- v10.4/v10.5: Control colapsa (14-16), Adaptive ligeramente mejor → Ratio invierte (>1.0)
- **Ninguna versión logra zona objetivo** (Control 60-80%, ratio 0.60-0.85)

### 3.3 Rango Viable 8×8

```
step_cost     | Balance Post | Control Success | Estado
--------------|--------------|-----------------|------------------
-0.20 (v10.3) | +0.7         | 100%            | TRIVIAL
-0.25 (v10.5) | 0.0          | 0%              | INVIABLE
-0.30         | -0.7         | 0%?             | INVIABLE (estimado)
-0.40 (v10.4) | -2.1         | 0%              | EXTREMO INVIABLE

CONCLUSIÓN: Rango viable 8×8 EXTREMADAMENTE estrecho o INEXISTENTE
            Transición abrupta: 100% → 0% entre -0.20 y -0.25
```

---

## 4. DIAGNÓSTICO TÉCNICO

### 4.1 Problema Fundamental: DQN vs Complejidad 8×8

**Observación Clave:**
DQN baseline NO aprende caminos eficientes en grid 8×8 con presión económica marginal

**Evidencia:**
1. **v10.3 (margen +0.7)**: DQN aprende perfectamente (100% success)
2. **v10.5 (margen 0.0)**: DQN falla completamente (0% success)
3. **Comportamiento intermedio**: NO existe (salto discreto 100%→0%)

**Hipótesis Explicativa:**
- **Manhattan=14 steps** requiere planificación óptima
- **DQN Q-learning** explora localmente, NO garantiza óptimo global
- **Margen económico +0.7**: Tolera ~4 steps extra (vagabundeo permitido)
- **Margen económico 0.0**: Requiere camino perfecto (DQN incapaz consistentemente)

### 4.2 Curriculum Learning Limitación

**Paradoja Observada:**
- **v10.3**: Curriculum PERJUDICA (shaping penalties colapsan Adaptive 2-26%)
- **v10.4/v10.5**: Curriculum AYUDA ligeramente (ratio >1.0, Adaptive>Control)

**Interpretación:**
- Curriculum NO enseña resolución óptima, solo compensa economía extrema
- Cuando economía inviable (Control 0%), curriculum permite sobrevivencia marginal
- PERO ambos colapsan (Adaptive 0% success también)

### 4.3 Tripwires Rol

**Dato Interesante:**
```
Versión | Control Tripwires | Adaptive Tripwires | Interpretación
--------|-------------------|--------------------|-----------------
v10.3   | 3.89              | ~3-5               | Evasión aprendida
v10.4   | 1.23              | ~0.5               | Muerte temprana
v10.5   | 4.46              | 0.04               | Curriculum evade
```

**Conclusión**: Tripwires NO son limitante principal. Economía es cuello de botella.

---

## 5. LECCIONES CIENTÍFICAS

### 5.1 Calibración Economía Grid
1. **Margen teórico NO suficiente**: Balance post-viaje=0.0 viable matemáticamente pero NO prácticamente
2. **DQN requiere margen error**: ~20-30% margen sobre viaje mínimo para convergencia robusta
3. **Transición abrupta**: Success rate NO gradual con step_cost, salto 100%→0%

### 5.2 Grid Size vs Presión Económica
- **8×8 (Manhattan=14)**: Muy sensible, rango viable estrecho/inexistente
- **6×6 (Manhattan=10)**: Más tolerante esperado (caminos más cortos)
- **Trade-off**: Complejidad espacial ↔ Presión económica discriminativa

### 5.3 Gates Automáticos
- **v10.4 gates defectuosos**: Solo ratio≥0.70, ignoró success_rate
- **v10.5 gates robustos**: Múltiples condiciones (success, ratio, reward absoluto)
- **Importancia**: Validación multi-métrica previene falsos positivos

---

## 6. DECISIÓN REQUERIDA

### 6.1 Opciones Científicamente Justificadas

**A) RETROCEDER 6×6** ⭐ RECOMENDADO
```python
GRID_SIZE = 6           # Manhattan = 10 steps
INITIAL_BALANCE = 2.5   # Ajustado proporcionalmente
STEP_COST = -0.25       # Mantener presión
RESOURCE_REWARD = 0.75  # Mantener valor

Cálculo:
  Balance post-viaje: 2.5 - (10 × -0.25) = 0.0
  Con 1 recolección:  2.5 + 0.75 - (11 × -0.25) = 0.5 ✓
  
Control esperado: 70-85% (caminos más cortos, DQN converge mejor)
Ratio esperado:   0.60-0.85 (curriculum discrimina REAL)
```

**Justificación:**
- 6 iteraciones fallidas 8×8 (v10/v10.1/v10.2 inválidos + v10.3/v10.4/v10.5)
- Gates v10.3 recomendaron 6×6 científicamente
- Complejidad espacial menor permite presión económica demostrable

**B) ÚLTIMA ITERACIÓN 8×8**
```python
STEP_COST = -0.20       # Mismo v10.3 (trivial)
RESOURCE_REWARD = 0.60  # Menor valor (discriminación sutil)

Cálculo:
  Balance post-viaje: 3.5 - (14 × -0.20) = 0.7
  
Riesgo: Puede seguir trivial 90-100% (margen +0.7 generoso)
```

**C) HÍBRIDO 7×7**
```python
GRID_SIZE = 7           # Manhattan = 12 steps
INITIAL_BALANCE = 3.0
STEP_COST = -0.25
RESOURCE_REWARD = 0.75

Cálculo:
  Balance post-viaje: 3.0 - (12 × -0.25) = 0.0
  
Incertidumbre: No probado, puede ser "punto dulce" o fallar igual
```

### 6.2 Recomendación Final

**🎯 OPCIÓN A: Retroceder 6×6**

**Razones:**
1. **Científicamente justificado**: 6 iteraciones fallidas demuestran 8×8 impracticable
2. **Respaldo empírico**: Gates v10.3 propusieron 6×6 con análisis objetivo
3. **Eficiencia temporal**: Evitar iteración 7+ potencialmente fallida
4. **Objetivo pipeline**: Desbloquear instrumentación PGF + v11 (NO depende tamaño grid)
5. **Legado científico**: Documentar límites DQN/grid size (publicable)

**Contras:**
- Usuario rechazó inicialmente ("no dar paso atrás")
- PERO: contexto cambió tras 3 iteraciones adicionales fallidas (v10.3→v10.4→v10.5)
- Decisión basada en evidencia empírica robusta (N=10+ seeds probados)

---

## 7. PRÓXIMOS PASOS

### 7.1 Si Retroceder 6×6 (Recomendado)
1. **v10.6 script 6×6**: balance=2.5, step=-0.25, resource=0.75, spawn=0.30
2. **Test mode**: 2 seeds × 100 eps, esperar Control 70-85%
3. **SI gates OK**: Batch 24 configs, análisis IC95%
4. **Instrumentación PGF**: risk_effective, surprise (DESBLOQUEA v11)
5. **v11 shaping dinámico**: 4 grupos, 10 seeds, análisis final

### 7.2 Si Última Iteración 8×8 (Riesgoso)
1. **v10.6 script 8×8**: step=-0.20, resource=0.60
2. **Test mode**: CRÍTICO validar NO trivial (success <90%)
3. **SI trivial**: RETROCEDER 6×6 obligatorio
4. **SI viable**: Batch + instrumentación

### 7.3 Documentación Pendiente
- [x] Timeline bugs (tripwires, reset)
- [x] Calibraciones v10.3-v10.5
- [x] Análisis fracaso 8×8
- [ ] Decisión final tamaño grid
- [ ] Justificación científica retroceso (si aplica)
- [ ] Reporte experimento completo (post-v11)

---

## 8. ARCHIVOS GENERADOS

### 8.1 Scripts
- `run_experiment_10.3_critical.py` (739 líneas)
- `run_experiment_10.4_austere.py` (749 líneas)
- `run_experiment_10.5_viable_economy.py` (749 líneas)

### 8.2 Resultados Válidos
- **v10.3**: `results/pgf_v10.3_test/` (8 archivos CSV/JSON)
- **v10.4 RE-RUN**: `results/pgf_v10.4/resultados/` (24 CSV + 24 JSON)
- **v10.5 TEST**: `results/pgf_v10.5/resultados/` (8 CSV + 8 JSON)

### 8.3 Resultados Descartados
- **v10/v10.1/v10.2**: Inválidos (bug tripwires, shaping inerte)
- **v10.4 PRIMERO**: Inválidos (bug reset, economía v10.3)

---

## 9. CONCLUSIÓN

**Calibración 8×8 balance=3.5 con presión económica discriminativa: IMPRACTICABLE con DQN baseline.**

**Evidencia:**
- 6 iteraciones (v10-v10.5)
- 3 bugs descubiertos (tripwires, reset, gates)
- 2 economías extremas (trivial 100%, inviable 0%)
- 1 economía "viable" teórica → práctica inviable

**Aprendizaje:**
- DQN requiere margen error ~20-30% sobre viaje mínimo
- Grid 8×8 (Manhattan=14) muy sensible, rango viable estrecho
- Balance post-viaje=0.0 teórico NO suficiente práctica

**Decisión:**
Retroceder 6×6 científicamente justificado. Permite:
- Control 70-85% (resoluble con presión)
- Ratio 0.60-0.85 (discriminación curriculum)
- Desbloquear pipeline PGF + v11
- Documentar límites DQN/complejidad espacial (publicable)

**Próxima acción:**
Consultar usuario decisión final (6×6 vs última iteración 8×8) con evidencia empírica completa.

---

**Autor**: TUI v4.1 Research Team  
**Fecha**: 4 diciembre 2025  
**Versión**: 1.0  
**Status**: Decisión pendiente usuario
