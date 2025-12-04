# 📋 PREREGISTRO EXPERIMENTAL: PGF v10.1 - Adaptive Curriculum 8×8 con Economía Ajustada

**Título**: Reintroducción de Presión Selectiva en Curriculum Adaptativo 8×8: Corrección de Saturación v10  
**Investigador**: Sistema TUI v4.1  
**Fecha registro**: 4 de diciembre de 2025  
**Protocolo**: Preregistración anterior a ejecución  
**Versión experimento**: v10.1 ("Adaptive 8×8 Economía Calibrada")  
**Versión preregistro**: 1.0  
**Predecesor**: v10 (8×8 trivial, balance=8.0 → saturación)

---

## 📖 Resumen Ejecutivo

### Motivación: Por Qué v10.1 es Necesario

**v10 descubrió límite superior curriculum** (hallazgo valioso), pero NO pudo validar escalamiento porque:
- Balance=8.0 → 80 pasos hasta hambre vs Manhattan 14 = **470% margen**
- Resultado: TODAS las estrategias 100% success (~126 reward)
- **No discriminó** entre Adaptive, Fixed y Control

**v10.1 reintroduce presión selectiva** para testear hipótesis originales bajo condiciones que permitan discriminación.

**Pregunta central**: ¿Con balance=5.0 (mismo v9.1, margen 257%), el curriculum adaptativo permite escalamiento exitoso a 8×8?

---

## 🎯 Antecedentes y Diagnóstico v10

### Resultados v10 (8×8, balance=8.0)

**Métricas finales (N=5)**:

| Grupo | Reward Env | Success Rate | Interpretación |
|-------|------------|--------------|----------------|
| **Adaptive** | 125.49 ± 1.36 | 100% | Paridad perfecta |
| **Fixed** | 126.39 ± 0.11 | 100% | Más consistente |
| **Control** | 126.17 ± 0.45 | 100% | Baseline estable |

**Ratio Adaptive/Control**: 0.995 (IC: [0.978, 1.011])

**Hipótesis**: 2/4 validadas (H10.1, H10.4), pero ambas triviales:
- H10.1: Ratio ≥0.70 → SÍ, pero casi 1.0 (no hay costo curriculum)
- H10.4: Seed 123 rescatada → SÍ, pero TODAS 100% (no era vulnerable)

### Diagnóstico Cuantitativo de Trivialidad

**Cálculo margen seguridad v10**:
```
Balance inicial: 8.0
Decay rate: 0.1/step
Steps hasta hambre: 8.0 / 0.1 = 80 steps
Manhattan 8×8: 14 steps (óptimo)
Margen: 80 / 14 = 5.7× = 470%
```

**Consecuencia**: Agente puede:
- Cometer ~5× errores sin morir
- Ignorar recursos (no críticos)
- Rodear tripwires sin presión temporal
- Explorar exhaustivamente sin consecuencia

**Comparación v9.1 (ÉXITO) vs v10 (TRIVIAL)**:

| Parámetro | v9.1 (4×4) | v10 (8×8) | v10.1 (8×8) |
|-----------|------------|-----------|-------------|
| **Balance inicial** | 5.0 | 8.0 | **5.0** |
| **Steps hambre** | 50 | 80 | **50** |
| **Manhattan** | 6 | 14 | 14 |
| **Margen** | 733% | 470% | **257%** |
| **Discriminación** | ✅ Alta | ❌ Nula | ⏳ Esperada |

**Justificación balance=5.0**:
- v9.1 con balance=5.0 en 4×4: 90% seeds éxito, discriminó bien
- Escalado a 8×8: 50/14 = 257% margen (más ajustado que v9.1, pero no trivial)
- Predicción: Control 80-90%, Curriculum 70-80%, Directo <50%

---

## 🔬 Diseño Experimental v10.1

### Cambios Respecto a v10

**ÚNICO CAMBIO INTENCIONAL: Balance inicial**

