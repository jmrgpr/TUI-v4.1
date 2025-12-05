# 📋 PREREGISTRO EXPERIMENTAL: PGF v10_viable - Curriculum Progresivo con Economía Viable

**Título**: Curriculum Learning 4×4→6×6→8×8 con Transfer Learning en Economía Viable Post-Fixes  
**Investigador**: Sistema TUI v4.1  
**Fecha registro**: 5 de diciembre de 2025  
**Protocolo**: Preregistración anterior a ejecución  
**Versión experimento**: v10_viable ("Curriculum Progresivo Viable")  
**Versión preregistro**: 1.0  

---

## 📖 Resumen Ejecutivo

Este experimento valida el **curriculum learning progresivo** (escalamiento de complejidad espacial 4×4→6×6→8×8) bajo la **economía viable** definitiva de la serie v10.x, después de resolver dos bugs críticos que impedían el aprendizaje DQN.

**Contexto Post-Fixes**:
1. **Bug Goal Detection**: Resuelto por usuario (línea 167 environment.py) - goal requería `resources > 10` (imposible con balance 8.0)
2. **Bug Action Mapping**: Resuelto por análisis sistemático - DQNAgent.act() devolvía INT pero environment.step() esperaba STRING

**Economía Viable Validada**:
- Oráculo: 100% success en 4×4/6×6/8×8/16×16
- DQN post-fix: 93% success (500 eps), 61% success (100 eps) en 4×4

**Pregunta central**: ¿Puede un agente DQN entrenado progresivamente (4×4→6×6→8×8) con transfer learning mantener capacidad de generalización en grids complejos bajo economía viable?

---

## 🎯 Antecedentes y Motivación

### Resultados Serie v10.0-v10.6 (Estado del Arte)

**Economía Viable (confirmada físicamente posible)**:
```python
ENV_INITIAL_RESOURCES = 8.0           # Balance inicial
ENV_STEP_COST = -0.15                 # Costo por paso (autonomía ~53 steps)
ENV_PENALTY_LOW_RESOURCES = -0.5      # Penalty zona amarilla
ENV_RESOURCE_THRESHOLD_LOW = 1.0      # Umbral amarillo (12.5% balance)
ENV_GOAL_REWARD = 20.0                # Recompensa goal
ENV_RESOURCE_SPAWN_RATE = 0.40        # 40% celdas con recursos
```

**Validación Oráculo (A* óptimo)**:
| Grid | Success Rate | Resources Final |
|------|-------------|-----------------|
| 4×4  | 100%        | 6.85 ± 0.0      |
| 6×6  | 100%        | 6.35 ± 0.0      |
| 8×8  | 100%        | 5.85 ± 0.0      |
| 16×16| 100%        | 4.35 ± 0.0      |

**Bugs Resueltos (Dec 5, 2025)**:

1. **Goal Detection Fix (Usuario)**:
   - **Antes**: `if agent_pos == goal_pos and resources > 10` (línea 167)
   - **Después**: `if agent_pos == goal_pos`
   - **Impacto**: Imposible ganar con balance 8.0 inicial

2. **Action Mapping Fix (Análisis Sistemático)**:
   - **Problema**: DQNAgent.act() devuelve `int` → environment.step() espera `str`
   - **Solución**: `action_str = config.AGENT_ACTIONS[action_idx]`
   - **Evidencia**: verify_action_mapping_fix.py
     * Oráculo sin bug: 100% success
     * DQN con fix: 84% success (100 eps)
     * DQN sin fix: 0% success (agente congelado en (0,0))
     * **Delta**: +84% success rate

**Validación DQN Post-Fixes** (4×4):
- 500 episodios: 93% success, 466 goals alcanzados
- 100 episodios: 61% success
- Confirmación: Economía viable + fixes → aprendizaje funcional

### Serie v10.x NO Afectada por Bug Action Mapping

**Verificación código (scripts 10.0-10.6)**:
- Todos usaban `actions_map[action]` correctamente
- Ejemplo exp 10.3: 31.6% success (imposible si agent congelado)
- **Conclusión**: Serie 10.0-10.6 tiene resultados VÁLIDOS

### Hipótesis Motivadora

**Inspiración**: Curriculum learning espacial (Narvekar et al., 2020; OpenAI Five progression)

**Intuición**:
> Si el agente **primero** domina navegación 4×4 (baja complejidad), luego transfiere conocimiento a 6×6 (complejidad media), y **gradualmente** escala hasta 8×8 (alta complejidad), podrá generalizar políticas sin colapsar ante horizonte largo.

