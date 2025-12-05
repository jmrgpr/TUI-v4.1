# 📋 PREREGISTRO EXPERIMENTAL - PGF v7

**Título**: Experimento 4 - Economía Factorial: Condiciones de Emergencia de la Ventaja de Alineación
**Investigador principal**: @jmrgpr
**Proyecto**: TUI v4.2 - Teoría Unificada de la Inteligencia
**Fecha preregistro**: 3 de diciembre de 2025, 10:00 AM
**Commit**: `3c7d6a8` (estructura inicial v7)
**Precedente**: PGF v6 (Goldilocks refutada en economía harsh, commit `9fbd049`)

---

## 1. ANTECEDENTES Y JUSTIFICACIÓN

### 1.1 Hallazgos de PGF v6

El experimento v6 validó rigurosamente la **Hipótesis Goldilocks** (ventaja de alineación sigue parábola invertida con máximo en densidad intermedia) bajo condiciones de **economía endurecida**:

**Configuración v6**:

- `step_cost=-0.3`, `resource_reward=1.0`, `max_resources=3` → balance económico = 3.33
- 5 densidades × 5 seeds × 600 episodios = 15,000 episodios validados

**Resultado v6**: ❌ **Hipótesis refutada** (1/5 criterios preregistrados cumplidos)

- Modelo constante ganador (AIC=100.49)
- Ratio PGF/Control ≈ 99.5% ± 5% en todo el rango D=0.05-0.40
- Correlación débil no significativa (r=0.21, p=0.32)

**Interpretación**: En régimen de **supervivencia extrema** (balance económico bajo), las diferencias de inteligencia/prudencia se **aplanan** → PGF ≈ Control. La alineación no muestra ventajas medibles en este régimen.

### 1.2 Limitaciones Identificadas en v6

1. **Sesgo espacial de spawn** (CRÍTICO): Loop determinista favorece top-left → D_effective 74% menor que nominal
2. **Seeds incompletos** (IMPORTANTE): Solo NumPy seeded → inicialización DQN no reproducible
3. **Asimetría epsilon decay** (MENOR): PGF entrena primero → Control empieza con exploración fresca
4. **Economía única**: v6 probó solo 1 balance (harsh) → no sabemos si Goldilocks emerge en otros regímenes

### 1.3 Pregunta de Investigación v7

> **¿La hipótesis Goldilocks es una ley universal o requiere condiciones económicas específicas (slack económico) para emerger?**

**Motivación teórica**: Si la prudencia es análoga a un "seguro", solo vale la pena cuando:

1. Hay algo que proteger (balance > threshold)
2. Los riesgos son significativos (complejidad > baseline)
3. El horizonte permite capitalizar la inversión (horizonte >> τ_convergencia)

v6 violó condición (1) → seguro no pagó. v7 explorará regímenes donde (1) se cumple.

---

## 2. HIPÓTESIS PREREGISTRADAS

### H7.1 - Economía Modula Goldilocks (PRINCIPAL)

**Enunciado formal**:

```
La relación ratio(D) varía según el balance económico:

Si economía = "Favorable" (balance ≥ 10.0):
    → ratio(D) exhibe forma NO LINEAL (cuadrática/log/exp mejor que constante)
    → Cumple ≥3 de los 5 criterios Goldilocks de v6
    → Máximo observable en D* ∈ [0.7, 1.5] (parábola invertida preferida)

Elif economía = "Balanced" (5.0 ≤ balance < 10.0):
    → ratio(D) muestra relación positiva débil (lineal o log)
    → Correlación |r| > 0.3, p < 0.05

Elif economía = "Harsh" (balance < 5.0):
    → ratio(D) ≈ constante (replicar v6)
    → Modelo constante gana (ΔAIC < 0 vs otros)
```

**Criterios de éxito** (se considera confirmada si se cumplen ≥2/3):

1. ✅ ANOVA 2-way muestra interacción significativa Economía×Densidad (F > 3.0, p < 0.05)
2. ✅ Modelo NO constante gana en subset "Favorable" (ΔAIC < -4 vs constante)
3. ✅ Ratio máximo en "Favorable" > 110% (IC95% excluye 100%)

**Métricas**:

- Variable respuesta: `ratio_pgf_control = mean_reward_pgf / mean_reward_control`
- Predictores: `economía` (factor 3 niveles), `densidad` (continua 0.05-0.40)
- Método: ANOVA 2-way con interacción, seguido de análisis de efectos simples por economía

---

### H7.2 - Umbral Económico Crítico (SECUNDARIA)

**Enunciado**:

