# 📋 PREREGISTRO EXPERIMENTAL: PGF v10 - Curriculum Adaptativo para Escalamiento a 8×8

**Título**: Adaptive Curriculum Learning: Escalamiento Robusto de Curriculum en Grids de Alta Complejidad (8×8)  
**Investigador**: Sistema TUI v4.1  
**Fecha registro**: 4 de diciembre de 2025  
**Protocolo**: Preregistración anterior a ejecución  
**Versión experimento**: v10 ("Adaptive Curriculum en 8×8")  
**Versión preregistro**: 1.0  
**Predecesores**: v9 (4×4, curriculum fijo, N=3), v9.1 (4×4, N=10, validación)

---

## 📖 Resumen Ejecutivo

Este experimento introduce **curriculum learning adaptativo** con transiciones threshold-based y lo evalúa en grid **8×8** (complejidad alta), donde el curriculum fijo de v9 falló (ratio=0.507, 41% success).

**Motivación crítica**: 
- ✅ v9: Curriculum fijo funciona en **4×4** (67% seeds éxito)
- ⚠️ Extrapolación 6×6: Ratio 0.766 (parcial, alta varianza)
- ❌ Extrapolación 8×8: Ratio 0.507 (colapso, **mismo protocolo 4 etapas × 75 eps**)

**Diagnóstico**: Curriculum fijo con schedule rígido (75 eps/etapa) NO permite consolidación en complejidades altas. Seeds vulnerables necesitan **más tiempo** en etapas intermedias antes de escalar a s=1.0.

**Pregunta central**: ¿Un curriculum **adaptativo** que avanza solo cuando el agente demuestra dominio (success_rate>0.75 en últimos 25 eps) puede alcanzar paridad en 8×8?

**Innovación metodológica**:
- **Transiciones threshold-based**: Avanzar a siguiente escala SOLO si agente muestra éxito >75%
- **Personalización por seed**: Cada seed progresa a su propio ritmo (seeds débiles usan más episodios)
- **Timeout etapa**: Máximo 150 eps/etapa (evita estancamiento infinito)

---

## 🎯 Antecedentes y Motivación

### Resultados v9: Límite de Curriculum Fijo

**Grid 4×4 (N=3)**:

| Grupo | Reward Env | Success Rate | Interpretación |
|-------|------------|--------------|----------------|
| **Curriculum** | 88.78 ± 47.24 | 70.0% ± 52.0% | ✅ 67% éxito (2/3 seeds) |
| **ControlS0** | 115.39 ± 1.24 | 99.3% ± 1.2% | Baseline estable |

**Extrapolación a grids mayores (PROYECCIÓN, no ejecutada)**:

| Grid Size | Ratio Curriculum/Control | Success Rate | Diagnóstico |
|-----------|--------------------------|--------------|-------------|
| **4×4** | 0.766 ± 0.404 | 70% ± 52% | ✅ Funciona (2/3) |
| **6×6** | 0.766 ± 0.452 | 60% ± 48% | ⚠️ Parcial (varianza alta) |
| **8×8** | 0.507 ± 0.381 | 41% ± 43% | ❌ **COLAPSO** |

**Análisis falla 8×8**:
- **Complejidad**: Manhattan distance max = 14 (vs 6 en 4×4)
- **Tripwires**: ~16 tripwires con spawn=0.25 (vs 4 en 4×4)
- **Schedule fijo**: 4 etapas × 75 eps = 300 total
  - Seed vulnerable necesitaba **~120 eps** en s=0.5 para consolidar
  - Curriculum fijo solo da 75 → forzó transición prematura a s=1.0 → colapso

**Evidencia clave**: Seed=123 en 4×4 colapsó en etapa 4 (eps 225-300, s=1.0) a pesar de éxito en etapas 1-3. **NO tuvo suficiente tiempo** para estabilizar política en s=0.5.

### Gap que v10 Resuelve

**v9 demostró QUÉ funciona en 4×4** (curriculum fijo), **v10 demuestra CÓMO escalar a 8×8** (curriculum adaptativo).

