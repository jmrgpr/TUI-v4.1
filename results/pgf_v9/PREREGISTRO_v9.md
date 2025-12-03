# 📋 PREREGISTRO EXPERIMENTAL: PGF v9 - Curriculum Learning para Mitigar Over-Alignment

**Título**: Curriculum Learning como Estrategia de Mitigación del Régimen de Over-Alignment en Agentes DQN con Reward Shaping Prudencial  
**Investigador**: Sistema TUI v4.1  
**Fecha registro**: 3 de diciembre de 2025  
**Protocolo**: Preregistración anterior a ejecución  
**Versión experimento**: v9 ("Curriculum vs Directo")  
**Versión preregistro**: 1.0  

---

## 📖 Resumen Ejecutivo

Este experimento investiga si el **curriculum learning** (escalamiento gradual de intensidad de shaping) puede mitigar el fenómeno de **over-alignment** descubierto en v8.

**Contexto v8**: Con shaping s=1.0 (penalty=-100, bonus=+50), PGF entra en parálisis conductual:
- Success rate: 16% (vs 84% Control)
- Timeout rate: 84% (inmovilidad adaptativa)
- Ratio reward env: 0.344 (colapso funcional)

**Pregunta central**: ¿Puede un entrenamiento por etapas (0.0→0.25→0.5→1.0) permitir al agente aprender balances intermedios y evitar parálisis final?

---

## 🎯 Antecedentes y Motivación

### Resultados v8 (Estado del Arte)

**Hallazgo principal**: Over-alignment detectado con s=1.0
```
Shaping Scale | Ratio PGF/Control | Interpretación
--------------|-------------------|-------------------
s = 0.0       | 0.987 ± 0.057    | Paridad (H8.3 ✅)
s = 0.25      | 0.595 ± 0.416    | Degradación leve
s = 0.5       | 0.535 ± 0.367    | Degradación moderada
s = 1.0       | 0.344 ± 0.318    | **PARÁLISIS CONDUCTUAL**
```

**Análisis temporal v8**: Over-alignment es **súbito desde inicio**, NO emerge gradualmente.
- Tramos (exploration/convergence/stability): Δ = +0.006 → estable en ~0.34

**Diagnóstico**:
> El agente aprende **inmediatamente** una política ultra-conservadora cuando enfrenta s=1.0 desde episodio 1. No tiene oportunidad de explorar balances intermedios.

**Ver**: `results/pgf_v8/reportes/REPORTE_FINAL_v8.md`, `docs/LECCIONES_v5-v8.md`

### Hipótesis Motivadora

**Inspiración**: Curriculum learning en deep RL (Bengio et al., 2009; Narvekar et al., 2020)

**Intuición**:
> Si el agente **primero** aprende a navegar sin shaping (s=0.0), luego incorpora señales débiles (s=0.25), y **gradualmente** escala hasta s=1.0, tendrá tiempo de ajustar su política en cada etapa sin colapsar.

**Mecanismo propuesto**:
1. **Etapa 1 (s=0.0)**: Aprende navegación básica, goal-seeking
2. **Etapa 2 (s=0.25)**: Introduce aversión leve a riesgos, mantiene exploración
3. **Etapa 3 (s=0.5)**: Incrementa prudencia, balancea seguridad-eficiencia
4. **Etapa 4 (s=1.0)**: Señal fuerte, pero **red ya tiene política funcional** como base

**Contraste con v8**:
- v8 directo s=1.0: Agente "congela" desde inicio (no sabe qué hacer, paraliza)
- v9 curriculum: Agente "escala" desde política conocida (puede adaptar gradualmente)

### Gap Metodológico

**v8 demostró QUÉ falla** (over-alignment), v9 testa **CÓMO mitigarlo**.

---

## 🔬 Diseño Experimental

### Variables Independientes

#### Factor 1: TRAINING_PROTOCOL (Principal)

**Tipo**: Categórica, 3 niveles (grupos experimentales)

**Valores**:

1. **CURRICULUM** (grupo experimental)
   - 4 etapas secuenciales × 75 episodios cada una = 300 total
   - Shaping escalado: s=0.0 → s=0.25 → s=0.5 → s=1.0
   - Pesos Q-network se **transfieren** entre etapas (transfer learning)
   - Epsilon **continúa decreciente** a través de etapas

