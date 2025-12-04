# 📂 Experimento v9.1: Validación Estadística Robusta (N=10)

**Título**: Validación Estadística del Curriculum Learning: Estudio con N=10 Seeds  
**Fecha inicio**: 4 de diciembre de 2025  
**Status**: 🔄 EN PREPARACIÓN  
**Preregistro**: `PREREGISTRO_v9.1.md` (v1.0 - CONGELADO)  
**Predecesor**: v9 (N=3, evidencia preliminar)

---

## 🎯 Objetivo

**Validar estadísticamente** los hallazgos preliminares de v9 (curriculum learning mitiga over-alignment) mediante incremento de muestra de **N=3 → N=10 seeds**, alcanzando potencia estadística adecuada (60-80% vs 18%).

**Pregunta central**: ¿Los efectos observados en v9 (ratio=0.766, d=0.661) alcanzan significancia estadística con N=10 y confirman la robustez del curriculum?

**Motivación crítica** (Peer Review v9):
- ⚠️ N=3 insuficiente → Potencia 18%
- ⚠️ H9.1/H9.2 no significativas (IC cruzaba thresholds, p>0.05)
- ⚠️ Alta varianza inter-seed (CV=0.532, seed=123 colapsó)

---

## 🔬 Diseño Experimental

### Diferencias vs v9 (ÚNICO CAMBIO: N)

| Parámetro | v9 (Original) | v9.1 (Este Estudio) |
|-----------|---------------|---------------------|
| **N Seeds** | 3 | **10** |
| **Seeds** | {42, 123, 456} | {42, 123, 456, 789, 101112, 131415, 161718, 192021, 222324, 252627} |
| **Grid** | 4×4 | 4×4 (idéntico) |
| **Curriculum** | [0.0→0.25→0.5→1.0] | [0.0→0.25→0.5→1.0] (idéntico) |
| **Episodios** | 300 (75/etapa) | 300 (75/etapa) (idéntico) |

**Total configuraciones**: 3 grupos × 10 seeds = **30 configs**  
**Total episodios**: 30 × 300 = **9,000 episodios**  
**Tiempo estimado**: ~6 horas cómputo

### Grupos Experimentales (Idénticos v9)

1. **CURRICULUM** (grupo experimental)
   - 4 etapas × 75 eps: s=0.0 → s=0.25 → s=0.5 → s=1.0
   - Transfer learning: pesos Q-network preservados

2. **DIRECTO_S1** (control positivo)
   - 300 eps s=1.0 constante

3. **CONTROL_S0** (control negativo, baseline)
   - 300 eps s=0.0 sin shaping

---

## 📊 Hipótesis Actualizadas (vs v9)

### H9.1.1: Curriculum Superior a Directo (ACTUALIZADA)

> Ratio Curriculum/Control ≥ 0.70 con IC 95% que **NO cruza threshold** (vs v9: IC cruzaba)

**Test**: Bootstrap 95% CI (10,000 iteraciones)  
**Criterio éxito**: mean(ratios) > 0.70 AND ci_lower > 0.70

### H9.2.1: Curriculum Alcanza Paridad con Control (ACTUALIZADA)

> Curriculum ≈ Control (no diferencia significativa) con **potencia adecuada** (vs v9: p=0.17, underpowered)

**Test**: Paired t-test (two-tailed), α=0.05  
**Criterio éxito**: p < 0.05 AND Cohen's d > 0.5

### H9.3.1: Curriculum Mantiene Prudencia (Replicación)

> Tripwires Curriculum ≤ Control (prudencia mantenida)

**Test**: Wilcoxon signed-rank test

### H9.4.1: Degradación Gradual (Replicación)

> Reward env decrece gradualmente (NO colapso súbito drop >50 entre etapas)

**Test**: Linear regression por seed, 0/10 seeds colapso súbito

---

## 📈 Predicciones Pre-Ejecución

### Escenario Optimista (70% probabilidad)

**Métricas finales**:

| Grupo | Reward Env | Success Rate | Seeds Exitosas | Interpretación |
|-------|------------|--------------|----------------|----------------|
| **Curriculum** | 100-110 | 75-85% | **7-8/10 (70-80%)** | Mayoría paridad |
| **DirectoS1** | 50-60 | 30-40% | 1-2/10 | Parálisis consistente |
| **ControlS0** | 114-116 | 98-100% | 10/10 | Baseline estable |

**Hipótesis**:
- ✅ H9.1.1: Ratio 0.75±0.20, IC [0.62, 0.88] → NO cruza 0.70
- ✅ H9.2.1: p<0.01, d=0.70
- ✅ Reducción CV: 0.30 vs 0.532 (v9)

**Patrón seeds vulnerables**: 2-3/10 colapsan en etapa 4 (tipo-123)

### Escenario Pesimista (30% probabilidad)

**Métricas finales**:
- Curriculum: 80-90 reward, 55-65% success, **5-6/10 exitosas**
- CV NO reduce (<0.50, alta varianza persiste)

**Hipótesis**:
- ⚠️ H9.1.1: Ratio 0.65±0.30, IC cruza 0.70 (marginal de nuevo)
- ⚠️ H9.2.1: p=0.03-0.06 (borderline)

**Interpretación**: Curriculum frágil, requiere adaptativo (v10)

---

## 📁 Estructura de Archivos

