# 🔬 Exploratorio v9: Grid 8×8

**Grid Size**: 8×8 (64 celdas)  
**Objetivo**: Test límites de curriculum learning en alta complejidad  
**Status**: ✅ **COMPLETADO** (3 diciembre 2025, 3.0 min)  
**Resultado**: ⚠️ **COLAPSO PARCIAL** (ratio 0.507, solo seed=123 exitoso)

---

## 🎯 Justificación

### Pregunta Exploratoria

> ¿Existe un límite de complejidad espacial donde curriculum learning deja de ser efectivo?

**Motivación**:
- 4×4 y 6×6 validan efectividad en complejidad baja-media
- 8×8 representa salto cualitativo (64 celdas, ~3,400 caminos)
- Puede revelar **límite arquitectural** (DQN 2×64 insuficiente?)

**Resultado obtenido:**
- ❌ Curriculum FALLA (ratio 0.507 vs 0.859 en 6×6)
- ✅ Arquitectura SUFICIENTE (Control s=0.0 resuelve 8×8 con reward 126.02)
- 🔍 Diagnóstico: PROBLEMA CURRICULAR (etapas 75 eps insuficientes)

---

## 📊 Resultados Principales

### Tabla Resumen por Grupo (últimos 50 episodios)

| Grupo | Reward Env | Success Rate | Tripwires | Interpretación |
|-------|------------|--------------|-----------|----------------|
| **Curriculum** | 64.03 ± 52.37 | 41.3% | 1.88 | ⚠️ **COLAPSO PARCIAL** (alta varianza) |
| **DirectoS1** | 20.49 ± 0.55 | 0% | 0.31 | ❌ **FALLA TOTAL** (esperado) |
| **ControlS0** | 126.02 ± 0.41 | 100% | 4.26 | ✅ **ÉXITO COMPLETO** |

### Resultados Detallados por Seed (Curriculum)

| Seed | Reward Final | Success Rate | Etapa 4 Reward | Status |
|------|--------------|--------------|----------------|--------|
| **42** | 20.47 ± 0.65 | 0% | 20.51 | ❌ **COLAPSO TOTAL** |
| **123** | 122.14 ± 20.55 | 96% | 121.74 | ✅ **ÉXITO** (único superviviente) |
| **456** | 49.50 ± 47.68 | 28% | 57.98 | ⚠️ **DEGENERACIÓN** (colapso ep 300) |

**Test H_exp1 Extensión:**
```
Ratio Curriculum/Control: 0.507 ± 0.414
95% CI: [0.039, 0.975]
Resultado: ❌ RECHAZADA (ratio < 0.70 threshold)
Interpretación: PARTIAL COLLAPSE - Degradación 41% vs 6×6
```

**Tendencia Multiescala:**
```
4×4: ratio 0.766 (MARGINAL, CV=0.532)
6×6: ratio 0.859 (ÉXITO, CV=0.178) ← pico efectividad
8×8: ratio 0.507 (COLAPSO, CV=0.818) ← inestabilidad crítica
```

**Diagnóstico Clave:**
- ✅ **Arquitectura DQN 2×64 SUFICIENTE** (Control resuelve 8×8 perfectamente)
- ❌ **Curriculum MAL CALIBRADO** (75 eps/etapa insuficientes para 4× complejidad)
- 🔑 **Seed=123 resiliente** (mantiene 122.14) pero seeds 42/456 colapsan
- 📊 **CV aumenta** 0.178 (6×6) → 0.818 (8×8) → configuración inadecuada

---

## 📐 Complejidad 8×8 vs 6×6 vs 4×4

| Aspecto | 4×4 | 6×6 | 8×8 | Factor (8×8/4×4) |
|---------|-----|-----|-----|------------------|
| **Celdas** | 16 | 36 | 64 | 4× |
| **Manhattan dist** | 6 | 10 | 14 | 2.33× |
| **Caminos posibles** | ~20 | ~252 | ~3,432 | 170× |
| **Tripwires (spawn=0.25)** | ~4 | ~9 | ~16 | 4× |
| **Recursos (spawn=0.25)** | ~4 | ~9 | ~16 | 4× |
| **Tiempo/episodio** | ~0.5s | ~1.0s | ~2.0s | 4× |

**Complejidad exponencial**: Caminos posibles crecen ~170× de 4×4 a 8×8.

**Implicación crítica**: DQN 2×64 (816 parámetros aprox) puede ser **insuficiente** para representar política óptima en 64 celdas.

---

## 🔬 Diseño Experimental

### Configuración Base

