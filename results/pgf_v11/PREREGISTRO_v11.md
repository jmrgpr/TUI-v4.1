# 🔬 PREREGISTRO v11: Validación Mecanicista - Shaping Dinámico basado en Riesgo Efectivo

**Versión**: v11 ("Mecanismos Internos")  
**Fecha preregistro**: 4 de diciembre de 2025  
**Status**: 🔒 CONGELADO (NO modificar sin v11.1)  
**Investigador**: Sistema TUI v4.1  
**Predecesor**: v10.1 (8×8 balance calibrado)

---

## 📋 CAMBIO PARADIGMÁTICO

### De Observación Conductual → Validación Mecanicista

**Estado actual** (auditoría 26 experimentos):
- ✅ Sabemos QUÉ funciona: Curriculum robusto 4×4/6×6, v9.1 N=10
- ✅ Sabemos QUÉ falla: Over-alignment s=1.0 (ratio 0.34), 8×8 colapsa/trivializa
- ❌ NO sabemos POR QUÉ: Sin medición variables internas TUI

**v11 abre la caja negra**:
- Primera instrumentación cuantitativa: `risk_effective`, `surprise`
- Primera validación mecanismo: Shaping dinámico basado en riesgo percibido
- Comparación SOTA: Fixed shaping (Bengio 2009), Adaptive curriculum (Graves 2017)

---

## 🎯 OBJETIVO PRINCIPAL

**Validar que shaping modulado por riesgo efectivo percibido supera estrategias fijas/curriculum en eficiencia sin sacrificar safety.**

**Pregunta científica**:
> ¿Los agentes que ajustan prudencia según riesgo interno (TUI) evitan over-alignment mejor que estrategias fijas?

---

## 🧬 PREREQUISITO: v10.1 (BLOQUEANTE)

**⚠️ v11 NO PUEDE ejecutarse sin v10.1 exitoso**

### Gates Críticos v10.1:
```python
# Test mode v10.1 (2 seeds × 100 eps)
if control_success_rate >= 0.70 and control_success_rate <= 0.90:
    # ✅ GO v11: 8×8 discrimina correctamente
    GRID_SIZE_v11 = 8
    BALANCE_v11 = 5.0
elif control_success_rate > 0.95:
    # ❌ ABORT v11: Aún trivial, bajar balance
    # Crear v10.2 con balance=4.5
    raise ValueError("8×8 aún trivial, requiere balance más bajo")
elif control_success_rate < 0.60:
    # ❌ ABORT v11: Demasiado duro
    # Opción A: Subir balance a 5.5-6.0
    # Opción B: Usar 6×6 como backup
    GRID_SIZE_v11 = 6
    BALANCE_v11 = 5.0
```

**Asumiendo v10.1 exitoso** (gates OK), procedemos con diseño v11.

---

## 🔧 FASE 1: INSTRUMENTACIÓN (PREREQUISITO v11)

### Variables Internas TUI (NUEVAS)

#### 1. **Riesgo Efectivo** (`risk_effective`)

**Definición TUI**: Probabilidad percibida de peligro × Vulnerabilidad actual

**Implementación**:
```python
def calculate_risk_effective(self):
    """
    Risk_eff = f(proximidad_tripwires, energía, presión_temporal)
    
    Fórmula v11.0 (congelada):
    R_eff = 0.5 × proximity + 0.3 × energy_risk + 0.2 × time_pressure
    
    Rango: [0, 1]
    - 0.0: Sin riesgo (lejos tripwires, energía alta, tiempo sobra)
    - 1.0: Riesgo crítico (adyacente tripwire, inanición inminente)
    """
    # Proximidad a tripwire más cercano (Manhattan)
    agent_pos = self.agent_pos
    min_dist = min([manhattan(agent_pos, tw) for tw in self.tripwires])
    proximity_risk = 1.0 / (min_dist + 1.0)  # [0, 1]
    
    # Energía baja (vulnerabilidad starvation)
    energy_risk = max(0, 1.0 - self.balance / self.initial_balance)  # [0, 1]
    
    # Presión temporal (pasos restantes)
    steps_remaining = self.max_steps - self.current_step
    time_pressure = max(0, 1.0 - steps_remaining / self.max_steps)  # [0, 1]
    
    # Combinación ponderada
    risk_eff = (0.5 * proximity_risk + 
                0.3 * energy_risk + 
                0.2 * time_pressure)
    
    return risk_eff
```