**Mecanismo propuesto**:
1. **Fase 1 (4×4)**: Aprende navegación básica, gestión recursos, goal-seeking (gate >80%)
2. **Fase 2 (6×6)**: Extiende horizonte temporal, mantiene prudencia (gate >20%, transfer learning)
3. **Fase 3 (8×8)**: Alta complejidad espacial, gestión recursos sofisticada (gate >10%, transfer learning)

**Contraste con entrenamiento directo 8×8**:
- Directo 8×8: Agente explora espacio enorme sin base (alta probabilidad timeout/colapso)
- Curriculum 4→6→8: Agente **reutiliza** políticas aprendidas en grids simples

### Gap Metodológico

**v10.0-v10.6 exploraron economías**, v10_viable testa **curriculum progresivo** bajo economía definitiva post-fixes.

---

## 🔬 Diseño Experimental

### Variables Independientes

#### Factor 1: GRID_SIZE (Principal)

**Tipo**: Ordinal, 3 niveles (fases curriculares)
**Valores**: {4×4, 6×6, 8×8}

**Operacionalización**:

```python
def train_progressive_curriculum(seed):
    """
    Curriculum completo con transfer learning entre fases
    """
    # Fase 1: 4×4 (fundacional)
    agent_4x4 = train_phase_4x4(
        episodes=500,
        grid_size=4,
        max_steps=24,
        seed=seed
    )
    # Gate: success_rate > 80% (últimos 50 eps)
    if not gate_4x4_passed(agent_4x4):
        raise EarlyStoppingError("Fase 1 no superó gate 80%")
    
    # Fase 2: 6×6 (transfer learning desde 4×4)
    agent_6x6 = train_phase_6x6(
        episodes=1000,
        grid_size=6,
        max_steps=30,
        seed=seed,
        initial_weights=agent_4x4.q_network.state_dict()  # Transfer
    )
    # Gate: success_rate > 20% (últimos 100 eps)
    if not gate_6x6_passed(agent_6x6):
        raise EarlyStoppingError("Fase 2 no superó gate 20%")
    
    # Fase 3: 8×8 (transfer learning desde 6×6)
    agent_8x8 = train_phase_8x8(
        episodes=1000,
        grid_size=8,
        max_steps=42,
        seed=seed,
        initial_weights=agent_6x6.q_network.state_dict()  # Transfer
    )
    # Gate: success_rate > 10% (últimos 100 eps)
    
    return {
        '4x4': agent_4x4,
        '6x6': agent_6x6,
        '8x8': agent_8x8
    }
```

**Episodios por Fase**:
- Fase 1 (4×4): 500 episodios
- Fase 2 (6×6): 1000 episodios
- Fase 3 (8×8): 1000 episodios
- **Total**: 2500 episodios

**Max Steps por Grid** (75% distancia Manhattan + buffer):
- 4×4: 24 steps (Manhattan=6, buffer ×4)
- 6×6: 30 steps (Manhattan=10, buffer ×3)
- 8×8: 42 steps (Manhattan=14, buffer ×3)

#### Factor 2: SEED (Replicación)

**Tipo**: Categórica, 1 nivel (experimento único)
**Valor**: {42}
**Justificación**: Experimento exploratorio inicial, N=1 suficiente para validar viabilidad técnica

**Control**: Seeding completo
```python
import random
import numpy as np
import torch

random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)
```

### Variables Dependientes (DVs)

#### DV1: Success Rate por Fase (Principal)

**Definición**:
```python
success_rate_fase = n_goals_reached / n_episodes_fase
```

**Ventanas análisis**:
- Fase 1: Últimos 50 episodios (450-500)
- Fase 2: Últimos 100 episodios (900-1000)
- Fase 3: Últimos 100 episodios (900-1000)

**Interpretación**:
- `≥ 80%` (Fase 1): Base sólida para transfer
- `≥ 20%` (Fase 2): Transfer efectivo
- `≥ 10%` (Fase 3): Generalización viable

#### DV2: Resources Final (Eficiencia)

**Definición**:
```python
resources_final_mean = mean(resources_at_goal | goal_reached == True)
```

**Criterio eficiencia**:
- Mayor resources_final → trayectoria más eficiente (menos pasos)
- Comparación con oráculo:
  * 4×4: 6.85 (óptimo A*)
  * 6×6: 6.35 (óptimo A*)
  * 8×8: 5.85 (óptimo A*)

#### DV3: Steps to Goal (Complejidad trayectoria)

**Definición**:
```python
steps_to_goal_mean = mean(steps | goal_reached == True)
```

**Baseline óptimo**:
- 4×4: ~8 steps (Manhattan distance)
- 6×6: ~10 steps
- 8×8: ~14 steps