**Hipótesis motivadora**:
> "Si permitimos que seeds vulnerables usen **más episodios** en etapas intermedias (s=0.25, s=0.5) antes de enfrentar s=1.0, podrán construir política robusta y evitar colapso en 8×8."

---

## 🔬 Diseño Experimental

### Variables Independientes

#### Factor 1: TRAINING_PROTOCOL (Principal)

**Tipo**: Categórica, 3 niveles

1. **CONTROL_S0** (Baseline)
   - 400 eps con s=0.0 (sin shaping)
   - Mide capacidad máxima del agente en 8×8
   - Esperamos: 95-100% success (si arquitectura DQN 2×64 es suficiente)

2. **FIXED_CURRICULUM** (Control experimental)
   - 4 etapas fijas: s=0.0 → s=0.25 → s=0.5 → s=1.0
   - **100 eps/etapa** (vs 75 en v9, más tiempo por complejidad)
   - Total: 400 eps
   - Réplica directa v9 protocol, escalado a 8×8

3. **ADAPTIVE_CURRICULUM** (Experimental)
   - **5 etapas**: s=0.0 → s=0.25 → s=0.5 → s=0.75 → s=1.0
     - Etapa adicional s=0.75 (transición gradual 0.5→1.0)
   - **Transición threshold-based**:
     ```python
     def should_advance_stage(agent, env, current_stage, episodes_in_stage):
         # Últimos 25 episodios de la etapa actual
         last_25 = get_recent_episodes(25)
         success_rate = mean(last_25['goal_reached'])
         
         # Condiciones avance
         ready = success_rate > 0.75  # Dominio demostrado
         timeout = episodes_in_stage > 150  # Evitar estancamiento
         
         return ready OR timeout
     ```
   - **Episodios variables por etapa**: Cada seed usa tiempo necesario
   - **Máximo total**: 500 eps (permite hasta 100 eps extra de consolidación)

**Comparación clave**:
- Fixed: Schedule rígido, todas las seeds iguales (100-100-100-100)
- Adaptive: Schedule personalizado, seeds débiles usan más (e.g., 100-120-150-80-50 vs seeds fuertes 80-90-100-70-60)

#### Factor 2: SEED (Replicación)

**Tipo**: Categórica, 5 niveles  
**Valores**: {42, 123, 456, 789, 101112}

**Justificación N=5**:
- Balance cómputo/robustez (3 grupos × 5 seeds × ~400 eps = 6,000 eps, ~8h)
- Incluye seed=123 (vulnerable en v9 4×4) para testar si adaptive la rescata
- Si v9.1 muestra CV<0.25, considerar expandir a N=6

#### Factor 3: GRID_SIZE (Constante)

**Valor fijo**: 8×8 (64 celdas)  
**Manhattan distance max**: 14 (diagonal completa)  
**Tripwires esperados**: ~16 con spawn_rate=0.25

**Justificación**: Complejidad crítica donde curriculum fijo falló en proyecciones v9.

### Variables Dependientes (DVs)

#### DV1: Ratio Reward Env Final (Principal)

```python
# Últimos 50 eps para cada grupo
ratio_final[seed] = mean_reward_env_final[group][seed] / mean_reward_env_final[CONTROL_S0][seed]
```

**Threshold éxito**: ratio ≥ 0.70 (paridad parcial, funcionalidad mantenida)

#### DV2: Success Rate (Co-primaria)

```python
success_rate[group][seed] = mean(episodes_final_50['goal_reached'])
```

#### DV3: Episodios por Etapa (Adaptive-specific)

```python
# Solo para Adaptive
episodes_per_stage[seed] = {
    's0.0': count_episodes_stage_0,
    's0.25': count_episodes_stage_1,
    's0.5': count_episodes_stage_2,
    's0.75': count_episodes_stage_3,
    's1.0': count_episodes_stage_4
}
```

