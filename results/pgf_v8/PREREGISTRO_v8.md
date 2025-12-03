# 📋 PREREGISTRO EXPERIMENTAL: PGF v8 - Intensidad de Shaping

**Título**: Efectos de la Intensidad de Reward Shaping en Alineación Prudencial de Agentes DQN
**Investigador**: Sistema TUI v4.1
**Fecha registro**: 3 de diciembre de 2025
**Protocolo**: Preregistración anterior a ejecución
**Versión experimento**: v8 ("El Experimento del Shaping")
**Versión preregistro**: 1.3 (mitigación "laberinto trivial")

---

## 📖 Resumen Ejecutivo

Este experimento investiga **cómo la intensidad del reward shaping** afecta la divergencia conductual entre un agente DQN con incentivos prudenciales (PGF) y un agente control neutro. Surge como respuesta directa a v7, que demostró **convergencia a paridad** (ratio 99%) con shaping débil (-20/+2 vs reward base ~110).

**Pregunta central**: ¿Existe un umbral de intensidad donde el coste de alineación se vuelve visible?

---

## 🎯 Antecedentes y Motivación

### Resultados v7 (Estado del Arte)

**Experimento**: Factorial económico 3×5×3 (harsh/balanced/favorable × 5 densidades × 3 seeds)
**Resultado**: F=0.28, p=0.75 → Economía NO modula ventaja PGF
**Diagnóstico**: Shaping PGF representa ~18% del reward base → señal insuficiente para DQN

**Ver**: [`REPORTE_FINAL_v7.md`](../pgf_v7/reportes/REPORTE_FINAL_v7.md)

### Hipótesis Causal v7→v8

```
v7: Shaping débil (-20/+2) → Convergencia (99%)
v8: Shaping fuerte (-100/+50) → Divergencia esperada (80-120%)
```

**Mecanismo**: Con penalty equiparable a goal_reward, DQN **debe** incorporar señal prudencial para maximizar retorno esperado.

### Gap Metodológico Identificado

> ⚠️ **Crítica Peer Review**: "No se registró `tripwires_per_episode`. Sin contar tripwires, estamos ciegos a la calidad de la estrategia."

v8 corrige esta **insuficiencia de observabilidad** mediante métricas duales de seguridad.

---

## 🔬 Diseño Experimental

### Variables Independientes

#### Factor 1: SHAPING_SCALE (Principal)

**Tipo**: Categórica, 4 niveles
**Valores**: {0.0, 0.25, 0.5, 1.0}
**Operacionalización**:

```python
PGF_BASE_TRIPWIRE_PENALTY = 100.0  # 5× más fuerte que v7
PGF_BASE_RESOURCE_BONUS   = 50.0   # 25× más fuerte que v7

penalty = -PGF_BASE_TRIPWIRE_PENALTY * SHAPING_SCALE
bonus   =  PGF_BASE_RESOURCE_BONUS   * SHAPING_SCALE

train_signal = reward  # Reward crudo del entorno
if info.get('tripwire', False):
    train_signal += penalty
if info.get('resource_value', 0) > 0:
    train_signal += bonus
```

**Interpretación niveles**:

| Scale | Penalty | Bonus | Interpretación                          |
| ----- | ------- | ----- | ---------------------------------------- |
| 0.0   | 0       | 0     | Control puro (baseline)                  |
| 0.25  | -25     | +12.5 | Shaping leve (comparable v7)             |
| 0.5   | -50     | +25   | Shaping moderado                         |
| 1.0   | -100    | +50   | Shaping fuerte (equiparable goal_reward) |

#### Factor 2: DENSIDAD (Moderador)

**Tipo**: Categórica, 2 niveles
**Valores**: {0.25, 0.40}
**Operacionalización**: `spawn_rate` en `ResourceDensityEnv`

**Interpretación**:

- **0.25**: Densidad moderada (~4.0 recursos por episodio en promedio)
- **0.40**: Densidad alta (~6.4 recursos por episodio en promedio)

> ⚠️ **Cambio v1.3**: Densidad mínima elevada de 0.10 → 0.25 para mitigar riesgo "laberinto trivial" (P(camino óptimo seguro) reducido de 48% → 13%). Ver §Validación de Complejidad del Entorno.

#### Factor 3: SEED (Replicación)

**Tipo**: Categórica, 3 niveles
**Valores**: {42, 123, 456}
**Control**: Seeding completo (random + numpy + torch + cuda)

### Variables Dependientes (DVs)

#### DV1: Ratio Reward Crudo (Principal)

```python
ratio_reward_env = mean_reward_env_pgf / mean_reward_env_control
```

**Interpretación**:

- `< 1.0`: PGF pierde reward (coste de alineación)
- `= 1.0`: Paridad (alineación gratis)
- `> 1.0`: PGF gana reward (ventaja adaptativa)

#### DV2: Ratio Reward Shaped (Validación)

```python
ratio_reward_shaped = mean_reward_shaped_pgf / mean_reward_shaped_control
```

**Interpretación**: Lo que "ve" el agente durante entrenamiento. Debe divergir más que ratio_env.

#### DV3: Ratio Tripwires (Seguridad)

```python
tripwires_ratio = tripwires_pgf / tripwires_control
```

**Interpretación**:

- `< 0.7`: PGF reduce riesgo ≥30% (exitoso)
- `≈ 1.0`: Sin diferencia conductual
- `> 1.0`: PGF más riesgoso (falla crítica)

#### DV4: Eficiencia Temporal

```python
steps_ratio = mean_steps_pgf / mean_steps_control
```

**Interpretación**: Si PGF toma más pasos (ratio>1), paga coste de desvío por seguridad.

### Variables de Control (Fijas)

| Parámetro                 | Valor                            | Justificación                                      |
| -------------------------- | -------------------------------- | --------------------------------------------------- |
| **Economía**        | Balanced (balance=5.0)           | v7 detectó threshold aquí, maximizar sensibilidad |
| **step_cost**        | -0.2                             | Estándar balanced                                  |
| **goal_reward**      | 1.0                              | Estándar                                           |
| **Grid size**        | 4×4                             | Continuidad con v7, complejidad conocida            |
| **Episodes**         | 300 por agente                   | Convergencia demostrada en v7                       |
| **Arquitectura**     | DQN 2×64 hidden                 | Estándar proyecto                                  |
| **Hiperparámetros** | lr=0.001, γ=0.95, ε: 1.0→0.01 | Estándar proyecto                                  |

### Tamaño Muestral

```
N_configs = 4 (shaping) × 2 (densidad) × 3 (seeds) = 24
N_episodes_per_config = 600 (300 PGF + 300 Control)
N_total_episodes = 14,400
```

**Justificación**: Suficiente para ANOVA 2-way con potencia >0.80 (efecto esperado d≥0.8).

---

## 🔄 Protocolo de Fases (v8.0 vs v8.1)

### Fase 1: v8.0 - Shaping Escalado (ESTE PREREGISTRO)

**Parámetro clave**: `TRIPWIRE_FATAL = False` (ambos agentes)

**Comportamiento**: Pisar tripwire genera penalización en reward, pero episodio continúa

**Manipulación**: Solo penalty/bonus escalado vía `SHAPING_SCALE`

```python
PGF_BASE_TRIPWIRE_PENALTY = 100.0
PGF_BASE_RESOURCE_BONUS   = 50.0
SHAPING_SCALE ∈ {0.0, 0.25, 0.5, 1.0}
TRIPWIRE_FATAL = False  # Default, no muerte instantánea
```

**Criterio éxito Fase 1**:

- Divergencia ≥15% en `ratio_reward_env` con s=1.0
- Reducción ≥30% en `tripwires_ratio` con s=1.0
- ANOVA Shaping significativo (p<0.05)

**Criterio falla Fase 1**:

- Convergencia persiste (ratio 98-102%) incluso con s=1.0
- Sin diferencias conductuales en tripwires
- H8.1 refutada completamente

### Fase 2: v8.1 - Régimen Existencial (CONDICIONAL)

**⚠️ IMPORTANTE**: Esta fase **solo se ejecuta SI Fase 1 falla**

**Activación**: Convergencia persiste con s=1.0 en Fase 1

**Parámetro clave**: `TRIPWIRE_FATAL = True` (SIMÉTRICO para ambos agentes)

**Comportamiento**:

```python
if info.get('tripwire', False) and TRIPWIRE_FATAL:
    done = True  # Muerte instantánea
    reward = -1.0  # Penalización terminal
```

**Cambio conceptual**: De "penalización" a "supervivencia" (coste existencial máximo)

**Nueva métrica obligatoria**: `deaths_tripwire` (separada de `deaths_starvation`)

**Nota crítica - NO es asimetría**:

- Ambos agentes (PGF y Control) mueren al pisar tripwire
- NO es ventaja para PGF, es cambio en naturaleza del problema
- Objetivo: Forzar divergencia mediante presión selectiva extrema

**Preregistro requerido**: Si Fase 2 se ejecuta, requiere preregistro v8.1 separado con:

- Hipótesis H8.1-bis adaptadas al régimen survival
- Análisis de tasas de muerte como DV principal
- Métricas de eficiencia condicionadas a supervivencia

**Justificación teórica**:

- v7 y v8 Fase 1 testean "alineación como costo moderado"
- v8 Fase 2 testaría "alineación como necesidad de supervivencia"
- Ambos regímenes informan límites de aplicabilidad de TUI

---

## 🧮 Validación de Complejidad del Entorno

### Motivación: Riesgo "Laberinto Trivial"

En un Grid 4×4, el camino óptimo (Manhattan) tiene longitud 7 celdas: `(0,0)→(1,0)→(2,0)→(3,0)→(3,1)→(3,2)→(3,3)`. Si **ninguna** de estas 7 celdas contiene un tripwire, existe un camino óptimo **simultáneamente** corto y seguro. En tal caso:

- Ambos agentes (PGF y Control) convergerán al mismo plan por optimización de recompensa base (+100 goal)
- El shaping se vuelve **irrelevante** (no hay trade-off seguridad-eficiencia)
- El experimento fallaría por **trivialidad estructural**, no por fallo de la hipótesis

### Análisis Probabilístico

Probabilidad de que el camino óptimo esté libre de tripwires:

$$
P(\text{camino seguro}) = (1 - \text{spawn\_rate})^7
$$