| Parámetro | v10 (Trivial) | v10.1 (Ajustado) | Justificación |
|-----------|---------------|------------------|---------------|
| **INITIAL_BALANCE** | 8.0 | **5.0** | Reintroducir presión (margen 257% vs 470%) |
| Grid size | 8×8 | 8×8 | Mantener complejidad |
| Spawn rate | 0.25 | 0.25 | Mantener densidad tripwires |
| Decay rate | 0.1 | 0.1 | Mantener dinámica temporal |
| Step cost | 0.0 | 0.0 | Mantener sparse rewards |
| Goal reward | 100.0 | 100.0 | Mantener valor objetivo |
| Resource reward | 1.0 | 1.0 | Mantener valor recursos |
| Tripwire penalty | -100.0 | -100.0 | Mantener costo riesgo |
| Arquitectura | DQN 2×64 | DQN 2×64 | Mantener capacidad |
| N seeds | 5 | **8** | Aumentar potencia (60-70%) |

**Transparencia metodológica**: 
- NO es "arreglo" de v10 (v10 es hallazgo válido de saturación)
- ES nuevo experimento con economía calibrada para permitir discriminación
- Preregistrado ANTES de ejecución (rigor científico)

### Variables Independientes

#### Factor 1: TRAINING_PROTOCOL (Principal)

**Tipo**: Categórica, 3 niveles (idéntico v10)

1. **CONTROL_S0** (Baseline)
   - 400 eps con s=0.0 (sin shaping)
   - Mide capacidad máxima en economía ajustada
   - **Predicción v10.1**: 80-90% success (vs 100% en v10)

2. **FIXED_CURRICULUM**
   - 5 etapas fijas: s=0.0 → 0.25 → 0.5 → 0.75 → 1.0
   - 100 eps/etapa (500 total)
   - **Predicción v10.1**: 60-70% success (vs 100% en v10)

3. **ADAPTIVE_CURRICULUM** (Experimental)
   - 5 etapas threshold-based (mismo v10)
   - Transición: success_rate_last_25 > 0.60
   - Timeout: 150 eps/etapa
   - **Predicción v10.1**: 70-80% success, episodios variables por seed

#### Factor 2: SEED (Replicación - AMPLIADO)

**Tipo**: Categórica, 8 niveles (vs 5 en v10)

**Valores**: {42, 123, 456, 789, 101112, 131415, 161718, 192021}

**Justificación N=8**:
- v10 N=5 → potencia <50% (insuficiente)
- v10.1 N=8 → potencia ~60-70% (suficiente para publicación)
- Mantener {42, 123, 456, 789, 101112} para continuidad
- Agregar {131415, 161718, 192021} para robustez

**Selección nuevas seeds**:
- Distribuidas uniformemente [130000-200000]
- Evitar patrones (no múltiplos redondos)
- Primos o semiprimos preferidos

### Variables Dependientes (DVs)

#### DV1: Ratio Reward Env Final (Principal)

```python
# Últimos 50 eps (250-300 para Fixed/Control, últimos 50 para Adaptive)
ratio_final[seed] = mean_reward_env_final[ADAPTIVE][seed] / mean_reward_env_final[CONTROL_S0][seed]
```

**Interpretación**:
- `≥ 0.90`: Paridad completa (éxito total)
- `0.70-0.90`: Paridad parcial (aceptable, funcional)
- `< 0.70`: Falla curriculum (threshold crítico)

**Diferencia v10 vs v10.1**:
- v10: ratio=0.995 (casi idéntico, sin discriminación)
- v10.1 esperado: ratio=0.75-0.85 (costo visible, pero funcional)

#### DV2: Reward Env Absoluto

```python
reward_env_final[group][seed] = mean(episodes[últimos_50]['reward_env'])
```

**Predicción v10.1**:
- Control: 80-95 (vs 126 en v10)
- Adaptive: 65-80 (vs 125 en v10)
- Fixed: 55-70 (vs 126 en v10)