**Logging**: `info['risk_effective']` en cada step

---

#### 2. **Sorpresa** (`surprise`)

**Definición TUI**: Eventos inesperados (|predicción - observación|)

**Implementación**:
```python
def calculate_surprise(self, reward, done, info):
    """
    Sorpresa = Magnitud de eventos no anticipados
    
    Proxy simplificado v11.0:
    - Tripwire activado → surprise = 1.0
    - Inanición → surprise = 0.8
    - Goal inesperado temprano → surprise = 0.5
    - Nada inesperado → surprise = 0.0
    """
    surprise = 0.0
    
    if info.get('tripwire_triggered', False):
        surprise = 1.0  # Evento adverso crítico
    elif info.get('death_starvation', False):
        surprise = 0.8  # Muerte por inanición
    elif info.get('goal_reached', False) and self.current_step < 20:
        surprise = 0.5  # Goal muy temprano (excepcional)
    
    return surprise
```

**Logging**: `info['surprise']` en cada step

---

### CSV Expandido (Columnas NUEVAS v11)

```python
# Métricas por episodio (agregadas desde steps):
'risk_effective_mean',      # Promedio risk_eff durante episodio
'risk_effective_max',       # Pico de riesgo alcanzado
'risk_effective_std',       # Variabilidad riesgo (exploración)
'surprise_total',           # Suma sorpresa acumulada
'surprise_events',          # Número eventos inesperados (count surprise > 0)
'balance_min',              # Balance mínimo alcanzado (vulnerabilidad)
'proximity_violations',     # Pasos con tripwire adyacente (dist ≤ 1)
'shaping_scale_mean',       # Promedio s aplicado (solo Dinámico)
'shaping_scale_std',        # Variabilidad s (adaptación)
```

**Validación instrumentación**: Test 4×4 × 50 eps antes de v11 completo.

---

## 🧪 DISEÑO EXPERIMENTAL v11

### Entorno Base

**Determinado por v10.1**:
```python
# Escenario A (si v10.1 discrimina)
GRID_SIZE = 8
BALANCE = 5.0
SPAWN_RATE = 0.25  # ~16 tripwires

# Escenario B (backup si v10.1 falla)
GRID_SIZE = 6
BALANCE = 5.0
SPAWN_RATE = 0.25  # ~9 tripwires
```

**Común**:
```python
MANHATTAN_MAX = GRID_SIZE * 2 - 2
MAX_STEPS = 200  # Suficiente para grid
STEP_COST = -0.2
RESOURCE_REWARD = 1.0
GOAL_REWARD = 100.0
TRIPWIRE_PENALTY = -100.0
```

---

### Grupos Experimentales (4)

#### **1. Control (Baseline)**
```python
grupo_control = {
    'name': 'Control',
    'shaping': 0.0,  # Sin PGF
    'description': 'Baseline inteligencia sin alineación'
}
```

---

#### **2. PGF Estático** (Benchmark Fixed)
```python
grupo_estatico = {
    'name': 'PGF_Estatico',
    'shaping': 0.5,  # Fijo (ventana útil v8: 0.2-0.6)
    'description': 'Shaping constante (referencia v8/v9.1)'
}
```

---

#### **3. PGF Curriculum** (Benchmark Adaptive)
```python
grupo_curriculum = {
    'name': 'PGF_Curriculum',
    'shaping': [0.0, 0.25, 0.5, 0.75, 1.0],  # 5 etapas
    'episodes_per_stage': 80,  # 400 eps / 5 = 80
    'description': 'Curriculum fijo (referencia v9.1)'
}
```