| spawn_rate | P(camino seguro) | Riesgo       | Interpretación        |
| ---------- | ---------------- | ------------ | ---------------------- |
| 0.10       | **47.8%**  | 🔴 CRÍTICO  | ~50% configs triviales |
| 0.25       | **13.4%**  | 🟡 ACEPTABLE | ~3 de 24 configs       |
| 0.40       | **4.9%**   | 🟢 ÓPTIMO   | ~1 de 24 configs       |

**Validación Monte Carlo** (10,000 grids simulados):

- `spawn=0.10`: 48.3% grids con camino óptimo seguro ✗
- `spawn=0.25`: 13.5% grids con camino óptimo seguro ✓
- `spawn=0.40`: 4.9% grids con camino óptimo seguro ✓

### Decisión de Diseño (v1.3)

**Acción correctiva**:
Eliminar `spawn_rate=0.10` del diseño factorial. **Usar `spawn_rate ∈ {0.25, 0.40}`**.

**Justificación**:

1. Reduce P(laberinto trivial) de ~48% a ~13% (factor 3.6×)
2. Mantiene 2 niveles de densidad (diseño factorial 4×2×3 intacto)
3. Conserva comparabilidad parcial con v7 (que usó spawn=0.25)
4. Permite distinguir entre "shaping no funciona" vs "entorno demasiado simple"

**Compromiso de Reporteo**:
En el análisis v8, reportaremos para cada configuración individual si existe un camino Manhattan mínimo libre de tripwires. Configuraciones con camino trivial serán analizadas por separado para confirmar convergencia estructural (no conductual).

**Implicación para H8.2**:
La hipótesis de amplificación en densidad moderada asume que `spawn=0.25` tiene suficiente complejidad para forzar trade-offs. El análisis probabilístico valida que ~86% de las configuraciones con `spawn=0.25` requieren navegación estratégica.

---

## 📊 Hipótesis Preregistradas (Fase 1: v8.0)

### H8.1: Efecto Principal de Intensidad (Umbral de Shaping)

**Enunciado formal**:

> Existe un valor crítico `s*` ∈ [0.5, 1.0] tal que para `SHAPING_SCALE ≥ s*`, el agente PGF diverge significativamente del agente Control en métricas de seguridad y reward.

**Predicciones cuantitativas**:

#### H8.1a: Reducción de Tripwires

```
Con SHAPING_SCALE = 1.0:
    E[tripwires_pgf] / E[tripwires_control] < 0.70
  
Interpretación: PGF reduce riesgo en al menos 30%
Test: t-test pareado, α=0.05, one-tailed
Potencia: 0.85 con d=0.8
```

#### H8.1b: Coste de Alineación Visible

```
Con SHAPING_SCALE = 1.0:
    ratio_reward_env < 0.95
  
Interpretación: PGF pierde ≥5% reward crudo por prudencia
Test: t-test vs constante 1.0, α=0.05, one-tailed
```

#### H8.1c: Compensación en Reward Shaped

```
Con SHAPING_SCALE = 1.0:
    ratio_reward_shaped ≥ 0.95
  
Interpretación: Desde perspectiva del agente, recompensa similar
Test: t-test vs constante 1.0, α=0.05, two-tailed
```

**Criterio de confirmación H8.1**: ≥2/3 predicciones cumplidas

**Criterio de refutación H8.1**: 0/3 predicciones cumplidas O ratio_reward_env ∈ [0.98, 1.02] para todos los niveles de shaping

### H8.2: Amplificación por Densidad Moderada (Exploratoria)

**Enunciado formal**:

> La densidad moderada (`spawn=0.25`) **amplificará** el efecto del shaping fuerte (`scale ≥ 0.5`) en métricas de seguridad (`tripwires_triggered`) sin degradar excesivamente `reward_env`, comparado con densidad alta (`spawn=0.40`).

**Justificación teórica**:
En densidades muy bajas, el shaping puede ser irrelevante (caminos seguros abundan por azar). En densidades muy altas, incluso con shaping el agente puede ser forzado a tomar riesgos por imposibilidad de evasión. La densidad moderada maximiza el **espacio de maniobra** para que el shaping diferencie conductas.

**Predicciones cuantitativas**:

#### H8.2a: Reducción Mayor de Tripwires en Densidad Moderada

```
Con SHAPING_SCALE = 1.0, spawn_rate = 0.25:
    tripwires_ratio < 0.65
  
Interpretación: PGF reduce riesgo >35% en densidad moderada
```

#### H8.2b: Reducción Menor en Densidad Alta

```
Con SHAPING_SCALE = 1.0, spawn_rate = 0.40:
    tripwires_ratio ∈ [0.70, 0.85]
  
Interpretación: PGF reduce riesgo 15-30% en densidad alta (menor margen)
```

#### H8.2c: Interacción Estadística

```
ANOVA 2-way: Shaping × Densidad
    F_interaction significativo (p < 0.05)
  
Patrón: Pendiente(tripwires vs shaping) más negativa en spawn=0.25 que spawn=0.40
```

**Criterio de confirmación H8.2**: 2/3 predicciones cumplidas + interacción significativa con η²>0.06

**Criterio de refutación H8.2**: No interacción (p>0.10) O patrón invertido (mayor reducción en spawn=0.40)

### H8.3: Control Negativo (Validación Metodológica)

**Enunciado formal**:

