# 📋 PREREGISTRO EXPERIMENTAL: PGF v9.1 - Validación Estadística Robusta (N=10)

**Título**: Validación Estadística del Curriculum Learning para Mitigación de Over-Alignment: Estudio con N=10 Seeds  
**Investigador**: Sistema TUI v4.1  
**Fecha registro**: 4 de diciembre de 2025  
**Protocolo**: Preregistración anterior a ejecución  
**Versión experimento**: v9.1 ("Validación Robusta v9")  
**Versión preregistro**: 1.0  
**Predecesor**: v9 (N=3, evidencia preliminar)

---

## 📖 Resumen Ejecutivo

Este experimento replica **exactamente** el protocolo v9 con **N=10 seeds** (vs N=3 original) para alcanzar potencia estadística adecuada (60-80% vs 18% en v9) y validar los hallazgos preliminares de efectividad del curriculum learning.

**Motivación crítica**: El peer review de v9 identificó:
- ⚠️ **N=3 insuficiente**: Potencia estadística 18% para detectar d=0.66
- ⚠️ **H9.1/H9.2 no significativas**: IC cruzaba thresholds, p>0.05
- ⚠️ **Alta varianza inter-seed**: CV=0.532, seed=123 colapsó

**Pregunta central**: ¿Con N=10, los efectos observados en v9 (ratio=0.766, d=0.661) alcanzan significancia estadística y confirman la efectividad del curriculum?

**Hallazgos v9 (N=3 preliminares)**:
- Ratio Curriculum: 0.766 ± 0.404 (2/3 seeds exitosas)
- H9.1: NO significativa (IC [-0.236, 1.769] cruza threshold 0.70)
- H9.2: p=0.17, d=0.661 (efecto medio presente, insuficientemente powered)
- Patrón bimodal: 67% éxito, 33% colapso (seed=123)

---

## 🎯 Antecedentes y Motivación

### Resultados v9 (Evidencia Preliminar)

**Grid 4×4, N=3 seeds:**

| Grupo | Reward Env | Success Rate | Tripwires | Interpretación |
|-------|------------|--------------|-----------|----------------|
| **Curriculum** | 88.78 ± 47.24 | 70.0% ± 52.0% | 0.57 ± 0.69 | Bimodal: 2/3 éxito |
| **DirectoS1** | 55.67 ± 52.81 | 33.3% ± 57.7% | 0.07 ± 0.08 | Bimodal: 1/3 éxito anómalo |
| **ControlS0** | 115.39 ± 1.24 | 99.3% ± 1.2% | 1.37 ± 1.05 | Estable 100% |

**Detalle Curriculum por seed:**
- Seed 42: 115.93, 100% success → ✅ PARIDAD
- Seed 123: 34.23, 10% success → ❌ COLAPSO
- Seed 456: 116.17, 100% success → ✅ PARIDAD

**Análisis estadístico v9:**
- H9.1: Ratio 0.766 > threshold 0.70, PERO IC [-0.236, 1.769] cruza → rechazo formal
- H9.2: t-test p=0.17 > 0.05, Cohen's d=0.661 (efecto medio)
- Potencia post-hoc: ~18% (requiere N≥23 para 80%)

**Conclusión v9**: Evidencia sugestiva de efectividad, pero estadísticamente no concluyente.

### Gap que v9.1 Resuelve

**v9 demostró QUÉ ocurre** (curriculum ayuda en 67% casos), **v9.1 valida SI es robusto** con muestra adecuada.

**Predicciones pre-ejecución:**

1. **Escenario optimista (70% probabilidad)**:
   - Ratio Curriculum: 0.75 ± 0.20 (IC: [0.62, 0.88])
   - H9.2.1: p < 0.01, potencia ~70%
   - Seeds exitosas: 7-8/10 (70-80%)
   - Patrón: 2-3 seeds tipo-123 colapsan, resto mantiene paridad

2. **Escenario pesimista (30% probabilidad)**:
   - Ratio: 0.65 ± 0.30 (varianza NO reduce)
   - H9.2.1: p = 0.03-0.06 (borderline)
   - Seeds exitosas: 5-6/10 (50-60%)
   - Conclusión: Curriculum frágil, alta dependencia seed