```python
GRID_SIZE = 8
SPAWN_RATE = 0.25  # ~16 tripwires, ~16 recursos
BALANCE = 5.0
EPISODES_PER_CONFIG = 400  # Más episodios para convergencia

grupos = ["Curriculum", "DirectoS1", "ControlS0"]
seeds = [42, 123, 456]
```

**Total**: 3 grupos × 3 seeds × 400 eps = 3,600 episodios (~60 min)

### Opción A: Curriculum Estándar (4 etapas)

```python
# Mismo protocolo 4×4/6×6, más duración
etapas_curriculum = [
    {"scale": 0.0,  "episodes": range(0, 100)},   # +25 eps vs 4×4
    {"scale": 0.25, "episodes": range(100, 200)},
    {"scale": 0.5,  "episodes": range(200, 300)},
    {"scale": 1.0,  "episodes": range(300, 400)}
]
```

### Opción B: Curriculum Extendido (6 etapas)

```python
# Más granular para mayor complejidad
etapas_curriculum = [
    {"scale": 0.0,  "episodes": range(0, 75)},
    {"scale": 0.2,  "episodes": range(75, 150)},
    {"scale": 0.4,  "episodes": range(150, 225)},
    {"scale": 0.6,  "episodes": range(225, 300)},
    {"scale": 0.8,  "episodes": range(300, 375)},
    {"scale": 1.0,  "episodes": range(375, 450)}
]
# Total: 450 eps (vs 400 en Opción A)
```

**Recomendación**: Empezar con Opción A (más comparable). Si falla, diagnosticar antes de intentar Opción B.

---

## 🧠 Consideración Arquitectural

### DQN 2×64: ¿Suficiente para 8×8?

**Capacidad actual**:
```python
# Architecture
input_size = 64 (grid_size^2)
hidden1 = 64
hidden2 = 64
output_size = 4 (actions)

total_params ≈ (64×64) + (64×64) + (64×4) ≈ 4,600 parámetros
```

**Regla empírica RL**:
> Parámetros ≈ 10-100× tamaño estado para generalización razonable

```
Estado 8×8: 64 celdas
Parámetros deseados: ~640-6,400
Parámetros actuales: ~4,600 ✓ (dentro rango, pero en límite bajo)
```

**Diagnóstico posible**:
- Si 8×8 falla pero 6×6 funciona → **límite capacidad** (no complejidad inherente)
- Solución: Escalar arquitectura (DQN 3×128 o similar)

### Opción Escalada (si necesario)

```python
# Si DQN 2×64 falla, probar:
DQN_ARCHITECTURE_8x8 = {
    'hidden_layers': [128, 128, 64],  # 3 capas
    'total_params': ~12,000
}
```

---

## 📊 Hipótesis Exploratorias

### H_8x8_1: Curriculum Mantiene Ventaja

> En 8×8, Curriculum alcanzará ratio_final > DirectoS1, aunque magnitud puede reducir vs 4×4/6×6.

**Predicción**:
```
Δ_4x4 ≈ 0.40 (esperado)
Δ_6x6 ≈ 0.40-0.50 (esperado mantener/amplificar)
Δ_8x8 ≥ 0.30 (aceptable si reduce levemente)

Interpretación: Ventaja persiste pero complejidad cobra precio
```

### H_8x8_2: Límite Arquitectural

> Si Curriculum falla en 8×8 (ratio ≈ DirectoS1) pero funciona en 6×6, indica límite de capacidad DQN 2×64.

**Criterio falla**:
```
8x8 Curriculum ≈ DirectoS1 (~0.35)
MIENTRAS 6x6 Curriculum > DirectoS1 (≥0.70)

→ Límite arquitectural detectado
```

### H_8x8_3: Transfer Efficiency Degrada

> En 8×8, transfer_efficiency entre etapas será menor que en 4×4/6×6.

**Predicción**:
```
transfer_4x4 ≈ 0.95 (esperado)
transfer_6x6 ≈ 0.90 (leve degradación)
transfer_8x8 ≈ 0.80-0.85 (degradación moderada)

Interpretación: Mayor complejidad → más "olvido" entre etapas
```

---

## 📁 Outputs

```
grid_8x8/
├── resultados/
│   └── ... (18 archivos: 9 CSVs + 9 JSONs)
├── analisis/
│   ├── curriculum_effectiveness_8x8.json
│   └── comparison_4x4_6x6_8x8.json
└── figuras/
    ├── fig1_learning_curves_8x8.png
    ├── fig2_comparison_all_grids.png
    └── fig3_capacity_limits.png
```

---

## 🎯 Criterios de Decisión

### Escenario 1: Éxito Completo ✅