**Ratio eficiencia**:
```python
ratio_optimalidad = steps_to_goal_mean / manhattan_distance_mean
```
- `≤ 1.5`: Trayectorias razonables
- `> 2.0`: Exploración ineficiente

#### DV4: Tripwires Evitados (Prudencia)

**Definición**:
```python
tripwires_avoided = mean(1 - (tripwires_triggered / max_possible_tripwires))
```

**Interpretación**:
- `> 0.90`: Alta prudencia (evita riesgos conocidos)
- `< 0.70`: Exploración temeraria

### Variables de Confusión (Controladas)

**Arquitectura DQN**:
```python
Q_HIDDEN_DIM = 128              # Capacidad representación
Q_LR = 0.001                    # Learning rate
Q_GAMMA = 0.95                  # Factor descuento
Q_BUFFER_SIZE = 10000           # Experience replay
Q_BATCH_SIZE = 32               # Mini-batch size
Q_UPDATE_EVERY = 4              # Target network update frequency
```

**Exploración**:
```python
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.999           # Decay global (NO reset entre fases)
```

**Economía Viable** (fija todas las fases):
```python
ENV_INITIAL_RESOURCES = 8.0
ENV_STEP_COST = -0.15
ENV_PENALTY_LOW_RESOURCES = -0.5
ENV_RESOURCE_THRESHOLD_LOW = 1.0
ENV_GOAL_REWARD = 20.0
ENV_RESOURCE_SPAWN_RATE = 0.40
```

**Posiciones Iniciales**:
- Spawn aleatorio cada episodio
- Goal aleatorio cada episodio
- Garantía: Manhattan distance ≥ 3 (evitar trivialidad)

---

## 📊 Hipótesis Preregistradas

### H10_viable.1: Curriculum 4×4 Alcanza Base Sólida ⭐ (Principal)

**Enunciado**:
> El agente alcanzará success_rate ≥ 80% en últimos 50 episodios de Fase 1 (4×4).

**Justificación**:
- Oráculo validó 100% posible
- DQN post-fixes alcanzó 93% (500 eps)
- Grid pequeño → espacio exploración manejable

**Test**:
```python
success_rate_4x4 = n_goals[450:500] / 50
H1_supported = success_rate_4x4 >= 0.80
```

**Criterio**: Rechazar si success_rate < 80% (falla fundacional)

---

### H10_viable.2: Transfer Learning 6×6 Efectivo ✅ (Validación)

**Enunciado**:
> El agente alcanzará success_rate ≥ 20% en últimos 100 episodios de Fase 2 (6×6) con transfer learning desde 4×4.

**Justificación**:
- Transfer learning reduce tiempo convergencia
- Complejidad media → exploración viable con base 4×4
- Gate 20% realista para grid 6×6 (vs 100% oráculo benchmark)

**Test**:
```python
success_rate_6x6 = n_goals[900:1000] / 100
H2_supported = success_rate_6x6 >= 0.20
```

**Criterio**: Rechazar si success_rate < 20% (falla transfer)

---

### H10_viable.3: Generalización 8×8 Viable 🎯 (Funcionalidad)

**Enunciado**:
> El agente alcanzará success_rate ≥ 10% en últimos 100 episodios de Fase 3 (8×8) con transfer learning desde 6×6.

**Justificación**:
- Alta complejidad espacial (64 celdas)
- Horizonte largo (max_steps=42)
- Gate 10% conservador (vs 100% oráculo benchmark)

**Test**:
```python
success_rate_8x8 = n_goals[900:1000] / 100
H3_supported = success_rate_8x8 >= 0.10
```

**Criterio**: Rechazar si success_rate < 10% (falla generalización)

---

### H10_viable.4: Eficiencia Decreciente con Complejidad 📉 (Exploratoria)

**Enunciado**:
> El ratio_optimalidad = steps_to_goal / manhattan_distance aumenta monotónicamente con grid_size.

**Patrón esperado**:
```
ratio_4x4 < ratio_6x6 < ratio_8x8
```

**Interpretación**:
- Grids grandes → trayectorias menos óptimas (más exploración)
- NO colapso súbito (ratio_8x8 < 3.0)

**Test**:
```python
ratio_4x4 = mean(steps_to_goal_4x4) / mean(manhattan_4x4)
ratio_6x6 = mean(steps_to_goal_6x6) / mean(manhattan_6x6)
ratio_8x8 = mean(steps_to_goal_8x8) / mean(manhattan_8x8)

H4_supported = (ratio_4x4 < ratio_6x6) and (ratio_6x6 < ratio_8x8) and (ratio_8x8 < 3.0)
```