---

## 🔬 Diseño Experimental

### Diferencias vs v9 (ÚNICO CAMBIO: N)

| Parámetro | v9 (Original) | v9.1 (Este Estudio) | Justificación |
|-----------|---------------|---------------------|---------------|
| **N Seeds** | 3 | **10** | Alcanzar potencia 60-80% |
| **Seeds** | {42, 123, 456} | **{42, 123, 456, 789, 101112, 131415, 161718, 192021, 222324, 252627}** | 7 nuevas seeds |
| **Grid Size** | 4×4 | 4×4 | Mantener continuidad |
| **Curriculum** | [0.0→0.25→0.5→1.0] | [0.0→0.25→0.5→1.0] | Idéntico |
| **Episodios** | 300 (75/etapa) | 300 (75/etapa) | Idéntico |
| **Arquitectura** | DQN 2×64 | DQN 2×64 | Idéntico |
| **Tripwires** | spawn_rate=0.25 | spawn_rate=0.25 | Idéntico |

**Total configuraciones**: 3 grupos × 10 seeds = **30 configs**  
**Total episodios**: 30 × 300 = **9,000 episodios**  
**Tiempo estimado**: ~6 horas cómputo

### Variables Independientes

#### Factor 1: TRAINING_PROTOCOL (Principal)

**Tipo**: Categórica, 3 niveles (idéntico v9)

1. **CURRICULUM**
   - 4 etapas × 75 eps: s=0.0 → s=0.25 → s=0.5 → s=1.0
   - Transfer learning: pesos Q-network se transfieren
   - Epsilon continuo decreciente

2. **DIRECTO_S1**
   - 300 eps con s=1.0 constante (control positivo)

3. **CONTROL_S0**
   - 300 eps con s=0.0 (control negativo, baseline capacidad)

#### Factor 2: SEED (Replicación - AMPLIADO)

**Tipo**: Categórica, 10 niveles  
**Valores**: {42, 123, 456, 789, 101112, 131415, 161718, 192021, 222324, 252627}

**Selección de seeds nuevas**:
- Mantener {42, 123, 456} para continuidad con v9
- Agregar 7 seeds distribuidas uniformemente en espacio [100, 300000]
- Evitar patrones (no múltiplos de 10, no secuenciales simples)

### Variables Dependientes (DVs)

#### DV1: Ratio Reward Env Final (Principal)

```python
# Últimos 50 eps (250-300) para cada grupo
ratio_final[seed] = mean_reward_env_final[CURRICULUM][seed] / mean_reward_env_final[CONTROL_S0][seed]
```

**Interpretación**:
- `≥ 0.90`: Paridad completa (éxito total)
- `0.70-0.90`: Paridad parcial (mejor que directo, funcional)
- `< 0.70`: Falla curriculum (threshold v9)

#### DV2: Reward Env Absoluto

```python
reward_env_final[group][seed] = mean(episodes[250:300]['reward_env'])
```

#### DV3: Success Rate

```python
success_rate[group][seed] = mean(episodes[250:300]['goal_reached'])
```

#### DV4: Tripwires per Episode

```python
tripwires_final[group][seed] = mean(episodes[250:300]['deaths_tripwire'])
```

#### DV5: Timeouts per Episode

```python
timeouts_final[group][seed] = mean(episodes[250:300]['timeout'])
```

---

## 🔢 Hipótesis y Tests Estadísticos

### H9.1.1: Curriculum Superior a Directo (ACTUALIZADA)

**Hipótesis nula (H0)**: Curriculum NO mejora vs Directo (ratio ≤ threshold)  
**Hipótesis alternativa (H1)**: Curriculum mejora (ratio > 0.70 con IC que NO cruza)

**Test estadístico**:
```python
# Ratio por seed
ratios = [reward_curriculum[s] / reward_directo[s] for s in seeds]

# Bootstrap 95% CI (10,000 iteraciones)
ci_lower, ci_upper = bootstrap_ci(ratios, alpha=0.05)

# Criterio validación
H9_1_1_validated = (mean(ratios) > 0.70) AND (ci_lower > 0.70)
```

