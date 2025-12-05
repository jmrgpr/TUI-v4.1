# RESUMEN EJECUTIVO: Multi-Seed Validation v10_viable

**Fecha**: 2025-12-05  
**Experimento**: Fase 1 Roadmap - Reproducibilidad Curriculum 4×4→6×6→8×8  
**Seeds**: [13, 42, 101, 2025, 9999]  
**Status**: ✅ **COMPLETADO**

---

## Resultados Clave

### Performance Agregada (N=5)

| Fase | Success Rate | Gate | Status |
|------|-------------|------|--------|
| **4×4** | **88.2% ± 11.4%** | >80% | ✅ 4/5 seeds pasaron |
| **6×6** | **66.8% ± 12.4%** | >20% | ✅ 4/4 seeds pasaron |
| **8×8** | **54.0% ± 39.6%** | >10% | ⚠️ 3/4 seeds pasaron |

### Análisis Seed 42 (Baseline)

| Fase | Seed 42 | Media Otras | Z-score | Conclusión |
|------|---------|-------------|---------|------------|
| 4×4 | 93.0% | 88.2% ± 11.4% | +0.42 | ✅ Representativa |
| 6×6 | 68.0% | 66.3% ± 15.1% | +0.11 | ✅ Representativa |
| 8×8 | 87.0% | 43.0% ± 40.3% | +1.09 | ⚡ Ligeramente superior |

**Conclusión seed 42**: Es **representativa** del comportamiento medio (|Z| < 2). La ligera superioridad en 8×8 (Z=1.09) está dentro de variabilidad esperada.

---

## Interpretación por Fase

### ✅ Fase 1 (4×4): ESTABLE
- **Success rate**: 88.2% ± 11.4%
- **Rango**: [68%, 95%]
- **First success**: Episodio 3 ± 2
- **Evaluación**: **Muy robusto**. Solo seed 2025 (68%) no pasó gate >80%, pero estuvo cerca.
- **Diagnóstico seed 2025**: Ejecución interrumpida por usuario (Ctrl+C), datos parciales.

### ✅ Fase 2 (6×6): CONSISTENTE
- **Success rate**: 66.8% ± 12.4%
- **Rango**: [49%, 77%]
- **First success**: Episodio 104 ± 204
- **Evaluación**: **Rendimiento excelente** para complejidad 2.25× respecto 4×4.
- **Transfer learning**: Efectivo - todas las seeds que completaron 4×4 superaron gate 6×6 (>20%).

### ⚠️ Fase 3 (8×8): ALTA VARIABILIDAD
- **Success rate**: 54.0% ± 39.6%
- **Rango**: [**0%**, 87%]
- **First success**: Episodio 2 ± 1
- **Evaluación**: **Inconsistente**.
  - **Seeds exitosas** (101, 42, 9999): 80%, 87%, 49% → Aprendizaje efectivo
  - **Seed fallida** (13): 0% → Colapso total
- **Hipótesis**: Curriculum 8×8 en filo inestable - pequeñas variaciones iniciales divergen.

---

## Diagnóstico: ¿Por qué seed 13 colapsó en 8×8?

### Datos seed 13:
- 4×4: 91% (✅ aprobó gate)
- 6×6: 49% (✅ aprobó gate >20%)
- **8×8: 0%** (❌ colapso total)

### Posibles causas:
1. **Transfer 6×6→8×8 frágil**: Seed 13 quedó en límite inferior 6×6 (49% vs 67% media) → No suficiente conocimiento para salto 8×8
2. **Horizonte corto insuficiente**: `max_steps_multiplier=3.0` en 8×8 (192 pasos) puede ser muy ajustado
3. **Epsilon decay agresivo**: `epsilon=0.3` inicial en 8×8 puede no dar suficiente exploración
4. **Economía no viable en 8×8**: `STEP_COST=-0.15` × 192 pasos = -28.8 recursos vs INITIAL=8.0

---

## Conclusiones Científicas

