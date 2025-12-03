# 📂 Experimento v9: Curriculum Learning para Mitigar Over-Alignment

**Título**: Curriculum Learning como Estrategia de Mitigación del Régimen de Over-Alignment  
**Fecha inicio**: 3 de diciembre de 2025  
**Status**: 🔄 EN PREPARACIÓN  
**Preregistro**: `PREREGISTRO_v9.md` (v1.0 - CONGELADO)

---

## 🎯 Objetivo

Investigar si el **curriculum learning** (escalamiento gradual de intensidad de shaping) puede mitigar el fenómeno de **over-alignment** descubierto en v8, donde s=1.0 causó parálisis conductual (84% timeouts, ratio 0.344).

**Pregunta central**: ¿Puede un entrenamiento por etapas (0.0→0.25→0.5→1.0) permitir al agente aprender balances intermedios y evitar parálisis final?

---

## 🔬 Diseño Experimental

### Grupos Experimentales (3)

1. **CURRICULUM** (grupo experimental)
   - 4 etapas secuenciales × 75 episodios = 300 total
   - Escalamiento: s=0.0 → s=0.25 → s=0.5 → s=1.0
   - Transfer learning: pesos Q-network continuos
   - Epsilon decreciente global (NO reset por etapa)

2. **DIRECTO_S1** (control positivo - réplica v8)
   - 300 episodios con s=1.0 constante desde inicio
   - Esperado: parálisis (ratio ~0.35, success ~16%)

3. **CONTROL_S0** (control negativo - baseline)
   - 300 episodios con s=0.0 (sin shaping)
   - Esperado: paridad (ratio ~0.99, success ~82%)

### Configuraciones

```
N_grupos = 3 (Curriculum, DirectoS1, ControlS0)
N_seeds = 3 (42, 123, 456)
N_configs = 3 × 3 = 9
N_episodes_per_config = 300
N_total_episodes = 2,700
```

### Variables Fijas

- **Grid**: 4×4
- **Densidad**: spawn_rate = 0.25
- **Economía**: Balanced (balance=5.0)
- **PGF penalties**: -100 × scale (v8 confirmado)
- **PGF bonus**: +50 × scale (v8 confirmado)
- **Arquitectura**: DQN 2×64 hidden
- **Hiperparámetros**: lr=0.001, γ=0.95, ε: 1.0→0.01

---

## 📊 Hipótesis Preregistradas

### H9.1: Curriculum Superior a Directo ⭐ (Principal)

> El agente Curriculum alcanzará ratio_reward_env_final ≥ 0.70, significativamente mayor que Directo_S1 (~0.35).

**Test**: t-test pareado, α=0.05, one-tailed

### H9.2: Curriculum Mantiene Prudencia ✅ (Validación)

> El agente Curriculum mostrará tripwires_final < Control_S0 × 0.80 (reducción ≥20%).

**Test**: t-test pareado, α=0.05, one-tailed

### H9.3: Curriculum Evita Parálisis 🎯 (Funcionalidad)

> El agente Curriculum tendrá success_rate_final ≥ 60%, significativamente mayor que Directo_S1 (~16%).

**Test**: t-test pareado, α=0.05, one-tailed

### H9.4: Degradación Gradual 📉 (Exploratoria)

> El ratio_reward_env en Curriculum decrece gradualmente a través de etapas, NO colapsa súbitamente en etapa 4.

**Patrón esperado**: Monotónico decreciente con pendiente <0.15 por etapa

---

## 📁 Estructura de Archivos

```
pgf_v9/
├── PREREGISTRO_v9.md          # Diseño experimental completo (v1.0 CONGELADO)
├── README.md                   # Este archivo
├── TRACKING_v9.md              # Log de ejecución
├── resultados/                 # CSVs + JSONs por config (9 archivos × 2)
│   ├── exp9_Curriculum_seed42_episodes.csv
│   ├── exp9_Curriculum_seed42_metrics.json
│   ├── exp9_DirectoS1_seed42_episodes.csv
│   ├── exp9_DirectoS1_seed42_metrics.json
│   ├── exp9_ControlS0_seed42_episodes.csv
│   └── ... (27 archivos total)
├── analisis/                   # Outputs análisis estadístico
│   ├── curriculum_effectiveness.json
│   ├── temporal_stages.json
│   └── transfer_learning.json
├── figuras/                    # Visualizaciones
│   ├── fig1_learning_curves_by_group.png
│   ├── fig2_barplot_ratios_final.png
│   ├── fig3_scatter_safety_reward_final.png
│   └── fig4_transfer_efficiency.png
└── reportes/                   # Reporte final narrativo
    └── REPORTE_FINAL_v9.md
```

---

## 🔑 Métricas Clave

### Primarias

- **ratio_reward_env_final**: PGF/Control en episodios 250-300
- **success_rate_final**: % goal_reached en episodios 250-300
- **tripwires_final**: Mean tripwires/episode en episodios 250-300

### Secundarias

- **transfer_efficiency**: Retención de performance entre etapas
- **ratio_por_etapa**: Evolución temporal del ratio (4 etapas)