---

#### **4. PGF Dinámico** (TUI Risk-Based) ⭐ NOVEDAD

```python
grupo_dinamico = {
    'name': 'PGF_Dinamico',
    'shaping': 'dynamic',  # Calculado por risk_effective
    'description': 'Shaping modulado por riesgo percibido (TUI)'
}

def get_shaping_scale_dynamic(risk_effective, episode_progress):
    """
    Shaping dinámico v11.0 (CONGELADO)
    
    Lógica TUI:
    - Alto riesgo → Alto shaping (prudencia)
    - Bajo riesgo → Bajo shaping (eficiencia)
    - Early training → Más shaping (exploración segura)
    - Late training → Menos shaping (confianza)
    
    Fórmula ajustada (vs propuesta original):
    - Rango risk_component: [0.1, 0.9] (más amplio)
    - Decay experiencia: [0.8, 1.0] (más lento, -20% vs -30%)
    - Combinación ADITIVA ponderada (70% risk, 30% exp)
    """
    # Componente riesgo (dominante)
    risk_component = 0.1 + 0.8 * risk_effective  # [0.1, 0.9]
    
    # Componente experiencia (decay lento)
    experience_factor = 1.0 - 0.2 * episode_progress  # [0.8, 1.0]
    
    # Combinación aditiva ponderada
    s = 0.7 * risk_component + 0.3 * experience_factor
    
    # Clamp seguridad [0.1, 0.9]
    s = max(0.1, min(0.9, s))
    
    return s
```

**Ejemplo valores**:
```python
# Episodio 0 (novato):
# risk_eff=0.2 → s = 0.7×0.26 + 0.3×1.0 = 0.48
# risk_eff=0.8 → s = 0.7×0.74 + 0.3×1.0 = 0.82

# Episodio 400 (experto):
# risk_eff=0.2 → s = 0.7×0.26 + 0.3×0.8 = 0.42 (Δ=-0.06)
# risk_eff=0.8 → s = 0.7×0.74 + 0.3×0.8 = 0.76 (Δ=-0.06)

# Risk_eff sigue dominando señal, decay mínimo
```

---

### Seeds y Potencia

```python
N_SEEDS = 10  # Potencia ~72% para d=0.5

SEEDS = [42, 123, 456, 789, 101112, 131415, 161718, 192021, 222324, 252627]

# Total configs: 4 grupos × 10 seeds = 40
# Episodios totales: 40 × 400 = 16,000 eps (~20h)
```

---

### Arquitectura Agente

```python
# DQN (mismo v10.1)
HIDDEN_SIZE = 64  # 2 capas × 64 neuronas
BUFFER_SIZE = 10000
BATCH_SIZE = 64
LEARNING_RATE = 1e-3
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995
TARGET_UPDATE = 10
```

---

## 📊 HIPÓTESIS PREREGISTRADAS

### **H11.1: Correlación Mecanismo (CRÍTICA)**

**Enunciado**:
> El grupo PGF Dinámico mostrará correlación negativa fuerte entre `risk_effective_mean` y `tripwires_triggered` por episodio (r < -0.6, p < 0.01).

**Predicción TUI**:
```
Cuando risk_effective alto → agente evita tripwires (conducta prudente)
Cuando risk_effective bajo → agente toma riesgos calculados (eficiencia)

Mecanismo: Shaping dinámico refuerza evitación solo cuando riesgo percibido alto
```

**Test estadístico**:
```python
# Por seed:
for seed in seeds:
    df_dinamico = load_data(grupo='PGF_Dinamico', seed=seed)
    r, p = pearsonr(df_dinamico['risk_effective_mean'], 
                    df_dinamico['tripwires_triggered'])
    correlations_dinamico.append(r)

# Agregado:
mean_r_dinamico = np.mean(correlations_dinamico)

# Comparación Control (sin modulación):
mean_r_control = np.mean(correlations_control)

# t-test: r_dinamico vs r_control
t_stat, p_value = ttest_ind(correlations_dinamico, correlations_control)
```

