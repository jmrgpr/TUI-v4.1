# 🔬 EXPLORATORIOS v9: Generalización a Grids Más Complejos

**Propósito**: Validar que curriculum learning generaliza a entornos de mayor complejidad (6×6 y 8×8)  
**Status**: 📋 PLANIFICADO (opcional, post-v9 principal)  
**Fecha**: 3 diciembre 2025

---

## 🎯 Motivación

### Contexto v8 Exploratorio 6×6

**Hallazgo v8**:
- Grid 6×6 muestra **mismo patrón cualitativo** que 4×4
- s=0.0 → paridad (~0.99)
- s=1.0 → over-alignment (~0.30-0.40)
- **Conclusión**: Fenómeno NO es artefacto de 4×4

**Gap**: v8 exploratorio 6×6 se hizo con código **pre-fixes v8.0.1** (sin death flags robustos)

### Pregunta Exploratoria v9

> ¿Curriculum learning sigue siendo efectivo en grids más complejos (6×6, 8×8)?

**Hipótesis**:
- **H_exp1**: Curriculum mantiene ventaja en 6×6 (ratio_curriculum > ratio_directo)
- **H_exp2**: Ventaja curriculum puede **amplificarse** en 8×8 (más espacio para aprender balances)
- **H_exp3**: Patrón temporal (degradación gradual vs súbita) se replica

---

## 📐 Complejidad por Grid Size

### Comparación Espacial

| Grid | Celdas | Manhattan Dist | Caminos posibles | Tripwires (spawn=0.25) | Complejidad |
|------|--------|----------------|------------------|------------------------|-------------|
| 4×4  | 16     | 6 steps        | ~20              | ~4                     | Baja        |
| 6×6  | 36     | 10 steps       | ~252             | ~9                     | Media       |
| 8×8  | 64     | 14 steps       | ~3,432           | ~16                    | Alta        |

### Implicaciones Curriculum

**6×6**:
- Caminos ~12× más complejos que 4×4
- Agente necesita **más episodios** para convergir
- Curriculum podría ser **más necesario** (más espacio de exploración)

**8×8**:
- Caminos ~170× más complejos que 4×4
- Complejidad exponencial: ¿DQN 2×64 suficiente?
- Curriculum podría ser **crítico** o **insuficiente** (requiere red más grande)

---

## 🔬 Diseño Experimental

### Prioridad 1: Grid 6×6 (CONFIRMADO)

**Justificación**:
- Ya validado en v8 (patrón conocido)
- Complejidad intermedia (balance exploración-convergencia)
- Tiempo razonable (~20 min ejecución)

**Configuración**:
```
Grid: 6×6
Densidad: spawn_rate = 0.25 (~9 tripwires, ~6 recursos)
Grupos: Curriculum, DirectoS1, ControlS0
Seeds: 3 (42, 123, 456)
Episodios: 300 por config
N_configs: 3 grupos × 3 seeds = 9
N_episodios: 2,700 total
```

**Curriculum 6×6**:
```python
# ¿Mismas duraciones o ajustadas?
# Opción A (conservadora): 75 eps/etapa (igual 4×4)
# Opción B (ajustada): 100 eps/etapa (más tiempo convergencia)

Etapas: 0.0 → 0.25 → 0.5 → 1.0
Duración: 75 eps/etapa (Opción A default)
```

**Tiempo estimado**: ~20 minutos

### Prioridad 2: Grid 8×8 (OPCIONAL)

**Justificación**:
- Complejidad alta: test límites curriculum
- Requiere más recursos computacionales
- Puede revelar nuevos regímenes

**Configuración**:
```
Grid: 8×8
Densidad: spawn_rate = 0.25 (~16 tripwires, ~10 recursos)
Grupos: Curriculum, DirectoS1, ControlS0
Seeds: 3 (42, 123, 456)
Episodios: 400-500 por config (más convergencia)
N_configs: 9
N_episodios: 3,600-4,500 total
```

**Curriculum 8×8 (propuesto)**:
```python
# Opción ajustada: más etapas + más duración
Etapas: 0.0 → 0.2 → 0.4 → 0.6 → 0.8 → 1.0
Duración: 75 eps/etapa (6 etapas = 450 eps)

# Alternativa: mismas etapas, más duración
Etapas: 0.0 → 0.25 → 0.5 → 1.0
Duración: 100 eps/etapa (4 etapas = 400 eps)
```

**Tiempo estimado**: ~40-60 minutos