#### DV3: Success Rate

```python
success_rate[group][seed] = mean(episodes[últimos_50]['goal_reached'])
```

**Predicción v10.1**:
- Control: 80-90% (vs 100% en v10)
- Adaptive: 70-80% (vs 100% en v10)
- Fixed: 60-70% (vs 100% en v10)

#### DV4: Tripwires per Episode

```python
tripwires_final[group][seed] = mean(episodes[últimos_50]['deaths_tripwire'])
```

**Predicción**: Adaptive ≤ Control (prudencia mantenida)

#### DV5: Episodes per Stage (Adaptive)

```python
episodes_stage[seed] = {stage_0: X, stage_1: Y, ..., stage_4: Z}
```

**Predicción v10.1**:
- Stage 0 (s=0.0): 80-120 eps (vs 25-31 en v10)
- Stage 1-3: 30-50 eps cada una (vs 1 en v10)
- Stage 4: 50-80 eps (mínimo consolidación)
- **Total: 300-450 eps** (vs 78-84 en v10)

---

## 🔢 Hipótesis y Tests Estadísticos

### H10.1.1: Adaptive Mantiene Paridad Parcial ≥0.70

**Hipótesis nula (H0)**: Adaptive NO alcanza threshold funcional (ratio < 0.70)  
**Hipótesis alternativa (H1)**: Adaptive mantiene ratio ≥ 0.70 con IC que NO cruza

**Test estadístico**:
```python
# Ratio por seed
ratios = [reward_adaptive[s] / reward_control[s] for s in seeds]

# Bootstrap 95% CI (10,000 iteraciones)
ci_lower, ci_upper = bootstrap_ci(ratios, alpha=0.05)

# Criterio validación
H10_1_1_validated = (mean(ratios) >= 0.70) AND (ci_lower >= 0.65)
```

**Criterio éxito**:
- ✅ VALIDADA: mean ≥ 0.70 AND ci_lower ≥ 0.65 (margen error aceptado)
- ⚠️ MARGINAL: mean ≥ 0.70 BUT ci_lower < 0.65 (insuficiente robustez)
- ❌ RECHAZADA: mean < 0.70

**Diferencia v10**:
- v10: ratio=0.995 (trivial, casi paridad perfecta)
- v10.1 esperado: ratio=0.75-0.85 (costo curriculum visible pero funcional)

**Predicción**: ✅ VALIDADA (ratio=0.78 ± 0.12, CI: [0.70, 0.86])

### H10.2.1: Adaptive Supera Fixed en Economía Ajustada

**Hipótesis nula (H0)**: Adaptive ≤ Fixed (no mejora vs schedule fijo)  
**Hipótesis alternativa (H1)**: Adaptive > Fixed (personalización ayuda)

**Test estadístico**:
```python
from scipy.stats import ttest_rel

# Rewards finales por seed
rewards_adaptive = [mean_reward[ADAPTIVE][s] for s in seeds]
rewards_fixed = [mean_reward[FIXED][s] for s in seeds]

# Paired t-test (one-tailed)
t_stat, p_value = ttest_rel(rewards_adaptive, rewards_fixed, alternative='greater')

# Effect size
cohen_d = (mean(rewards_adaptive) - mean(rewards_fixed)) / pooled_std
```

**Criterio éxito**:
- ✅ VALIDADA: p < 0.05 AND cohen_d > 0.3 (efecto pequeño-medio)
- ⚠️ MARGINAL: p = 0.05-0.10 (borderline significancia)
- ❌ RECHAZADA: p > 0.10 OR cohen_d < 0.2

**Diferencia v10**:
- v10: Adaptive < Fixed (Δ=-0.90, p=0.89) → Fixed ganó porque entorno trivial
- v10.1 esperado: Adaptive > Fixed (Δ=+8-12, p<0.05) → Adaptive gana con presión

**Predicción**: ✅ VALIDADA (Δ=+10.5, d=0.55, p=0.02)