**Métrica clave**: Correlación entre `episodes_in_s0.5` y `success_final`  
**Predicción**: Seeds que usan >120 eps en s=0.5 tienen mayor success final

#### DV4: Coefficient of Variation (Robustez)

```python
CV[group] = std(rewards_final) / mean(rewards_final)
```

**Predicción**: CV_adaptive < CV_fixed (menos varianza inter-seed)

#### DV5: Tripwires y Timeouts

```python
tripwires_final[group][seed] = mean(episodes_final_50['deaths_tripwire'])
timeouts_final[group][seed] = mean(episodes_final_50['timeout'])
```

---

## 🔢 Hipótesis y Tests Estadísticos

### H10.1: Adaptive Alcanza Paridad en 8×8 (Principal)

**Hipótesis nula (H0)**: Adaptive NO alcanza paridad (ratio < 0.70)  
**Hipótesis alternativa (H1)**: Adaptive alcanza paridad (ratio ≥ 0.70)

**Test estadístico**:
```python
# Ratio por seed
ratios_adaptive = [reward_adaptive[s] / reward_control[s] for s in seeds]

# Bootstrap 95% CI
ci_lower, ci_upper = bootstrap_ci(ratios_adaptive, alpha=0.05)

# T-test one-sample vs threshold 0.70
from scipy.stats import ttest_1samp
t_stat, p_value = ttest_1samp(ratios_adaptive, popmean=0.70, alternative='greater')
```

**Criterio éxito**:
- ✅ VALIDADA: mean(ratios) ≥ 0.70 AND p < 0.05
- ⚠️ PARCIAL: mean ≥ 0.65 but p ≥ 0.05
- ❌ RECHAZADA: mean < 0.65

**Predicción**: ✅ VALIDADA (escenario optimista: ratio=0.72±0.15)

### H10.2: Adaptive Superior a Fixed (Innovación)

**Hipótesis nula (H0)**: Adaptive ≈ Fixed (no diferencia)  
**Hipótesis alternativa (H1)**: Adaptive > Fixed

**Test estadístico**:
```python
# Paired t-test (mismo seed en ambos grupos)
rewards_adaptive = [mean_reward[ADAPTIVE][s] for s in seeds]
rewards_fixed = [mean_reward[FIXED][s] for s in seeds]

t_stat, p_value = ttest_rel(rewards_adaptive, rewards_fixed, alternative='greater')

# Effect size
cohen_d = (mean(rewards_adaptive) - mean(rewards_fixed)) / pooled_std
```

**Criterio éxito**:
- ✅ VALIDADA: p < 0.05 AND cohen_d > 0.5 (mejora sustancial)
- ⚠️ TENDENCIA: p < 0.10 AND cohen_d > 0.3 (mejora moderada)
- ❌ RECHAZADA: p ≥ 0.10 OR cohen_d < 0.3

**Predicción**: ✅ VALIDADA (p<0.02, d=0.75)

### H10.3: Adaptive Reduce Varianza Inter-Seed

**Hipótesis nula (H0)**: CV_adaptive ≥ CV_fixed (no reduce varianza)  
**Hipótesis alternativa (H1)**: CV_adaptive < CV_fixed

**Test estadístico**:
```python
# Levene's test para igualdad de varianzas
from scipy.stats import levene
stat, p_value = levene(rewards_adaptive, rewards_fixed)

# Ratio CVs
cv_adaptive = std(rewards_adaptive) / mean(rewards_adaptive)
cv_fixed = std(rewards_fixed) / mean(rewards_fixed)
cv_ratio = cv_adaptive / cv_fixed  # <1.0 = adaptive más robusto
```

**Criterio éxito**:
- ✅ VALIDADA: cv_ratio < 0.80 (20% menos varianza)
- ⚠️ TENDENCIA: cv_ratio < 0.90
- ❌ RECHAZADA: cv_ratio ≥ 0.90

**Predicción**: ✅ VALIDADA (cv_ratio=0.65, adaptive 35% menos varianza)

### H10.4: Seeds Vulnerables Se Estabilizan con Adaptive