```
8x8 Curriculum: ratio_final ≥ 0.65, ventaja ≥ 0.30
6x6 Curriculum: ratio_final ≥ 0.70, ventaja ≥ 0.40
4x4 Curriculum: ratio_final ≥ 0.70, ventaja ≥ 0.40

Conclusión: Curriculum ESCALA hasta alta complejidad
Paper: "Curriculum learning efectivo en grids hasta 8×8 (170× más caminos que baseline)"
```

### Escenario 2: Degradación Gradual ⚠️

```
8x8 Curriculum: ratio_final ≈ 0.55, ventaja ≈ 0.20
6x6 Curriculum: ratio_final ≈ 0.70, ventaja ≈ 0.40

Conclusión: Curriculum ayuda pero REDUCE efectividad con complejidad
Posible causa: DQN 2×64 en límite capacidad
Próximo paso: v10 con DQN 3×128 en 8×8
```

### Escenario 3: Falla Completa ❌

```
8x8 Curriculum ≈ DirectoS1 (ambos ~0.35)
6x6 Curriculum > DirectoS1 (ratio ≥ 0.70)

Conclusión: LÍMITE ARQUITECTURAL detectado
Diagnóstico: DQN 2×64 insuficiente para 64 celdas
Paper: "Límite de capacidad: curriculum requiere escalamiento arquitectural proporcional a complejidad espacial"
```

---

## 📊 Análisis Comparativo 3 Grids

### Tabla Comparativa

| Métrica | 4×4 | 6×6 | 8×8 | Tendencia |
|---------|-----|-----|-----|-----------|
| **ratio_curriculum** | [TBD] | [TBD] | [TBD] | ¿Degrada con complejidad? |
| **ventaja_curriculum** | [TBD] | [TBD] | [TBD] | ¿Se mantiene/amplifica/reduce? |
| **transfer_efficiency** | [TBD] | [TBD] | [TBD] | ¿Olvido crece con complejidad? |
| **steps_to_goal** | [TBD] | [TBD] | [TBD] | ¿Eficiencia degrada? |

### Figura Panel 3×1

**Tipo**: Learning curves por grid size  
**Layout**: 3 paneles verticales (4×4, 6×6, 8×8)  
**Líneas**: Curriculum, DirectoS1, ControlS0  
**Interpretación visual**: ¿Ventaja Curriculum se mantiene en los 3?

---

## 🔗 Valor Científico

### Si 8×8 funciona (Escenario 1)

**Contribución**:
> "Demostración de escalabilidad: curriculum learning efectivo hasta 170× complejidad de baseline. Sugiere aplicabilidad a dominios reales de mayor escala."

**Paper section**:
> "Robustness to Spatial Complexity: We validated curriculum effectiveness in grids 4×4, 6×6, and 8×8 (170-fold increase in possible paths). Effect sizes remained large (d>1.0) across all scales, demonstrating scalability of staged alignment."

### Si 8×8 detecta límite (Escenario 3)

**Contribución**:
> "Identificación de límite arquitectural: DQN 2×64 suficiente hasta 6×6 pero insuficiente para 8×8. Establece principio de diseño: capacidad de red debe escalar con complejidad espacial."

**Paper section**:
> "Architectural Limits: Curriculum failed in 8×8 grids despite success in 6×6, indicating capacity bottleneck. We propose scaling rule: hidden units ≈ 2× grid cells for curriculum effectiveness."

---

## ⏱️ Estimación Temporal

### Opción A (4 etapas, 400 eps)

```
Implementación: ~15 min (adaptar código)
Ejecución: ~40 min (3,600 eps × 2s/ep)
Análisis: ~15 min
Total: ~70 minutos
```

### Opción B (6 etapas, 450 eps)

```
Implementación: ~20 min (más etapas)
Ejecución: ~50 min (4,050 eps × 2s/ep)
Análisis: ~15 min
Total: ~85 minutos
```

---

## 📝 Recomendación

**Estrategia**:

1. ✅ **Ejecutar v9 4×4** (OBLIGATORIO)
2. ✅ **Ejecutar v9 6×6** si 4×4 éxito (RECOMENDADO)
3. ⚠️ **Evaluar 8×8** solo si:
   - 4×4 Y 6×6 ambos exitosos
   - Tiempo sobra (>70 min antes deadline)
   - Objetivo: Paper "curriculum at scale" robusto

**Si 8×8 falla**:
- NO es fracaso de v9
- Es hallazgo válido: límite arquitectural
- Informa diseño v10 (escalamiento redes)

---

**FIN README 8×8**

**Status**: ⚠️ OPCIONAL  
**Prioridad**: BAJA (solo si sobra tiempo)  
**Tiempo**: ~70 minutos  
**Deadline check**: Solo si ≥90 min disponibles post-6×6