**Criterio éxito**:
- ✅ VALIDADA: mean > 0.70 AND ci_lower > 0.70 (IC NO cruza threshold)
- ⚠️ MARGINAL: mean > 0.70 BUT ci_lower ≤ 0.70 (mismo resultado v9)
- ❌ RECHAZADA: mean ≤ 0.70

**Predicción**: ✅ VALIDADA (escenario optimista: ratio=0.75, IC=[0.62, 0.88])

### H9.2.1: Curriculum Alcanza Paridad con Control (ACTUALIZADA)

**Hipótesis nula (H0)**: Curriculum < Control (diferencia significativa)  
**Hipótesis alternativa (H1)**: Curriculum ≈ Control (no diferencia significativa, O superior)

**Test estadístico**:
```python
from scipy.stats import ttest_rel  # Paired t-test (mismo seed en ambos grupos)

# Rewards finales por seed
rewards_curriculum = [mean_reward[CURRICULUM][s] for s in seeds]
rewards_control = [mean_reward[CONTROL_S0][s] for s in seeds]

# Paired t-test (two-tailed)
t_stat, p_value = ttest_rel(rewards_curriculum, rewards_control)

# Effect size
cohen_d = (mean(rewards_curriculum) - mean(rewards_control)) / pooled_std
```

**Criterio éxito**:
- ✅ VALIDADA: p < 0.05 AND cohen_d > 0.5 (diferencia significativa con efecto medio-grande)
- ⚠️ INSUF. POWERED: p ≥ 0.05 BUT cohen_d > 0.3 (efecto presente, aún underpowered)
- ❌ RECHAZADA: p ≥ 0.05 AND cohen_d < 0.3 (no hay efecto real)

**Predicción**: ✅ VALIDADA (escenario optimista: p<0.01, d~0.70)

### H9.3.1: Curriculum Mantiene Prudencia (Replicación)

**Hipótesis**: Tripwires finales: Curriculum ≤ Control (prudencia mantenida)

**Test estadístico**:
```python
tripwires_curriculum = [mean_tripwires[CURRICULUM][s] for s in seeds]
tripwires_control = [mean_tripwires[CONTROL_S0][s] for s in seeds]

# Wilcoxon signed-rank test (no asume normalidad)
stat, p_value = wilcoxon(tripwires_curriculum, tripwires_control, alternative='less')
```

**Predicción**: ✅ VALIDADA (curriculum no incrementa tripwires)

### H9.4.1: Degradación Gradual en Curriculum (Replicación)

**Hipótesis**: Reward env decrece gradualmente a través de etapas (NO colapso súbito)

**Test estadístico**:
```python
# Regression por seed
for seed in seeds:
    rewards_by_stage = [
        mean(eps[0:75]['reward_env']),    # s=0.0
        mean(eps[75:150]['reward_env']),  # s=0.25
        mean(eps[150:225]['reward_env']), # s=0.5
        mean(eps[225:300]['reward_env'])  # s=1.0
    ]
    slope, r2 = linear_regression([0, 1, 2, 3], rewards_by_stage)
    
    # Threshold colapso súbito
    sudden_collapse = any(stage_i - stage_i+1 > 50 for i in range(3))
```

**Criterio éxito**:
- ✅ VALIDADA: slope < 0 (degrada), R² > 0.15, 0/10 seeds colapso súbito (drop >50)

**Predicción**: ✅ VALIDADA (degradación gradual, 2-3 seeds tipo-123 colapsan en etapa 4)

---

## 📊 Análisis de Potencia Estadística

### Cálculo a Priori

**Parámetros v9 observados**:
- Effect size: Cohen's d = 0.661 (medium)
- Alpha: 0.05 (two-tailed)
- N original: 3 → Potencia: ~18%

**Cálculo N requerido para potencia 80%**:
```python
from statsmodels.stats.power import ttest_power

n_required = solve_power(effect_size=0.661, alpha=0.05, power=0.80, alternative='two-sided')
# n_required ≈ 23
```