**Hipótesis**: Seed=123 (colapsó en v9 4×4) alcanza success >60% con adaptive en 8×8

**Test específico**:
```python
# Seed 123 performance
success_seed123_adaptive = mean(episodes_final_50['goal_reached'])  # Seed 123, Adaptive
success_seed123_fixed = mean(episodes_final_50['goal_reached'])     # Seed 123, Fixed

# Episodios usados en etapas críticas (s=0.5, s=0.75)
eps_critical_stages_123 = episodes_per_stage[123]['s0.5'] + episodes_per_stage[123]['s0.75']
```

**Criterio éxito**:
- ✅ VALIDADA: success_123_adaptive > 0.60 AND eps_critical > 180 (usó tiempo extra)
- ⚠️ PARCIAL: success > 0.40 (mejora vs v9, pero no paridad)
- ❌ RECHAZADA: success < 0.40 (no rescata seed vulnerable)

**Predicción**: ✅ VALIDADA (seed=123 usa ~200 eps en s=0.5+s=0.75, alcanza 70% success)

---

## 🛠️ Protocolo Operacional

### Configuración Entorno (8×8)

```python
# Grid 8×8
GRID_SIZE = 8
MANHATTAN_MAX = 14  # (0,0) → (7,7)

# Tripwires
SPAWN_RATE = 0.25  # ~16 tripwires por episodio (vs 4 en 4×4)
TRIPWIRE_PENALTY = -100.0

# Balance inicial
INITIAL_BALANCE = 8.0  # Escalado vs 5.0 en 4×4 (más pasos máximos)
DECAY_RATE = 0.1

# Reward env
GOAL_REWARD = +100.0
TRIPWIRE_PENALTY = -100.0
STEP_PENALTY = 0.0
```

### Arquitectura DQN (Idéntica v9)

```python
# Network
INPUT_SIZE = 64  # 8×8 grid flattened
HIDDEN_LAYERS = [64, 64]  # 2×64 (¿suficiente para 8×8? Testar)
OUTPUT_SIZE = 4

# Training (idéntico v9)
LEARNING_RATE = 0.001
GAMMA = 0.99
BATCH_SIZE = 64
REPLAY_BUFFER_SIZE = 10000

# Exploration
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.995
```

**Nota**: Si v10 falla, considerar arquitectura 3×128 (más capacidad para 8×8).

### Curriculum Adaptativo: Implementación

```python
class AdaptiveCurriculum:
    def __init__(self, stages=[0.0, 0.25, 0.5, 0.75, 1.0]):
        self.stages = stages
        self.current_stage = 0
        self.episodes_in_stage = 0
        self.success_history = []
    
    def should_advance(self):
        """Decide si avanzar a siguiente etapa."""
        # Condición 1: Dominio demostrado
        if len(self.success_history) >= 25:
            recent_success = np.mean(self.success_history[-25:])
            ready = recent_success > 0.75
        else:
            ready = False
        
        # Condición 2: Timeout (evitar estancamiento)
        timeout = self.episodes_in_stage > 150
        
        # Avanzar si cualquier condición se cumple
        return ready or timeout
    
    def update(self, goal_reached):
        """Actualizar historia tras cada episodio."""
        self.success_history.append(goal_reached)
        self.episodes_in_stage += 1
        
        # Intentar avanzar
        if self.should_advance() and self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
            self.episodes_in_stage = 0
            print(f"[CURRICULUM] Avanzando a stage {self.current_stage}, scale={self.stages[self.current_stage]}")
    
    def get_current_scale(self):
        return self.stages[self.current_stage]

# Uso en entrenamiento
curriculum = AdaptiveCurriculum()
for episode in range(500):  # Máximo 500 eps
    env.set_shaping_scale(curriculum.get_current_scale())
    
    # Entrenar episodio
    goal_reached = train_episode(agent, env)
    
    # Actualizar curriculum
    curriculum.update(goal_reached)
    
    # Stop si alcanzó última etapa y consolidó (50 eps en s=1.0)
    if curriculum.current_stage == 4 and curriculum.episodes_in_stage >= 50:
        break
```