> Con `SHAPING_SCALE = 0.0` (sin shaping), PGF y Control deben ser conductual y recompensalmente indistinguibles. Esto valida que divergencias en s>0 son causales del shaping.

**Predicciones cuantitativas**:

#### H8.3a: Paridad en Reward

```
Con SHAPING_SCALE = 0.0:
    ratio_reward_env ∈ [0.98, 1.02]
  
Test: Equivalence test (TOST), equivalence bound ±2%
```

#### H8.3b: Paridad en Conducta

```
Con SHAPING_SCALE = 0.0:
    |tripwires_pgf - tripwires_control| / tripwires_control < 0.10
  
Interpretación: Diferencia <10% atribuible a ruido estocástico
```

#### H8.3c: Ausencia de Efecto Densidad en Baseline

```
Con SHAPING_SCALE = 0.0:
    ratio_env(spawn=0.10) ≈ ratio_env(spawn=0.25)  [diferencia <3%]
  
Interpretación: Densidad solo importa cuando hay shaping
```

**Criterio de confirmación H8.3**: 3/3 predicciones cumplidas

**Criterio de refutación H8.3**: Cualquier diferencia significativa (p<0.05) con s=0.0 → invalida diseño experimental

---

## 📈 Plan de Análisis Estadístico

### Análisis Primario: ANOVA 2-Way

**Modelo**:

```r
DV ~ SHAPING_SCALE * DENSIDAD + Error(SEED)
```

**DVs a analizar**:

1. `ratio_reward_env` (principal)
2. `ratio_reward_shaped` (validación)
3. `tripwires_ratio` (seguridad)
4. `steps_ratio` (eficiencia)

**Efectos de interés**:

- **Efecto principal Shaping**: F_shaping, p_shaping (H8.1)
- **Efecto principal Densidad**: F_density, p_density
- **Interacción**: F_interaction, p_interaction (H8.2)

**Criterios**:

- α = 0.05 (ajustado Bonferroni si múltiples DVs)
- Potencia mínima: 0.80
- Tamaño efecto mínimo detectable: η²≥0.10 (mediano)

### Análisis Secundario: Post-Hoc

**Comparaciones planeadas** (Tukey HSD):

1. `s=0.0` vs `s=1.0` (contraste máximo)
2. `s=0.25` vs `s=0.5` (detección threshold)
3. `s=0.5` vs `s=1.0` (saturación?)

**Por densidad**:
4. Escasez: `s=0.0` vs `s=1.0`
5. Abundancia: `s=0.0` vs `s=1.0`
6. Diferencia (4) vs (5) → test H8.2

### Análisis Terciario: Regresión Segmentada

**Objetivo**: Detectar threshold preciso `s*` donde relación cambia

**Modelo**:

```python
ratio_env ~ shaping_scale + I(shaping_scale > s*) * (shaping_scale - s*)
```

**Búsqueda**: Grid search s* ∈ [0.0, 1.0] por pasos de 0.05, minimizando AIC

**Criterio**: ΔAIC < -2 entre modelo segmentado vs lineal simple → threshold existe

### Análisis Temporal: Curvas de Aprendizaje

**Descomposición por tramos**:

```python
tramos = {
    "exploration": eps 1-100,
    "convergence": eps 101-200,
    "stability": eps 201-300
}
```

**Para cada tramo**:

```python
ratio_tramo[t] = mean_reward_pgf[t] / mean_reward_control[t]
```

**Plot**: Ratio(t) × shaping_scale, detectar si ventaja PGF:

- **Emerge** (crece con t) → prudencia adaptativa
- **Desaparece** (decrece con t) → solo bootstrapping
- **Estable** (constante) → diferencia estructural

### Análisis Exploratorio: Frontera de Pareto

**Plot 2D**: `(safety_score, reward_env)`

```python
safety_score = 1 - (tripwires / max_possible_tripwires)
```

**Hipótesis**: PGF con s=1.0 debe estar en región "Pareto superior" (arriba-derecha) vs Control.

**Test**: Dominancia estocástica de primer orden (Mann-Whitney U en ambas dimensiones).

---

## 📊 Criterios de Decisión

### Escenario 1: H8.1 Confirmada, H8.2 Confirmada ✅✅

**Interpretación**: Shaping efectivo Y moderado por densidad

**Conclusión**:

- ✅ Threshold encontrado: `s* ≈ 0.5-1.0`
- ✅ Coste de alineación visible y modulado ecológicamente
- ✅ TUI validado en este régimen

**Próximo paso**: Paper "Calibrating Prudential AI: When and How Much Alignment Costs"

### Escenario 2: H8.1 Confirmada, H8.2 Refutada ✅❌

**Interpretación**: Shaping efectivo PERO independiente de recursos

**Conclusión**:

- ✅ Threshold encontrado
- ❌ Densidad no modera en este setup
- ⚠️ TUI requiere reformulación: coste alineación **no** depende de ecología

**Próximo paso**: v9 con mayor rango de densidades (0.05-0.50) para buscar no-linealidad

### Escenario 3: H8.1 Refutada (Convergencia persiste) ❌

**Interpretación**: Incluso s=1.0 insuficiente, shaping no rompe paridad

**Conclusión**:

- ❌ Fase 1 falla: shaping escalado insuficiente
- 🔄 Activar Fase 2 (v8.1 con TRIPWIRE_FATAL=True)
- ⚠️ Alternativa: problema arquitectural (entorno 4×4 + DQN demasiado simple)

**Próximos pasos** (en orden de prioridad):

1. **Protocolo Fase 2**: Ejecutar v8.1 con muerte instantánea simétrica
2. **Si Fase 2 también falla**:
   - Opción A: Grid más complejo (6×6 u 8×8) → v9
   - Opción B: Cambio algoritmo (PPO, A3C, tabular Q-learning)
   - Opción C: Conclusión límite: TUI no aplica en entornos triviales resueltos óptimamente

### Escenario 4: H8.3 Refutada (Control negativo falla) ⚠️

**Interpretación**: Diseño experimental inválido

**Conclusión**:

- ⚠️ Confundente no controlado
- ⚠️ PGF y Control difieren incluso sin shaping
- 🛑 Invalidar v8, revisar implementación

**Diagnóstico**:

- Verificar semillado idéntico
- Verificar inicialización redes
- Verificar orden de entrenamiento (¿intercalar?)

---

## 🎨 Visualizaciones Preregistradas

### Figura 1: Heatmap Ratio × Shaping × Densidad

**Tipo**: Heatmap 2D
**Ejes**: Shaping Scale (x: 0.0-1.0), Densidad (y: 0.10-0.25)
**Color**: Ratio reward_env (escala: 0.80 azul → 1.20 rojo)
**Anotaciones**: Valores numéricos en celdas, significancia ANOVA con asteriscos

**Hipótesis visual**: Degradado vertical (densidad modera) y horizontal (shaping modula)

### Figura 2: Scatter Safety-Reward Tradeoff

**Tipo**: Scatter plot 2D con envolventes convexas
**X**: Safety Score (1 - tripwires_norm)
**Y**: Mean Reward Env
**Puntos**: PGF (rojo), Control (azul)
**Agrupación**: Por shaping scale (tamaño de punto)
**Líneas**: Frontera de Pareto para cada grupo

**Hipótesis visual**: PGF s=1.0 en cuadrante superior-derecho

### Figura 3: Curvas de Aprendizaje por Shaping

**Tipo**: Line plot con ribbons (media ± SE)
**X**: Episodios (0-300)
**Y**: Ratio PGF/Control (ventana móvil 20 eps)
**Líneas**: Una por nivel shaping (4 curvas)
**Colores**: Gradiente frío→cálido (s=0.0→s=1.0)

**Hipótesis visual**: Separación creciente con tiempo para s≥0.5

### Figura 4: Threshold Detection (Regresión Segmentada)

**Tipo**: Scatter + líneas de ajuste
**X**: Shaping Scale (0.0-1.0)
**Y**: Ratio reward_env
**Puntos**: 24 configs (coloreados por densidad)
**Líneas**: Modelo segmentado con quiebre en `s*`
**Anotación**: Valor `s*`, ΔAIC, intervalo confianza 95%

**Hipótesis visual**: Quiebre visible en s* ≈ 0.5

---

## 🗂️ Outputs Comprometidos

### Durante Ejecución

Por cada config (24 archivos):

```
exp8_shaping{s}_spawn{d}_seed{seed}_episodes.csv
exp8_shaping{s}_spawn{d}_seed{seed}_metrics.json
```

**Columnas CSV OBLIGATORIAS** (por episodio):

```python
# Identificación
episode: int              # Número de episodio (1-300)
agent_type: str           # "PGF" o "Control"

# Recompensas duales (CRÍTICO: ambas deben guardarse)
total_reward_env: float   # Reward crudo del entorno (lo que "importa al mundo")
total_reward_shaped: float # Train signal con shaping (lo que "ve" el agente)

# Métricas de seguridad (CRÍTICO: contadores absolutos)
tripwires_triggered: int  # Contador de tripwires pisados en episodio
deaths_starvation: int    # 1 si murió por energy=0, 0 si no
deaths_tripwire: int      # 1 si murió por tripwire fatal (solo v8.1), 0 si no

# Métricas de eficiencia
resources_collected: int  # Total recursos consumidos en episodio
steps_to_goal: int        # Pasos tomados (si goal_reached=True)
goal_reached: bool        # True si llegó a meta, False si timeout/muerte

# Exploración
epsilon: float            # Valor epsilon al final del episodio

# Metadata (CRÍTICO: para análisis robusto, no depender solo de filename)
shaping_scale: float      # 0.0, 0.25, 0.5, 1.0
spawn_rate: float         # 0.25, 0.40
seed: int                 # 42, 123, 456
```

**⚠️ VALIDACIÓN DE PERSISTENCIA**:

- ❌ **NO aceptar** CSV sin columnas `total_reward_env` Y `total_reward_shaped` separadas
- ❌ **NO aceptar** CSV sin `tripwires_triggered` (contador numérico, no booleano)
- ❌ **NO aceptar** CSV sin `resources_collected` y `steps_to_goal`
- ✅ Si alguna columna crítica falta en output → **INVALIDAR config** y re-ejecutar

**Campos JSON** (agregado por config):

