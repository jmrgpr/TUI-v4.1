# 📂 Experimento v10_viable: Curriculum Progresivo con Economía Viable Post-Fixes

**Título**: Curriculum Learning 4×4→6×6→8×8 con Transfer Learning en Economía Viable  
**Fecha inicio**: 5 de diciembre de 2025  
**Status**: 🔄 EN PREPARACIÓN  
**Preregistro**: `PREREGISTRO_v10_viable.md` (v1.0 - CONGELADO)

---

## 🎯 Objetivo

Validar el **curriculum learning progresivo** (escalamiento de complejidad espacial 4×4→6×6→8×8) bajo la **economía viable** definitiva de la serie v10.x, después de resolver dos bugs críticos que impedían el aprendizaje DQN.

**Pregunta central**: ¿Puede un agente DQN entrenado progresivamente con transfer learning mantener capacidad de generalización en grids complejos bajo economía viable?

---

## 🔧 Contexto Post-Fixes

### Bugs Resueltos (Dec 5, 2025)

#### Bug 1: Goal Detection (Resuelto por Usuario)

**Problema**: Goal requería `resources > 10` (imposible con balance 8.0)
```python
# environment.py línea 167 (ANTES)
if agent_pos == goal_pos and resources > 10:
    done = True

# environment.py línea 167 (DESPUÉS)
if agent_pos == goal_pos:
    done = True
```

**Impacto**: 
- Oráculo: 0% success → **100% success** (4×4/6×6/8×8/16×16)
- Economía viable físicamente imposible de ganar antes del fix

---

#### Bug 2: Action Mapping (Resuelto por Análisis Sistemático)

**Problema**: Type mismatch INT vs STRING
```python
# DQNAgent.act() devolvía INT
action = torch.argmax(q_values).item()  # → int

# environment.step() esperaba STRING
action = 'up'  # → str
```

**Solución**: Mapeo en scripts
```python
action_idx = agent.act(state)  # INT
action_str = config.AGENT_ACTIONS[action_idx]  # STRING
next_state, reward, done, info = env.step(action_str)
```

**Evidencia** (`scripts/verify_action_mapping_fix.py`):
| Configuración | Success Rate |
|---------------|--------------|
| Oráculo (sin bug) | 100% |
| DQN con fix | 84% (100 eps) |
| DQN sin fix | 0% (agente congelado) |
| **Delta** | **+84%** |

**Validación adicional** (4×4):
- 500 episodios: **93% success**, 466 goals alcanzados
- 100 episodios: **61% success**

---

### Serie v10.0-v10.6 NO Afectada

**Verificación código**: Scripts 10.0-10.6 usaban `actions_map[action]` correctamente

**Evidencia resultados válidos**:
- Experimento 10.3: 31.6% success (imposible si agent congelado)
- Conclusión: Serie 10.0-10.6 tiene resultados **VÁLIDOS**

---

## 🔬 Diseño Experimental

### Economía Viable (Configuración Definitiva)

```python
# sim/config.py (líneas 47-77)
ENV_INITIAL_RESOURCES = 8.0           # Balance inicial
ENV_STEP_COST = -0.15                 # Costo por paso (autonomía ~53 steps)
ENV_PENALTY_LOW_RESOURCES = -0.5      # Penalty zona amarilla
ENV_RESOURCE_THRESHOLD_LOW = 1.0      # Umbral amarillo (12.5%)
ENV_GOAL_REWARD = 20.0                # Recompensa goal
ENV_RESOURCE_SPAWN_RATE = 0.40        # 40% celdas con recursos
```

**Validación Oráculo (A* óptimo)**:
| Grid | Success | Resources Final | Steps Mean |
|------|---------|-----------------|------------|
| 4×4  | 100%    | 6.85 ± 0.0      | ~8         |
| 6×6  | 100%    | 6.35 ± 0.0      | ~10        |
| 8×8  | 100%    | 5.85 ± 0.0      | ~14        |
| 16×16| 100%    | 4.35 ± 0.0      | ~20        |

---

### Fases Curriculum

#### Fase 1: 4×4 (Fundacional)
- **Episodios**: 500
- **Max steps**: 24
- **Gate**: success_rate ≥ 80% (últimos 50 eps)
- **Objetivo**: Base sólida navegación + gestión recursos