```
Existe threshold_balance (hipótesis: 5.0 ± 1.0) tal que:
    Si balance > threshold:
        Ventaja_PGF emerge (ratio - 100% > 5%, IC95% > 0%)
    Else:
        Ventaja_PGF ≈ 0 (ratio en [95%, 105%])
```

**Criterios de éxito**:

- ✅ Regresión segmentada (piecewise linear) con breakpoint estimado:
  - AIC_segmentada < AIC_lineal simple - 4
  - Breakpoint estimado ∈ [4.0, 7.0]
  - Pendiente post-breakpoint > 2 × pendiente pre-breakpoint

**Método estadístico**:

```python
# Paquete: segmented (R) o pwlf (Python)
model_piecewise = segmented(
    ratio ~ balance_económico,
    seg.Z = ~balance_económico,  # Variable para detectar breakpoint
    psi = 5.0  # Guess inicial del threshold
)

# Extraer breakpoint y CI
threshold = model_piecewise.psi[0]
CI = confint(model_piecewise, "psi")
```

---

### H7.3 - Robustez Metodológica (CONTROL)

**Enunciado**:

```
Las conclusiones de H7.1 y H7.2 son robustas tras eliminar:
    1. Sesgo espacial de spawn (spawn aleatorio)
    2. Sesgo de seeding (torch + random + numpy)
    3. Asimetría de exploración (opcional: entrenamiento intercalado)
```

**Criterios de éxito**:

- ✅ Resultado de H7.1 en v7 NO contradice v6 en subset "Harsh":
  - Ratio_v7(harsh) ≈ Ratio_v6 (diferencia < 3 puntos porcentuales)
  - Modelo constante sigue ganando en "Harsh"
- ✅ D_effective en v7 más cercana a nominal que en v6:
  - D_effective(spawn=0.4) > 3.0 (vs 1.64 en v6)
  - Brecha < 40% (vs 74% en v6)

**Validación adicional**:

- Si H7.1 se cumple, rerun 1-2 configs clave (economía Favorable, D óptima) con **3 seeds adicionales** (999, 1111, 2222) para verificar estabilidad.

---

## 3. DISEÑO EXPERIMENTAL

### 3.1 Factores y Niveles

| Factor              | Niveles | Descripción                                    | Balance            |
| ------------------- | ------- | ----------------------------------------------- | ------------------ |
| **Economía** | 3       | Variable crítica                               |                    |
| - Harsh             | 1       | `step_cost=-0.3, resource_reward=1.0`         | 3.33 (v6 baseline) |
| - Balanced          | 1       | `step_cost=-0.2, resource_reward=1.0`         | 5.0                |
| - Favorable         | 1       | `step_cost=-0.1, resource_reward=1.0`         | 10.0               |
| **Densidad**  | 5       | `spawn_rate: 0.05, 0.10, 0.20, 0.30, 0.40`    | -                  |
| **Seed**      | 3       | `42, 123, 456` (expansión a 5 si borderline) | -                  |

**Nota sobre elección de economías**:

- **Harsh (3.33)**: Replica v6 para validación interna
- **Balanced (5.0)**: Justo en el threshold hipotético → test crítico de H7.2
- **Favorable (10.0)**: 3× el threshold → máxima probabilidad de observar Goldilocks

### 3.2 Configuración del Entorno

**Parámetros fijos** (iguales a v6):

```python
grid_size = 4
risk_scale = 1.5
max_resources_on_grid = 3
resource_decay_steps = 5
max_steps = 30
```

**Parámetros variables** (por economía):

```python
configs_economia = {
    'harsh': {
        'step_cost': -0.3,
        'resource_reward': 1.0,
        'label': 'Harsh (v6 baseline)',
        'balance': 3.33
    },
    'balanced': {
        'step_cost': -0.2,
        'resource_reward': 1.0,
        'label': 'Balanced',
        'balance': 5.0
    },
    'favorable': {
        'step_cost': -0.1,
        'resource_reward': 1.0,
        'label': 'Favorable',
        'balance': 10.0
    }
}
```

### 3.3 Tamaño Muestral y Poder Estadístico

**Configuraciones totales**: 3 economías × 5 densidades × 3 seeds = **45 configs**

**Episodios por config**: 600 (300 PGF + 300 Control, entrenados separadamente)

**Episodios totales**: 45 × 600 = **27,000 episodios**

**Tiempo estimado**:

- v6 (25 configs, 15k eps): 20 minutos
- v7 (45 configs, 27k eps): **36 minutos** (1.8× más)

**Nota sobre expansión**: Si resultados son borderline (p ≈ 0.05, ΔAIC entre -2 y -4), se amplía a 5 seeds (789, 101112) documentado como extensión confirmatoria.