2. **DIRECTO_S1** (grupo control positivo)
   - 300 episodios con s=1.0 desde inicio (réplica v8)
   - Shaping constante máximo
   - Esperamos parálisis (baseline de falla)

3. **CONTROL_S0** (grupo control negativo)
   - 300 episodios con s=0.0 (sin shaping)
   - Réplica v8 control negativo
   - Esperamos paridad (baseline funcional)

**Operacionalización**:

```python
# Curriculum (detallado)
def train_curriculum(agent, env, seed):
    episodes_per_stage = 75
    stages = [
        {'scale': 0.0,  'episodes': range(0, 75)},
        {'scale': 0.25, 'episodes': range(75, 150)},
        {'scale': 0.5,  'episodes': range(150, 225)},
        {'scale': 1.0,  'episodes': range(225, 300)}
    ]
    
    for stage in stages:
        env.set_shaping_scale(stage['scale'])  # Actualizar entorno
        # NO reiniciar agent.epsilon ni agent.q_network (transfer learning)
        for episode in stage['episodes']:
            train_episode(agent, env)
    
    return agent

# Directo s=1.0
def train_direct_s1(agent, env, seed):
    env.set_shaping_scale(1.0)  # Fijo desde inicio
    for episode in range(300):
        train_episode(agent, env)
    
    return agent

# Control s=0.0
def train_control_s0(agent, env, seed):
    env.set_shaping_scale(0.0)  # Sin shaping
    for episode in range(300):
        train_episode(agent, env)
    
    return agent
```

#### Factor 2: SEED (Replicación)

**Tipo**: Categórica, 3 niveles
**Valores**: {42, 123, 456}
**Control**: Seeding completo (random + numpy + torch + cuda)

### Variables Dependientes (DVs)

#### DV1: Ratio Reward Env Final (Principal)

```python
# Solo últimos 50 episodios (250-300) para cada grupo
ratio_final = mean_reward_env_final[group] / mean_reward_env_final[CONTROL_S0]
```

**Interpretación**:
- `≥ 0.90`: Curriculum exitoso (paridad mantenida)
- `0.70-0.90`: Curriculum parcial (mejor que directo, no "bueno")
- `< 0.50`: Curriculum falla (similar a directo s=1.0)

#### DV2: Success Rate Final

```python
success_rate_final = mean(goal_reached[episodes 250-300])
```

**Interpretación**:
- `> 70%`: Política funcional
- `50-70%`: Política intermedia
- `< 30%`: Parálisis (como directo s=1.0)

#### DV3: Tripwires Finales

```python
tripwires_final = mean(tripwires_triggered[episodes 250-300])
```

**Interpretación**:
- Comparar Curriculum vs Control_S0 → ¿Mantiene prudencia?
- Comparar Curriculum vs Directo_S1 → ¿Evita hiperconservación?

#### DV4: Curva de Aprendizaje (Temporal)

```python
# Ratio por etapa para Curriculum
ratio_stage[i] = mean_reward_env[stage i] / mean_reward_env_control_s0[stage i]
```

**Interpretación**: ¿Degradación gradual o colapso en etapa final?

### Variables de Control (Fijas)

| Parámetro | Valor | Justificación |
|-----------|-------|--------------|
| **Grid size** | 4×4 | Continuidad con v8 |
| **Densidad** | spawn_rate = 0.25 | v8 validado, evita laberintos triviales |
| **Economía** | Balanced (balance=5.0) | v8 estándar |
| **step_cost** | -0.2 | Estándar |
| **goal_reward** | 1.0 | Estándar |
| **Arquitectura** | DQN 2×64 hidden | Estándar proyecto |
| **Hiperparámetros** | lr=0.001, γ=0.95 | Estándar proyecto |
| **Epsilon decay** | 1.0 → 0.01 lineal | Estándar proyecto |
| **PGF penalties** | -100 × scale | v8 confirmado |
| **PGF bonus** | +50 × scale | v8 confirmado |

### Tamaño Muestral

```
N_grupos = 3 (Curriculum, Directo_S1, Control_S0)
N_seeds = 3 (42, 123, 456)
N_configs = 3 × 3 = 9
N_episodes_per_config = 300
N_total_episodes = 9 × 300 = 2,700
```