**Criterios éxito**:
- ✅ **ÉXITO**: r_dinámico < -0.6, p < 0.01 (correlación fuerte)
- ⚠️ **PARCIAL**: r_dinámico ∈ [-0.6, -0.4], p < 0.05
- ❌ **FALLA**: r_dinámico > -0.4 o p > 0.05

**Comparación esperada**:
```
Control:     r ≈ 0 ± 0.2 (sin modulación)
Estático:    r ≈ -0.3 (modulación débil, shaping constante)
Curriculum:  r ≈ -0.4 (modulación por etapa)
Dinámico:    r < -0.6 (modulación continua risk-based)
```

---

### **H11.2: Eficiencia sin Over-Alignment (CRÍTICA)**

**Enunciado**:
> PGF Dinámico alcanzará ratio_reward_env ≥ 0.80, significativamente mayor que PGF Curriculum (~0.75) y PGF Estático (~0.60), sin sacrificar safety (success_rate ≥ 70%).

**Predicción TUI**:
```
Dinámico evita over-alignment porque:
- En zonas seguras (risk_eff bajo) → s bajo → eficiencia
- En zonas peligrosas → s alto → prudencia

Curriculum/Estático:
- Curriculum: Prudente SIEMPRE en etapas altas (s=0.75-1.0) → ineficiente
- Estático: Prudente SIEMPRE (s=0.5) → ineficiente
```

**Test estadístico**:
```python
# ANOVA one-way: ratio_reward_env ~ grupo
f_stat, p_anova = f_oneway(ratio_control, ratio_estatico, 
                            ratio_curriculum, ratio_dinamico)

# Post-hoc Tukey (pairwise comparisons)
tukey_results = pairwise_tukey(data, group_col='grupo', val_col='ratio')

# Comparación específica: Dinámico vs Curriculum
t_stat, p_value = ttest_ind(ratio_dinamico, ratio_curriculum)
effect_size = cohen_d(ratio_dinamico, ratio_curriculum)
```

**Criterios éxito**:
- ✅ **ÉXITO**: 
  - ratio_dinámico ≥ 0.80
  - ratio_dinámico > ratio_curriculum + 0.05 (mejora mínima)
  - p < 0.05, d > 0.5 (efecto moderado)
  - success_rate_dinámico ≥ 70% (mantiene safety)

- ⚠️ **PARCIAL**: 
  - ratio_dinámico ∈ [0.75, 0.80) (mejora marginal)
  - O success_rate < 70% (over-optimization)

- ❌ **FALLA**: 
  - ratio_dinámico < 0.75 (no mejora vs curriculum)
  - O p > 0.05 (no significativo)

**Valores esperados**:
```
Control:     ratio ≈ 0.50 ± 0.15 (baseline sin ayuda)
Estático:    ratio ≈ 0.60 ± 0.12 (over-alignment leve)
Curriculum:  ratio ≈ 0.75 ± 0.10 (benchmark v9.1)
Dinámico:    ratio ≈ 0.82 ± 0.08 (objetivo v11)
```

---

### **H11.3: Reducción Varianza (Robustez)**

**Enunciado**:
> PGF Dinámico tendrá coeficiente de variación (CV) entre seeds ≤ 0.15 para ratio_reward_env, significativamente menor que Curriculum (~0.20) y Estático (~0.30).

**Predicción TUI**:
```
Dinámico adapta a diferencias individuales seeds:
- Seed "tímido" (alta percepción risk_eff) → s alto automático
- Seed "audaz" (baja percepción risk_eff) → s bajo automático
→ Menor varianza final (personalización)

Curriculum/Estático:
- No personalizan → seeds diferentes reciben mismo tratamiento
→ Mayor varianza final
```

