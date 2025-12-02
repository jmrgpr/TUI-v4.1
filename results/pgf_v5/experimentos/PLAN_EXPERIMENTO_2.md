# Experimento 2: Manipulación de Densidad de Recursos

**Objetivo:** Demostrar que el ratio PGF/Control sigue la densidad de recursos, NO el grid size

**Fecha:** 2 de diciembre de 2025  
**Investigador:** Jose M Rivera Garcia

---

## Hipótesis Principal

$$\frac{Reward_{PGF}}{Reward_{Control}} \propto \frac{1}{D_{recursos}}$$

**En palabras:**
> El ratio de desempeño es inversamente proporcional a la densidad de recursos. A mayor abundancia, menor ventaja de la prudencia (PGF).

---

## Diseño Experimental

### Variables Independientes:
1. **Spawn Rate** (tasa de aparición de recursos): 0.2, 0.5, 0.8
2. **Death Penalty** (penalización por muerte): -100, -200
3. **Grid Size** (control): 4x4, 5x5

### Variables Dependientes:
1. **Ratio PGF/Control** (primaria)
2. **Densidad efectiva** ($D_{eff}$)
3. **Resource Utilization Rate** (RUR)
4. **Death Rate** (por inanición vs trampas)

### Variables Controladas:
- Episodios: 500 por seed
- Seeds: 42, 123, 456 (reproducibilidad)
- Risk scale: 1.5
- PGF mix: 0.2
- Max steps: 30

---

## Configuraciones Experimentales

### Exp 2A: Baja Densidad (Escasez)
```bash
python sim/prototipo_rl_simbiosis.py \
    --episodes 500 \
    --seed {42,123,456} \
    --grid_size 4 \
    --risk_scale 1.5 \
    --pgf_mix 0.2 \
    --spawn_rate 0.2 \
    --output_prefix results/pgf_v5/resultados/exp2a_low_density_seed{N}
```

**Predicción:** Ratio ~60-70% (escasez → prudencia valiosa)

---

### Exp 2B: Densidad Media (Baseline)
```bash
python sim/prototipo_rl_simbiosis.py \
    --episodes 500 \
    --seed {42,123,456} \
    --grid_size 4 \
    --risk_scale 1.5 \
    --pgf_mix 0.2 \
    --spawn_rate 0.5 \
    --output_prefix results/pgf_v5/resultados/exp2b_med_density_seed{N}
```

**Predicción:** Ratio ~32% (replicación de PGF v4)

---

### Exp 2C: Alta Densidad (Abundancia)
```bash
python sim/prototipo_rl_simbiosis.py \
    --episodes 500 \
    --seed {42,123,456} \
    --grid_size 4 \
    --risk_scale 1.5 \
    --pgf_mix 0.2 \
    --spawn_rate 0.8 \
    --output_prefix results/pgf_v5/resultados/exp2c_high_density_seed{N}
```

**Predicción:** Ratio ~20-25% (abundancia → imprudencia domina)

---

### Exp 2D: Castigo Aumentado
```bash
python sim/prototipo_rl_simbiosis.py \
    --episodes 500 \
    --seed {42,123,456} \
    --grid_size 4 \
    --risk_scale 1.5 \
    --pgf_mix 0.2 \
    --spawn_rate 0.5 \
    --death_penalty -200 \
    --output_prefix results/pgf_v5/resultados/exp2d_high_penalty_seed{N}
```

**Predicción:** Ratio ~50-60% (castigo mayor → prudencia más valiosa)

---

### Exp 2E: Control 5x5
```bash
python sim/prototipo_rl_simbiosis.py \
    --episodes 500 \
    --seed {42,123,456} \
    --grid_size 5 \
    --risk_scale 1.5 \
    --pgf_mix 0.2 \
    --spawn_rate 0.5 \
    --output_prefix results/pgf_v5/resultados/exp2e_grid5_seed{N}
```

**Predicción:** Ratio ~39% (baseline PGF v4 para comparación)

---

## Análisis Planificado

### 1. Correlación Densidad vs Ratio
```python
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Cargar datos
data = {
    'exp': ['2A', '2B', '2C', '2D', '2E'],
    'spawn_rate': [0.2, 0.5, 0.8, 0.5, 0.5],
    'grid': [4, 4, 4, 4, 5],
    'penalty': [-100, -100, -100, -200, -100],
    'ratio': [?, 32, ?, ?, 39]  # A completar con resultados reales
}

# Scatter plot: Densidad vs Ratio
plt.scatter(data['spawn_rate'], data['ratio'])
plt.xlabel('Spawn Rate (Densidad)')
plt.ylabel('Ratio PGF/Control (%)')
plt.title('Optimal Foraging Paradox: Density-Dependent Alignment Cost')

# Correlación
r, p = pearsonr(data['spawn_rate'], data['ratio'])
print(f'Correlación: r={r:.3f}, p={p:.4f}')
```

**Criterio de éxito:** $R^2 > 0.7$ y $p < 0.05$

---

### 2. ANOVA de un Factor
```python
from scipy.stats import f_oneway

# Comparar ratios entre configuraciones
f_stat, p_value = f_oneway(ratio_2A, ratio_2B, ratio_2C)
print(f'ANOVA: F={f_stat:.2f}, p={p_value:.4f}')
```