```
pgf_v9.1/
├── PREREGISTRO_v9.1.md             # Diseño experimental (v1.0 CONGELADO)
├── README.md                        # Este archivo
├── TRACKING_v9.1.md                 # Log de ejecución
├── resultados/                      # 30 CSVs (3 grupos × 10 seeds)
│   ├── curriculum_seed42_episodes.csv
│   ├── curriculum_seed123_episodes.csv
│   ├── curriculum_seed456_episodes.csv
│   ├── curriculum_seed789_episodes.csv
│   ├── ... (7 seeds más)
│   ├── directo_s1_seed42_episodes.csv
│   ├── ... (10 CSVs)
│   └── control_s0_seed42_episodes.csv
│       ... (10 CSVs)
├── analisis/                        # Outputs análisis estadístico
│   ├── curriculum_summary.json
│   ├── directo_s1_summary.json
│   ├── control_s0_summary.json
│   ├── hypothesis_tests.json        # H9.1.1-H9.4.1
│   ├── power_analysis.json          # N=3 vs N=10 comparación
│   └── seed_clustering.json         # Exitosas vs vulnerables
├── figuras/                         # Visualizaciones
│   ├── ratio_comparison_n3_vs_n10.png
│   ├── reward_by_group_n10.png
│   ├── success_rate_by_seed.png
│   ├── curriculum_trajectory_by_seed.png
│   └── hypothesis_tests_summary.png
├── exploratorios/                   # Análisis adicionales
│   └── seed_vulnerability_analysis.json
└── reportes/
    └── REPORTE_FINAL_v9.1.md        # Reporte post-ejecución
```

---

## 🔑 Métricas Clave

### Primarias (Idénticas v9)

- **ratio_reward_env_final**: Curriculum/Control en eps 250-300
- **success_rate_final**: % goal_reached eps 250-300
- **tripwires_final**: Mean tripwires/episode eps 250-300

### Nuevas Métricas (v9.1 específicas)

- **Coefficient of Variation (CV)**: std/mean por grupo
- **Seeds exitosas**: Count seeds con ratio ≥ 0.70
- **Clustering**: K-means (exitosas vs vulnerables)

---

## 📊 Análisis Comparativos v9 vs v9.1

### Reducción Incertidumbre

```
N=3 (v9):   ratio = 0.766 ± 0.404 (IC: [-0.236, 1.769])
N=10 (v9.1): ratio = 0.75 ± 0.20 (IC: [0.62, 0.88]) esperado
```

**Reducción IC width**: 50% (2.005 → 0.26)

### Aumento Potencia

```
N=3:  Potencia = 18% (para d=0.661)
N=10: Potencia = 60-65% esperada
```

**Mejora**: 3.3× más potencia

---

## 🔗 Contexto Experimental

### Basado en v9 (Evidencia Preliminar)

**Hallazgos v9 (N=3)**:
- Ratio Curriculum: 0.766 ± 0.404 (2/3 seeds exitosas)
- H9.1: NO significativa (IC cruza threshold)
- H9.2: p=0.17 (insuficientemente powered)
- Patrón bimodal: 67% éxito, 33% colapso (seed=123)

**Conclusión v9**: "Evidencia sugestiva de efectividad"

**Gap v9.1 resuelve**: Validación estadística definitiva con muestra adecuada

**Ver**: 
- `results/pgf_v9/REPORTE_FINAL_v9.md` (reporte v9 completo)
- `results/pgf_v9/PEER_REVIEW_RESPONSE.md` (análisis críticas)

---

## 🚀 Estado de Ejecución

**Pre-ejecución**:
- ✅ Preregistro v1.0 completo y congelado (4 dic 2025)
- ✅ Estructura de carpetas creada
- ✅ README documentado
- ⏳ TRACKING iniciado
- ⏳ Implementación código (adaptación v9 con 10 seeds)
- ⏳ Test mode (2 seeds × 30 eps)
- ⏳ Ejecución completa (30 configs × 300 eps = 9,000 eps)

**Timeline estimado**:
- Implementación: ~15 min (adaptar script v9)
- Test mode: ~1 min
- Ejecución: ~6 horas (background)
- Análisis: ~30 min
- Reporte: ~1 hora

**Deadline**: 6 diciembre 2025, 18:00 (permite análisis + v10 desarrollo)

---

## 📝 Criterios de Éxito

### ÉXITO COMPLETO ✅

- H9.2.1 significativa (p<0.05)
- H9.1.1: IC NO cruza 0.70
- ≥60% seeds exitosas (6/10)
- Reducción CV < 0.40

**Conclusión**: Curriculum robusto en 4×4 → Escalar a v10 (8×8 adaptive)

### ÉXITO PARCIAL ⚠️

- H9.2.1: p=0.05-0.10
- 50-60% seeds exitosas
- CV reduce a 0.45-0.50

**Conclusión**: Curriculum funciona pero frágil → v10 adaptativo crítico

### FALLA ❌

- H9.2.1: p>0.10
- <50% seeds exitosas
- CV NO reduce (≥0.50)

**Conclusión**: Curriculum NO robusto → Investigar causas fundamentales antes de v10

---

## 📚 Referencias

- **Preregistro**: `PREREGISTRO_v9.1.md` (30 páginas, 620 líneas)
- **v9 Original**: `results/pgf_v9/REPORTE_FINAL_v9.md`
- **Peer Review v9**: `results/pgf_v9/PEER_REVIEW_RESPONSE.md`
- **Teoría TUI**: `docs/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md`

---

**Fecha creación**: 4 diciembre 2025  
**Status**: 🔄 PREPARACIÓN  
**Próximo paso**: Crear `scripts/run_experiment_9.1_robust.py`
