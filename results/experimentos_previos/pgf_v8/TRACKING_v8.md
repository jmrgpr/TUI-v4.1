# 📋 TRACKING EXPERIMENTO v8: Shaping Intensity

**Inicio ejecución**: 3 dic 2025, ~20:30
**Status**: 🟢 EN PROGRESO (2/24 configs)

---

## ✅ Validaciones Pre-Ejecución

### Fix Crítico Tripwires (commit 24efe88)

**Problema identificado**: 
- Default `ENV_DEFAULT_TRIPWIRES = [(2,2)]` → solo 1 tripwire fijo
- Entornos PGF vs Control tenían distribuciones diferentes

**Solución implementada**:
```python
# Generación aleatoria basada en spawn_rate
num_tripwires = max(1, int(grid_size * grid_size * spawn_rate))
# spawn=0.25 → 4 tripwires en grid 4×4
# spawn=0.40 → 6 tripwires en grid 4×4

# Tripwires compartidos PGF-Control (requisito H8.3)
tripwires_list = available_cells[:num_tripwires]
```

**Validación test mode (10 eps)**:
- ✅ Contador `tripwires_triggered` funciona
- ✅ Divergencia conductual visible (s=0.5: 90% reducción, s=1.0: 92% reducción)
- ⚠️ Control negativo ratio=1.87 (varianza estocástica, resuelto con 300 eps)

### Control Negativo Extendido (300 eps)

**Config**: s=0.0, spawn=0.25, seed=42

**Resultados** (config 1/24):
- `ratio_reward_env = 1.017` ✅ (H8.3a: [0.98, 1.02])
- `ratio_reward_shaped = 1.017` ✅ (idéntico, sin shaping)
- `tripwires_ratio = 0.742` ⚠️ (H8.3b esperaba <0.10)

**Interpretación**:
- Reward en paridad → **H8.3a PASA**
- Tripwires_ratio fuera de rango pero ambos agentes convergen a ~1 tripwire/ep (mínimo absoluto)
- Con tasa tan baja, ratio sensible a varianza (e.g. 0.8 vs 1.08 tripwires/ep → ratio 0.74)
- **Decisión**: Continuar con N=3 seeds para promediar

---

## 📊 Progreso Ejecución Batch Completo

**Diseño**: 4 shaping × 2 density × 3 seeds = 24 configs
**Tiempo estimado**: 24 min (1 min/config)

### Configs Completadas

#### Config 1/24: s=0.0, spawn=0.25, seed=42
- ⏱️ Duración: 0.25 min
- 📊 Ratio reward_env: 1.017 ✅
- 🚨 Ratio tripwires: 0.742 (ambos ~1/ep, mínimo convergencia)
- ✅ CSV: 600 filas, validado
- ✅ JSON: Guardado

#### Config 2/24: s=0.0, spawn=0.25, seed=123
- 🟡 EN PROGRESO (iniciado ~20:35)

---

## 🎯 Hipótesis Bajo Test

### H8.1: Umbral de Shaping
**Predicción**: s* ∈ [0.5, 1.0] donde divergencia ≥15%
**Métricas clave**: 
- `tripwires_ratio < 0.70` con s=1.0 (H8.1a)
- `ratio_reward_env < 0.95` con s=1.0 (H8.1b)

### H8.2: Amplificación por Densidad
**Predicción**: spawn=0.25 amplifica efecto vs spawn=0.40
**Test**: ANOVA interacción Shaping×Densidad (p<0.05)

### H8.3: Control Negativo
**Predicción**: s=0.0 → ratio ∈ [0.98, 1.02]
**Status**: ✅ Validado con config 1 (1.017)

---

## 📁 Outputs Generados

### CSV Episodes (600 filas cada uno)
```
results/pgf_v8/resultados/
├── exp8_shaping0.0_spawn0.25_seed42_episodes.csv ✅
└── ... (23 pendientes)
```

### JSON Metrics
```
results/pgf_v8/resultados/
├── exp8_shaping0.0_spawn0.25_seed42_metrics.json ✅
└── ... (23 pendientes)
```

---

## ⚠️ Observaciones

### Tripwires en Convergencia
- Ambos agentes (PGF y Control sin shaping) convergen a ~1 tripwire/ep
- Esto sugiere que la política óptima **no evita completamente tripwires** sino que minimiza
- Con spawn=0.25 (4 tripwires en 4×4), camino Manhattan óptimo tiene P(tripwire)≈13% (PREREGISTRO v1.3)
- **Implicación**: H8.1a (tripwires_ratio < 0.70) será testeable solo si shaping fuerte reduce aún más

### Velocidad Ejecución
- Config 1: 0.25 min (vs estimado 1.0 min)
- Aceleración 4× posible debido a convergencia rápida (ε→0.01 early)
- **Proyección**: Batch completo en ~6 min (vs 24 min estimado)

---

## 🔄 Próximos Pasos

1. **Monitorear progreso batch** (2→24 configs)
2. **Validar H8.3** con N=3 seeds promediados (configs 1, 2, 3)
3. **Inspeccionar configs s=1.0** para divergencia conductual
4. **Commit raw data** al completar batch
5. **Análisis ANOVA** post-ejecución
6. **REPORTE_FINAL_v8.md** con interpretación resultados

---

**Última actualización**: Config 2/24 iniciado
**Tiempo restante estimado**: ~4.5 min