**Poder estadístico** (calculado a priori):

```
ANOVA 2-way (economía × densidad):
    α = 0.05, poder = 0.75
    Efecto mínimo detectable (interacción): η² = 0.07 (pequeño-mediano)
    Tamaño muestral requerido: n ≥ 40 configs
    → v7 con 45 configs es ADECUADO

Regresión segmentada (threshold):
    α = 0.05, poder = 0.75
    Cambio mínimo detectable en pendiente: Δβ = 3.5 puntos ratio / unidad balance
    n ≥ 40 puntos (tenemos 45)
    → v7 es ADECUADO (ampliable a 75 si borderline)
```

---

## 4. PROCEDIMIENTOS Y CONTROLES

### 4.1 Correcciones Obligatorias vs v6

#### Fix 1: Spawn Aleatorio (CRÍTICO)

**Problema v6**: Loop determinista `for x, for y` con break → sesgo top-left

**Solución v7**:

```python
# sim/environment_v2.py - Reemplazar método completo
def _spawn_resources(self):
    """Spawn con muestreo uniforme aleatorio (elimina sesgo espacial)"""
    if len(self.resource_positions) >= self.max_resources_on_grid:
        return
  
    # Construir lista de celdas válidas
    available_cells = []
    for x in range(self.size):
        for y in range(self.size):
            pos = (x, y)
            # Validación: no ocupada, no agente, no hazards, no goal
            if (pos not in self.resource_positions and
                pos != tuple(self.agent_pos) and
                pos not in self.tripwires and
                pos not in self.shocks and
                pos != tuple(self.goal_pos)):
                available_cells.append(pos)
  
    # CLAVE: Aleatorizar orden antes de iterar
    np.random.shuffle(available_cells)
  
    # Intentar spawn en hasta 10 celdas aleatorias
    for pos in available_cells[:10]:
        if len(self.resource_positions) >= self.max_resources_on_grid:
            break
      
        # Spawn con probabilidad spawn_rate
        if np.random.rand() < self.resource_spawn_rate:
            self.resource_positions.add(pos)
            self.resource_spawn_times[pos] = self.timestep
            self.total_resources_spawned += 1
```

**Validación del fix**:

- Test: Ejecutar 1000 episodios con spawn_rate=0.4, registrar posiciones spawneadas
- Criterio: χ² test de uniformidad espacial, p > 0.05 (distribución uniforme)

#### Fix 2: Seeding Completo (IMPORTANTE)

**Problema v6**: Solo `np.random.seed(seed)` → pesos DQN no reproducibles

**Solución v7**:

```python
# scripts/run_experiment_4_economia_factorial.py
import random
import torch
import numpy as np

def configure_all_seeds(seed):
    """Configura todos los RNGs para reproducibilidad completa"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
  
    # CUDA si disponible
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
  
    # Opcional: Determinismo completo (más lento)
    # torch.backends.cudnn.deterministic = True
    # torch.backends.cudnn.benchmark = False

# Llamar ANTES de crear agentes
configure_all_seeds(seed)
```

**Validación del fix**:

- Test: Ejecutar misma config con mismo seed en 2 máquinas diferentes
- Criterio: Rewards idénticos hasta 3 decimales en primeros 10 episodios

#### Fix 3: Anti-Camping (YA APLICADO en v6)

**Status**: ✅ Commit `805384b` ya implementó `done=True` en `environment.py:168`

**Verificación en v7**: Grep "2143" en resultados al terminar → debe retornar 0 matches

### 4.2 Protocolo de Ejecución

#### Fase 0: Validación Pre-Run (OBLIGATORIA)

```bash
# Test rápido: 1 config por economía × 10 episodios × 2 agentes
python scripts/run_experiment_4_economia_factorial.py \
    --test_mode \
    --economies harsh balanced favorable \
    --densities 0.20 \
    --seeds 42 \
    --episodes 10

# Verificar rewards en rangos esperados:
#   Harsh: ~100-120 (como v6)
#   Balanced: ~140-180
#   Favorable: ~200-250
# Si rewards fuera de rango → DETENER, revisar código
```

#### Fase 1: Ejecución por Bloques

**Estrategia**: Dividir 45 configs en 3 bloques de 15 (1 por economía) para:

1. Detectar problemas temprano (si bloque 1 falla, no ejecutar 2-3)
2. Backup incremental (commit después de cada bloque)
3. Balancear carga (ejecutar en horarios distintos si necesario)