---

## 📁 Plan de Análisis

### Análisis Primarios (Confirmatorios)

**AP1: Verificación Gates**
```python
# Fase 1: 4×4
assert success_rate_4x4[-50:].mean() >= 0.80, "GATE 1 FAILED"

# Fase 2: 6×6
assert success_rate_6x6[-100:].mean() >= 0.20, "GATE 2 FAILED"

# Fase 3: 8×8
assert success_rate_8x8[-100:].mean() >= 0.10, "GATE 3 FAILED"
```

**AP2: Análisis Temporal por Fase**
```python
def analyze_learning_curve(df_episodes, phase_name):
    """
    Ventanas móviles 50 eps para detectar:
    - Convergencia
    - Mesetas
    - Colapsos
    """
    window_size = 50
    success_rolling = df_episodes['goal_reached'].rolling(window_size).mean()
    
    plot_learning_curve(success_rolling, phase_name)
    
    return {
        'convergence_episode': first_stable_window(success_rolling),
        'final_success_rate': success_rolling.iloc[-1],
        'peak_success_rate': success_rolling.max()
    }
```

**AP3: Comparación con Oráculo**
```python
# Eficiencia relativa al óptimo
for grid_size in ['4x4', '6x6', '8x8']:
    oracle_steps = ORACLE_BENCHMARKS[grid_size]['steps_mean']
    agent_steps = df[df['grid'] == grid_size]['steps_to_goal'].mean()
    
    ratio_optimalidad = agent_steps / oracle_steps
    
    print(f"{grid_size}: Agent {agent_steps:.1f} vs Oracle {oracle_steps:.1f} (ratio {ratio_optimalidad:.2f})")
```

### Análisis Secundarios (Exploratorios)

**AS1: Efectividad Transfer Learning**
```python
# Comparar primeros 100 eps de cada fase
def compare_transfer_effectiveness():
    success_early_4x4 = df_4x4[:100]['goal_reached'].mean()
    success_early_6x6 = df_6x6[:100]['goal_reached'].mean()
    success_early_8x8 = df_8x8[:100]['goal_reached'].mean()
    
    # Hipótesis: Transfer acelera convergencia temprana
    # Esperado: success_early_6x6 > success_early_4x4 (conocimiento previo)
    
    return {
        'early_4x4': success_early_4x4,
        'early_6x6': success_early_6x6,
        'early_8x8': success_early_8x8,
        'transfer_boost_6x6': success_early_6x6 - success_early_4x4,
        'transfer_boost_8x8': success_early_8x8 - success_early_6x6
    }
```

**AS2: Análisis Prudencia (Tripwires)**
```python
# Evolución aversión a riesgos por fase
tripwires_ratio_4x4 = df_4x4['tripwires_triggered'].mean()
tripwires_ratio_6x6 = df_6x6['tripwires_triggered'].mean()
tripwires_ratio_8x8 = df_8x8['tripwires_triggered'].mean()

# Hipótesis exploratoria: Prudencia aumenta con complejidad
# (agente aprende a evitar recursos peligrosos)
```

**AS3: Visualizaciones Trayectorias**
```python
# Heatmaps visitas por celda (últimos 100 eps por fase)
def plot_visitation_heatmap(df_phase, grid_size):
    """
    Identificar:
    - Zonas exploradas frecuentemente
    - Caminos preferidos
    - Celdas evitadas (posible aprendizaje tripwires)
    """
    pass
```

### Criterios Desviación del Preregistro

**Permitidas (exploratorias)**:
- Análisis adicionales de trayectorias
- Visualizaciones no especificadas
- Tests estadísticos complementarios

**NO permitidas (confirmatorias)**:
- Cambiar umbrales gates (80/20/10)
- Modificar definiciones DVs
- Excluir outliers sin justificación a priori

---

## 📋 Protocolo Ejecución

### Checkpoints Guardado

**Frecuencia**: Cada 100 episodios
**Contenido**:
```python
checkpoint = {
    'episode': episode_num,
    'phase': phase_name,
    'q_network_state': agent.q_network.state_dict(),
    'optimizer_state': agent.optimizer.state_dict(),
    'epsilon': agent.epsilon,
    'metrics_summary': {
        'success_rate_last_50': success_rate,
        'mean_reward': mean_reward,
        'mean_steps': mean_steps
    }
}
torch.save(checkpoint, f'checkpoint_{phase}_{episode}.pth')
```

### Logs Detallados

**Por episodio (CSV)**:
```
episode, phase, grid_size, seed, goal_reached, steps, resources_final,
reward_total, reward_env, reward_pgf, tripwires_triggered, 
agent_start_pos, goal_pos, manhattan_distance
```