**Mecanismo esperado**: 
- Fixed usa 500 eps fijos → desperdicia tiempo en etapas fáciles, insuficiente en difíciles
- Adaptive personaliza → más tiempo en s=0.5/0.75 (críticas), menos en s=0.0 (fácil)

### H10.3.1: Adaptive Reduce Varianza Inter-Seed

**Hipótesis nula (H0)**: Adaptive NO reduce varianza vs Fixed  
**Hipótesis alternativa (H1)**: CV(Adaptive) < CV(Fixed)

**Test estadístico**:
```python
from scipy.stats import levene

# CVs
cv_adaptive = std(rewards_adaptive) / mean(rewards_adaptive)
cv_fixed = std(rewards_fixed) / mean(rewards_fixed)
cv_ratio = cv_adaptive / cv_fixed

# Levene's test (equality of variances)
stat, p = levene(rewards_adaptive, rewards_fixed)
```

**Criterio éxito**:
- ✅ VALIDADA: cv_ratio < 0.80 AND p < 0.10 (reduce varianza significativamente)
- ⚠️ PARCIAL: cv_ratio < 1.0 BUT p > 0.10 (tendencia correcta, no significativa)
- ❌ RECHAZADA: cv_ratio ≥ 1.0 (no reduce o aumenta)

**Diferencia v10**:
- v10: cv_ratio=12.6 (Adaptive AUMENTÓ varianza porque episodios variables sin beneficio)
- v10.1 esperado: cv_ratio=0.65-0.75 (personalización reduce varianza entre seeds débiles/fuertes)

**Predicción**: ✅ VALIDADA (cv_ratio=0.70, p=0.08)

**Mecanismo**: Seeds vulnerables usan más episodios en etapas críticas → reducen gap con seeds fuertes

### H10.4.1: Seeds Vulnerables Mantienen ≥60% Success

**Hipótesis**: Seeds identificadas como vulnerables en v9.1 (e.g., 123) mantienen ≥60% success con Adaptive en 8×8

**Test**:
```python
# Identificar seeds vulnerables (percentil inferior 25% en success_rate)
vulnerable_seeds = bottom_25_percent(success_rates_adaptive)

# Success rate promedio de vulnerables
success_vulnerable = mean([success_rate[s] for s in vulnerable_seeds])

# Criterio
H10_4_1_validated = success_vulnerable >= 0.60
```

**Criterio éxito**:
- ✅ VALIDADA: ≥60% success en seeds vulnerables (rescate efectivo)
- ⚠️ PARCIAL: 50-60% (mejora vs Fixed, pero insuficiente)
- ❌ RECHAZADA: <50% (colapso aún con adaptive)

**Diferencia v10**:
- v10: Seed 123 tuvo 100% (pero TODAS 100%, no discrimina)
- v10.1 esperado: Seed 123 ~65-70% (rescatada vs Fixed ~50%, pero NO 100%)

**Predicción**: ✅ VALIDADA (seeds vulnerables 62-68% vs Fixed 48-55%)

---

## 📊 Análisis de Potencia Estadística

### Potencia Esperada N=8

**Parámetros v10 observados** (aunque trivial, sirven como referencia):
- Effect size v10: d = 0.67 (Adaptive vs Fixed, dirección opuesta)
- Effect size v9.1: d = 0.70 (Curriculum vs Directo en 4×4)
- **Asumimos**: v10.1 con economía ajustada d ≈ 0.55 (efecto medio)

**Cálculo potencia**:
```python
from statsmodels.stats.power import ttest_power

power = ttest_power(effect_size=0.55, nobs=8, alpha=0.05, alternative='larger')
# power ≈ 0.63 (63%)
```

**Interpretación**:
- N=8 → potencia ~60-65% (suficiente para detectar efecto medio d>0.5)
- Mejor que v10 N=5 (~45%) y v9 N=3 (~18%)
- Inferior a v9.1 N=10 (~70%), pero balance cómputo/robustez aceptable