### Columnas CSV Requeridas

```python
# Identificación
episode, agent_type, group, seed

# Curriculum específico
stage              # 1-4 (solo Curriculum), null para otros
shaping_scale_current  # s actual en ese episodio

# Recompensas duales
total_reward_env
total_reward_shaped

# Seguridad
tripwires_triggered
deaths_starvation
deaths_tripwire

# Eficiencia
resources_collected
steps_to_goal
goal_reached

# Exploración
epsilon
```

---

## 📈 Escenarios y Criterios

### Escenario 1: Éxito ✅

```
Curriculum:  ratio_final = 0.75 ± 0.10, success = 70%, tripwires = 1.5
Directo_S1:  ratio_final = 0.35 ± 0.25, success = 16%, tripwires = 0.4
```

**Conclusión**: Curriculum **mitiga** over-alignment efectivamente.  
**Próximo paso**: v10 optimización (duración etapas, secuencias alternativas).

### Escenario 2: Intermedio ⚠️

```
Curriculum:  ratio_final = 0.55 ± 0.15, success = 45%, tripwires = 2.0
Directo_S1:  ratio_final = 0.35 ± 0.25, success = 16%, tripwires = 0.4
```

**Conclusión**: Curriculum **ayuda** pero insuficiente.  
**Próximo paso**: v9.1 más etapas (6 stages × 50 eps) o v9.2 secuencia alternativa.

### Escenario 3: Falla ❌

```
Curriculum:  ratio_final = 0.38 ± 0.20, success = 20%, tripwires = 0.5
Directo_S1:  ratio_final = 0.35 ± 0.25, success = 16%, tripwires = 0.4
```

**Conclusión**: s=1.0 es **inherentemente inentrenable** incluso con curriculum.  
**Próximo paso**: v10 con s_max = 0.6 (evitar s=1.0 completamente).

---

## 🔗 Contexto Experimental

### Basado en v8 (Over-Alignment Discovery)

**Hallazgo v8**:
- s=1.0 causa parálisis conductual súbita desde inicio
- Ratio: 0.344 (colapso funcional)
- Success: 16% (84% timeouts)
- Tripwires: casi cero (hiperconservación)

**Análisis temporal v8**:
- Over-alignment NO emerge gradualmente
- Agente "congela" política ultra-conservadora desde episodio 1
- NO tuvo oportunidad de explorar balances intermedios

**Ver**: `results/pgf_v8/reportes/REPORTE_FINAL_v8.md`

### Inspiración: Curriculum Learning

**Bengio et al. (2009)**: Aprendizaje más efectivo con ejemplos ordenados por dificultad.

**Narvekar et al. (2020)**: Curriculum learning en RL mejora sample efficiency y performance final.

**Hipótesis v9**: Escalamiento gradual de señal prudencial es análogo a curriculum de dificultad.

---

## 📚 Referencias

- **Preregistro**: `PREREGISTRO_v9.md` (diseño completo, 30 páginas)
- **Lecciones v5-v8**: `docs/LECCIONES_v5-v8.md` (consolidación, 76 páginas)
- **v8 Final Report**: `results/pgf_v8/reportes/REPORTE_FINAL_v8.md`
- **TUI Theory**: `docs/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md`
- **Environment**: `sim/environment_v2.py`
- **Agent**: `sim/dqn_agent.py`

---

## 🚀 Estado de Ejecución

**Pre-ejecución**:
- ✅ Preregistro v1.0 completo y congelado (3 dic 2025)
- ✅ Estructura de carpetas creada
- ✅ README documentado
- ⏳ TRACKING iniciado
- ⏳ Implementación código curriculum
- ⏳ Test mode
- ⏳ Ejecución completa

**Timeline estimado**:
- Implementación: ~30 min
- Test mode: ~2 min
- Ejecución: ~15 min (2,700 episodios)
- Análisis: ~10 min
- Reporte: ~30 min

**Deadline**: 4 diciembre 2025, 23:59

---

## 📝 Notas de Implementación

### Transfer Learning Details

**Qué se transfiere entre etapas**:
- ✅ `agent.q_network.state_dict()` (pesos Q-network)
- ✅ `agent.target_network.state_dict()` (pesos target)
- ✅ `agent.memory` (replay buffer, opcional)
- ✅ `agent.epsilon` (continúa decreciente, NO reset)
- ✅ `agent.optimizer.state_dict()` (momentos Adam)

**Qué se actualiza entre etapas**:
- `env.shaping_scale` (0.0 → 0.25 → 0.5 → 1.0)

**Validación crítica**:
```python
# Verificar que epsilon NO resetea
assert epsilon_end_stage1 > epsilon_start_stage2  # Debe continuar decreciente

# Verificar que pesos se transfieren
assert q_network_end_stage1 == q_network_start_stage2  # Mismos pesos
```

---

**FIN README v9**

**Fecha creación**: 3 diciembre 2025  
**Status**: 🔄 PREPARACIÓN  
**Próximo paso**: Implementar `scripts/run_experiment_9_curriculum.py`