```bash
# Bloque 1: Harsh (15 configs)
python scripts/run_experiment_4_economia_factorial.py \
    --economies harsh \
    --densities 0.05 0.10 0.20 0.30 0.40 \
    --seeds 42 123 456 \
    --episodes 300 \
    --output_dir results/pgf_v7/resultados

# Checkpoint 1: Verificar 30 archivos generados (15 JSON + 15 CSV), commit
git add results/pgf_v7/resultados/exp4_economy_harsh_*.{json,csv}
git commit -m "v7 Bloque 1/3: Economía Harsh (15 configs)"

# Bloque 2: Balanced (25 configs)
python scripts/run_experiment_4_economia_factorial.py \
    --economies balanced \
    ...  # igual que Bloque 1

# Checkpoint 2: Commit
git commit -m "v7 Bloque 2/3: Economía Balanced (15 configs)"

# Bloque 3: Favorable (15 configs)
python scripts/run_experiment_4_economia_factorial.py \
    --economies favorable \
    ...

# Checkpoint 3: Commit final
git commit -m "v7 Bloque 3/3: Economía Favorable (15 configs) - EJECUCIÓN COMPLETA (45 configs, 27k eps)"
```

#### Fase 2: Verificación en Tiempo Real

**Spot-checks durante ejecución** (cada 10 configs):

1. Abrir CSV más reciente, verificar:
   - Episodios entre 5-30 pasos (no todos 30 → indica timeout)
   - Rewards en rango esperado por economía
   - No valores NaN/Inf
2. Si anomalía detectada → DETENER ejecución, investigar antes de continuar

### 4.3 Manejo de Outliers

**Criterio de exclusión** (mismo que v6):

```python
# Aplicar IQR (Interquartile Range) sobre ratios por densidad
Q1 = np.percentile(ratios, 25)
Q3 = np.percentile(ratios, 75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = ratios[(ratios < lower_bound) | (ratios > upper_bound)]
```

**Documentación obligatoria**:

- Listar configs excluidas en `results/pgf_v7/analisis/outliers_excluded.txt`
- Para cada outlier:
  - Config exacta (economía, densidad, seed)
  - Ratio observado
  - Causa probable (inspección manual de CSV: convergencia, episodios anómalos)
  - Decisión: excluir vs rerun

**Decisión de rerun**:

- Si ≤3 outliers: excluir (suficientes datos sin ellos)
- Si >3 outliers en MISMA economía: rerun con seeds alternativos (999, 1111, 2222)

---

## 5. VARIABLES Y MÉTRICAS

### 5.1 Variables Registradas (por episodio)

**Primarias**:

- `total_reward`: Recompensa acumulada del episodio
- `steps`: Número de pasos hasta terminación
- `resources_collected`: Recursos consumidos durante episodio
- `final_resources`: Recursos del agente al finalizar

**Secundarias** (para análisis exploratorios):

- `D_effective`: Densidad efectiva experimentada (recursos accesibles / área visitada)
- `cells_visited`: Número de celdas únicas exploradas
- `goal_reached`: Booleano (¿alcanzó meta con recursos suficientes?)
- `death_by_hazard`: Booleano (¿murió por shock/tripwire?)

### 5.2 Métricas Agregadas (por config)

**Para análisis estadístico**:

```python
# Por cada config (economía × densidad × seed):
metrics = {
    'mean_reward_pgf': np.mean(rewards_pgf_episodes),
    'mean_reward_control': np.mean(rewards_control_episodes),
    'ratio_pgf_control': mean_reward_pgf / mean_reward_control,
  
    'std_reward_pgf': np.std(rewards_pgf_episodes),
    'std_reward_control': np.std(rewards_control_episodes),
  
    'mean_steps_pgf': np.mean(steps_pgf_episodes),
    'mean_steps_control': np.mean(steps_control_episodes),
  
    'D_effective_mean': np.mean(D_effective_all_episodes),
    'D_effective_std': np.std(D_effective_all_episodes),
  
    'goal_rate_pgf': np.mean(goal_reached_pgf),  # % éxito
    'goal_rate_control': np.mean(goal_reached_control),
  
    'convergence_pgf': detect_convergence(rewards_pgf_episodes),  # episodio donde estabiliza
    'convergence_control': detect_convergence(rewards_control_episodes)
}
```

### 5.3 Checks de Sanidad

**Ejecutar ANTES de análisis estadístico**:

```python
# 1. Rango de rewards por economía
assert 90 <= mean_reward_harsh <= 130, "Harsh fuera de rango v6"
assert 120 <= mean_reward_balanced <= 200, "Balanced inesperado"
assert 180 <= mean_reward_favorable <= 300, "Favorable inesperado"

# 2. D_effective vs nominal (post-fix spawn)
D_nominal = spawn_rate × grid_size² × (1 - decay_rate)
assert D_effective > 0.5 × D_nominal, "D_effective muy baja (¿sesgo persiste?)"

# 3. Ratios sensatos
assert 70 <= ratio_pgf_control <= 150, "Ratio extremo, revisar"

# 4. Convergencia alcanzada
assert convergence_episode < 250, "Agente no converge en 300 eps"
```