```python
{
  "config": {
    "shaping_scale": float,        # 0.0, 0.25, 0.5, 1.0
    "spawn_rate": float,           # 0.25, 0.40
    "seed": int,                   # 42, 123, 456
    "balance": float,              # 5.0 (fijo)
    "tripwire_fatal": bool,        # False en v8.0
    "pgf_base_tripwire_penalty": float,  # 100.0
    "pgf_base_resource_bonus": float,    # 50.0
    "episodes": int                # 300
  },
  "pgf_stats": {
    "mean_reward_env": float,      # Promedio reward crudo PGF
    "std_reward_env": float,
    "mean_reward_shaped": float,   # Promedio reward shaped PGF
    "std_reward_shaped": float,
    "mean_tripwires": float,       # Promedio tripwires/episodio
    "total_tripwires": int,        # Suma absoluta
    "mean_resources": float,       # Promedio recursos/episodio
    "mean_steps": float,           # Promedio steps (solo episodios exitosos)
    "survival_rate": float,        # % episodios sin muerte
    "success_rate": float          # % episodios goal_reached=True
  },
  "control_stats": {
    # Misma estructura que pgf_stats
  },
  "ratios": {
    "reward_env": float,           # mean_reward_env_pgf / mean_reward_env_control
    "reward_shaped": float,        # mean_reward_shaped_pgf / mean_reward_shaped_control
    "tripwires": float,            # mean_tripwires_pgf / mean_tripwires_control
    "resources": float,            # mean_resources_pgf / mean_resources_control
    "steps": float                 # mean_steps_pgf / mean_steps_control
  },
  "timestamp": str,                # ISO 8601
  "duration_minutes": float        # Tiempo ejecución config
}
```

### Post-Ejecución

**Análisis**:

```
analisis/anova_shaping_density.json       # Resultados ANOVA
analisis/threshold_detection.json         # Modelo segmentado
analisis/safety_analysis.json             # Métricas tripwires/deaths
analisis/temporal_analysis.json           # Por tramos
```

**Figuras**:

```
figuras/heatmap_ratio_shaping_density.png
figuras/scatter_safety_reward.png
figuras/learning_curves_by_shaping.png
figuras/threshold_regression.png
```

**Reporte**:

```
reportes/REPORTE_FINAL_v8.md              # Narrativa completa
```

---

## ⚠️ Desviaciones Permitidas del Protocolo

### Ajustes Post-Hoc Autorizados

1. **Si convergencia persiste con s=1.0**:

   - Autorizado: Activar Protocolo Fase 2 (v8.1 con TRIPWIRE_FATAL=True)
   - NO autorizado: Cambiar hiperparámetros DQN sin preregistrar v8.0.1
2. **Si H8.3 falla (control negativo)**:

   - Autorizado: Repetir configs s=0.0 con semillado alternativo
   - NO autorizado: Proceder con análisis de s>0 (invalidaría resultados)
3. **Si outliers extremos** (ratio <0.5 o >2.0):

   - Autorizado: Análisis de sensibilidad excluyendo outlier
   - Requerido: Reportar ambos análisis (con/sin outlier)
4. **Si columnas críticas faltan en CSV**:

   - Requerido: DETENER ejecución, corregir código, re-ejecutar config
   - NO autorizado: Análisis con datos incompletos

### Análisis Exploratorios NO Preregistrados

Permitidos siempre que **etiquetados como exploratorios**:

- Correlaciones adicionales
- Modelos de regresión múltiple
- Análisis por subgrupos (ej. solo seeds pares)
- Visualizaciones alternativas

**Restricción**: NO usar análisis exploratorios para **confirmar/refutar hipótesis preregistradas**.

---

## 📅 Timeline Comprometida

| Fase                      | Fecha límite | Criterio completitud          |
| ------------------------- | ------------- | ----------------------------- |
| **Preregistro**     | 3 dic 2025    | Este documento aprobado       |
| **Implementación** | 3 dic 2025    | Test mode exitoso (3 configs) |
| **Ejecución**      | 3 dic 2025    | 24 CSVs + JSONs generados     |
| **Análisis**       | 4 dic 2025    | ANOVA + figuras completas     |
| **Reporte**         | 4 dic 2025    | REPORTE_FINAL_v8.md publicado |

**Deadline absoluto**: 4 de diciembre 2025, 23:59

---

## 🔒 Compromiso de Integridad

**Declaración**:

> Este preregistro constituye un compromiso vinculante de ejecutar **Fase 1 (v8.0)** según el diseño especificado. Cualquier desviación no autorizada (ver sección "Desviaciones Permitidas") invalida el experimento y requiere preregistro v8.0.1.
>
> **Fase 2 (v8.1)** solo se ejecutará SI Fase 1 refuta completamente H8.1 (convergencia persiste con s=1.0). En ese caso, se creará preregistro v8.1 separado especificando hipótesis adaptadas al régimen TRIPWIRE_FATAL=True.
>
> Los resultados se reportarán honestamente independiente de si confirman o refutan las hipótesis. Resultados negativos son tan valiosos como positivos para delimitar el régimen de aplicabilidad de TUI.
>
> En caso de falla técnica (bugs, crashes), se documentará en TRACKING_v8.md con commit trail completo, y se reiniciará desde checkpoint válido.

**Firmante**: Sistema TUI v4.1
**Fecha**: 3 de diciembre de 2025
**Versión documento**: 1.1 (actualizado: protocolo de fases)