### ✅ H1: Curriculum 4×4→6×6 es ROBUSTO
- Success rates reproducibles (88% y 67%)
- Transfer learning efectivo (4/4 seeds pasaron gate 6×6)
- Variabilidad aceptable (CoV ~13-19%)

### ⚠️ H2: Fase 8×8 REQUIERE AJUSTES
- Alta variabilidad (CoV ~73%)
- 1 de 4 seeds colapsó completamente
- No apto como baseline para ablation sin corrección

### ✅ H3: Seed 42 ES VÁLIDA como baseline
- Representativa en 4×4 y 6×6 (Z < 0.5)
- Ligeramente superior en 8×8 (Z=1.09), pero dentro de 1 std
- NO es outlier estadístico

---

## Decisiones

### ✅ PROCEDER con Fase 2 (Ablation) EN FASES ESTABLES
**Recomendación**: Ejecutar ablation solo en **4×4 y 6×6** donde curriculum es robusto.

**Justificación**:
1. 4×4 y 6×6 tienen variabilidad <15% → Cambios >15% serán detectables
2. 8×8 con variabilidad 73% → Imposible distinguir efecto ablation de ruido
3. Economía viable validada en grids pequeños es suficiente para paper TUI

### ⚠️ CONGELAR 8×8 para debugging
**Tareas pendientes**:
- [ ] Aumentar `max_steps_multiplier` a 4.0 o 5.0
- [ ] Probar `epsilon=0.5` inicial (más exploración)
- [ ] Validar economía 8×8: SPAWN_RATE=0.50 o INITIAL_RESOURCES=10.0
- [ ] Re-ejecutar multi-seed solo para 8×8 con ajustes

---

## Archivos Críticos Generados

### Datos
- `results/pgf_v10_multiseed/analisis_agregado/multiseed_summary.csv` (13 registros, 5 seeds)
- `results/pgf_v10_multiseed/analisis_agregado/multiseed_statistics.csv`

### Figuras
- `boxplot_success_rates_5seeds.png` (distribución por fase)
- `phase2_breakthrough_histogram.png` (convergencia 6×6)
- `transfer_effectiveness_comparison.png`

### Raw Data (por seed)
- `results/pgf_v10_multiseed/seeds/seed_XXXX/` (phase CSVs + curriculum_summary)

---

## Commits Relevantes

- `61e07a7` - Roadmap v10 estructura completa
- `74c72b6` - Resumen Fase 0
- `8324c5b` - Fix DQNAgent seed parameter
- `fbd90fe` - Fix env.reset() seed parameter
- `be674c5` - Fix análisis: fracción→%, seed 42 formato baseline

---

## Próximos Pasos (Roadmap Actualizado)

### ✅ Fase 0: Setup
- Completada 2025-12-05

### ✅ Fase 1: Multi-Seed Validation
- Completada 2025-12-05
- **Output**: Curriculum 4×4→6×6 robusto, 8×8 inestable

### ➡️ **Fase 2: Ablation Studies (MODIFICADA)**
**Scope reducido**: Solo 4×4 y 6×6 (grids estables)

**Ablations a ejecutar**:
1. **Economía no viable** (STEP_COST=-0.40, seeds=[13,42,101])
2. **Sin transfer learning** (train desde cero cada fase, seeds=[13,42,101])
3. **Sin curriculum** (train directo en 6×6 sin 4×4, seeds=[13,42,101])

**Criterio éxito**: Baseline supera ablations en >10% success rate

### ⏸️ Fase 3: Debugging 8×8 (NUEVA)
- Diagnosticar colapso seed 13
- Ajustar hiperparámetros 8×8
- Re-validar con N=3 seeds

### 🔮 Fase 4: Paper Writing
- Figuras finales
- Redacción secciones experimentales
- Comparación SOTA

---

**Estado General**: ⚡ **BASELINE PARCIALMENTE VALIDADO** - Proceder con ablation en grids estables (4×4, 6×6)