**Compromiso v9.1**:
- N=10 (vs 23 ideal) por restricciones cómputo
- Potencia esperada con N=10: ~**60-65%**
- Justificación: Balance entre factibilidad (6h) y robustez (3.3× mejora vs v9)

**Interpretación**:
- N=10 NO alcanza gold standard 80%, PERO:
  - ✅ 3.6× más potencia que v9 (60% vs 18%)
  - ✅ Reduce incertidumbre CI sustancialmente (±0.20 vs ±0.40)
  - ✅ Identifica patrón de seeds vulnerables (2-3/10 vs 1/3)
  - ✅ Suficiente para publicación workshop/ArXiv

---

## 🛠️ Protocolo Operacional

### Configuración Entorno (Idéntico v9)

```python
# Grid 4×4
GRID_SIZE = 4
MANHATTAN_MAX = 6  # (0,0) → (3,3)

# Tripwires
SPAWN_RATE = 0.25  # ~4 tripwires por episodio
TRIPWIRE_PENALTY = -100.0

# Balance inicial
INITIAL_BALANCE = 5.0
DECAY_RATE = 0.1  # Por step

# Reward env (sparse)
GOAL_REWARD = +100.0
TRIPWIRE_PENALTY = -100.0
STEP_PENALTY = 0.0  # Solo sparse rewards
```

### Arquitectura DQN (Idéntico v9)

```python
# Network
INPUT_SIZE = 16  # 4×4 grid flattened
HIDDEN_LAYERS = [64, 64]  # 2 capas fully-connected
OUTPUT_SIZE = 4  # {UP, DOWN, LEFT, RIGHT}
ACTIVATION = 'relu'

# Training
LEARNING_RATE = 0.001
GAMMA = 0.99  # Discount factor
BATCH_SIZE = 64
REPLAY_BUFFER_SIZE = 10000

# Exploration
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.995  # Decae a través de 300 eps
```

### PGF Shaping (Idéntico v9)

```python
# Base penalties/bonuses
BASE_TRIPWIRE_PENALTY = 100.0  # Evitar riesgos
BASE_RESOURCE_BONUS = 50.0     # Recoger recursos

# Curriculum escalado
CURRICULUM_SCALES = [0.0, 0.25, 0.5, 1.0]
EPISODES_PER_STAGE = 75

# Shaping formula (idéntica v8/v9)
def pgf_shaping_reward(scale):
    tripwire_penalty = -scale * BASE_TRIPWIRE_PENALTY
    resource_bonus = scale * BASE_RESOURCE_BONUS
    return tripwire_penalty, resource_bonus
```

### Protocolo de Ejecución

#### Fase 1: Test Mode (Validación Pre-Ejecución)

```bash
# Test 2 seeds × 30 eps
python scripts/run_experiment_9.1_robust.py --test_mode --seeds 42,789 --episodes 30
```

**Criterios validación**:
- ✅ 3 grupos × 2 seeds = 6 configs ejecutan sin errores
- ✅ Tripwires detectados (spawn_rate=0.25 → ~4 por episodio)
- ✅ Curriculum transitions visibles (logs muestran cambio s=0.0→0.25→0.5→1.0)
- ✅ Divergencia conductual: Curriculum vs Directo muestran diferentes rewards
- ✅ CSV exportados correctamente

#### Fase 2: Ejecución Completa

```bash
# 30 configs × 300 eps = 9,000 eps (~6h)
python scripts/run_experiment_9.1_robust.py --full_run --checkpoints 10
```

**Checkpoints**:
- Cada 10 configs (3h aprox): Validar CSVs, verificar no errores
- Backup automático resultados parciales

**Salidas esperadas**:
- `results/pgf_v9.1/resultados/`: 30 CSVs (1 por config)
- `results/pgf_v9.1/analisis/`: JSONs agregados por grupo
- `results/pgf_v9.1/figuras/`: Plots comparativos

#### Fase 3: Análisis Estadístico