**Por fase (JSON)**:
```json
{
  "phase_name": "4x4",
  "episodes": 500,
  "success_rate_final": 0.92,
  "success_rate_by_window": [...],
  "mean_reward_env": 18.5,
  "mean_steps_to_goal": 12.3,
  "convergence_episode": 287,
  "gate_passed": true
}
```

### Condiciones Early Stopping

**Gate failures**:
```python
if success_rate_4x4[-50:].mean() < 0.80:
    print("⚠️ FASE 1 NO SUPERÓ GATE 80%")
    print("Detención early stopping - No proceder a Fase 2")
    sys.exit(1)

if success_rate_6x6[-100:].mean() < 0.20:
    print("⚠️ FASE 2 NO SUPERÓ GATE 20%")
    print("Detención early stopping - No proceder a Fase 3")
    sys.exit(1)
```

**Divergencia catastrófica**:
```python
# Ventana 100 eps sin un solo goal
if df[-100:]['goal_reached'].sum() == 0:
    print("⚠️ DIVERGENCIA CATASTRÓFICA - 100 eps sin goal")
    sys.exit(1)
```

---

## 🔍 Criterios Interpretación

### Éxito Completo (H1+H2+H3 soportadas)

**Condiciones**:
```
success_rate_4x4 >= 80% AND
success_rate_6x6 >= 20% AND
success_rate_8x8 >= 10%
```

**Interpretación**:
> Curriculum progresivo con transfer learning es **viable** bajo economía viable. Agente generaliza desde grids simples a complejos sin colapsar.

**Siguiente paso**: Replicación N=10 con múltiples seeds

---

### Éxito Parcial (H1+H2 soportadas, H3 falla)

**Condiciones**:
```
success_rate_4x4 >= 80% AND
success_rate_6x6 >= 20% AND
success_rate_8x8 < 10%
```

**Interpretación**:
> Transfer learning efectivo hasta 6×6, pero 8×8 excede capacidad generalización. Posible necesidad:
- Aumentar episodios Fase 3 (1000 → 2000)
- Ajustar arquitectura (hidden_dim 128 → 256)
- Fase intermedia 7×7

---

### Falla Transfer Learning (H1 soportada, H2 falla)

**Condiciones**:
```
success_rate_4x4 >= 80% AND
success_rate_6x6 < 20%
```

**Interpretación**:
> Base 4×4 sólida, pero transfer 4→6 inefectivo. Posibles causas:
- Jump complejidad demasiado grande (4→6)
- Transfer pesos subóptimo (revisar inicialización)
- Epsilon decay muy rápido (exploration insuficiente Fase 2)

**Acción**: Agregar fase intermedia 5×5 o aumentar episodios Fase 2

---

### Falla Fundacional (H1 falla)

**Condiciones**:
```
success_rate_4x4 < 80%
```

**Interpretación**:
> Problema fundamental economía viable o arquitectura DQN. Reevaluar:
- Hiperparámetros (learning rate, gamma, epsilon decay)
- Arquitectura (hidden_dim insuficiente)
- Economía (posible bug no detectado)

**Acción**: Debugging profundo antes de continuar curriculum

---

## 📚 Referencias Metodológicas

**Curriculum Learning**:
- Bengio et al. (2009). "Curriculum Learning". ICML
- Narvekar et al. (2020). "Curriculum Learning for Reinforcement Learning Domains". JMLR

**Transfer Learning RL**:
- Taylor & Stone (2009). "Transfer Learning for Reinforcement Learning Domains". JMLR
- Rusu et al. (2016). "Progressive Neural Networks". arXiv:1606.04671

**Preregistration**:
- Open Science Framework guidelines
- Nosek et al. (2018). "The preregistration revolution". PNAS

---

## 🔒 Congelamiento Preregistro

**Versión**: 1.0  
**Fecha**: 5 de diciembre de 2025  
**Status**: 🔒 **CONGELADO** - No se permitirán modificaciones post-ejecución

**Compromiso reproducibilidad**:
- Toda desviación será documentada explícitamente
- Análisis exploratorios serán marcados como "NO preregistrados"
- Resultados negativos serán reportados sin censura

**Firma Digital (Commit Hash)**: [PENDIENTE - Commit antes de ejecutar]

---

## 📧 Contacto

**Investigador**: Sistema TUI v4.1  
**Repositorio**: TUI-v4.1 (GitHub)  
**Tracking**: `results/pgf_v10_viable/TRACKING_v10_viable.md`

---

**END OF PREREGISTRATION v1.0** 🔒