**Criterio:** $p < 0.05$ indica diferencias significativas entre densidades

---

### 3. Test Post-hoc (Tukey HSD)
```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Comparaciones múltiples
tukey = pairwise_tukeyhsd(all_ratios, all_conditions)
print(tukey)
```

**Esperado:**
- 2A > 2B (escasez > media)
- 2B > 2C (media > abundancia)
- 2D > 2B (castigo alto > castigo base)

---

## Visualizaciones Planificadas

### Figura 1: Curva de Densidad
**Tipo:** Scatter plot con línea de tendencia  
**Ejes:** 
- X: Spawn Rate (0.2, 0.5, 0.8)
- Y: Ratio PGF/Control (%)
**Elementos:**
- Puntos individuales (3 seeds por configuración)
- Barras de error (std)
- Línea de regresión con $R^2$
- Anotación de predicción teórica

---

### Figura 2: Barras Comparativas
**Tipo:** Bar plot con error bars  
**Grupos:** 2A, 2B, 2C, 2D, 2E  
**Colores:**
- Verde: Ratio > 50% (PGF domina)
- Amarillo: Ratio 30-50% (competitivo)
- Rojo: Ratio < 30% (Control domina)

---

### Figura 3: Heatmap de Configuraciones
**Tipo:** Heatmap 2D  
**Ejes:**
- X: Spawn Rate
- Y: Death Penalty
- Color: Ratio PGF/Control
**Objetivo:** Visualizar espacio de parámetros donde PGF gana/pierde

---

## Métricas Secundarias

### Resource Utilization Rate (RUR)
$$RUR = \frac{Resources_{collected}}{Resources_{spawned}}$$

**Predicción:**
- Alta densidad (2C): RUR bajo (~50%) - hay desperdicio
- Baja densidad (2A): RUR alto (~90%) - todo se consume

---

### Death Rate Decomposition
```python
death_rate_hunger = deaths_hunger / total_episodes
death_rate_traps = deaths_traps / total_episodes

print(f'2A: Hunger={death_rate_hunger:.2%}, Traps={death_rate_traps:.2%}')
```

**Predicción:**
- 2A (escasez): Alta mortalidad por hambre
- 2C (abundancia): Baja mortalidad total

---

## Criterios de Éxito

### Confirmación Fuerte (Todos cumplidos):
✅ $Ratio_{2A} > Ratio_{2B} > Ratio_{2C}$ (tendencia monotónica)  
✅ Correlación $R^2 > 0.7$ entre spawn_rate y ratio  
✅ $Ratio_{2D} > Ratio_{2B}$ (castigo aumenta valor de prudencia)  
✅ ANOVA $p < 0.05$ (diferencias significativas)

### Confirmación Débil (Al menos 2 de 4):
⚠️ Tendencia correcta pero no monotónica  
⚠️ $R^2 > 0.5$ (correlación moderada)  
⚠️ $Ratio_{2D}$ marginalmente mayor que $Ratio_{2B}$  
⚠️ ANOVA $p < 0.1$ (tendencia)

### Refutación (Cualquiera):
❌ $Ratio_{2A} < Ratio_{2C}$ (invertido)  
❌ $R^2 < 0.3$ (no correlación)  
❌ $Ratio_{2D} < Ratio_{2B}$ (castigo no funciona)

---

## Timeline

| Fase | Duración | Actividades |
|------|----------|-------------|
| **Preparación** | 1 día | Modificar código para spawn_rate, validar |
| **Ejecución 2A** | 0.5 días | 3 seeds × 500 ep (~1.5-2 horas) |
| **Ejecución 2B** | 0.5 días | Replicación baseline |
| **Ejecución 2C** | 0.5 días | Alta densidad |
| **Análisis parcial** | 0.5 días | Verificar tendencia 2A-2B-2C |
| **Ejecución 2D** | 0.5 días | Castigo alto |
| **Ejecución 2E** | 0.5 días | Control 5x5 |
| **Análisis completo** | 2 días | Estadística, figuras, interpretación |
| **Reporte** | 1 día | Redacción informe |

**Total estimado:** 7 días (1 semana intensiva)

---

## Notas Metodológicas

### Reproducibilidad:
- Mismas seeds (42, 123, 456) para todas las configuraciones
- Código con metadata completa (aprendizaje de PGF v4)
- Git tag: `pgf_v5_exp2` antes de iniciar

### Consideraciones:
- Si `spawn_rate` no está implementado, usar proxy: `initial_resources` y `resource_decay_rate`
- Monitorear tiempo de ejecución: si > 15 min/seed, reducir a 300 episodios
- Backup incremental después de cada configuración

---

## Próximos Pasos Post-Experimento

### Si se confirma hipótesis:
1. Escribir draft paper: "The Optimal Foraging Paradox in Aligned AI"
2. Experimento 3: Manipular otros parámetros (tripwires density, shock frequency)
3. Generalizar TUI v4.2 con ecuación formal de $Tax_{align}(D)$

### Si se refuta hipótesis:
1. Re-analizar factores confundidores (grid size, random seed effects)
2. Hipótesis alternativa: "Spatial configuration matters more than density"
3. Experimento 3: Grid topologies (rectangular vs cuadrado)

---

**Status:** Diseño experimental completo  
**Próximo paso:** Implementar spawn_rate en environment.py