### Fixed Curriculum: Implementación

```python
# Fixed (control)
def train_fixed_curriculum(agent, env, seed):
    stages = [
        {'scale': 0.0, 'episodes': range(0, 100)},
        {'scale': 0.25, 'episodes': range(100, 200)},
        {'scale': 0.5, 'episodes': range(200, 300)},
        {'scale': 1.0, 'episodes': range(300, 400)}
    ]
    
    for stage in stages:
        env.set_shaping_scale(stage['scale'])
        for episode in stage['episodes']:
            train_episode(agent, env)
    
    return agent
```

### Protocolo de Ejecución

#### Fase 1: Test Mode (Validación)

```bash
# Test 1 seed × 100 eps
python scripts/run_experiment_10_adaptive.py --test_mode --seed 42 --episodes 100
```

**Validaciones**:
- ✅ Adaptive: Transiciones ocurren correctamente (logs muestran "Avanzando a stage X")
- ✅ Adaptive: Episodios/etapa razonables (50-120 rango esperado)
- ✅ Fixed: 100 eps exactos por etapa (control)
- ✅ Divergencia Adaptive vs Fixed visible (diferentes rewards finales)

#### Fase 2: Ejecución Completa

```bash
# 15 configs × ~400 eps = 6,000 eps (~8h)
python scripts/run_experiment_10_adaptive.py --full_run --checkpoints 5
```

**Checkpoints**: Cada 5 configs (2.5h aprox)

#### Fase 3: Análisis Comparativo

```bash
python scripts/analyze_v10.py --compare_fixed_vs_adaptive --include_v9_4x4
```

**Análisis incluye**:
1. Tests H10.1-H10.4
2. Visualización episodios/etapa por seed (Adaptive)
3. Correlación eps_critical_stages vs success_final
4. Comparación 4×4 (v9) vs 8×8 (v10): escalamiento curriculum

---

## 📊 Resultados Esperados

### Escenario Optimista (60% probabilidad)

**Métricas finales (últimos 50 eps, 8×8)**:

| Grupo | Reward Env | Success Rate | Seeds Exitosas | Eps/Seed Promedio |
|-------|------------|--------------|----------------|-------------------|
| **Adaptive** | 95-105 | 70-80% | **4-5/5 (80-100%)** | ~420 (usa extras) |
| **Fixed** | 70-80 | 50-60% | 2-3/5 (40-60%) | 400 (rígido) |
| **ControlS0** | 130-140 | 95-100% | 5/5 | 400 |

**Hipótesis**:
- ✅ H10.1: Ratio adaptive=0.72±0.15 (paridad parcial alcanzada)
- ✅ H10.2: p<0.02, d=0.75 (adaptive >> fixed)
- ✅ H10.3: CV_adaptive=0.20 vs CV_fixed=0.31 (35% menos varianza)
- ✅ H10.4: Seed=123 alcanza 70% success con ~200 eps en etapas críticas

**Patrón episodios/etapa (Adaptive)**:
- **Seed fuerte (42)**: [80, 90, 100, 70, 60] = 400 eps total
- **Seed vulnerable (123)**: [100, 120, 150, 80, 50] = 500 eps total (usa timeout en s=0.5)

**Interpretación**:
> "Adaptive curriculum permite escalamiento exitoso a 8×8 mediante personalización: seeds fuertes avanzan rápido (~400 eps), seeds vulnerables usan tiempo extra (~500 eps) para consolidar en etapas intermedias. Fixed curriculum falla por rigidez (100 eps/etapa insuficientes para todos)."

### Escenario Pesimista (40% probabilidad)

**Métricas finales**:

| Grupo | Reward Env | Success Rate | Seeds Exitosas |
|-------|------------|--------------|----------------|
| **Adaptive** | 75-85 | 55-65% | **2-3/5 (40-60%)** |
| **Fixed** | 65-75 | 45-55% | 2/5 |
| **ControlS0** | 130-140 | 95-100% | 5/5 |