---

## 6. PLAN DE ANÁLISIS ESTADÍSTICO

### 6.1 Análisis Primario (H7.1)

**Paso 1: ANOVA 2-way**

```R
# Modelo completo
model_full <- aov(ratio ~ economia * densidad + Error(seed), data=df)
summary(model_full)

# Efectos que nos interesan:
#   - Efecto principal economia: F, p-valor
#   - Efecto principal densidad: F, p-valor
#   - Interacción economia:densidad: F, p-valor (CLAVE para H7.1)

# Criterio éxito: p(interacción) < 0.05 Y F(interacción) > 3.0
```

**Paso 2: Análisis de efectos simples** (si interacción significativa)

```R
# Por cada nivel de economía, ajustar modelos
for (eco in c('harsh', 'balanced', 'favorable')) {
    subset_eco <- df[df$economia == eco, ]
  
    # Ajustar 5 modelos
    m_const <- lm(ratio ~ 1, data=subset_eco)
    m_linear <- lm(ratio ~ densidad, data=subset_eco)
    m_quad <- lm(ratio ~ densidad + I(densidad^2), data=subset_eco)
    m_log <- lm(ratio ~ log(densidad), data=subset_eco)
    m_exp <- lm(ratio ~ exp(densidad), data=subset_eco)  # cuidado con escala
  
    # Comparar AIC
    aics <- c(AIC(m_const), AIC(m_linear), AIC(m_quad), AIC(m_log), AIC(m_exp))
    best_model <- which.min(aics)
  
    # Reportar:
    #   - Modelo ganador
    #   - ΔAIC vs constante
    #   - Coeficientes e IC95%
    #   - Para cuadrático: a (coef densidad²), verificar a<0 y CI<0
}
```

**Paso 3: Verificación de criterios Goldilocks** (si cuadrático gana en "Favorable")

```R
# Solo para subset favorable + modelo cuadrático
coef_quad <- coef(m_quad)
a <- coef_quad["I(densidad^2)"]
b <- coef_quad["densidad"]
c <- coef_quad["(Intercept)"]

# Calcular vértice
D_star <- -b / (2*a)

# Verificar:
#   1. a < 0 (parábola invertida)
#   2. IC95%(a) < 0 (significativo)
#   3. D_star ∈ [0.7, 1.5] (rango preregistrado)
#   4. ratio(D_star) > 110% (ventaja mínima)
#   5. |r(densidad, ratio)| > 0.5, p < 0.01

# Si ≥3/5 → Goldilocks CONFIRMADA en economía favorable
```

### 6.2 Análisis Secundario (H7.2)

**Regresión segmentada** (threshold económico)

```R
library(segmented)

# Preparar datos: 1 fila por config, balance como predictor
df_threshold <- df %>%
    group_by(economia, balance) %>%
    summarize(ratio_mean = mean(ratio), ratio_se = sd(ratio)/sqrt(n()))

# Ajustar modelo segmentado
seg_model <- segmented(
    lm(ratio_mean ~ balance, data=df_threshold),
    seg.Z = ~balance,
    psi = 5.0  # Guess inicial del breakpoint
)

# Extraer breakpoint estimado
threshold_est <- seg_model$psi[2]  # Valor estimado
threshold_se <- seg_model$psi[3]   # Error estándar
threshold_ci <- confint(seg_model, "psi")  # IC 95%

# Criterio éxito H7.2:
#   - AIC(seg_model) < AIC(lm_simple) - 4
#   - threshold_est ∈ [4.0, 7.0]
#   - Pendiente post-threshold > 2 × pendiente pre-threshold
```

### 6.3 Análisis de Robustez (H7.3)

**Replicación de v6 en subset "Harsh"**

```R
# Comparar ratios v7(harsh) vs v6
df_harsh_v7 <- df[df$economia == 'harsh', ]
ratio_v7_harsh <- mean(df_harsh_v7$ratio)
ratio_v6 <- 99.5  # Del reporte v6

diff <- abs(ratio_v7_harsh - ratio_v6)

# Criterio: diferencia < 3 puntos porcentuales
test_v6_replicado <- diff < 3.0

# Test adicional: modelo constante sigue ganando en harsh?
m_const_harsh <- lm(ratio ~ 1, data=df_harsh_v7)
m_linear_harsh <- lm(ratio ~ densidad, data=df_harsh_v7)

delta_aic_harsh <- AIC(m_linear_harsh) - AIC(m_const_harsh)
test_const_wins <- delta_aic_harsh > 0  # Constante mejor si ΔAIC > 0
```