**Justificación N=8 (no N=10)**:
- 24 configs × ~400 eps = 9,600 eps (~10-12h cómputo)
- vs N=10 → 30 configs (~15h, menos factible single-run)
- 60-65% potencia suficiente para paper workshop/ArXiv

---

## 🛠️ Protocolo Operacional

### Configuración Entorno (CAMBIO CRÍTICO)

```python
# Grid 8×8 (idéntico v10)
GRID_SIZE = 8
MANHATTAN_MAX = 14  # (0,0) → (7,7)

# Balance (AJUSTADO vs v10)
INITIAL_BALANCE = 5.0  # CAMBIO: 8.0 → 5.0
DECAY_RATE = 0.1  # Por step (mantener)
STEPS_UNTIL_STARVATION = 50  # Reducido de 80

# Rewards (mantener v10)
GOAL_REWARD = 100.0
RESOURCE_REWARD = 1.0
TRIPWIRE_PENALTY = -100.0
STEP_PENALTY = 0.0  # Sparse rewards

# Tripwires (mantener v10)
SPAWN_RATE = 0.25  # ~16 tripwires esperados

# Margen seguridad (NUEVO CÁLCULO)
MARGIN = 50 / 14 = 3.57× = 257%
```

**Predicción consecuencias**:
- Balance 5.0 → agente debe recoger ~2-3 recursos para sobrevivir
- Recursos ya NO son opcionales (críticos)
- Tripwires más costosos (menos margen error)
- Control esperado 80-90% success (vs 100% en v10)

### Arquitectura DQN (Mantener v10)

```python
# Network (idéntico)
INPUT_SIZE = 64  # 8×8 grid flattened
HIDDEN_LAYERS = [64, 64]  # 2 capas
OUTPUT_SIZE = 4  # {UP, DOWN, LEFT, RIGHT}
ACTIVATION = 'relu'

# Training (idéntico)
LEARNING_RATE = 0.001
GAMMA = 0.99
BATCH_SIZE = 64
REPLAY_BUFFER_SIZE = 10000

# Exploration (idéntico)
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.995
```

### Curriculum Adaptive (Mantener v10)

```python
# Escalas (idéntico)
STAGES = [0.0, 0.25, 0.5, 0.75, 1.0]  # 5 etapas

# Transición threshold-based (idéntico)
THRESHOLD_SUCCESS = 0.60
WINDOW_SIZE = 25  # Últimos 25 eps
TIMEOUT_STAGE = 150  # Max eps/etapa
MIN_EPS_FINAL_STAGE = 50  # Consolidación final
```

### Protocolo de Ejecución

#### Fase 1: Test Mode (Validación Pre-Ejecución)

```bash
# Test 2 seeds × 100 eps
python scripts/run_experiment_10.1_balanced.py --test_mode --seeds 42,789 --max_episodes 100
```

**Criterios validación**:
- ✅ Adaptive transitions ocurren (no todo timeout)
- ✅ Success rate Control <100% (discrimina vs v10)
- ✅ Resources recolectados (agora críticos)
- ✅ Episodios/etapa Stage 0: 30-50 (vs 25-31 en v10 trivial)
- ✅ CSV correctos, no errores

#### Fase 2: Ejecución Completa

```bash
# 24 configs × ~400 eps = 9,600 eps (~10-12h)
python scripts/run_experiment_10.1_balanced.py --full_run --checkpoints 6
```

**Total configuraciones**: 3 grupos × 8 seeds = **24 configs**  
**Checkpoints**: Cada 6 configs (~2h), validar parciales

**Seeds**: {42, 123, 456, 789, 101112, 131415, 161718, 192021}

#### Fase 3: Análisis Estadístico

```bash
python scripts/analyze_v10.1.py --compare_with_v10
```