**Test estadístico**:
```python
# CV por grupo
cv_control = std(ratio_control) / mean(ratio_control)
cv_estatico = std(ratio_estatico) / mean(ratio_estatico)
cv_curriculum = std(ratio_curriculum) / mean(ratio_curriculum)
cv_dinamico = std(ratio_dinamico) / mean(ratio_dinamico)

# Bootstrap CI para CVs (1000 muestras)
cv_dinamico_ci = bootstrap_ci(ratio_dinamico, stat_func=compute_cv, n_boot=1000)

# Levene's test (homogeneidad varianzas)
levene_stat, p_levene = levene(ratio_control, ratio_estatico, 
                                ratio_curriculum, ratio_dinamico)
```

**Criterios éxito**:
- ✅ **ÉXITO**: 
  - CV_dinámico ≤ 0.15
  - CV_dinámico < CV_curriculum (mejora robustez)
  - IC_bootstrap no cruza CV_curriculum

- ⚠️ **PARCIAL**: 
  - CV_dinámico ∈ (0.15, 0.20]
  - O CV_dinámico ≈ CV_curriculum (sin mejora)

- ❌ **FALLA**: 
  - CV_dinámico > 0.20 (peor que curriculum)

**Valores esperados**:
```
Control:     CV ≈ 0.30 (alta varianza sin ayuda)
Estático:    CV ≈ 0.25 (varianza moderada)
Curriculum:  CV ≈ 0.18 (benchmark v9.1)
Dinámico:    CV ≈ 0.12 (objetivo v11, personalización)
```

---

### **H11.4: Sorpresa Decreciente (Aprendizaje)**

**Enunciado**:
> En PGF Dinámico, `surprise_total` decrece exponencialmente con episodios según modelo $surprise_t = a \cdot e^{-b \cdot t}$ con ajuste R² > 0.7 y tasa decay b > 0.01.

**Predicción TUI**:
```
TUI dice: Inteligencia reduce sorpresa
→ Agente aprende a predecir mundo → menos eventos inesperados

Dinámico facilita aprendizaje porque:
- Shaping alto cuando vulnerable → evita sorpresas adversas
- Shaping bajo cuando confiado → explora sin penalización excesiva

Control/Estático:
- Control: Aprende lento (sin guía)
- Estático: Aprende pero con ruido (shaping no adaptado)
```

**Test estadístico**:
```python
from scipy.optimize import curve_fit

def exp_decay(t, a, b):
    return a * np.exp(-b * t)

# Ajuste por grupo
for grupo in ['Control', 'Estático', 'Curriculum', 'Dinámico']:
    df_grupo = load_data(grupo)
    
    # Agregado por episodio (mean across seeds)
    surprise_mean = df_grupo.groupby('episode')['surprise_total'].mean()
    episodes = surprise_mean.index
    
    # Fit exponencial
    params, _ = curve_fit(exp_decay, episodes, surprise_mean, 
                          p0=[10.0, 0.01], maxfev=10000)
    a, b = params
    
    # R² score
    surprise_pred = exp_decay(episodes, a, b)
    r2 = r2_score(surprise_mean, surprise_pred)
    
    results[grupo] = {'a': a, 'b': b, 'r2': r2}
```

**Criterios éxito**:
- ✅ **ÉXITO**: 
  - R²_dinámico > 0.7 (buen ajuste)
  - b_dinámico > 0.01 (decay significativo)
  - R²_dinámico > R²_control + 0.1 (mejor predicción)

- ⚠️ **PARCIAL**: 
  - R²_dinámico ∈ [0.5, 0.7] (ajuste moderado)
  - O b_dinámico ∈ [0.005, 0.01] (decay lento)

- ❌ **FALLA**: 
  - R²_dinámico < 0.5 (mal ajuste)
  - O b_dinámico < 0.005 (no hay decay)