**Justificación**: Suficiente para t-tests pareados con potencia >0.80 (efecto esperado d≥0.8).

---

## 📊 Hipótesis Preregistradas

### H9.1: Curriculum Superior a Directo (Principal)

**Enunciado formal**:

> El agente entrenado con curriculum alcanzará un ratio_reward_env_final significativamente mayor que el agente entrenado directo con s=1.0.

**Predicción cuantitativa**:

```
H9.1a: Ratio Final
  Curriculum: ratio_final ≥ 0.70
  Directo_S1: ratio_final ≈ 0.35 (replicar v8)
  
  Test: t-test pareado (Curriculum vs Directo_S1), α=0.05, one-tailed
  H_a: mean(ratio_curriculum) > mean(ratio_directo)
```

**Criterio de confirmación**: p < 0.05 AND diferencia >20 puntos porcentuales

**Criterio de refutación**: p > 0.10 OR diferencia <10 puntos porcentuales

### H9.2: Curriculum Mantiene Prudencia (Validación)

**Enunciado formal**:

> El agente curriculum mostrará menor tasa de tripwires que Control_S0 en etapa final, demostrando que la prudencia aprendida se mantiene.

**Predicción cuantitativa**:

```
H9.2a: Tripwires Finales
  Curriculum: tripwires_final < tripwires_control_s0 × 0.80
  
  Interpretación: Curriculum reduce tripwires ≥20% vs baseline
  Test: t-test pareado (Curriculum vs Control_S0), α=0.05, one-tailed
```

**Criterio de confirmación**: p < 0.05 AND reducción >20%

**Criterio de refutación**: p > 0.10 OR reducción <10%

### H9.3: Curriculum Evita Parálisis (Funcionalidad)

**Enunciado formal**:

> El agente curriculum tendrá success_rate_final significativamente mayor que Directo_S1, demostrando que evita parálisis.

**Predicción cuantitativa**:

```
H9.3a: Success Rate Final
  Curriculum: success_rate_final ≥ 60%
  Directo_S1: success_rate_final ≈ 16% (replicar v8)
  
  Test: t-test pareado (Curriculum vs Directo_S1), α=0.05, one-tailed
```

**Criterio de confirmación**: p < 0.05 AND diferencia >30 puntos porcentuales

**Criterio de refutación**: p > 0.10 OR diferencia <15 puntos porcentuales

### H9.4: Degradación Gradual en Curriculum (Exploratoria)

**Enunciado formal**:

> El ratio_reward_env en Curriculum **decrece gradualmente** a través de las etapas, NO colapsa súbitamente en etapa 4.

**Predicción cualitativa**:

```
Ratios esperados por etapa:
  Etapa 1 (s=0.0):  ratio ≈ 0.98 (baseline)
  Etapa 2 (s=0.25): ratio ≈ 0.85 (leve degradación)
  Etapa 3 (s=0.5):  ratio ≈ 0.75 (degradación moderada)
  Etapa 4 (s=1.0):  ratio ≈ 0.70 (degradación contenida)
  
Patrón: Monotónico decreciente con pendiente <0.15 por etapa
```

**Criterio**: Pendiente (ratio vs stage) uniforme (no salto >0.30 en ninguna transición)

---

## 📈 Plan de Análisis Estadístico

### Análisis Primario: Comparaciones Pareadas

**Comparación 1: Curriculum vs Directo_S1** (H9.1)

```python
# Por seed (paired samples)
diff = ratio_final_curriculum - ratio_final_directo
test_statistic, p_value = ttest_rel(ratio_curriculum, ratio_directo, alternative='greater')
effect_size = cohens_d(ratio_curriculum, ratio_directo)
```

**Comparación 2: Curriculum vs Control_S0** (H9.2)

```python
# Tripwires finales
reduction = (tripwires_control - tripwires_curriculum) / tripwires_control
test_statistic, p_value = ttest_rel(tripwires_curriculum, tripwires_control, alternative='less')
```

**Comparación 3: Success Rates** (H9.3)

```python
success_improvement = success_curriculum - success_directo
test_statistic, p_value = ttest_rel(success_curriculum, success_directo, alternative='greater')
```

### Análisis Secundario: Curvas Temporales

**Por grupo**:

```python
# Curriculum: descomponer en 4 etapas
for stage in [1, 2, 3, 4]:
    ratio_stage[stage] = compute_ratio(episodes_stage[stage])

# Plot: ratio vs stage (monotónico decreciente esperado)

# Directo_S1: descomponer en 4 tramos equivalentes
# Comparar: ¿colapso súbito vs degradación gradual?
```

**Test pendiente**:

```python
# Curriculum: pendiente ratio vs stage
slope_curriculum = linregress(stages, ratios).slope

# Esperado: slope ≈ -0.08 a -0.15 (gradual)
# Patológico: slope < -0.25 OR quiebre en etapa 4
```

### Análisis Terciario: Transferencia entre Etapas

**Pregunta**: ¿Qué tanto "olvida" el agente al cambiar de etapa?

**Métrica**:

```python
# Primeros 10 episodios de cada etapa
transfer_efficiency[stage] = ratio_first10_eps / ratio_last10_prev_stage

# Esperado: transfer_efficiency ≈ 0.90-1.05 (retención alta)
# Patológico: transfer_efficiency < 0.70 (olvido catastrófico)
```

### Análisis Exploratorio: Policy Visualization

**Heatmap de políticas finales**:

```python
# Grid 4×4: probabilidad de acción por celda
policy_map[group] = extract_policy_heatmap(agent, grid)

# Comparar:
# - Curriculum: ¿política balanceada?
# - Directo_S1: ¿política ultra-conservadora?
# - Control_S0: ¿política directa (no evita tripwires)?
```

---

## 📊 Criterios de Decisión

### Escenario 1: Curriculum Exitoso (H9.1✅, H9.2✅, H9.3✅)

**Métricas observadas**:
```
Curriculum:  ratio_final = 0.75 ± 0.10, success = 70%, tripwires = 1.5
Directo_S1:  ratio_final = 0.35 ± 0.25, success = 16%, tripwires = 0.4
Control_S0:  ratio_final = 0.98 ± 0.05, success = 82%, tripwires = 4.5
```

**Interpretación**:
- ✅ Curriculum **mitiga** over-alignment (0.75 >> 0.35)
- ✅ Mantiene **prudencia útil** (tripwires reducidos 67% vs control)
- ✅ **Funcional** (70% success vs 82% baseline = coste 15%)

**Conclusión**:
> Curriculum learning es estrategia **efectiva** para entrenar agentes con shaping fuerte sin parálisis.

**Próximo paso**:
- **v10**: Optimización de duración de etapas (¿50 eps mejor que 75?)
- **Paper**: "Staged Alignment: Mitigating Over-Alignment via Curriculum Learning"

### Escenario 2: Curriculum Intermedio (H9.1✅, H9.2~, H9.3~)

**Métricas observadas**:
```
Curriculum:  ratio_final = 0.55 ± 0.15, success = 45%, tripwires = 2.0
Directo_S1:  ratio_final = 0.35 ± 0.25, success = 16%, tripwires = 0.4
```

**Interpretación**:
- ✅ Curriculum **mejor** que directo (0.55 > 0.35)
- ⚠️ Aún **sub-óptimo** (success 45% vs 82% ideal)
- ⚠️ Prudencia parcial (tripwires reducidos solo 56%)

**Conclusión**:
> Curriculum ayuda, pero **insuficiente**. Requiere refinamiento.

**Próximo paso**:
- **v9.1**: Más etapas (6 stages × 50 eps) para gradualidad mayor
- **v9.2**: Secuencia alternativa (0.0→0.15→0.30→0.50→0.75→1.0)

### Escenario 3: Curriculum Falla (H9.1❌)

**Métricas observadas**:
```
Curriculum:  ratio_final = 0.38 ± 0.20, success = 20%, tripwires = 0.5
Directo_S1:  ratio_final = 0.35 ± 0.25, success = 16%, tripwires = 0.4
```

**Interpretación**:
- ❌ Curriculum ≈ Directo (sin ventaja)
- ❌ Colapso en etapa 4 (s=1.0 demasiado fuerte incluso con curriculum)

**Diagnóstico posible**:
1. **Olvido catastrófico**: Agente "resetea" al subir a s=1.0
2. **Threshold absoluto**: s=1.0 es inherentemente inentrenable
3. **Duración insuficiente**: 75 eps/etapa no bastan para consolidar