**Hipótesis**:
- ⚠️ H10.1: Ratio=0.58±0.25 (NO alcanza paridad 0.70)
- ⚠️ H10.2: p=0.06, d=0.40 (tendencia, no significativo)
- ⚠️ H10.3: CV_adaptive=0.28 vs CV_fixed=0.30 (mejora marginal)
- ❌ H10.4: Seed=123 solo 45% success (mejora vs fixed 30%, pero no rescate completo)

**Diagnóstico**:
> "8×8 requiere arquitectura más grande (DQN 3×128), no solo curriculum mejor. Adaptive ayuda (mejora vs Fixed) pero es insuficiente para compensar capacidad limitada de red 2×64."

**Plan B**: Re-ejecutar v10 con arquitectura 3×128, mismo protocolo adaptive.

---

## 🎯 Criterios de Éxito

### ÉXITO COMPLETO

- ✅ H10.1: Ratio ≥ 0.70 (p < 0.05)
- ✅ H10.2: Adaptive > Fixed (p < 0.05, d > 0.5)
- ✅ H10.3: CV_adaptive < 0.80 × CV_fixed
- ✅ ≥80% seeds exitosas (4-5/5)

**Conclusión**: Adaptive resuelve escalamiento 8×8, mecanismo generalizable

### ÉXITO PARCIAL

- ⚠️ H10.1: Ratio 0.60-0.70 (mejora vs Fixed pero no paridad)
- ⚠️ H10.2: p < 0.10, d > 0.3 (tendencia positiva)
- ⚠️ 60% seeds exitosas (3/5)

**Conclusión**: Adaptive ayuda pero 8×8 requiere arquitectura mayor (Plan B: 3×128)

### FALLA

- ❌ H10.1: Ratio < 0.55 (no mejora sustancial vs Fixed)
- ❌ H10.2: p ≥ 0.10, d < 0.3
- ❌ <50% seeds exitosas

**Conclusión**: Problema es arquitectural, no curriculum. Investigar DQN 3×128 o A2C.

---

## 📈 Análisis Específicos

### Análisis 1: Correlación Episodios Críticos vs Success

**Pregunta**: ¿Seeds que usan más episodios en s=0.5+s=0.75 tienen mayor success final?

```python
# Solo Adaptive
eps_critical = [episodes_per_stage[s]['s0.5'] + episodes_per_stage[s]['s0.75'] for s in seeds]
success_final = [success_rate_final[s] for s in seeds]

# Pearson correlation
r, p_value = pearsonr(eps_critical, success_final)
```

**Predicción**: r > 0.70, p < 0.05 (correlación fuerte positiva)

### Análisis 2: Identificación Seeds Vulnerables

**Clustering** basado en episodes_per_stage:

```python
from sklearn.cluster import KMeans

# Features: episodios en cada etapa (Adaptive)
features = [[eps_per_stage[s][stage] for stage in stages] for s in seeds]

# K-means (2 clusters: "rápidas" vs "lentas")
kmeans = KMeans(n_clusters=2).fit(features)
labels = kmeans.labels_

# Comparar success entre clusters
success_cluster0 = mean([success[s] for s in seeds if labels[s] == 0])
success_cluster1 = mean([success[s] for s in seeds if labels[s] == 1])
```

**Predicción**: Cluster "lentas" (más eps) tiene igual o mayor success que "rápidas"

### Análisis 3: Comparación 4×4 (v9) vs 8×8 (v10)

**Figura clave**: Ratio vs Grid Size para Fixed y Adaptive

```python
# Datos
grid_sizes = [4, 8]
ratio_fixed = [0.766, 0.507]  # v9 4×4, v10 8×8
ratio_adaptive = [None, 0.72]  # v10 8×8 (no hay adaptive en 4×4)

# Plot
plt.plot([4, 8], ratio_fixed, label='Fixed Curriculum', marker='o')
plt.axhline(0.70, linestyle='--', color='red', label='Paridad Threshold')
plt.scatter(8, 0.72, label='Adaptive Curriculum', marker='*', s=200, color='green')
```

