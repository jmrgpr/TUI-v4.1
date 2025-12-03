# 🎯 PGF v8: Experimento de Intensidad de Shaping

**Versión**: v8  
**Fecha inicio**: 3 de diciembre de 2025  
**Status**: 🟢 PREREGISTRADO (v1.3)  
**Paradigma**: "El Experimento del Shaping"

---

## 🔬 Motivación

### Lección de v7: Régimen de Saturación

El experimento v7 (factorial económico 3×5×3, 27k episodios) demostró que:

```
❌ Economía (harsh/balanced/favorable) NO modula ventaja PGF (F=0.28, p=0.75)
❌ Goldilocks NO detectado (modelos lineales/log dominan)
✅ Convergencia a paridad (ratio 99%, rango 96-103%)

Diagnóstico: Shaping PGF (-20 tripwire, +2 recurso) representa solo 
~18% del reward base (~110) → DQN ignora señal prudencial
```

**Ver**: [`REPORTE_FINAL_v7.md`](../pgf_v7/reportes/REPORTE_FINAL_v7.md)

### Pregunta Central v8

> **"¿A partir de qué intensidad de shaping aparece un coste/beneficio visible de la prudencia PGF?"**

En otras palabras: ¿Cuándo la señal de alineación es **suficientemente fuerte** para que DQN aprenda políticas divergentes?

---

## 🎯 Objetivos

### Objetivo Principal

Medir el **umbral de intensidad** donde:
1. **PGF diverge conductualmente** de Control (menos tripwires, menos muertes)
2. **Aparece coste de alineación** (PGF pierde reward por ser prudente)
3. **O alineación es gratis** (PGF mantiene reward con mejor seguridad)

### Objetivos Secundarios

- Validar si densidad de recursos **modera** el coste de alineación
- Establecer **métricas duales** (reward crudo vs shaped, conducta vs outcome)
- Identificar **régimen de aplicabilidad** de TUI (dónde prudencia importa)

---

## 🧪 Diseño Experimental

### Factor Principal: INTENSIDAD DE SHAPING

**Novedad conceptual**: Parametrizar shaping con escala multiplicativa

```python
# Baselines (5x más fuertes que v7)
PGF_BASE_TRIPWIRE_PENALTY = 100.0  # vs -20 en v7
PGF_BASE_RESOURCE_BONUS   = 50.0   # vs +2 en v7

# Factor a explorar
SHAPING_SCALE ∈ {0.0, 0.25, 0.5, 1.0}

# Aplicación
penalty = -PGF_BASE_TRIPWIRE_PENALTY * SHAPING_SCALE
bonus   =  PGF_BASE_RESOURCE_BONUS   * SHAPING_SCALE
```

**Interpretación de escalas**:

| Scale | Tripwire | Recurso | Significado |
|-------|----------|---------|-------------|
| 0.0 | 0 | 0 | **Control puro** (sin shaping) |
| 0.25 | -25 | +12.5 | **Shaping leve** (comparable a v7) |
| 0.5 | -50 | +25 | **Shaping moderado** |
| 1.0 | -100 | +50 | **Shaping fuerte** (equiparable a goal_reward) |

### Diseño Factorial Reducido

**NO otro 3×5×3 gigante**. Enfoque quirúrgico:

| Factor | Niveles | Justificación |
|--------|---------|---------------|
| **Shaping Scale** | {0.0, 0.25, 0.5, 1.0} | Gradiente de intensidad prudencial |
| **Densidad** | {0.25, 0.40} | Moderada vs alta (mitigación "laberinto trivial") |
| **Economía** | **Balanced (5.0) fija** | Aislamiento: eliminar variable confundente |
| **Seeds** | {42, 123, 456} | Control variabilidad estocástica |

**Total**: 4 × 2 × 3 = **24 configuraciones**