**Próximo paso**:
- **v10**: Curriculum con s_max = 0.6 (evitar s=1.0 completamente)
- **Alternativa**: Tunear penalty/bonus base (reducir de -100/+50 a -50/+25)

### Escenario 4: Transfer Learning Falla

**Síntoma**:
```
transfer_efficiency[2] = 0.50  # Olvido severo al pasar a etapa 2
transfer_efficiency[3] = 0.45  # Empeora
```

**Diagnóstico**:
> Red neural "olvida" política anterior al cambiar shaping. Problema arquitectural, no de curriculum.

**Próximo paso**:
- **v9.1**: Progressive neural networks (columnas separadas por etapa)
- **v9.2**: Regularización de policy distillation (mantener política anterior)

---

## 🎨 Visualizaciones Preregistradas

### Figura 1: Curvas de Aprendizaje por Grupo

**Tipo**: Line plot con ribbons (media ± SE)
**Ejes**: Episodios (0-300) × Ratio PGF/Control
**Líneas**:
- Curriculum (rojo, 4 segmentos visibles por cambio etapa)
- Directo_S1 (azul, constante s=1.0)
- Control_S0 (gris, baseline)

**Anotaciones**: Líneas verticales en episodios 75, 150, 225 (transiciones curriculum)

**Hipótesis visual**: Curriculum degrada gradualmente, Directo colapsa desde inicio.

### Figura 2: Barplot Ratios Finales (250-300)

**Tipo**: Barplot con error bars
**Ejes**: Grupos (3) × Ratio Final
**Colores**: Curriculum (rojo), Directo_S1 (azul), Control_S0 (gris)
**Línea horizontal**: Paridad (ratio=1.0)

**Hipótesis visual**: Curriculum >> Directo, Curriculum < Control.

### Figura 3: Scatter Safety-Reward Tradeoff (Etapa Final)

**Tipo**: Scatter plot 2D
**X**: Safety Score (1 - tripwires/max)
**Y**: Mean Reward Env (episodios 250-300)
**Puntos**:
- Curriculum: rojo, tamaño grande
- Directo_S1: azul, tamaño grande
- Control_S0: gris, tamaño grande

**Regiones**:
- Cuadrante superior-derecho: Ideal (alta safety, alta reward)
- Cuadrante superior-izquierdo: Over-safety (alta safety, baja reward)
- Cuadrante inferior-derecho: Riesgoso (baja safety, alta reward)

**Hipótesis visual**: Curriculum en región ideal, Directo en over-safety, Control en riesgoso.

### Figura 4: Transfer Efficiency por Etapa

**Tipo**: Line plot
**Ejes**: Etapas (1→2, 2→3, 3→4) × Transfer Efficiency
**Línea**: Curriculum (única)
**Línea horizontal**: 1.0 (retención perfecta)

**Hipótesis visual**: Transfer efficiency ≥ 0.90 (alta retención).

---

## 🗂️ Outputs Comprometidos

### Durante Ejecución

Por cada config (9 archivos):

```
exp9_{group}_seed{seed}_episodes.csv
exp9_{group}_seed{seed}_metrics.json
```

**Columnas CSV OBLIGATORIAS**:

```python
# Identificación
episode: int              # 1-300
agent_type: str           # "PGF_Curriculum", "PGF_DirectoS1", "PGF_ControlS0"
group: str                # "Curriculum", "DirectoS1", "ControlS0"

# Curriculum específico
stage: int                # 1-4 (solo Curriculum), null para otros
shaping_scale_current: float  # s actual en ese episodio

# Recompensas duales
total_reward_env: float
total_reward_shaped: float

# Métricas de seguridad
tripwires_triggered: int
deaths_starvation: int
deaths_tripwire: int      # (no usado v9, preparado para v9.1 si needed)

# Métricas de eficiencia
resources_collected: int
steps_to_goal: int
goal_reached: bool

# Exploración
epsilon: float

# Metadata
seed: int
spawn_rate: float         # 0.25 (fijo)
balance: float            # 5.0 (fijo)
```

**Validación**:

```python
def validate_csv_v9(csv_path: str) -> bool:
    df = pd.read_csv(csv_path)
    
    required = [
        'episode', 'agent_type', 'group', 'stage', 'shaping_scale_current',
        'total_reward_env', 'total_reward_shaped',
        'tripwires_triggered', 'resources_collected', 'steps_to_goal',
        'goal_reached', 'deaths_starvation', 'epsilon', 'seed'
    ]
    
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")
    
    # Validar Curriculum tiene 4 stages
    if df['group'].iloc[0] == 'Curriculum':
        stages = df['stage'].unique()
        if set(stages) != {1, 2, 3, 4}:
            raise ValueError(f"Curriculum debe tener stages 1-4, encontrados: {stages}")
    
    # Validar episodios
    if len(df) != 300:
        raise ValueError(f"Esperados 300 episodios, encontrados: {len(df)}")
    
    return True
```

### Post-Ejecución

**Análisis**:

```
analisis/curriculum_effectiveness.json   # Comparaciones H9.1, H9.2, H9.3
analisis/temporal_stages.json            # Ratios por etapa
analisis/transfer_learning.json          # Eficiencia de transferencia
```

**Figuras**:

```
figuras/fig1_learning_curves_by_group.png
figuras/fig2_barplot_ratios_final.png
figuras/fig3_scatter_safety_reward_final.png
figuras/fig4_transfer_efficiency.png
```

**Reporte**:

```
reportes/REPORTE_FINAL_v9.md
```

---

## ⚠️ Desviaciones Permitidas del Protocolo

### Ajustes Post-Hoc Autorizados

1. **Si transfer efficiency < 0.60 en alguna etapa**:
   - Autorizado: Análisis de "olvido catastrófico" como hallazgo secundario
   - Requerido: Documentar en TRACKING_v9.md

2. **Si colapso en etapa 4 aun con curriculum**:
   - Autorizado: Análisis separado de etapa 3 (s=0.5) como "máximo entrenable"
   - Requerido: Actualizar H9.1 con criterio alternativo (ratio en s=0.5)

3. **Si varianza extrema (SD > 0.50)**:
   - Autorizado: Análisis de sensibilidad excluyendo outlier seed
   - Requerido: Reportar ambos análisis (con/sin outlier)

### Análisis Exploratorios NO Preregistrados

Permitidos siempre que **etiquetados como exploratorios**:

- Visualización de políticas (heatmaps Q-values)
- Análisis de trayectorias individuales
- Correlaciones adicionales (epsilon vs success rate, etc.)

**Restricción**: NO usar análisis exploratorios para **confirmar/refutar hipótesis preregistradas**.

---

## 📅 Timeline Comprometida

| Fase | Fecha límite | Criterio completitud |
|------|--------------|---------------------|
| **Preregistro** | 3 dic 2025 | Este documento aprobado |
| **Implementación** | 3 dic 2025 | Test mode exitoso (1 config) |
| **Ejecución** | 3 dic 2025 | 9 CSVs + JSONs generados |
| **Análisis** | 4 dic 2025 | Comparaciones + figuras |
| **Reporte** | 4 dic 2025 | REPORTE_FINAL_v9.md |

**Deadline absoluto**: 4 de diciembre 2025, 23:59

---

## 🔒 Compromiso de Integridad

**Declaración**:

> Este preregistro constituye un compromiso vinculante de ejecutar v9 según el diseño especificado. Cualquier desviación no autorizada (ver sección "Desviaciones Permitidas") invalida el experimento y requiere preregistro v9.1.
>
> Los resultados se reportarán honestamente independiente de si confirman o refutan las hipótesis. Resultados negativos son tan valiosos como positivos:
> - Si curriculum funciona → demostramos mitigación de over-alignment
> - Si curriculum falla → demostramos límite absoluto de s=1.0

**Firmante**: Sistema TUI v4.1  
**Fecha**: 3 de diciembre de 2025  
**Versión documento**: 1.0  

---

## 📚 Referencias

1. **v8 Final Report**: `results/pgf_v8/reportes/REPORTE_FINAL_v8.md`
2. **Lecciones v5-v8**: `docs/LECCIONES_v5-v8.md`
3. **v8 Preregistro**: `results/pgf_v8/PREREGISTRO_v8.md`
4. **TUI Theory**: `docs/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md`
5. **Environment v2**: `sim/environment_v2.py`
6. **DQN Agent**: `sim/dqn_agent.py`