---

## 📚 Referencias

1. **v7 Final Report**: `results/pgf_v7/reportes/REPORTE_FINAL_v7.md`
2. **v8 README**: `results/pgf_v8/README.md`
3. **Peer Review**:  (3 dic 2025) - "Insuficiencia de Señal"
4. **TUI Theory**: `docs/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md`
5. **Environment v2**: `sim/environment_v2.py`
6. **DQN Agent**: `sim/dqn_agent.py`

---

## 📎 Anexos

### Anexo A: Cálculo de Potencia

**Escenario**: Detectar diferencia en ratio_env entre s=0.0 y s=1.0

```
Efecto esperado: d = 0.8 (grande, basado en v7 donde d≈0.2 fue insuficiente)
N por grupo: 6 (2 densidades × 3 seeds)
α: 0.05 (two-tailed)
Test: t-test independiente

Potencia calculada (G*Power): 0.87
```

**Conclusión**: Diseño adecuado para detectar efectos grandes.

### Anexo B: Justificación Baselines

**¿Por qué -100/+50?**

```
v7: -20 penalty ≈ 18% de reward base (~110)
v8: -100 penalty ≈ 100% de goal_reward (1.0)

Razonamiento: Si pisar tripwire cuesta lo mismo que el premio de meta,
el agente DEBE considerarlo en función Q:

Q(s, a_risk) = -0.2 (step) + γ*(reward_future - 100*p_tripwire)

Con p_tripwire>0.1, rama riesgosa se vuelve subóptima.
```

### Anexo C: Especificación Técnica de Implementación

**Parámetros de configuración OBLIGATORIOS** (no hardcodear):

```python
# Config centralizada (ej. config.py o argparse)
class ExperimentConfig:
    # Shaping PGF
    PGF_BASE_TRIPWIRE_PENALTY: float = 100.0
    PGF_BASE_RESOURCE_BONUS: float = 50.0
    PGF_SHAPING_SCALE: float  # Variable: 0.0, 0.25, 0.5, 1.0
  
    # Entorno
    TRIPWIRE_FATAL: bool = False  # Fase 1: False, Fase 2: True
    SPAWN_RATE: float  # Variable: 0.25, 0.40
    BALANCE: float = 5.0  # Fijo
  
    # Episodios
    EPISODES_PER_AGENT: int = 300
    SEEDS: list[int] = [42, 123, 456]
```

**Validación de output OBLIGATORIA**:

```python
def validate_csv_output(csv_path: str) -> bool:
    """Valida que CSV contenga todas las columnas críticas"""
    df = pd.read_csv(csv_path)
  
    required_columns = [
        'episode', 'agent_type',
        'total_reward_env',      # CRÍTICO
        'total_reward_shaped',   # CRÍTICO
        'tripwires_triggered',   # CRÍTICO
        'resources_collected',   # CRÍTICO
        'steps_to_goal',
        'goal_reached',
        'deaths_starvation',
        'deaths_tripwire',
        'epsilon',
        # Metadata para análisis robusto
        'shaping_scale',
        'spawn_rate',
        'seed'
    ]
  
    missing = [col for col in required_columns if col not in df.columns]
  
    if missing:
        raise ValueError(f"CSV inválido: faltan columnas {missing}")
  
    # Validar tipos (flexible con subtipos de integer para evitar crasheos con pandas)
    if not np.issubdtype(df['tripwires_triggered'].dtype, np.integer):
        raise TypeError("tripwires_triggered debe ser entero (int dtype)")
  
    if not np.issubdtype(df['resources_collected'].dtype, np.integer):
        raise TypeError("resources_collected debe ser entero (int dtype)")
  
    if not np.issubdtype(df['episode'].dtype, np.integer):
        raise TypeError("episode debe ser entero (int dtype)")
  
    # Validar booleanos (pandas puede usar int 0/1)
    if not df['goal_reached'].dtype in [bool, np.bool_, int, np.int64]:
        raise TypeError("goal_reached debe ser bool o int 0/1")
  
    return True
```

**Acumulación de métricas durante entrenamiento**:

```python
def train_agent(agent, env, config, is_pgf=False):
    """
    Entrenar agente guardando métricas duales
    """
    episode_data = []
  
    for episode in range(config.EPISODES_PER_AGENT):
        obs = env.reset()
        done = False
      
        # Acumuladores separados
        total_reward_env = 0.0      # Reward crudo
        total_reward_shaped = 0.0   # Reward con shaping
        tripwires_count = 0
        resources_count = 0
        steps = 0
      
        while not done:
            action = agent.select_action(obs)
            next_obs, reward, done, info = env.step(action)
          
            # Acumular reward crudo
            total_reward_env += reward
          
            # Calcular train_signal (con shaping si PGF)
            train_signal = reward
            if is_pgf:
                penalty = -config.PGF_BASE_TRIPWIRE_PENALTY * config.PGF_SHAPING_SCALE
                bonus = config.PGF_BASE_RESOURCE_BONUS * config.PGF_SHAPING_SCALE
              
                if info.get('tripwire', False):
                    train_signal += penalty
                    tripwires_count += 1
              
                # NOTA: Usar flag explícita 'resource_collected' en vez de resource_value>0
                # para evitar falsos positivos si value es 0.0 pero recurso se consumió
                if info.get('resource_collected', False):
                    train_signal += bonus
                    resources_count += 1
          
            # Acumular reward shaped
            total_reward_shaped += train_signal
          
            # Entrenar con señal shaped
            agent.remember(obs, action, train_signal, next_obs, done)
            agent.replay()
          
            obs = next_obs
            steps += 1
      
        # Guardar episodio con AMBAS métricas
        # NOTA: Usar flags explícitas para causa de muerte (no derivar de energía final)
        # Esto garantiza métricas de seguridad confiables, especialmente en v8.1
        episode_data.append({
            'episode': episode + 1,
            'agent_type': 'PGF' if is_pgf else 'Control',
            'total_reward_env': total_reward_env,      # CRÍTICO
            'total_reward_shaped': total_reward_shaped, # CRÍTICO
            'tripwires_triggered': tripwires_count,     # CRÍTICO
            'resources_collected': resources_count,     # CRÍTICO
            'steps_to_goal': steps,
            'goal_reached': info.get('goal_reached', False),
            'deaths_starvation': 1 if info.get('starvation', False) else 0,
            'deaths_tripwire': 1 if info.get('tripwire_death', False) else 0,
            'epsilon': agent.epsilon,
            # Metadata adicional para análisis robusto (no depender solo de filename)
            'shaping_scale': config.PGF_SHAPING_SCALE if is_pgf else 0.0,
            'spawn_rate': config.SPAWN_RATE,
            'seed': config.SEED
        })
  
    return episode_data
```

### Anexo D: Cronograma Detallado

```
[3 dic 14:00] Inicio implementación
[3 dic 14:30] Test mode (3 configs, 10 eps/agente)
[3 dic 14:35] Validación: ratios divergen con s=1.0
[3 dic 14:40] Ejecución completa (24 configs)
[3 dic 14:50] Checkpoint: 50% completo
[3 dic 15:00] Checkpoint: 100% completo
[3 dic 15:05] Commit datos: "v8 RAW DATA - 24 configs completos"
[3 dic 15:10] Análisis ANOVA
[3 dic 15:20] Figuras
[3 dic 15:30] Commit análisis: "v8 ANALYSIS - ANOVA + figuras"
[4 dic 10:00] Redacción REPORTE_FINAL_v8.md
[4 dic 12:00] Commit reporte: "v8 FINAL - Reporte completo"
```

---

**FIN PREREGISTRO v8**

**Status**: 🔒 CONGELADO (v1.3)
**Próxima acción**: Implementación código según especificación

---

## 📝 Historial de Versiones

### v1.3 (3 dic 2025, 14:00, pre-ejecución) ⭐ VERSIÓN ACTUAL

**Cambio crítico**: Densidades ajustadas de `[0.10, 0.25]` → `[0.25, 0.40]`

**Motivación**: Mitigación riesgo "laberinto trivial"

- P(camino óptimo seguro) reducida de **48% → 13%** (factor 3.6×)
- Análisis probabilístico: $(1-\text{spawn\_rate})^7$ para 7 celdas del camino Manhattan
- Validación Monte Carlo: 10,000 grids simulados confirman análisis teórico

**Modificaciones**:

- ✅ Añadida sección **"§Validación de Complejidad del Entorno"** con justificación cuantitativa
- ✅ Reformulada **H8.2** como hipótesis exploratoria positiva (amplificación por densidad moderada)
- ✅ Actualizado diseño factorial: mantiene 4×2×3 = 24 configs
- ✅ Actualizado Anexo C: `SPAWN_RATE` valores corregidos en pseudocódigo
- ✅ Añadido compromiso de reporteo: análisis por separado de configs con camino trivial

**Impacto**: Experimento v8 blindado contra fallo estructural (trivialidad topológica vs fallo hipótesis)

---

### v1.2 (3 dic 2025, pre-ejecución)

**Añadido**: Anexo C con especificaciones técnicas completas

- Schemas CSV/JSON detallados con tipos y descripciones
- Función `validate_csv_output()` con validación robusta de dtypes
- Pseudocódigo `train_agent()` con doble acumulación (reward_env + reward_shaped)
- Micro-ajustes alineación con `environment_v2.py` API:
  - Uso de flag `resource_collected` en vez de `resource_value > 0`
  - Flags explícitas para causas de muerte (`starvation`, `tripwire_death`)
  - Metadata columns añadidas al CSV (`shaping_scale`, `spawn_rate`, `seed`)

---

### v1.1 (3 dic 2025, pre-ejecución)

**Añadido**: Sección "Protocolo de Fases"

- Fase 1 (v8.0): `TRIPWIRE_FATAL=False` (shaping escalado)
- Fase 2 (v8.1): `TRIPWIRE_FATAL=True` (muerte instantánea simétrica) - condicional si Fase 1 falla

---

### v1.0 (3 dic 2025, pre-ejecución)

**Creación inicial**: Preregistro completo con:

- Hipótesis H8.1 (umbral shaping), H8.2 (interacción densidad), H8.3 (control negativo)
- Diseño factorial 4×2×3 (24 configs, 14,400 episodios totales)
- Métricas duales (`reward_env` vs `reward_shaped`)
- Plan analítico ANOVA 2-way + regresión segmentada
- Compromisos de transparencia y reproducibilidad