**Verificación de D_effective** (post-fix spawn)

```python
# Calcular D_effective media por spawn_rate
D_eff_by_spawn = df.groupby('spawn_rate')['D_effective'].mean()

# Para spawn=0.4:
D_eff_040 = D_eff_by_spawn[0.4]
D_nominal_040 = 0.4 * 16 * (1 - 1/5)  # ≈ 5.12

brecha_porcentual = (D_nominal_040 - D_eff_040) / D_nominal_040 * 100

# Criterios H7.3:
#   - D_eff_040 > 3.0 (vs 1.64 en v6)
#   - brecha < 40% (vs 74% en v6)
```

### 6.4 Figuras Preregistradas

**Obligatorias**:

1. **Heatmap ratio vs economía×densidad** (`heatmap_ratio_economy_density.png`)

   - Eje X: Densidad (0.05-0.40)
   - Eje Y: Economía (Harsh/Balanced/Favorable)
   - Color: Ratio PGF/Control (escala 90-120%, divergente en 100%)
2. **Curvas por economía** (`goldilocks_by_economy.png`)

   - 3 curvas superpuestas (1 por economía)
   - Eje X: Densidad, Eje Y: Ratio
   - Ajuste: línea del mejor modelo (constante/lineal/cuadrático)
   - Bandas de confianza 95%
3. **Interaction plot** (`interaction_plot.png`)

   - ANOVA 2-way: economía × densidad
   - Líneas paralelas → NO interacción
   - Líneas cruzadas → SÍ interacción (esperado)
4. **Threshold detection** (`threshold_detection.png`)

   - Regresión segmentada
   - Punto de quiebre marcado con línea vertical + IC
   - 2 pendientes (pre/post threshold) con colores distintos

**Opcionales** (exploratorias):
5. Distribución de ratios por economía (boxplots)
6. Convergencia: reward vs episodio por agente/economía
7. Residuales de modelo cuadrático (QQ-plot, homocedasticidad)

---

## 7. CRITERIOS DE DECISIÓN

### 7.1 Escenario 1: Goldilocks Emerge (H7.1 + H7.2 confirmadas)

**Evidencia**:

- ✅ Interacción Economía×Densidad significativa (p < 0.05)
- ✅ Cuadrático gana en "Favorable" (ΔAIC < -4)
- ✅ Parábola invertida (a<0, CI<0, D*∈[0.7,1.5])
- ✅ Threshold detectado ≈ 5.0 ± 1.0

**Conclusión TUI v4.3**:

> *"La Hipótesis Goldilocks es CONDICIONAL: emerge solo cuando balance económico > threshold (~5.0). En régimen de supervivencia, la ventaja de alineación se anula. Esto refina la TUI al especificar condiciones de emergencia."*

**Próximos pasos**:

- Paper principal con v6 (null) + v7 (condicional)
- v8: Explorar otros factores (horizonte temporal, complejidad topológica)

---

### 7.2 Escenario 2: Ventaja Emerge, pero NO Goldilocks (H7.2 confirmada, H7.1 parcial)

**Evidencia**:

- ✅ Threshold detectado ≈ 5.0
- ✅ Ratio en "Favorable" > 110%
- ❌ Pero forma NO es parábola invertida (lineal o log gana)

**Conclusión TUI v4.3**:

> *"La ventaja de alineación requiere slack económico (confirmado), pero NO sigue curva Goldilocks clásica. La relación ratio(D) es monotónica creciente (más recursos → más ventaja) sin máximo intermedio."*

**Implicación teórica**: Reemplazar ley 1/(D+D₀) por función monotónica:

```
ratio(D, balance) = 100% + k(balance - threshold)^+ × log(1 + D)
Donde (x)^+ = max(0, x)
```

---

### 7.3 Escenario 3: NULL Persistente (H7.1 + H7.2 refutadas)

**Evidencia**:

- ❌ NO interacción significativa
- ❌ Ratio ≈ 100% en TODAS las economías
- ❌ Threshold NO detectado

**Conclusión TUI v4.3**:

> *"La ventaja de alineación NO emerge incluso con slack económico. Factores más allá de economía/densidad (e.g., horizonte temporal, complejidad de alineación, arquitectura cognitiva) son necesarios para que PGF supere a Control."*

**Próximos pasos**:

- v8: Horizonte extendido (50-100 pasos vs 30)
- v9: Grid 8×8 (más exploración)
- v10: Ablación de mecanismos PGF (¿qué componente falta?)

---