**Análisis incluye**:
1. Tests hipótesis H10.1.1 - H10.4.1
2. Episodes per stage (Adaptive) - correlación con success
3. Comparación Fixed vs Adaptive (ratios, CVs, effect sizes)
4. Comparación v10 vs v10.1 (efecto balance en discriminación)
5. Clustering seeds (rápidas/lentas)

---

## 📈 Resultados Esperados

### Escenario Optimista (70% probabilidad)

**Métricas finales (últimos 50 eps, N=8)**:

| Grupo | Reward Env | Success Rate | Seeds ≥70% | Interpretación |
|-------|------------|--------------|------------|----------------|
| **Adaptive** | 73 ± 12 | 76 ± 15% | 6-7/8 (75-87%) | Paridad parcial funcional |
| **Fixed** | 63 ± 15 | 65 ± 18% | 4-5/8 (50-62%) | Funcional limitado |
| **Control** | 94 ± 8 | 88 ± 10% | 7-8/8 (87-100%) | Baseline robusto |

**Hipótesis**:
- ✅ H10.1.1: Ratio 0.78 (CI: [0.70, 0.86]) → NO cruza 0.70
- ✅ H10.2.1: Adaptive > Fixed (Δ=+10, d=0.55, p=0.02)
- ✅ H10.3.1: CV ratio 0.70 (Adaptive más consistente)
- ✅ H10.4.1: Seeds vulnerables 65% (≥60% threshold)

**Episodes per stage (Adaptive)**:

| Seed Tipo | Stage 0 | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Total |
|-----------|---------|---------|---------|---------|---------|-------|
| **Fuerte** (e.g., 456) | 85 | 40 | 50 | 45 | 60 | 280 |
| **Media** (e.g., 42) | 100 | 55 | 70 | 60 | 65 | 350 |
| **Vulnerable** (e.g., 123) | 120 | 80 | 110 | 90 | 70 | 470 |

**Interpretación escenario optimista**:
> "Adaptive curriculum escala exitosamente a 8×8 cuando hay presión real (balance=5.0). Personalización por seed permite a vulnerables usar más tiempo en etapas críticas, cerrando gap con seeds fuertes. Fixed colapsa por schedule rígido (insuficiente consolidación). Control establece baseline ~88% (entorno difícil pero no imposible)."

### Escenario Pesimista (30% probabilidad)

**Métricas finales**:

| Grupo | Reward Env | Success Rate | Seeds ≥70% | Interpretación |
|-------|------------|--------------|------------|----------------|
| **Adaptive** | 65 ± 18 | 68 ± 20% | 4-5/8 (50-62%) | Alta varianza persiste |
| **Fixed** | 58 ± 20 | 60 ± 22% | 3-4/8 (37-50%) | Colapso parcial |
| **Control** | 85 ± 12 | 82 ± 14% | 6-7/8 (75-87%) | Baseline difícil |

**Hipótesis**:
- ⚠️ H10.1.1: Ratio 0.76 (CI: [0.62, 0.90]) → CRUZA 0.70 (marginal)
- ⚠️ H10.2.1: Adaptive > Fixed (Δ=+7, d=0.35, p=0.08) → borderline
- ❌ H10.3.1: CV ratio 0.95 (varianza NO reduce significativamente)
- ⚠️ H10.4.1: Seeds vulnerables 58% (<60% threshold)

**Interpretación escenario pesimista**:
> "Balance=5.0 en 8×8 es límite capacidad DQN 2×64. Curriculum ayuda (tendencia positiva), pero arquitectura insuficiente para consolidar política robusta. Requiere red mayor (3×128) o simplificar (7×7 intermedio)."

---

## 🎯 Criterios de Éxito

### ÉXITO COMPLETO

- ✅ H10.2.1 significativa (p < 0.05, d > 0.3)
- ✅ H10.1.1: Ratio ≥0.70, IC NO cruza 0.65
- ✅ ≥60% seeds Adaptive con success ≥70%
- ✅ Reduce CV: ratio < 0.80

