# PREREGISTRO: Multi-Seed Validation v10_viable

**Fecha**: 5 de diciembre de 2025  
**Investigador**: Sistema Autónomo TUI v4.1  
**Baseline**: v10_viable (seed=42, commit `cf1438c`)

---

## Objetivo

Validar reproducibilidad del curriculum 4×4→6×6→8×8 bajo economía viable mediante N=5 seeds independientes.

---

## Hipótesis (Pre-Registro)

### H1: Success Rates Reproducibles
**Predicción**: Los success rates (últimos 100 eps) de seed=42 están dentro de ±1σ de la media de 5 seeds.

**Métricas**:
- Media 4×4: 85% ± 10%
- Media 6×6: 50% ± 20%
- Media 8×8: 70% ± 15%

**Criterio validación**:
- ✅ Si seed=42 está en [media-σ, media+σ] en las 3 fases
- ❌ Si seed=42 es outlier en 2+ fases

---

### H2: Breakthrough 6×6 es Patrón Reproducible
**Predicción**: El "breakthrough" (convergencia súbita) en 6×6 ocurre en rango [400, 700] episodios en la mayoría de seeds.

**Operacionalización**:
- Breakthrough = primer episodio donde ventana móvil 50 eps alcanza >50% success

**Criterio validación**:
- ✅ Si 4/5 seeds tienen breakthrough en [400, 700]
- ❌ Si 3+ seeds nunca alcanzan >50% en ventana móvil

---

### H3: Transfer 6×6→8×8 Superior a 4×4→6×6
**Predicción**: En todas las seeds, transfer 6×6→8×8 es más efectivo que 4×4→6×6.

**Métricas**:
- Episodio primer éxito 6×6 (desde 4×4)
- Episodio primer éxito 8×8 (desde 6×6)
- Episodio convergencia 6×6 vs 8×8

**Criterio validación**:
- ✅ Si en 4/5 seeds: convergencia_8×8 < convergencia_6×6
- ✅ Si en 4/5 seeds: primer_éxito_8×8 < 20 eps

---

### H4: Varianza 6×6 es Estructural, no Artefacto
**Predicción**: La alta varianza 6×6 (peak 96% vs final 68% en seed=42) se replica en otras seeds.

**Métricas**:
- Desviación estándar últimos 500 eps fase 6×6
- Diferencia peak vs final por seed

**Criterio validación**:
- ✅ Si 4/5 seeds tienen σ últimos 500 eps >15%
- ❌ Si 3+ seeds tienen políticas estables (σ <10%)

---

## Configuración Experimental

### Seeds
```python
SEEDS = [13, 42, 101, 2025, 9999]
```

**Justificación**:
- 13: Seed común benchmark RL
- 42: Baseline v10_viable
- 101: Valor intermedio
- 2025: Año actual (trazabilidad)
- 9999: Extremo (test robustez RNG)

### Economía (Idéntica a v10_viable)
```python
INITIAL_RESOURCES = 8.0
STEP_COST = -0.15
RESOURCE_SPAWN_RATE = 0.40
GOAL_REWARD = 20.0
```

### Hyperparameters (Fijos)
```python
LEARNING_RATE = 0.001
GAMMA = 0.99
EPSILON_DECAY = 0.995
HIDDEN_DIM = 128
BATCH_SIZE = 32
MEMORY_SIZE = 10000
```

### Curriculum (Fijo)
- **Fase 1 (4×4)**: 500 eps, epsilon 1.0→0.1, max_steps 24
- **Fase 2 (6×6)**: 1000 eps, epsilon 0.9→0.1, max_steps 50
- **Fase 3 (8×8)**: 1000 eps, epsilon 0.3→0.1, max_steps 42

---

## Gates de Validación

| Fase | Gate | Criterio Éxito (N=5) | Criterio Fracaso |
|------|------|----------------------|------------------|
| 1 (4×4) | >80% | Media >85% | <2 seeds pasan |
| 2 (6×6) | >20% | Media >40% | ≥2 seeds <20% |
| 3 (8×8) | >10% | Media >65% | <3 seeds >60% |

---

## Análisis Planeado

### Estadística Descriptiva
- Media, desviación estándar, min, max por fase
- Boxplots success rate (últimos 100 eps)
- Histograma episodio breakthrough 6×6

### Comparaciones
- Seed 42 vs media otras 4 (t-test)
- Convergencia 6×6 vs 8×8 (paired t-test)
- Overhead steps vs Manhattan (ANOVA)

### Figuras
1. Boxplot success rates (3 fases, 5 seeds)
2. Breakthrough distribution 6×6 (histogram)
3. Transfer effectiveness (scatter primer_éxito vs seed)
4. Varianza temporal 6×6 (líneas por seed)

---

## Resultados Esperados

### Escenario A: Multi-Seed Exitoso (Mejor Caso)
- 5/5 seeds pasan gates
- Media 4×4: 87% ± 8%
- Media 6×6: 55% ± 18%
- Media 8×8: 78% ± 12%
- Breakthrough 6×6: 550 ± 100 eps
- **Conclusión**: v10_viable reproducible, curriculum robusto

### Escenario B: Multi-Seed Parcial (Caso Realista)
- 4/5 seeds pasan gates (1 seed falla 6×6)
- Media 6×6: 45% ± 25%
- Varianza alta pero breakthrough consistente
- **Conclusión**: Curriculum funcional pero sensible, requiere documentar fragilidad

### Escenario C: Multi-Seed Falla (Peor Caso)
- ≤2 seeds pasan gate 6×6
- Media 6×6 <30%
- No hay patrón breakthrough reproducible
- **Conclusión**: seed=42 fue suerte, curriculum necesita rediseño

---

## Decisiones Post-Hoc

### Si Escenario A o B:
1. ✅ Generar `REPORTE_MULTISEED.md`
2. ✅ Proceder con Fase 2 (ablation study)
3. ✅ Proceder con Fase 3 (PGF offline)

### Si Escenario C:
1. ⚠️ **NO proceder** con ablation/PGF
2. 🔧 Rediseñar curriculum:
   - Opción 1: Fase intermedia 5×5
   - Opción 2: Ajustar hyperparameters 6×6
   - Opción 3: Curriculum adaptativo (gates dinámicos)
3. 📝 Documentar v10_viable como "resultado preliminar N=1"

---

## Compromiso Científico

**Declaro públicamente**:
- Estos criterios están fijados **antes de ejecutar** las nuevas seeds
- No ajustaré gates post-hoc para "forzar" éxito
- Reportaré resultados honestos incluso si contradicen v10_viable
- Si multi-seed falla, documentaré limitaciones sin ocultarlas

**Trazabilidad**:
- Este preregistro se guarda en commit independiente
- Fecha commit: _pendiente_
- Hash commit: _pendiente_

---

## Firma

**Investigador**: Sistema Autónomo TUI v4.1  
**Fecha**: 5 de diciembre de 2025  
**Status**: ⏳ Pendiente ejecución

---

## Referencias

- **Baseline v10_viable**: `results/pgf_v10_viable/`
- **Preregistro baseline**: commit `e099ab9`
- **Configuración exacta**: `scripts/run_curriculum_complete_viable.py`