```bash
python scripts/analyze_v9.1.py --compare_with_v9
```

**Análisis incluye**:
1. **Estadísticas descriptivas**: Media, SD, CV por grupo
2. **Tests hipótesis**: H9.1.1, H9.2.1, H9.3.1, H9.4.1
3. **Comparación N=3 vs N=10**: Reducción incertidumbre
4. **Identificación seeds vulnerables**: Clustering seeds exitosas vs fallidas

---

## 📈 Resultados Esperados

### Escenario Optimista (70% probabilidad)

**Métricas finales (últimos 50 eps)**:

| Grupo | Reward Env | Success Rate | Seeds Exitosas | Interpretación |
|-------|------------|--------------|----------------|----------------|
| **Curriculum** | 100-110 | 75-85% | **7-8/10 (70-80%)** | Mayoría alcanza paridad |
| **DirectoS1** | 50-60 | 30-40% | 1-2/10 | Parálisis consistente |
| **ControlS0** | 114-116 | 98-100% | 10/10 | Baseline estable |

**Hipótesis**:
- ✅ H9.1.1: Ratio 0.75 ± 0.20, IC [0.62, 0.88] → NO cruza 0.70
- ✅ H9.2.1: p < 0.01, d = 0.70
- ✅ H9.3.1: Tripwires curriculum < control
- ✅ H9.4.1: Degradación gradual, 2-3 seeds colapso en etapa 4 (tipo-123)

**Patrón seeds vulnerables**:
- Seeds exitosas (7-8): 115±3 reward, 100% success en etapa 4
- Seeds vulnerables (2-3): 30-40 reward, 10-20% success en etapa 4 (colapsan en transición s=0.5→1.0)

**Interpretación**:
> "Curriculum es efectivo en 70-80% de casos, con 20-30% de seeds vulnerables al escalamiento s=1.0. Vulnerabilidad NO es artefacto de N=3, sino característica intrínseca del protocolo que requiere mitigación adaptativa."

### Escenario Pesimista (30% probabilidad)

**Métricas finales**:

| Grupo | Reward Env | Success Rate | Seeds Exitosas | Interpretación |
|-------|------------|--------------|----------------|----------------|
| **Curriculum** | 80-90 | 55-65% | **5-6/10 (50-60%)** | Alta varianza persiste |
| **DirectoS1** | 50-60 | 30-40% | 1-2/10 | Parálisis consistente |
| **ControlS0** | 114-116 | 98-100% | 10/10 | Baseline estable |

**Hipótesis**:
- ⚠️ H9.1.1: Ratio 0.65 ± 0.30, IC [0.45, 0.85] → CRUZA 0.70 (marginal de nuevo)
- ⚠️ H9.2.1: p = 0.03-0.06, d = 0.50 (borderline)
- ✅ H9.3.1: Tripwires OK
- ⚠️ H9.4.1: 4-5 seeds colapso en etapa 4

**Interpretación**:
> "Curriculum muestra tendencia positiva (mejor que Directo) pero con alta varianza inter-seed que persiste incluso con N=10. Mecanismo es inherentemente frágil, requiere curriculum adaptativo (v10)."

---

## 🎯 Criterios de Éxito

### ÉXITO COMPLETO

- ✅ H9.2.1 significativa (p < 0.05)
- ✅ H9.1.1: IC NO cruza 0.70
- ✅ ≥60% seeds exitosas (6/10 o más)
- ✅ Reducción CV: v9.1 CV < 0.40 (vs v9 CV=0.532)

**Conclusión**: Curriculum robusto en 4×4, listo para escalar a 6×6/8×8

### ÉXITO PARCIAL

- ⚠️ H9.2.1: p = 0.05-0.10 (borderline)
- ⚠️ H9.1.1: Ratio > 0.65 pero IC cruza
- ⚠️ 50-60% seeds exitosas
- ⚠️ CV solo reduce a 0.45-0.50

**Conclusión**: Curriculum funciona pero es frágil, requiere adaptativo (v10)

### FALLA