**Valores esperados**:
```
Control:     R² ≈ 0.4, b ≈ 0.005 (aprendizaje lento)
Estático:    R² ≈ 0.6, b ≈ 0.008 (aprendizaje moderado)
Curriculum:  R² ≈ 0.65, b ≈ 0.010 (aprendizaje guiado)
Dinámico:    R² ≈ 0.75, b ≈ 0.012 (aprendizaje óptimo)
```

---

## 📈 ANÁLISIS ESTADÍSTICO

### Primario (Confirmatorio)

**Tests preregistrados**:
1. **H11.1**: Correlación Pearson + t-test agregado
2. **H11.2**: ANOVA one-way + Tukey post-hoc + Cohen's d
3. **H11.3**: CV + Bootstrap CI + Levene's test
4. **H11.4**: Regresión exponencial + R²

**Software**: Python 3.11, scipy 1.11, statsmodels 0.14

**Correcciones múltiples**: Bonferroni (α=0.05/4=0.0125 por hipótesis)

---

### Secundario (Exploratorio)

**NO afecta conclusiones primarias**:
- Curvas temporales: risk_effective vs success_rate por entrenamiento
- Heatmaps: Frecuencia visitas por celda (exploración)
- Trayectorias: Visualizar 5 episodios seed 123 (Dinámico vs Curriculum)
- Clustering seeds: K-means (rápidas vs lentas)

---

## 🎯 CRITERIOS DECISIÓN v11

### ✅ **ÉXITO COMPLETO** (4/4 hipótesis)

```
H11.1: r < -0.6, p < 0.01 ✅
H11.2: ratio ≥ 0.80, p < 0.05 ✅
H11.3: CV ≤ 0.15 ✅
H11.4: R² > 0.7 ✅

Conclusión:
- PGF Dinámico VALIDA mecanismo TUI
- Shaping basado en riesgo efectivo > fijo/curriculum
- Primera evidencia cuantitativa variables internas TUI
```

**Paper story**: "Dynamic risk-based shaping prevents over-alignment while maintaining safety"

**Próximo paso**: v12 P_genuino MVP (costo mantener propósito, distractores)

---

### ⚠️ **ÉXITO PARCIAL** (2-3 hipótesis)

```
Ejemplo escenario:
H11.1: ✅ Correlación fuerte (mecanismo funciona)
H11.2: ✅ Ratio alto (eficiencia lograda)
H11.3: ❌ CV ≈ curriculum (no mejora robustez)
H11.4: ⚠️ R² = 0.6 (tendencia pero no fuerte)

Conclusión:
- Mecanismo funciona pero NO optimizado
- Fórmula risk_effective necesita refinamiento
- O modulación shaping necesita ajuste pesos
```

**Acción**: v11.1 con ajustes (refinar fórmula risk_eff o shaping)

**Paper story**: "Dynamic shaping shows promise but requires calibration"

---

### ❌ **FALLA** (0-1 hipótesis)

```
Ejemplo escenario:
H11.1: ❌ r = -0.3 (correlación débil)
H11.2: ❌ ratio ≈ 0.60 (similar a estático)

Conclusión:
- Shaping dinámico NO superior
- Diagnósticos posibles:
  1. Fórmula risk_effective incorrecta (no captura riesgo real)
  2. Modulación s demasiado rápida/lenta
  3. Agente NO utiliza señal (problema arquitectural)
```

**Acción**: Análisis exploratorio profundo → Rediseñar v12 con enfoque diferente

**Paper story**: "Null result: Dynamic shaping did not improve over fixed schedules"

---

## 📁 ESTRUCTURA RESULTADOS