**Criterio ejecución**: Solo si v9 4×4 muestra **éxito claro** (ratio_curriculum > 0.70)

---

## 📊 Hipótesis Exploratorias

### H_exp1: Curriculum Generaliza a 6×6

**Enunciado**:
> En grid 6×6, Curriculum alcanzará ratio_final > DirectoS1 con magnitud similar o mayor que en 4×4.

**Predicción cuantitativa**:
```
4×4 esperado: ratio_curriculum - ratio_directo ≈ 0.40 (0.75 - 0.35)
6×6 esperado: ratio_curriculum - ratio_directo ≥ 0.40

Interpretación: Ventaja se mantiene o amplifica
```

### H_exp2: Amplificación en Mayor Complejidad

**Enunciado**:
> La ventaja de Curriculum sobre DirectoS1 es **mayor** en 6×6 que en 4×4 (medida por Cohen's d).

**Predicción**:
```
d_4x4 = (0.75 - 0.35) / SD_pooled ≈ 1.5 (esperado)
d_6x6 ≥ d_4x4

Mecanismo: En entornos complejos, entrenamiento directo s=1.0 colapsa más rápido
```

### H_exp3: Patrón Temporal Replicado

**Enunciado**:
> En 6×6, el patrón de degradación gradual (NO súbita) en Curriculum se replica.

**Predicción**:
```
Ratios por etapa:
  Etapa 1 (s=0.0):  ~0.98
  Etapa 2 (s=0.25): ~0.80-0.85
  Etapa 3 (s=0.5):  ~0.70-0.75
  Etapa 4 (s=1.0):  ~0.65-0.70

Pendiente: uniforme, NO salto >0.30 en etapa 4
```

### H_exp4: Límite Arquitectural en 8×8 (si se ejecuta)

**Enunciado**:
> En grid 8×8, DQN 2×64 puede mostrar límites de capacidad, reduciendo efectividad de curriculum.

**Predicción**:
```
Si curriculum falla en 8×8 pero funciona en 4×4 y 6×6:
  → Límite arquitectural (red pequeña para complejidad)
  → Requiere escalamiento (DQN 3×128 o similar)
```

---

## 📁 Estructura de Outputs

### Grid 6×6

```
exploratorios/grid_6x6/
├── README_6x6.md              # Diseño específico
├── resultados/
│   ├── exp9_6x6_Curriculum_seed42_episodes.csv
│   ├── exp9_6x6_Curriculum_seed42_metrics.json
│   └── ... (18 archivos: 9 CSVs + 9 JSONs)
├── analisis/
│   ├── curriculum_effectiveness_6x6.json
│   └── comparison_4x4_vs_6x6.json
└── figuras/
    ├── fig1_learning_curves_6x6.png
    ├── fig2_comparison_grid_sizes.png
    └── fig3_scatter_safety_reward_6x6.png
```

### Grid 8×8 (si se ejecuta)

```
exploratorios/grid_8x8/
├── README_8x8.md
├── resultados/
│   └── ... (18 archivos si 400 eps, más si 500)
├── analisis/
│   ├── curriculum_effectiveness_8x8.json
│   └── comparison_4x4_6x6_8x8.json
└── figuras/
    ├── fig1_learning_curves_8x8.png
    └── fig2_comparison_all_grids.png
```

---

## ⚖️ Decisión de Ejecución

### Criterios para 6×6

✅ **EJECUTAR SI**:
- v9 4×4 completado con éxito (todas hipótesis validadas)
- Tiempo disponible (~20 min adicionales)
- Objetivo: Robustecer hallazgo para paper

❌ **OMITIR SI**:
- v9 4×4 muestra falla (curriculum ≈ directo)
- Rationale: No tiene sentido validar en 6×6 algo que no funciona en 4×4

### Criterios para 8×8

✅ **EJECUTAR SI**:
- v9 4×4 **Y** 6×6 muestran éxito claro
- Objetivo: Test límites + paper "Curriculum at Scale"
- Tiempo disponible (~40-60 min adicionales)

⚠️ **CONSIDERAR SI**:
- v9 4×4 éxito, 6×6 falla parcial
- Rationale: Diagnosticar si problema es complejidad o arquitectura

❌ **OMITIR SI**:
- v9 4×4 falla
- v9 6×6 falla completamente
- Deadline presión (4 dic 23:59)

---

## 🔄 Workflow Propuesto

### Fase 1: v9 Principal 4×4 (PRIORITARIO)

1. Implementar `run_experiment_9_curriculum.py`
2. Test mode (120 eps)
3. Ejecución completa (2,700 eps, ~15 min)
4. Análisis rápido (H9.1, H9.2, H9.3)

**Checkpoint decisión**: ¿Curriculum funciona?

### Fase 2: Exploratorio 6×6 (CONDICIONAL)

**Si v9 4×4 éxito**:
5. Adaptar script para grid_size=6
6. Ejecutar 6×6 (2,700 eps, ~20 min)
7. Análisis comparativo 4×4 vs 6×6

**Checkpoint decisión**: ¿Patrón se replica?

### Fase 3: Exploratorio 8×8 (OPCIONAL)

**Si v9 6×6 éxito**:
8. Adaptar script con arquitectura escalada (opcional: DQN 3×128)
9. Ejecutar 8×8 (3,600-4,500 eps, ~40-60 min)
10. Análisis completo 4×4 vs 6×6 vs 8×8

---

## 📊 Análisis Comparativo Grid Sizes

### Métricas Clave por Grid

| Métrica | 4×4 | 6×6 | 8×8 | Interpretación |
|---------|-----|-----|-----|----------------|
| **ratio_curriculum** | [TBD] | [TBD] | [TBD] | ¿Se mantiene efectividad? |
| **ventaja_curriculum** | [TBD] | [TBD] | [TBD] | ¿Amplifica con complejidad? |
| **pendiente_etapas** | [TBD] | [TBD] | [TBD] | ¿Degradación gradual replica? |
| **transfer_efficiency** | [TBD] | [TBD] | [TBD] | ¿Retención empeora con complejidad? |

### Figura Comparativa (si ambos ejecutados)

**Tipo**: Panel 3×1 (learning curves por grid size)
**Ejes**: Episodios × Ratio (PGF/Control)
**Líneas**: Curriculum (rojo), DirectoS1 (azul), ControlS0 (gris)
**Paneles**:
- Panel A: 4×4 (baseline)
- Panel B: 6×6 (validación)
- Panel C: 8×8 (límite - si ejecutado)

---

## 🎯 Valor Científico

### Para Paper

**Si 6×6 replica 4×4**:
> "Curriculum learning mitiga over-alignment robustamente en grids 4×4 y 6×6 (d=1.5 y d=1.7 respectivamente), demostrando generalización a mayor complejidad espacial."

**Si 8×8 también funciona**:
> "Efectividad de curriculum persiste hasta grids 8×8, sugiriendo escalabilidad del método. Ventaja crece con complejidad del entorno (d_4x4=1.5, d_6x6=1.7, d_8x8=2.1)."

**Si 8×8 falla**:
> "Límite arquitectural detectado: DQN 2×64 insuficiente para 8×8 con curriculum. Sugiere necesidad de escalamiento de red proporcional a complejidad espacial."

### Para TUI

**Robustez empírica**:
- Fenómeno over-alignment replicado en 3 escalas espaciales
- Mitigación via curriculum validada en múltiples regímenes
- Acota límites de aplicabilidad (arquitectura vs complejidad)

---

## ⏱️ Estimación Temporal Total

```
v9 4×4 principal:     ~60 min (implementación + ejecución + análisis)
Exploratorio 6×6:     ~30 min (adaptación + ejecución + análisis)
Exploratorio 8×8:     ~70 min (ajustes + ejecución + análisis)
                      --------
TOTAL máximo:         ~160 min (~2.7 horas)

Deadline: 4 dic 23:59 → Tiempo suficiente si priorizado
```

---

## 📝 Recomendación

**Estrategia pragmática**:

1. ✅ **Ejecutar v9 4×4** (OBLIGATORIO)
2. ✅ **Ejecutar 6×6** si v9 4×4 éxito (ALTAMENTE RECOMENDADO)
   - Costo bajo (~30 min)
   - Valor alto (robustez paper)
3. ⚠️ **Evaluar 8×8** solo si tiempo sobra (OPCIONAL)
   - Costo alto (~70 min)
   - Valor medio (límites interesantes pero no críticos)

**Si deadline aprieta**:
- 4×4 + 6×6 suficientes para paper robusto
- 8×8 queda para extensión futura (v10 o paper 2)

---

**FIN README EXPLORATORIOS**

**Fecha**: 3 diciembre 2025  
**Status**: 📋 PLANIFICADO  
**Decisión final**: Post-ejecución v9 4×4