**Literatura Curriculum Learning**:
- Bengio et al. (2009). "Curriculum Learning". ICML.
- Narvekar et al. (2020). "Curriculum Learning for Reinforcement Learning Domains: A Framework and Survey". JMLR.

---

## 📎 Anexos

### Anexo A: Cálculo de Potencia

**Escenario**: Detectar diferencia Curriculum vs Directo_S1

```
Efecto esperado: d = 1.0 (grande, basado en v8 donde d=2.82 para s=0.0 vs s=1.0)
N por grupo: 3 (seeds pareados)
α: 0.05 (one-tailed)
Test: t-test pareado

Potencia calculada (G*Power): 0.78
```

**Nota**: Potencia ligeramente baja, pero aceptable dado:
- Efecto esperado muy grande
- Diseño pareado (mayor potencia que independiente)
- Costo computacional bajo (podemos reejecutar con más seeds si needed)

### Anexo B: Justificación Duración Etapas

**¿Por qué 75 episodios/etapa?**

```
v8 análisis temporal:
- Convergence phase: episodios 101-200 (100 eps)
- Stability phase: episodios 201-300 (100 eps)

Conclusión: Con 75-100 eps, DQN converge a política estable.

v9 etapas 75 eps:
- Tiempo suficiente para aprender (50+ eps exploración)
- Tiempo suficiente para estabilizar (25+ eps explotación)
- 4 etapas × 75 = 300 total (comparable v8)
```

### Anexo C: Transfer Learning Details

**Qué se transfiere**:
```python
# SÍ transfer entre etapas
agent.q_network.state_dict()      # Pesos Q-network
agent.target_network.state_dict() # Pesos target network
agent.memory                       # Replay buffer (opcional)

# NO reset entre etapas
agent.epsilon                      # Continúa decreciente
agent.optimizer.state_dict()       # Momentos Adam
```

**Rationale**:
- Pesos: Política aprendida se **adapta** (no reinicia)
- Epsilon: Exploración **decrece globalmente** (no vuelve a 1.0 cada etapa)
- Memory: Experiencias previas **informan** futuras (no olvida)

**Alternativa si falla**:
- v9.1: Reiniciar epsilon cada etapa (más exploración en transiciones)
- v9.2: Freeze early layers (solo tunear capas finales en etapas avanzadas)

### Anexo D: Cronograma Detallado

```
[3 dic 16:00] Inicio implementación v9
[3 dic 16:30] Test mode (1 config Curriculum, 30 eps/etapa)
[3 dic 16:35] Validación: transiciones etapas detectadas en CSV
[3 dic 16:40] Ejecución completa (9 configs)
[3 dic 16:50] Checkpoint: 50% completo
[3 dic 17:00] Checkpoint: 100% completo
[3 dic 17:05] Commit datos: "v9 RAW DATA - 9 configs (3 grupos × 3 seeds)"
[3 dic 17:10] Análisis comparaciones H9.1, H9.2, H9.3
[3 dic 17:20] Figuras
[3 dic 17:30] Commit análisis: "v9 ANALYSIS - curriculum effectiveness"
[4 dic 10:00] Redacción REPORTE_FINAL_v9.md
[4 dic 12:00] Commit reporte: "v9 FINAL - Reporte completo"
```

---

**FIN PREREGISTRO v9**

**Status**: 🔒 CONGELADO (v1.0)  
**Próxima acción**: Implementación código curriculum learning

---

## 📝 Historial de Versiones

### v1.0 (3 dic 2025, pre-ejecución) ⭐ VERSIÓN INICIAL

**Creación**: Preregistro completo basado en lecciones v5-v8

**Hipótesis**:
- H9.1: Curriculum > Directo_S1 (mitigación over-alignment)
- H9.2: Curriculum < Control_S0 en tripwires (mantiene prudencia)
- H9.3: Curriculum > Directo_S1 en success rate (evita parálisis)
- H9.4: Degradación gradual NO súbita (exploratoria)

**Diseño**:
- 3 grupos: Curriculum (4 etapas), Directo_S1, Control_S0
- 3 seeds × 3 grupos = 9 configs
- 300 episodios/config
- Transfer learning entre etapas

**Métricas clave**:
- ratio_final (episodios 250-300)
- success_rate_final
- tripwires_final
- transfer_efficiency (etapa-a-etapa)