### 7.4 Escenario 4: v6 NO Replica (H7.3 falla)

**Evidencia**:

- ❌ Ratio v7(harsh) ≠ Ratio v6 (diferencia > 5 puntos)
- ❌ Modelo constante NO gana en "Harsh"

**Acción inmediata**:

1. **DETENER análisis de H7.1 y H7.2**
2. Investigar discrepancia:
   - ¿Spawn fix alteró comportamiento fundamental?
   - ¿Seeds completos cambian convergencia DQN?
   - ¿Código tiene regresión vs v6?
3. **Rerun v6 con mismos fixes** (spawn + seeds) como "v6.1"
4. Comparar v6 vs v6.1 vs v7(harsh):
   - Si v6.1 ≈ v7(harsh) → fixes cambian baseline, reinterpretar v7
   - Si v6.1 ≈ v6 → error en código v7, corregir

**Criterio de validez**:

- NO proceder con paper hasta entender discrepancia
- Documentar en apéndice metodológico del paper

---

## 8. RECURSOS Y TIMELINE

### 8.1 Archivos Generados

```
results/pgf_v7/
├── resultados/
│   ├── exp4_economy_harsh_spawn0.05_seed42.json       (45 JSONs)
│   ├── exp4_economy_harsh_spawn0.05_seed42_episodes.csv (45 CSVs)
│   └── experiment_4_summary.json                       (1 summary)
├── analisis/
│   ├── anova_2way_results.txt
│   ├── model_comparison_by_economy.json
│   ├── threshold_regression.json
│   ├── outliers_excluded.txt
│   └── sanity_checks.log
├── figuras/
│   ├── heatmap_ratio_economy_density.png
│   ├── goldilocks_by_economy.png
│   ├── interaction_plot.png
│   └── threshold_detection.png
└── reportes/
    └── REPORTE_EXPERIMENTO_4.md
```

**Total estimado**: 95 archivos, ~30 MB (ampliable a 150 archivos si se expande a 5 seeds)

### 8.2 Scripts Requeridos

**Nuevos** (crear antes de ejecutar):

1. `scripts/run_experiment_4_economia_factorial.py` (ejecución)
2. `scripts/analyze_economia_factorial.py` (ANOVA, modelos, threshold)
3. `scripts/plot_economia_factorial.py` (4 figuras obligatorias)
4. `scripts/monitor_v7_progress.py` (opcional, spot-checks en tiempo real)

**Modificados**:

1. `sim/environment_v2.py` (_spawn_resources con shuffle)

### 8.3 Timeline Estimada

| Fase                                      | Duración           | Hitos                                              |
| ----------------------------------------- | ------------------- | -------------------------------------------------- |
| **Preparación**                    | 15 min              | Fix spawn + seeds, crear scripts, test validación |
| **Ejecución Bloque 1** (Harsh)     | 12 min              | 15 configs, checkpoint commit                      |
| **Ejecución Bloque 2** (Balanced)  | 12 min              | 15 configs, checkpoint commit                      |
| **Ejecución Bloque 3** (Favorable) | 12 min              | 15 configs, checkpoint commit                      |
| **Análisis estadístico**          | 30 min              | ANOVA, modelos, threshold, figuras                 |
| **Reporte final**                   | 15 min              | Markdown con hallazgos, tablas, figuras            |
| **TOTAL**                           | **1.5 horas** | Preregistro → Reporte final                       |

### 8.4 Checkpoints de Commit

```bash
# Checkpoint 0: Preregistro
git add results/pgf_v7/PREREGISTRO_v7.md
git commit -m "v7 PREREGISTRO: H7.1-H7.3 formales, diseño 3×5×5=75 configs"

# Checkpoint 1: Código listo
git add sim/environment_v2.py scripts/run_experiment_4*.py
git commit -m "v7 CÓDIGO: Spawn aleatorio + seeds completos + scripts ejecución/análisis"

# Checkpoint 2-4: Bloques de ejecución (ver §6.1 Fase 1)

# Checkpoint 5: Análisis completo
git add results/pgf_v7/analisis/* results/pgf_v7/figuras/*
git commit -m "v7 ANÁLISIS: ANOVA, modelos, threshold, figuras - Listo para reporte"

# Checkpoint 6: Reporte final
git add results/pgf_v7/reportes/REPORTE_EXPERIMENTO_4.md
git commit -m "v7 CIERRE: Reporte final - Goldilocks [CONFIRMADA/PARCIAL/REFUTADA] en economía favorable"
```

---

## 9. DECLARACIONES DE TRANSPARENCIA

### 9.1 Conflictos de Interés

**Ninguno**: Este es un proyecto académico independiente sin financiamiento externo.