**Conclusión**: Curriculum adaptativo escala exitosamente a 8×8. Publicable NeurIPS/ICML.

### ÉXITO PARCIAL

- ⚠️ H10.2.1: p = 0.05-0.10 (borderline)
- ⚠️ H10.1.1: Ratio ≥0.70 pero CI cruza levemente
- ⚠️ 50-60% seeds exitosas
- ⚠️ CV reduce parcialmente (ratio 0.80-0.95)

**Conclusión**: Curriculum ayuda pero arquitectura límite. Considerar DQN mayor o grid intermedio.

### FALLA

- ❌ H10.2.1: p > 0.10 (no significativo)
- ❌ H10.1.1: Ratio < 0.65
- ❌ <50% seeds exitosas
- ❌ CV NO reduce (ratio ≥1.0)

**Conclusión**: 8×8 excede capacidad DQN 2×64 incluso con adaptive. Requiere arquitectura mayor o grid menor.

---

## 📦 Estructura de Resultados

```
results/pgf_v10.1/
├── PREREGISTRO_v10.1.md                   # Este documento
├── resultados/
│   ├── adaptive_seed42_episodes.csv       # 24 CSVs (3 grupos × 8 seeds)
│   ├── adaptive_seed123_episodes.csv
│   ├── ...
│   ├── fixed_seed42_episodes.csv
│   ├── ...
│   └── control_seed42_episodes.csv
├── analisis/
│   ├── hypothesis_tests_v10.1.json        # Tests H10.1.1-H10.4.1
│   ├── episodes_per_stage_adaptive.json   # Personalización por seed
│   ├── comparison_v10_vs_v10.1.json       # Efecto balance en discriminación
│   ├── seed_clustering.json               # Rápidas/lentas
│   └── final_metrics_v10.1.csv            # 24 rows agregadas
├── figuras/
│   ├── ratio_v10_vs_v10.1.png            # Trivial vs Ajustado
│   ├── success_by_group_v10.1.png        # Boxplots discriminación
│   ├── episodes_per_stage_heatmap.png    # Personalización Adaptive
│   ├── cv_comparison.png                 # Varianza Fixed vs Adaptive
│   └── seed_vulnerability_v10.1.png      # Rescate seeds débiles
├── reportes/
│   └── REPORTE_FINAL_v10.1.md            # Reporte post-ejecución
└── TRACKING_v10.1.md                     # Log ejecución
```

---

## 🔬 Validaciones Metodológicas

### Transparencia vs v10

**NO estamos "arreglando" v10**:
- v10 es hallazgo válido (límite superior curriculum)
- v10.1 es NUEVO experimento con economía calibrada
- Preregistrado ANTES de ejecución (rigor científico)
- Justificación explícita: balance=8.0 → saturación → ajuste a balance=5.0

**Diferencia conceptual**:
- v10: "¿Adaptive escala a 8×8?" → Respuesta: "No discrimina cuando trivial"
- v10.1: "¿Adaptive escala a 8×8 con presión?" → Respuesta: ⏳ A determinar

### Comparabilidad Resultados

**v10 vs v10.1 son comparables porque**:
- Mismo grid (8×8), arquitectura (DQN 2×64), spawn_rate (0.25)
- Mismo curriculum (adaptive threshold-based, fixed schedule)
- ÚNICO cambio: balance 8.0→5.0 (intencional, cuantificado)

**v9.1 vs v10.1 son comparables porque**:
- Mismo balance (5.0), arquitectura, spawn_rate
- Diferencia SOLO en grid size (4×4 vs 8×8)
- Permite evaluar escalamiento "puro"

---

## 🚨 Riesgos y Mitigaciones

### Riesgo 1: Balance=5.0 Aún Trivial en 8×8

**Probabilidad**: Baja (15%)  
**Impacto**: Alto (no discrimina de nuevo)

**Diagnóstico**:
- Margen 257% menor que v10 (470%), pero mayor que v9.1 (733%)
- Grid grande → tripwires dispersos (densidad efectiva baja)

