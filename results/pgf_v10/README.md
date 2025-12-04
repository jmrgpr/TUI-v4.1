# 📂 Experimento v10: Adaptive Curriculum Learning en 8×8

**Título**: Adaptive Curriculum Learning para Escalamiento Robusto en Grids de Alta Complejidad  
**Fecha inicio**: 4 de diciembre de 2025 (desarrollo), 5-6 dic (ejecución)  
**Status**: 🔄 EN PREPARACIÓN (ejecutar DESPUÉS de v9.1)  
**Preregistro**: `PREREGISTRO_v10.md` (v1.0 - CONGELADO)  
**Predecesores**: v9 (4×4 curriculum fijo, N=3), v9.1 (4×4, N=10 validación)

---

## 🎯 Objetivo

**Escalar curriculum learning a grid 8×8** (complejidad alta) mediante **curriculum adaptativo** con transiciones threshold-based, resolviendo el colapso observado en proyecciones v9 (ratio=0.507, 41% success en 8×8 con curriculum fijo).

**Pregunta central**: ¿Un curriculum que avanza solo cuando el agente demuestra dominio (success_rate>0.75) puede alcanzar paridad en 8×8?

**Innovación metodológica**:
- **Transiciones threshold-based**: Avanzar a siguiente escala SOLO si success>0.75 en últimos 25 eps
- **Personalización por seed**: Cada seed progresa a su propio ritmo
- **5 etapas** (vs 4 en v9): [0.0→0.25→0.5→**0.75**→1.0]
- **Timeout**: Máximo 150 eps/etapa (evita estancamiento)

---

## 🔬 Diseño Experimental

### Grupos Experimentales (3)

1. **CONTROL_S0** (Baseline capacidad 8×8)
   - 400 eps con s=0.0 (sin shaping)
   - Mide capacidad máxima agente en 8×8
   - Esperado: 95-100% success (si DQN 2×64 es suficiente)

2. **FIXED_CURRICULUM** (Control experimental)
   - 4 etapas fijas: s=0.0→0.25→0.5→1.0
   - **100 eps/etapa** (vs 75 en v9, escalado por complejidad)
   - Total: 400 eps
   - Réplica v9 protocol en 8×8

3. **ADAPTIVE_CURRICULUM** (Experimental, innovación)
   - **5 etapas**: s=0.0→0.25→0.5→**0.75**→1.0
   - Transición: Avanza SI `success_rate_last_25 > 0.75` OR `episodes_in_stage > 150`
   - Episodios variables por etapa (personalizado)
   - Máximo total: 500 eps

### Configuraciones

```
N_grupos = 3 (ControlS0, FixedCurriculum, AdaptiveCurriculum)
N_seeds = 5 (42, 123, 456, 789, 101112)
Grid_size = 8×8 (64 celdas)
N_configs = 3 × 5 = 15
N_episodes_approx = 15 × 400 = 6,000
```

**Tiempo estimado**: ~8 horas cómputo

---

## 📊 Hipótesis Preregistradas

### H10.1: Adaptive Alcanza Paridad en 8×8 ⭐ (Principal)

> Adaptive ratio ≥ 0.70 (paridad parcial funcional)

**Test**: Bootstrap 95% CI + t-test one-sample vs 0.70  
**Criterio éxito**: mean(ratios) ≥ 0.70 AND p<0.05

**Predicción optimista**: ratio=0.72±0.15

### H10.2: Adaptive Superior a Fixed 🚀 (Innovación)

> Adaptive > Fixed en 8×8 (mejora sustancial)

**Test**: Paired t-test (two-tailed)  
**Criterio éxito**: p<0.05 AND Cohen's d>0.5

**Predicción**: p<0.02, d=0.75

### H10.3: Adaptive Reduce Varianza ✅ (Robustez)

> CV_adaptive < CV_fixed (menos varianza inter-seed)

**Test**: Levene's test + ratio CVs  
**Criterio éxito**: cv_ratio < 0.80 (20% menos varianza)

**Predicción**: cv_ratio=0.65 (35% reducción)

### H10.4: Seeds Vulnerables Se Estabilizan 🎯 (Rescate)

> Seed=123 (colapsó en v9 4×4) alcanza success>60% con adaptive en 8×8

**Test**: Caso específico + correlación eps_critical vs success  
**Predicción**: seed=123 usa ~200 eps en s=0.5+s=0.75, alcanza 70% success

---

## 📈 Predicciones Pre-Ejecución

### Escenario Optimista (60% probabilidad)

**Métricas finales (últimos 50 eps, 8×8)**:

| Grupo | Reward Env | Success Rate | Seeds Exitosas | Eps/Seed Promedio |
|-------|------------|--------------|----------------|-------------------|
| **Adaptive** | 95-105 | 70-80% | **4-5/5 (80-100%)** | ~420 (usa extras) |
| **Fixed** | 70-80 | 50-60% | 2-3/5 (40-60%) | 400 (rígido) |
| **ControlS0** | 130-140 | 95-100% | 5/5 | 400 |

**Interpretación**:
> "Adaptive permite escalamiento exitoso mediante personalización: seeds fuertes avanzan rápido (~400 eps), vulnerables usan tiempo extra (~500 eps) para consolidar."

**Paper story**: "Fixed colapsa en 8×8, Adaptive recupera paridad"

### Escenario Pesimista (40% probabilidad)

**Métricas finales**:
- Adaptive: 75-85 reward, 55-65% success, **2-3/5 exitosas**
- Ratio: 0.58±0.25 (NO alcanza 0.70)

**Diagnóstico**:
> "8×8 requiere arquitectura más grande (DQN 3×128), no solo curriculum mejor."

**Plan B**: Re-ejecutar con DQN 3×128, mismo protocolo adaptive

---

## 📁 Estructura de Archivos

```
pgf_v10/
├── PREREGISTRO_v10.md                       # Diseño experimental (v1.0 CONGELADO)
├── README.md                                 # Este archivo
├── TRACKING_v10.md                           # Log de ejecución
├── resultados/                               # 15 CSVs (3 grupos × 5 seeds)
│   ├── adaptive_seed42_episodes.csv
│   ├── adaptive_seed123_episodes.csv
│   ├── ... (5 CSVs Adaptive)
│   ├── fixed_seed42_episodes.csv
│   ├── ... (5 CSVs Fixed)
│   └── control_s0_seed42_episodes.csv
│       ... (5 CSVs Control)
├── analisis/                                 # Outputs análisis estadístico
│   ├── adaptive_summary.json
│   ├── fixed_summary.json
│   ├── control_s0_summary.json
│   ├── hypothesis_tests.json                # H10.1-H10.4
│   ├── episodes_per_stage_adaptive.json     # Métrica clave
│   └── correlation_eps_vs_success.json
├── figuras/                                  # Visualizaciones
│   ├── ratio_fixed_vs_adaptive_8x8.png
│   ├── episodes_per_stage_by_seed.png       # Barplot stacked
│   ├── success_vs_eps_critical.png          # Scatterplot correlación
│   ├── scaling_4x4_vs_8x8.png               # Fixed colapsa, Adaptive escala
│   └── seed123_rescue.png                   # Caso específico
├── exploratorios/                            # Análisis adicionales
│   ├── seed_clustering_adaptive.json
│   └── threshold_sensitivity_analysis.json
└── reportes/
    └── REPORTE_FINAL_v10.md
```

---

## 🔑 Métricas Clave

### Primarias

- **ratio_reward_env_final**: Adaptive/Control en eps finales
- **success_rate_final**: % goal_reached eps finales
- **CV por grupo**: std/mean (robustez)

### v10-Específicas (Adaptive)

- **episodes_per_stage[seed]**: Distribución episodios por etapa
  - Ejemplo seed fuerte: [80, 90, 100, 70, 60] = 400 total
  - Ejemplo seed vulnerable: [100, 120, 150, 80, 50] = 500 total
- **eps_critical_stages**: suma eps en s=0.5 + s=0.75
- **correlation**: eps_critical vs success_final (esperado r>0.70)

### Columnas CSV Requeridas

```python
# Básico
episode, agent_type, group, seed

# Adaptive específico
stage                    # 1-5 (Adaptive), 1-4 (Fixed), null (Control)
shaping_scale_current    # 0.0/0.25/0.5/0.75/1.0
episodes_in_stage        # Counter dentro de etapa actual
transition_triggered     # Boolean (True cuando avanza)
success_rate_last_25     # Métrica decisión threshold

# Recompensas + métricas estándar
total_reward_env, tripwires_triggered, goal_reached, etc.
```

---

## 💡 Lógica Adaptive Curriculum

### Implementación Core

```python
class AdaptiveCurriculum:
    def __init__(self, stages=[0.0, 0.25, 0.5, 0.75, 1.0]):
        self.stages = stages
        self.current_stage = 0
        self.episodes_in_stage = 0
        self.success_history = []
    
    def should_advance(self):
        """Decide si avanzar a siguiente etapa."""
        # Condición 1: Dominio demostrado
        if len(self.success_history) >= 25:
            recent_success = np.mean(self.success_history[-25:])
            ready = recent_success > 0.75
        else:
            ready = False
        
        # Condición 2: Timeout (evitar estancamiento)
        timeout = self.episodes_in_stage > 150
        
        return ready or timeout
    
    def update(self, goal_reached):
        """Actualizar tras cada episodio."""
        self.success_history.append(goal_reached)
        self.episodes_in_stage += 1
        
        if self.should_advance() and self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
            self.episodes_in_stage = 0
            print(f"[ADAPTIVE] Stage {self.current_stage} → scale={self.stages[self.current_stage]}")
    
    def get_current_scale(self):
        return self.stages[self.current_stage]
```