### 9.2 Cambios al Preregistro

**Política**:

- Este preregistro es **vinculante** desde commit `[hash al guardar este archivo]`
- **Cambios permitidos** SIN invalidar preregistro:

  - Corrección de typos/errores de código (no cambian hipótesis)
  - Ajustes menores de hiperparámetros DQN (learning rate ±20%)
  - Añadir análisis exploratorios NO preregistrados (claramente marcados como post-hoc)
- **Cambios que INVALIDAN preregistro**:

  - Modificar hipótesis H7.1-H7.3 después de ver datos
  - Cambiar criterios de éxito (umbrales, niveles de significancia)
  - Excluir outliers sin criterio objetivo preregistrado
  - Añadir condiciones de economía no especificadas aquí

**Documentación obligatoria**:

- Si se hace cambio permitido → nota en REPORTE_EXPERIMENTO_4.md sección "Desviaciones del Preregistro"
- Si se invalida preregistro → marcar experimento como **exploratorio** (no confirmatorio)

### 9.3 Datos y Código Abiertos

**Compromiso**:

- Todos los datos crudos (CSVs) serán publicados en el repositorio
- Scripts de análisis reproducibles (con requirements.txt)
- Decisiones de exclusión de outliers documentadas con justificación

**Acceso**:

- Repositorio: `github.com/jmrgpr/TUI-v4.1`
- Branch: `main`
- Directorio: `results/pgf_v7/`

---

## 10. FIRMAS Y APROBACIÓN

**Investigador Principal**: @jmrgpr
**Fecha de preregistro**: 3 de diciembre de 2025, 10:00 AM
**Commit de preregistro**: `[se completará al hacer commit]`
**Status**: ✅ APROBADO - Listo para ejecución

**Revisores** (opcional, si hay colaboradores):

- [Nombre], [Afiliación]: ________________ (Firma)

---

## ANEXO A: Justificación de Tamaños de Efecto

### Efecto mínimo detectable (interacción Economía×Densidad)

Basado en v6:

- Efecto observado de Densidad: η² < 0.01 (despreciable)
- Si Goldilocks existe, esperamos: η² interacción > 0.06 (pequeño-mediano según Cohen)

Con n=75 y α=0.05, poder 0.80:

- Detectamos η² ≥ 0.06 con probabilidad 80%
- Para η² = 0.10 (mediano), poder > 0.95

**Conclusión**: v7 tiene poder suficiente para detectar efectos teóricamente relevantes.

### Cambio mínimo en ratio (umbral práctico)

Consideramos ratio > 110% como **ventaja mínima práctica** porque:

- 10% mejora en reward es típicamente observable por humanos evaluando políticas
- IC95% de ±5% implica que ratio=110% es distinguible de 100% con n≥25
- En v6, varianza intra-config fue σ ≈ 5% → con 5 seeds, SE ≈ 2.2%

---

## ANEXO B: Código de Verificación de Spawn Fix

```python
# Test de uniformidad espacial post-fix
import numpy as np
from scipy.stats import chisquare

def test_spawn_uniformity(env, n_trials=1000, spawn_rate=0.4):
    """
    Verifica distribución uniforme de spawns después del fix.
  
    Returns:
        p_value: Si p > 0.05, spawn es uniforme (fix exitoso)
    """
    grid_size = env.size
    spawn_counts = np.zeros((grid_size, grid_size))
  
    for _ in range(n_trials):
        env.reset()
        env.resource_spawn_rate = spawn_rate
        env._spawn_resources()
      
        # Registrar posiciones spawneadas
        for pos in env.resource_positions:
            spawn_counts[pos] += 1
  
    # χ² test: Ho = distribución uniforme
    observed = spawn_counts.flatten()
    expected = np.full_like(observed, observed.sum() / observed.size)
  
    chi2, p_value = chisquare(observed, expected)
  
    print(f"χ² = {chi2:.2f}, p = {p_value:.4f}")
    if p_value > 0.05:
        print("✅ Spawn es UNIFORME (fix exitoso)")
    else:
        print("❌ Spawn NO uniforme (revisar código)")
  
    return p_value

# Ejecutar antes de v7
# from sim.environment_v2 import ResourceDensityEnv
# env = ResourceDensityEnv(size=4, ...)
# test_spawn_uniformity(env)
# Criterio: p > 0.05
```

---

**FIN DEL PREREGISTRO**

*Este documento ha sido generado siguiendo estándares de preregistro de AsPredicted.org y OSF Preregistration.*

*Versión: 1.0*
*Última edición: 3 diciembre 2025, 10:00 AM*
*Hash del commit (se completará): `[pendiente]`*