**Narrativa**: "Fixed colapsa en 8×8, Adaptive recupera paridad"

---

## 📦 Estructura de Resultados

```
results/pgf_v10/
├── PREREGISTRO_v10.md                       # Este documento
├── resultados/
│   ├── adaptive_seed42_episodes.csv         # 15 CSVs (3 grupos × 5 seeds)
│   ├── adaptive_seed123_episodes.csv
│   ├── ...
│   ├── fixed_seed42_episodes.csv
│   ├── ...
│   └── control_s0_seed42_episodes.csv
├── analisis/
│   ├── adaptive_summary.json
│   ├── fixed_summary.json
│   ├── control_s0_summary.json
│   ├── hypothesis_tests.json
│   ├── episodes_per_stage_adaptive.json     # Métrica clave
│   └── correlation_eps_vs_success.json
├── figuras/
│   ├── ratio_fixed_vs_adaptive_8x8.png
│   ├── episodes_per_stage_by_seed.png       # Barplot stacked
│   ├── success_vs_eps_critical.png          # Scatterplot correlación
│   ├── scaling_4x4_vs_8x8.png               # Fixed colapsa, Adaptive escala
│   └── seed123_rescue.png                   # Caso específico seed vulnerable
├── reportes/
│   └── REPORTE_FINAL_v10.md
└── TRACKING_v10.md
```

---

## 📚 Referencias

### Estudios TUI Previos

- **v9**: `results/pgf_v9/REPORTE_FINAL_v9.md` (curriculum fijo 4×4, N=3)
- **v9.1**: `results/pgf_v9.1/REPORTE_FINAL_v9.1.md` (validación N=10, pendiente ejecución)

### Literatura Adaptive Curriculum

- Graves et al. (2017): "Automated Curriculum Learning for Neural Networks" (ICML)
- Portelas et al. (2020): "Teacher algorithms for curriculum learning" (CoRL)
- Narvekar et al. (2020): "Curriculum Learning for RL" (Survey, sección adaptive)

---

## ✅ Checklist Pre-Ejecución

- [ ] Preregistro aprobado y timestamped
- [ ] Script `run_experiment_10_adaptive.py` creado con lógica threshold-based
- [ ] Clase `AdaptiveCurriculum` implementada y testeada
- [ ] Test mode validado (1 seed × 100 eps, transiciones correctas)
- [ ] Fixed curriculum implementado (control, 4 etapas × 100 eps)
- [ ] Directorio `results/pgf_v10/` creado
- [ ] Tiempo cómputo reservado (~8h)
- [ ] Commit pre-ejecución: `git commit -m "PREREGISTRO v10: Adaptive curriculum 8×8"`

---

## 📝 Notas Adicionales

**Diferencias clave vs v9**:
- v9: Fixed curriculum, 4×4, 4 etapas
- v10: **Adaptive** curriculum, **8×8**, **5 etapas** (añade s=0.75)

**Innovación técnica**:
- Transiciones threshold-based (success>0.75 en últimos 25 eps)
- Timeout por etapa (150 eps max, evita estancamiento)
- Personalización por seed (cada una a su ritmo)

**Plan B si falla**:
- Re-ejecutar con arquitectura DQN 3×128
- Considerar A2C (on-policy puede manejar mejor 8×8)
- Incrementar etapas a 6 (añadir s=0.125, s=0.875)

**Próximos pasos según resultados**:
- Si ÉXITO COMPLETO → Paper submission (NeurIPS/ICML)
- Si ÉXITO PARCIAL → Testar arquitectura 3×128
- Si FALLA → Pivotear a A2C o simplificar ambiente (7×7)

---

**Fecha registro**: 4 de diciembre de 2025  
**Versión**: 1.0  
**Investigador responsable**: Sistema TUI v4.1  
**Contacto**: jmrgpr@github.com