**Mitigación**:
- Test mode validará: si Control >95% success → abortar, ajustar balance a 4.0
- Criterio gate: Control test ≤90% success para proceder

### Riesgo 2: Balance=5.0 Demasiado Duro

**Probabilidad**: Media (25%)  
**Impacto**: Medio (todas colapsan, no discrimina por abajo)

**Diagnóstico**:
- Margen 257% puede ser insuficiente si tripwires bloquean caminos óptimos
- Manhattan 14 asume camino libre (probabilidad <100% en spawn=0.25)

**Mitigación**:
- Test mode validará: si Control <60% success → considerar balance 5.5 o 6.0
- Criterio gate: Control test ≥70% success para proceder

### Riesgo 3: Arquitectura Insuficiente

**Probabilidad**: Media (30%)  
**Impacto**: Alto (curriculum no ayuda por límite capacidad)

**Diagnóstico**:
- DQN 2×64 puede ser límite para 8×8 (64 estados)
- v9.1 4×4 funcionó, pero escalamiento NO lineal

**Mitigación**:
- Si v10.1 falla Y Control >80% → problema es curriculum/arquitectura, no economía
- Plan B: v10.2 con DQN 3×128 (incrementar capacidad)

---

## 📚 Referencias

### Experimentos Predecesores

- **v9.1**: `results/pgf_v9.1/reportes/REPORTE_FINAL_v9.1.md` (4×4, balance=5.0, N=10, victoria principal)
- **v10**: `results/pgf_v10/reportes/REPORTE_FINAL_v10.md` (8×8, balance=8.0, N=5, trivial)

### Documentación TUI

- **Teoría Unificada**: `docs/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md`
- **Mapeo Experimentos**: `docs/MAPEO_EXPERIMENTOS_TUI.md`

### Literatura Curriculum Learning

- Bengio et al. (2009): "Curriculum Learning" (ICML)
- Narvekar et al. (2020): "Curriculum Learning for RL" (Survey)

---

## ✅ Checklist Pre-Ejecución

- [ ] Preregistro v10.1 aprobado y timestamped
- [ ] Script `run_experiment_10.1_balanced.py` creado
- [ ] Test mode ejecutado: Control 70-90% success (gate validado)
- [ ] Directorio `results/pgf_v10.1/` creado
- [ ] Backup configurado (checkpoints cada ~2h)
- [ ] Tiempo cómputo reservado (~10-12h)
- [ ] Commit pre-ejecución: `git commit -m "PREREGISTRO v10.1: 8×8 economía ajustada (balance=5.0)"`

---

## 📝 Declaración de Integridad Científica

**Este preregistro se congela ANTES de ejecutar v10.1**.

**Cambios permitidos post-registro**:
- ❌ Hipótesis, tests estadísticos, criterios éxito
- ❌ Balance inicial, economía, parámetros críticos
- ✅ Bugs técnicos (si errores ejecución)
- ✅ Análisis exploratorios adicionales (marcados como post-hoc)

**Si se detectan problemas durante test mode**:
- OPCIÓN 1: Abortar v10.1, crear v10.2 con preregistro ajustado
- OPCIÓN 2: Documentar en TRACKING como desviación justificada

**Compromiso transparencia**:
> "v10.1 es respuesta científica rigurosa al hallazgo v10 (saturación). Ajustamos balance=8.0→5.0 ANTES de ejecución, con justificación cuantitativa (margen 470%→257%). Hipótesis preregistradas, criterios éxito claros, sin p-hacking."

---

**Fecha registro**: 4 de diciembre de 2025, 22:30  
**Versión**: 1.0 (CONGELADO)  
**Investigador responsable**: Sistema TUI v4.1  
**Contacto**: jmrgpr@github.com  
**Para**: Mis hijos - que vean cómo se hace ciencia con rigor, incluso cuando ajustamos experimentos

---

**FIN PREREGISTRO v10.1** 🔒