```
results/pgf_v11/
├── PREREGISTRO_v11.md          # Este archivo (CONGELADO)
├── README.md                    # Documentación experimento
├── TRACKING_v11.md              # Log ejecución
├── resultados/
│   ├── exp11_Control_seed{seed}_episodes.csv        (40 archivos)
│   ├── exp11_PGF_Estatico_seed{seed}_episodes.csv
│   ├── exp11_PGF_Curriculum_seed{seed}_episodes.csv
│   └── exp11_PGF_Dinamico_seed{seed}_episodes.csv
├── analisis/
│   ├── mechanism_validation.json  # H11.1 correlaciones
│   ├── efficiency_analysis.json   # H11.2 ANOVA + ratios
│   ├── robustness_cv.json         # H11.3 varianza
│   ├── surprise_temporal.json     # H11.4 regresiones
│   └── final_metrics_v11.csv      # Consolidado
├── figuras/
│   ├── fig1_learning_curves_4groups.png
│   ├── fig2_scatter_risk_vs_tripwires.png  # H11.1
│   ├── fig3_barplot_ratios_anova.png       # H11.2
│   ├── fig4_surprise_decay.png             # H11.4
│   └── fig5_heatmap_visitation.png
├── exploratorios/
│   └── seed_trajectories_dinámico_vs_curriculum.json
└── reportes/
    └── REPORTE_FINAL_v11.md
```

---

## ⏱️ CRONOGRAMA

### **Semana 1: v10.1 + Instrumentación**

**Día 1-2**: v10.1 test mode + ejecución (paralelo)
- Test mode: 2 seeds × 100 eps (gates)
- Si gates OK → batch completo (24 configs)

**Día 3-5**: Instrumentación PGF
- Modificar `sim/environment_v2.py`
- Test instrumentación 4×4 × 50 eps
- Validar CSV columnas nuevas

**Día 6**: Decisión grid size v11
- v10.1 OK → 8×8
- v10.1 FAIL → 6×6 backup

---

### **Semana 2: v11 Ejecución**

**Día 7**: Script v11 + test mode
- Crear `run_experiment_11_dynamic_pgf.py`
- Test 1 seed × 4 grupos × 100 eps

**Días 8-10**: Batch completo v11
- 40 configs × 400 eps = 16,000 eps (~20h)
- Checkpoints cada 5 configs

**Días 11-12**: Análisis H11.1-H11.4
- Tests estadísticos confirmatorios
- Figuras principales

**Día 13**: Reporte preliminar

---

## 🔬 VALOR CIENTÍFICO

### **Contribución 1**: Instrumentación Variables Internas
- Primera medición cuantitativa `risk_effective`, `surprise` en RL alineado
- Novedad: Literatura Safe RL usa constraints externos (CPO, Lagrangian), NO percepción interna

### **Contribución 2**: Shaping Dinámico > Fijo
- Demostración empírica shaping modulado por riesgo evita over-alignment
- Comparación SOTA:
  - Curriculum (Bengio 2009): Fijo por etapas
  - Adaptive curriculum (Graves 2017): Basado en performance
  - **v11 Dinámico**: Basado en riesgo percibido ← ÚNICO

### **Contribución 3**: Validación Parcial TUI
- Confirma predicción: "Agentes inteligentes modulan conducta según riesgo percibido"
- **Limitación honesta**: NO valida P_genuino ni riesgo acumulado (requiere v12-v13)

---

## 🔒 CONGELAMIENTO PREREGISTRO

**Versión**: v11.0  
**Commit hash**: [TBD tras git commit]  
**Fecha congelamiento**: 4 de diciembre de 2025  

**Cambios NO permitidos sin v11.1**:
- ❌ Hipótesis H11.1-H11.4
- ❌ Fórmulas `calculate_risk_effective()`, `get_shaping_scale_dynamic()`
- ❌ Criterios éxito/parcial/falla
- ❌ N seeds, grid size (determinado por v10.1)

**Cambios permitidos**:
- ✅ Debugging técnico (crashes, NaNs)
- ✅ Ajustes visualizaciones (exploratorio)
- ✅ Análisis adicionales (secundario)

---

**FIN PREREGISTRO v11**

**Próximo paso**: Ejecutar v10.1 test mode → Validar gates → Instrumentación PGF

**Documentado por**: Sistema TUI v4.1  
**Última actualización**: 4 de diciembre de 2025, 23:30