#### Fase 2: 6×6 (Transfer Learning)
- **Episodios**: 1000
- **Max steps**: 30
- **Gate**: success_rate ≥ 20% (últimos 100 eps)
- **Transfer**: Pesos Q-network desde Fase 1
- **Objetivo**: Generalización complejidad media

#### Fase 3: 8×8 (Alta Complejidad)
- **Episodios**: 1000
- **Max steps**: 42
- **Gate**: success_rate ≥ 10% (últimos 100 eps)
- **Transfer**: Pesos Q-network desde Fase 2
- **Objetivo**: Validar generalización espacial compleja

---

### Configuración DQN

```python
# Arquitectura
Q_HIDDEN_DIM = 128              # Capacidad representación aumentada
Q_LR = 0.001                    # Learning rate
Q_GAMMA = 0.95                  # Factor descuento
Q_BUFFER_SIZE = 10000           # Experience replay
Q_BATCH_SIZE = 32               # Mini-batch size

# Exploración
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.999           # Decay global (NO reset entre fases)
```

---

### Seed Experimental

**N = 1** (experimento exploratorio inicial)
- **Seed**: 42
- **Justificación**: Validación viabilidad técnica antes de replicación N=10

---

## 📊 Hipótesis Preregistradas

### H10_viable.1: Base 4×4 Sólida ⭐

> El agente alcanzará **success_rate ≥ 80%** en últimos 50 episodios de Fase 1 (4×4).

**Criterio éxito**: Rechazar si success_rate < 80% (falla fundacional)

---

### H10_viable.2: Transfer Learning 6×6 ✅

> El agente alcanzará **success_rate ≥ 20%** en últimos 100 episodios de Fase 2 (6×6).

**Criterio éxito**: Rechazar si success_rate < 20% (falla transfer)

---

### H10_viable.3: Generalización 8×8 🎯

> El agente alcanzará **success_rate ≥ 10%** en últimos 100 episodios de Fase 3 (8×8).

**Criterio éxito**: Rechazar si success_rate < 10% (falla generalización)

---

### H10_viable.4: Eficiencia Decreciente 📉

> El ratio_optimalidad = steps_to_goal / manhattan_distance aumenta monotónicamente con grid_size.

**Patrón esperado**: `ratio_4x4 < ratio_6x6 < ratio_8x8` (grids grandes → menos óptimos)

---

## 📁 Estructura de Archivos

```
pgf_v10_viable/
├── PREREGISTRO_v10_viable.md   # Diseño experimental completo (v1.0 CONGELADO)
├── README.md                    # Este archivo
├── TRACKING_v10_viable.md       # Log de ejecución (a crear)
├── resultados/                  # CSVs + JSONs por fase
│   ├── curriculum_4x4_seed42_episodes.csv
│   ├── curriculum_4x4_seed42_metrics.json
│   ├── curriculum_6x6_seed42_episodes.csv
│   ├── curriculum_6x6_seed42_metrics.json
│   ├── curriculum_8x8_seed42_episodes.csv
│   ├── curriculum_8x8_seed42_metrics.json
│   └── curriculum_summary_seed42.csv
├── analisis/                    # Outputs análisis estadístico
│   ├── learning_curves_by_phase.png
│   ├── transfer_effectiveness.csv
│   └── hypothesis_testing.txt
├── figuras/                     # Visualizaciones
│   ├── success_rate_progression.png
│   ├── heatmaps_visitation_4x4.png
│   ├── heatmaps_visitation_6x6.png
│   └── heatmaps_visitation_8x8.png
├── exploratorios/               # Análisis NO preregistrados
│   └── tripwires_analysis.ipynb
└── reportes/                    # Reporte final
    └── REPORTE_FINAL_v10_viable.md
```

---

## 📈 Métricas Esperadas

### Benchmarks Pre-Fixes (Referencia)

| Métrica | Oráculo 4×4 | DQN Post-Fix 4×4 |
|---------|-------------|------------------|
| Success Rate | 100% | 93% (500 eps) |
| Resources Final | 6.85 | ~6.5 |
| Steps to Goal | 8 | ~12 |

### Objetivos Curriculum

| Fase | Grid | Success Gate | Episodios |
|------|------|-------------|-----------|
| 1    | 4×4  | ≥ 80%       | 500       |
| 2    | 6×6  | ≥ 20%       | 1000      |
| 3    | 8×8  | ≥ 10%       | 1000      |

---

## 🔍 Criterios Interpretación