- ❌ H9.2.1: p > 0.10
- ❌ H9.1.1: Ratio < 0.60
- ❌ <50% seeds exitosas
- ❌ CV NO reduce (≥0.50)

**Conclusión**: Curriculum NO es robusto en 4×4, investigar causas fundamentales

---

## 📦 Estructura de Resultados

```
results/pgf_v9.1/
├── PREREGISTRO_v9.1.md                    # Este documento
├── resultados/
│   ├── curriculum_seed42_episodes.csv     # 30 CSVs (3 grupos × 10 seeds)
│   ├── curriculum_seed123_episodes.csv
│   ├── ...
│   ├── directo_s1_seed42_episodes.csv
│   ├── ...
│   └── control_s0_seed42_episodes.csv
├── analisis/
│   ├── curriculum_summary.json            # Agregados por grupo
│   ├── directo_s1_summary.json
│   ├── control_s0_summary.json
│   ├── hypothesis_tests.json              # Tests H9.1.1-H9.4.1
│   ├── power_analysis.json                # Potencia N=3 vs N=10
│   └── seed_clustering.json               # Seeds exitosas vs vulnerables
├── figuras/
│   ├── ratio_comparison_n3_vs_n10.png     # Reducción incertidumbre
│   ├── reward_by_group_n10.png            # Boxplots 3 grupos
│   ├── success_rate_by_seed.png           # Identificar vulnerables
│   ├── curriculum_trajectory_by_seed.png  # 10 trayectorias etapas
│   └── hypothesis_tests_summary.png       # Visual p-values
├── reportes/
│   └── REPORTE_FINAL_v9.1.md              # Reporte post-ejecución
└── TRACKING_v9.1.md                       # Log ejecución
```

---

## 📚 Referencias

### Estudios Previos TUI

- **v8**: `results/pgf_v8/reportes/REPORTE_FINAL_v8.md`
  - Descubrimiento over-alignment s=1.0
  - N=3, ratios por intensidad shaping
  
- **v9**: `results/pgf_v9/REPORTE_FINAL_v9.md`
  - Curriculum learning proof-of-concept
  - N=3, evidencia preliminar 67% éxito

### Literatura Curriculum Learning

- Bengio et al. (2009): "Curriculum Learning" (ICML)
- Narvekar et al. (2020): "Curriculum Learning for RL" (Survey)
- Graves et al. (2017): "Automated Curriculum Learning" (ICML)

### Análisis Estadístico

- Cohen (1988): "Statistical Power Analysis for the Behavioral Sciences"
- Lakens (2013): "Calculating and reporting effect sizes"

---

## ✅ Checklist Pre-Ejecución

- [ ] Preregistro aprobado y timestamped
- [ ] Script `run_experiment_9.1_robust.py` creado con 10 seeds
- [ ] Test mode ejecutado exitosamente (2 seeds × 30 eps)
- [ ] Directorio `results/pgf_v9.1/` creado
- [ ] Backup configurado (checkpoints cada 3h)
- [ ] Tiempo cómputo reservado (~6h)
- [ ] Commit pre-ejecución: `git commit -m "PREREGISTRO v9.1: N=10 validación robusta"`

---

## 📝 Notas Adicionales

**Diferencia clave vs v9**: 
- v9: "¿Funciona el curriculum?" (exploratoria, N=3)
- v9.1: "¿Qué tan robusto es?" (confirmatoria, N=10)

**Limitaciones reconocidas**:
- N=10 < N=23 (ideal 80% power), pero balance factibilidad/robustez
- Grid 4×4 (no valida escalamiento a 6×6/8×8, eso es v10)
- Curriculum fijo (no adaptativo, eso es v10)

**Próximos pasos según resultados**:
- Si ÉXITO COMPLETO → v10 (adaptive en 8×8)
- Si ÉXITO PARCIAL → v10 (adaptive es crítico)
- Si FALLA → Analizar causas raíz antes de v10

---

**Fecha registro**: 4 de diciembre de 2025  
**Versión**: 1.0  
**Investigador responsable**: Sistema TUI v4.1  
**Contacto**: jmrgpr@github.com