### Validaciones Críticas

**Test transitions**:
- Seed fuerte debe avanzar rápido (80-100 eps/etapa)
- Seed vulnerable debe usar timeout (120-150 eps en s=0.5)
- NO debe estancarse indefinidamente (timeout funciona)

---

## 🔗 Contexto Experimental

### Basado en v9/v9.1

**v9 (4×4, N=3)**: Curriculum fijo funciona (67% seeds éxito)  
**v9.1 (4×4, N=10)**: Validación estadística robusta (pendiente ejecución)  
**v10 (8×8, N=5)**: Escalamiento con adaptive curriculum

**Proyección v9 a 8×8** (FALLÓ):
- Fixed curriculum: ratio=0.507, success=41%
- Diagnóstico: Schedule rígido (75 eps/etapa) insuficiente para 8×8

**Gap v10 resuelve**: Personalización permite consolidación en complejidad alta

**Ver**:
- `results/pgf_v9/REPORTE_FINAL_v9.md` (evidencia 4×4)
- `results/pgf_v9.1/README.md` (validación N=10)

---

## 🚀 Estado de Ejecución

**Pre-ejecución**:
- ✅ Preregistro v1.0 completo y congelado (4 dic 2025)
- ✅ Estructura de carpetas creada
- ✅ README documentado
- ⏳ TRACKING iniciado
- ⏳ Implementación lógica adaptive (2-3 días desarrollo)
- ⏳ Test mode (1 seed × 100 eps)
- ⏳ Ejecución completa (15 configs × ~400 eps = 6,000 eps)

**Timeline estimado**:
- Desarrollo: ~2-3 días (mientras v9.1 ejecuta)
- Test mode: ~5 min
- Ejecución: ~8 horas
- Análisis: ~1 hora
- Reporte: ~2 horas

**Dependencias**:
- ⚠️ **CRÍTICO**: Esperar resultados v9.1 antes de ejecutar v10
  - Si v9.1 falla (p>0.10, <50% seeds), investigar causas antes de v10
  - Si v9.1 éxito parcial, v10 adaptive es crítico
  - Si v9.1 éxito completo, v10 demuestra escalamiento

**Deadline**: 7 diciembre 2025, 18:00

---

## 📝 Criterios de Éxito

### ÉXITO COMPLETO ✅

- H10.1: Ratio ≥0.70 (p<0.05)
- H10.2: Adaptive > Fixed (p<0.05, d>0.5)
- H10.3: CV_adaptive < 0.80 × CV_fixed
- H10.4: Seed=123 rescatada (success>60%)
- ≥80% seeds exitosas (4-5/5)

**Conclusión**: Adaptive resuelve escalamiento 8×8 → Paper submission NeurIPS/ICML

### ÉXITO PARCIAL ⚠️

- H10.1: Ratio 0.60-0.70 (mejora vs Fixed)
- H10.2: p<0.10, d>0.3 (tendencia)
- 60% seeds exitosas (3/5)

**Conclusión**: Adaptive ayuda, pero 8×8 requiere arquitectura mayor (Plan B: DQN 3×128)

### FALLA ❌

- H10.1: Ratio <0.55
- H10.2: p≥0.10, d<0.3
- <50% seeds exitosas (≤2/5)

**Conclusión**: Problema arquitectural, no curriculum. Testar DQN 3×128 o A2C.

---

## 📚 Referencias

- **Preregistro**: `PREREGISTRO_v10.md` (30 páginas, 599 líneas)
- **v9 Original**: `results/pgf_v9/REPORTE_FINAL_v9.md`
- **v9.1 Validación**: `results/pgf_v9.1/README.md`
- **Teoría TUI**: `docs/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md`
- **Literatura**: Graves et al. (2017) - Automated Curriculum Learning

---

**Fecha creación**: 4 diciembre 2025  
**Status**: 🔄 PREPARACIÓN (desarrollo mientras v9.1 ejecuta)  
**Próximo paso**: Desarrollar `scripts/run_experiment_10_adaptive.py`  
**Dependencia crítica**: ⚠️ Analizar resultados v9.1 antes de ejecutar v10