### ✅ Éxito Completo (H1+H2+H3)

**Condiciones**:
```
success_rate_4x4 ≥ 80% AND
success_rate_6x6 ≥ 20% AND
success_rate_8x8 ≥ 10%
```

**Interpretación**: Curriculum progresivo viable. Proceder a replicación N=10.

---

### ⚠️ Éxito Parcial (H1+H2, NO H3)

**Condiciones**:
```
success_rate_4x4 ≥ 80% AND
success_rate_6x6 ≥ 20% AND
success_rate_8x8 < 10%
```

**Interpretación**: Transfer efectivo hasta 6×6. Necesita ajustes para 8×8.

**Acción**: Aumentar episodios Fase 3 o agregar fase intermedia 7×7.

---

### ❌ Falla Transfer (H1 OK, NO H2)

**Condiciones**:
```
success_rate_4x4 ≥ 80% AND
success_rate_6x6 < 20%
```

**Interpretación**: Base sólida pero transfer 4→6 inefectivo.

**Acción**: Revisar jump complejidad (agregar fase 5×5) o aumentar episodios Fase 2.

---

### 🚨 Falla Fundacional (NO H1)

**Condiciones**:
```
success_rate_4x4 < 80%
```

**Interpretación**: Problema fundamental economía/arquitectura.

**Acción**: Debugging profundo antes de continuar curriculum.

---

## 🚀 Scripts Ejecución

### Script Principal

```bash
python scripts/run_curriculum_complete_viable.py
```

**Duración estimada**: 30-40 minutos (2500 episodios total)

**Outputs**:
- `results/pgf_v10_viable/resultados/curriculum_*_seed42_episodes.csv`
- `results/pgf_v10_viable/resultados/curriculum_*_seed42_metrics.json`
- Checkpoints cada 100 episodios: `checkpoints/phase*_ep*.pth`

---

### Script Validación Rápida

```bash
python scripts/run_curriculum_quick_validate_viable.py
```

**Duración**: ~5 minutos (100 eps/fase = 300 total)

**Uso**: Smoke test pre-ejecución completa

---

## 📚 Documentos Relacionados

### Serie v10.x

- `results/pgf_v10.3/REPORTE_FINAL_v10.3.md` - Adaptive curriculum 8×8
- `results/pgf_v10.4/README.md` - Economía austera
- `results/pgf_v10.5/README.md` - Economía generosa
- `results/pgf_v10.6_exploratory_16x16/README.md` - Exploración 16×16

### Debugging Post-Fixes

- `scripts/verify_action_mapping_fix.py` - Evidencia bug action mapping
- `scripts/run_validation_4x4_FIXED.py` - Validación 93% success

### Preregistros Previos

- `results/pgf_v9/PREREGISTRO_v9.md` - Curriculum learning shaping
- `results/pgf_v9.1/PREREGISTRO_v9.1.md` - Validación robusta N=10

---

## 📋 Checklist Pre-Ejecución

- [x] Bugs goal detection y action mapping resueltos
- [x] Economía viable validada con oráculo (100% success)
- [x] DQN post-fixes validado (93% success 4×4)
- [x] Preregistro v1.0 congelado
- [x] Scripts curriculum completo creados
- [x] Estructura carpetas estándar creada
- [x] README documentación completa
- [ ] **Commit preregistro** (antes de ejecutar)
- [ ] Ejecutar `run_curriculum_complete_viable.py`
- [ ] Crear `TRACKING_v10_viable.md` durante ejecución

---

## 🔗 Próximos Pasos

1. **Commit preregistro** → Congelar diseño experimental
2. **Ejecutar curriculum completo** → 2500 episodios (~30-40 min)
3. **Análisis resultados** → Verificar H1/H2/H3/H4
4. **Reporte final** → Documentar hallazgos
5. **SI éxito completo** → Replicación N=10 con múltiples seeds
6. **SI éxito parcial/falla** → Ajustes diseño según criterios interpretación

---

## 📧 Contacto

**Investigador**: Sistema TUI v4.1  
**Repositorio**: TUI-v4.1 (GitHub)  
**Tracking**: `results/pgf_v10_viable/TRACKING_v10_viable.md` (a crear)

---

**Status**: 🔄 **PREPARADO PARA EJECUCIÓN** - Esperando confirmación usuario

**Última actualización**: 5 de diciembre de 2025