> ⚠️ **Cambio v1.3**: Densidad mínima elevada de 0.10 → 0.25 para mitigar riesgo "laberinto trivial" (P(camino óptimo seguro) reducido de 48% → 13%). Ver [PREREGISTRO v1.3](PREREGISTRO_v8.md#validación-de-complejidad-del-entorno).

### Parámetros de Entrenamiento

```python
episodes_per_agent = 300
total_episodes_per_config = 600  # 300 PGF + 300 Control
total_episodes_experiment = 14,400  # 24 configs × 600 eps

# Estimación tiempo ejecución: ~10-12 minutos
```

### Economía Fija (Balanced)

```python
step_cost = -0.2
goal_reward = 1.0
balance = goal_reward / abs(step_cost) = 5.0
TRIPWIRE_FATAL = False  # Fase 1: penalización, no muerte instantánea
```

**Justificación**: v7 detectó threshold en balance=5.0 (ΔAIC=-185), aunque efecto débil. Fijamos en ese umbral para maximizar sensibilidad a shaping.

**Nota Fase 2**: Si convergencia persiste con s=1.0, existe protocolo de escalada a v8.1 con `TRIPWIRE_FATAL=True` (muerte instantánea simétrica para ambos agentes). Ver [`PREREGISTRO_v8.md`](PREREGISTRO_v8.md) sección "Protocolo de Fases".

---

## 📊 Métricas (Nuevo Sistema Dual)

### Crítica Metodológica v7

> ⚠️ **"No se registró `tripwires_per_episode`. Sin contar tripwires, estamos ciegos a la calidad de la estrategia."** - Peer Review

v8 corrige esta **insuficiencia de observabilidad**.

### Métricas Obligatorias por Episodio

#### Rewards Duales
```python
"total_reward_env": sum(reward crudo del entorno),      # Lo que "importa al mundo"
"total_reward_shaped": sum(train_signal con shaping),   # Lo que "ve" el agente
```

**Análisis**: Comparar ratios en ambas dimensiones
- Si `ratio_env < 95%` pero `tripwires ↓` → **Coste de alineación visible**
- Si `ratio_env ≈ 100%` y `tripwires ↓` → **Alineación gratis**

#### Métricas de Seguridad
```python
"tripwires_triggered": int,     # Contador absoluto por episodio
"deaths_starvation": int,       # Muertes por energy=0
"deaths_tripwire": int,         # Solo relevante en v8.1 (TRIPWIRE_FATAL=True)
```

#### Métricas de Eficiencia
```python
"resources_collected": int,     # Total recursos consumidos
"steps_to_goal": int,          # Eficiencia pura (Manhattan + desvíos)
"goal_reached": bool,          # Éxito/fracaso episodio
```

### Análisis por Tramos Temporales

Reportar en ventanas de convergencia:

```python
tramos = {
    "exploration": episodes 1-100,   # Alta ε, alta varianza
    "convergence": episodes 101-200, # ε→0.01, estabilizando
    "stability": episodes 201-300    # ε=0.01, política asintótica
}
```

**Pregunta clave**: ¿Shaping solo acelera aprendizaje (ventaja en tramo 1) o cambia política final (ventaja en tramo 3)?

---

## 📋 Hipótesis Preregistradas

### H8.1: Umbral de Shaping (Efecto Principal)

> **Enunciado**: Existe un `SHAPING_SCALE` crítico (s* ∈ [0.5, 1.0]) donde PGF diverge significativamente de Control en seguridad y reward.

**Predicciones cuantitativas**:

1. **Seguridad**: 
   ```
   Con s=1.0: tripwires_pgf / tripwires_control < 0.7  (reducción ≥30%)
   ```

2. **Coste de alineación**:
   ```
   Con s=1.0: ratio_reward_env < 0.95  (pérdida ≥5% en reward crudo)
   ```

3. **Compensación shaped**:
   ```
   Con s=1.0: ratio_reward_shaped ≥ 0.95  (agente PGF ve recompensa similar)
   ```

**Criterio de éxito H8.1**: 2/3 predicciones cumplidas con p<0.05 en ANOVA.

### H8.2: Interacción Shaping × Densidad

> **Enunciado**: La densidad de recursos **modera** el coste de alineación. En escasez, prudencia es más costosa que en abundancia.

**Predicciones específicas**:

1. **En densidad=0.10 (escasez)**:
   ```
   ratio_env(s=1.0) < 0.90  (coste severo: -10%)
   tripwires_pgf ≈ 0         (necesidad forzada de prudencia)
   ```

2. **En densidad=0.25 (abundancia)**:
   ```
   ratio_env(s=1.0) ≥ 0.95   (coste mitigado: -5%)
   tripwires_pgf ≈ 0          (prudencia sin sacrificio)
   ```

**Criterio de éxito H8.2**: Interacción significativa (p<0.05) en ANOVA 2-way Shaping×Densidad, con diferencia ≥5 puntos porcentuales entre densidades.

### H8.3: Convergencia Conductual (Metodológica)

> **Enunciado**: Con s=0.0 (sin shaping), PGF y Control deben ser **indistinguibles** en todas las métricas. Esto valida que la divergencia en s>0 es causal.

**Predicciones**:
```
ratio_env(s=0.0) ∈ [0.98, 1.02]       (paridad ±2%)
tripwires_pgf(s=0.0) ≈ tripwires_control(s=0.0)  (conducta idéntica)
```

**Criterio de éxito H8.3**: No diferencias significativas (p>0.10) entre PGF y Control cuando s=0.0.

---

## 🔍 Análisis Planeado

### 1. ANOVA 2-Way: Shaping × Densidad

```python
DV: ratio_reward_env, ratio_reward_shaped, tripwires_ratio
IV1: SHAPING_SCALE (4 niveles)
IV2: Densidad (2 niveles)
Replicaciones: 3 seeds por celda
```

**Preguntas**:
- ¿Efecto principal Shaping significativo? (esperado: p<0.001)
- ¿Interacción Shaping×Densidad? (H8.2)
- ¿Efecto densidad en s=0.0? (control negativo)

### 2. Post-Hoc: Comparaciones Múltiples

Tukey HSD para comparar:
- s=0.0 vs s=1.0 (máximo contraste)
- s=0.25 vs s=0.5 (detección threshold)
- Por densidad: escasez vs abundancia en cada nivel s

### 3. Regresión: Threshold Detection

```python
# Modelo segmentado
ratio ~ scale + I(scale > threshold) * (scale - threshold)
```

Buscar punto de quiebre donde relación ratio-shaping cambia pendiente (¿existe "demasiado shaping"?).

### 4. Análisis Temporal: Curvas de Aprendizaje

```python
# Por tramos
ratio_tramo_i = mean_reward_pgf[tramo_i] / mean_reward_control[tramo_i]
```

**Plot**: Evolución ratio(t) para cada nivel s. Ver si ventaja PGF **emerge** (crece con t) o **desaparece** (solo bootstrapping).

### 5. Métricas de Seguridad

Análisis descriptivo:
```python
safety_score = 1 - (tripwires_triggered / max_possible_tripwires)
survival_rate = 1 - (deaths_total / episodes)
efficiency = steps_optimal / steps_actual
```

Comparar PGF vs Control en scatter plot 2D: `(safety_score, reward)`. Buscar frontera de Pareto.

---

## 📐 Comparación con v7

| Aspecto | v7 (Factorial Económico) | v8 (Intensidad Shaping) |
|---------|--------------------------|-------------------------|
| **Factor principal** | Economía (3 niveles) | Shaping Scale (4 niveles) |
| **Configs totales** | 45 | 24 |
| **Episodios totales** | 27,000 | 14,400 |
| **Tiempo ejecución** | ~17 min | ~10 min |
| **Shaping PGF** | Fijo (-20/+2) | Variable (0 a -100/+50) |
| **Métricas seguridad** | ❌ No guardadas | ✅ Obligatorias |
| **Reward dual** | ❌ Solo shaped | ✅ Crudo + Shaped |
| **Resultado esperado** | Convergencia (99%) | **Divergencia (80-120%)** |

---

## 🎨 Visualizaciones Planeadas

### Figura 1: Heatmap Ratio × Shaping × Densidad
```
Ejes: Shaping Scale (x), Densidad (y)
Color: Ratio reward_env PGF/Control
Escala: 0.80 (azul, PGF pierde) → 1.20 (rojo, PGF gana)
```

### Figura 2: Scatter Safety-Reward Tradeoff
```
X: Safety Score (1 - tripwires_norm)
Y: Mean Reward Env
Puntos: PGF (rojo), Control (azul)
Agrupación: Por shaping scale
Ideal: PGF arriba-derecha (más seguro, más reward)
```

### Figura 3: Curvas de Aprendizaje por Shaping
```
X: Episodios (0-300)
Y: Ratio PGF/Control (ventana móvil 20 eps)
Líneas: Una por shaping scale
Hipótesis: s=1.0 diverge desde episodio ~50
```

### Figura 4: Threshold Detection (Regresión Segmentada)
```
X: Shaping Scale
Y: Ratio reward_env
Modelo: Piecewise linear con quiebre en s*
Detectar: ¿Existe "too much shaping"?
```

---

## 🚦 Criterios de Éxito Global v8

| Criterio | Métrica | Threshold |
|----------|---------|-----------|
| **Divergencia básica** | `max(ratio) - min(ratio)` | ≥ 15 puntos % |
| **Seguridad PGF** | `tripwires_pgf(s=1.0)` | < 0.5 × `tripwires_control(s=1.0)` |
| **Coste visible** | `ratio_env(s=1.0)` | < 0.95 en al menos 1 densidad |
| **Significancia estadística** | ANOVA p-value Shaping | < 0.01 |
| **Consistencia seeds** | `std(ratio)` entre seeds | < 0.05 |

**Veredicto**: v8 exitoso si ≥4/5 criterios cumplidos.

---

## 🗂️ Estructura de Archivos

```
results/pgf_v8/
├── README.md                          # Este archivo
├── PREREGISTRO_v8.md                  # Hipótesis formales H8.1-H8.3
├── TRACKING_v8.md                     # Timeline ejecución
├── resultados/
│   ├── exp8_shaping0.00_spawn0.10_seed42_episodes.csv
│   ├── exp8_shaping0.00_spawn0.10_seed42_metrics.json
│   ├── ...                            # 24 configs × 2 archivos
│   └── experiment_8_summary.json      # Agregado global
├── analisis/
│   ├── anova_shaping_density.json     # Resultados ANOVA 2-way
│   ├── threshold_detection.json       # Modelo segmentado
│   ├── safety_analysis.json           # Métricas tripwires/deaths
│   └── temporal_analysis.json         # Curvas aprendizaje
├── figuras/
│   ├── heatmap_ratio_shaping_density.png
│   ├── scatter_safety_reward.png
│   ├── learning_curves_by_shaping.png
│   └── threshold_regression.png
└── reportes/
    └── REPORTE_FINAL_v8.md            # Post-ejecución
```

---

## 🎓 Conexión Teórica TUI

### Régimen de Aplicabilidad

v7 demostró un **límite inferior**: cuando shaping es débil, TUI no predice gradientes.

v8 busca **límite superior**: ¿existe un punto donde shaping es "demasiado fuerte" y contraproducente?

**Marco conceptual**:
```
Shaping débil (s<0.25):   Régimen de saturación → paridad
Shaping moderado (s≈0.5): Zona Goldilocks → ventaja PGF óptima?
Shaping fuerte (s=1.0):   Coste alto → ventaja solo en abundancia?
```

### Predicción TUI Ampliada

> "La inteligencia prudente (PGF) ofrece ventaja adaptativa **solo cuando**:
> 1. **Riesgo efectivo es significativo** (shaping s ≥ 0.5)
> 2. **Recursos suficientes** para exploración segura (densidad ≥ 0.15)
> 3. **Presión selectiva moderada** (ni demasiado dura ni demasiado fácil)"

v8 testa puntos (1) y (2).

---

## 🔄 Iteración con v7

### Qué se Mantiene (Estabilidad)

✅ Entorno: `ResourceDensityEnv` (environment_v2.py)  
✅ Grid: 4×4  
✅ Arquitectura: DQN (2×64 hidden)  
✅ Hiperparámetros: lr=0.001, γ=0.95, ε decay 0.995  
✅ Seeds: {42, 123, 456}  
✅ Seeding completo: random + numpy + torch  
✅ Anti-camping fix: `done=True` al goal  
✅ Spawn uniforme: `random.shuffle()`

### Qué Cambia (Innovación)

🔄 **Shaping parametrizado**: Baselines × Scale (no hardcoded)  
🔄 **Economía fija**: Solo Balanced (eliminar confundente)  
🔄 **Densidades**: Solo {0.10, 0.25} (contraste escasez/abundancia)  
🔄 **Métricas duales**: reward_env + reward_shaped  
🔄 **Seguridad registrada**: tripwires, deaths, resources  
🔄 **Análisis temporal**: Por tramos exploración/convergencia/estabilidad

---

## 📚 Referencias

- **v7 Report**: [`REPORTE_FINAL_v7.md`](../pgf_v7/reportes/REPORTE_FINAL_v7.md)
- **v7 Preregistro**: [`PREREGISTRO_v7.md`](../pgf_v7/PREREGISTRO_v7.md)
- **Peer Review**: Codex AI Review (3 dic 2025) - Sección "Insuficiencia de Señal"
- **TUI Theory**: `docs/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md`

---

## 🚀 Timeline Planeada

| Fase | Actividad | Duración | Status |
|------|-----------|----------|--------|
| **Diseño** | README + PREREGISTRO | 1 hora | 🟡 EN CURSO |
| **Implementación** | Modificar runner con SHAPING_SCALE | 30 min | ⏳ PENDIENTE |
| **Validación** | Test mode (3 configs, 10 eps/agente) | 5 min | ⏳ PENDIENTE |
| **Ejecución** | 24 configs × 600 eps | 10-12 min | ⏳ PENDIENTE |
| **Análisis** | ANOVA, threshold, figuras | 15 min | ⏳ PENDIENTE |
| **Reporte** | REPORTE_FINAL_v8.md | 2 horas | ⏳ PENDIENTE |

**Fecha estimada finalización**: 3-4 de diciembre de 2025

---

## ⚠️ Riesgos y Mitigaciones

### Riesgo 1: Convergencia Persiste (s=1.0 no suficiente)

**Probabilidad**: Media  
**Impacto**: Alto (refuta H8.1, activa Fase 2)  
**Mitigación**: 
- **Protocolo preregistrado**: Activar v8.1 con `TRIPWIRE_FATAL=True`
- Muerte instantánea simétrica (ambos agentes) fuerza presión selectiva máxima
- Si v8.1 también falla → Conclusión: Grid 4×4 demasiado simple, pasar a v9 (6×6 u 8×8)

### Riesgo 2: Shaping Fuerte Colapsa Aprendizaje

**Probabilidad**: Baja  
**Impacto**: Medio (PGF no aprende nada, reward→0)  
**Mitigación**: Análisis por tramos detectará si PGF "se rinde". Ajustar balance económico (subir goal_reward a 2.0).

### Riesgo 3: Densidad No Modera (H8.2 refutada)

**Probabilidad**: Media  
**Impacto**: Bajo (resultado científicamente válido)  
**Mitigación**: No es falla del experimento. Documentar que coste de alineación es **independiente** de recursos en este régimen.

---

## 🎯 Salida Esperada

Si v8 tiene éxito, obtendremos:

✅ **Threshold de shaping** donde PGF diverge (s* ≈ 0.5-1.0)  
✅ **Evidencia de coste de alineación** (ratio_env < 95%)  
✅ **Ventaja en seguridad** (tripwires reducidos 30-50%)  
✅ **Moderación por densidad** (o refutación de H8.2)  
✅ **Paper-ready**: "Intensity Matters: Calibrating Reward Shaping for AI Alignment"

Si v8 falla (convergencia persiste):

📊 **Régimen identificado**: Entorno 4×4 + DQN es "demasiado simple"  
🔄 **Pivote necesario**: v9 con grid 6×6 u 8×8, mayor complejidad  
📚 **Contribución**: Delimitar dónde TUI aplica (no es falla de teoría, es boundary condition)

---

**Última actualización**: 3 de diciembre de 2025  
**Próximo paso**: Crear `PREREGISTRO_v8.md` con hipótesis formales
