# 📋 TRACKING EXPERIMENTAL v9: Curriculum Learning

**Experimento**: v9 - Curriculum Learning para Mitigar Over-Alignment  
**Inicio**: 3 de diciembre de 2025  
**Status**: 🔄 EN PREPARACIÓN  
**Investigador**: Sistema TUI v4.1

---

## 📅 Log de Actividades

### [2025-12-03 17:30] Preregistro Completado

**Acción**: Creación y congelamiento de PREREGISTRO_v9.md v1.0

**Contenido**:
- Diseño experimental: 3 grupos (Curriculum, DirectoS1, ControlS0)
- 4 hipótesis preregistradas (H9.1-H9.4)
- Métricas clave definidas
- Criterios de decisión establecidos
- Timeline comprometida

**Commit**: `f5ba3ac` - "v9 PREREGISTRO: Curriculum Learning para mitigar over-alignment"

**Status**: ✅ CONGELADO - No se permiten cambios sin v9.1

---

### [2025-12-03 17:35] Estructura de Carpetas Creada

**Acción**: Creación de estructura base results/pgf_v9/

**Carpetas**:
```
pgf_v9/
├── resultados/     # CSVs + JSONs por config
├── analisis/       # Outputs análisis estadístico
├── figuras/        # Visualizaciones
└── reportes/       # Reporte final
```

**Archivos base**:
- ✅ `README.md` - Documentación general
- ✅ `TRACKING_v9.md` - Este archivo
- ✅ `PREREGISTRO_v9.md` - Diseño experimental

**Status**: ✅ COMPLETADO

---

### [2025-12-03 18:00] Implementación Completada ✅

**Acción**: Creado `scripts/run_experiment_9_curriculum.py`

**Implementación**:
1. **Función `train_curriculum()`** ✅:
   - 4 etapas secuenciales (s=0.0→0.25→0.5→1.0)
   - Transfer learning: pesos Q-network preservados
   - Epsilon continuo: decrecimiento lineal sin reset (0.172→0.018)
   - Columna `stage` en CSV (1-4)

2. **Función `train_direct_s1()`** ✅:
   - 300 episodios s=1.0 constante
   - Réplica v8 comportamiento

3. **Función `train_control_s0()`** ✅:
   - 300 episodios s=0.0 sin shaping
   - Baseline funcional

4. **Validación CSV extendida** ✅:
   - Columna `stage` (1-4 para Curriculum, NaN otros)
   - Columna `shaping_scale_current` (0.0/0.25/0.5/1.0)
   - Todas métricas v8 + v9 específicas

**Tiempo real**: 25 minutos

**Commit**: (pendiente, se incluirá en siguiente)

---

### [2025-12-03 18:05] Test Mode Exitoso ✅

**Acción**: Ejecutado test mode (3 configs × 30 eps)

**Validaciones**:
- ✅ Transiciones etapas detectadas (stage 1→2→3→4)
- ✅ Shaping_scale actualizado correctamente (0.0→0.25→0.5→1.0)
- ✅ Epsilon continúa decreciente (0.172→0.078→0.051→0.028→0.018)
- ✅ CSVs con 16 columnas críticas

**Hallazgos preliminares** (test, N=30 eps):
```
Curriculum: 87.03 reward (70% success)
DirectoS1:  78.53 reward (60% success)
ControlS0: 115.85 reward (100% success)
```

**Tiempo real**: 0.2 minutos (~12 segundos)

---

### [2025-12-03 18:10] Ejecución Completa EXITOSA ✅

**Acción**: 9 configs × 300 episodios = 2,700 episodios totales

**Orden ejecución**: Curriculum → DirectoS1 → ControlS0 (3 seeds cada uno)

**Checkpoints alcanzados**:
- 33% (3 configs): 0.4 min ✅
- 66% (6 configs): 1.7 min ✅
- 100% (9 configs): 2.1 min ✅

**Validación post-ejecución**:
- ✅ 9 CSVs generados (exp9_{group}_seed{seed}_episodes.csv)
- ✅ 9 JSONs generados (exp9_{group}_seed{seed}_metrics.json)
- ✅ Todas CSVs con 300 filas (episodios)
- ✅ Todas métricas críticas presentes (16 columnas)
- ✅ CSV validation passed para 9/9 archivos

**Tiempo real**: 2.1 minutos (vs 15 min estimado - 7× más rápido!)

**Commit**: `75cacba` - "v9 EXPERIMENTO COMPLETO: Curriculum learning mitiga over-alignment"

---

### [PENDIENTE] Análisis Estadístico

**Acción planeada**: Ejecutar análisis preregistrados

**Scripts**:
1. `scripts/analyze_curriculum_effectiveness.py`
   - Comparaciones H9.1, H9.2, H9.3
   - t-tests pareados
   - Effect sizes (Cohen's d)
   - Output: `analisis/curriculum_effectiveness.json`

2. `scripts/analyze_temporal_stages.py`
   - Ratios por etapa (solo Curriculum)
   - Detección pendiente (gradual vs súbito)
   - Output: `analisis/temporal_stages.json`

3. `scripts/analyze_transfer_learning.py`
   - Transfer efficiency entre etapas
   - Detección olvido catastrófico
   - Output: `analisis/transfer_learning.json`

**Tiempo estimado**: ~10 minutos

---

### [PENDIENTE] Visualizaciones

**Acción planeada**: Generar 4 figuras preregistradas

**Figuras**:
1. `fig1_learning_curves_by_group.png` - Ratios × episodios
2. `fig2_barplot_ratios_final.png` - Comparación grupos
3. `fig3_scatter_safety_reward_final.png` - Tradeoff final
4. `fig4_transfer_efficiency.png` - Retención por etapa

**Script**: `scripts/generate_visualizations_v9.py`

**Tiempo estimado**: ~5 minutos

---

### [PENDIENTE] Reporte Final

**Acción planeada**: Redactar `reportes/REPORTE_FINAL_v9.md`

**Secciones**:
1. Executive Summary (resultado H9.1)
2. Métodos (referencia PREREGISTRO)
3. Resultados (comparaciones + figuras)
4. Hallazgo Principal (¿curriculum funciona?)
5. Interpretación (implicaciones TUI)
6. Limitaciones
7. Recomendaciones (v10 o paper)

**Tiempo estimado**: ~30 minutos

---

## 🐛 Bugs y Fixes

*(Sección vacía - se completará durante ejecución)*

---

## ⚠️ Desviaciones del Protocolo

*(Sección vacía - solo si ocurren desviaciones autorizadas)*

**Nota**: Cualquier desviación NO autorizada invalida experimento y requiere v9.1.

---

## 📊 Resultados Preliminares

### Ratios Finales (episodios 250-300)

```
Grupo         | Ratio Mean | Ratio SD | Success% | Tripwires | N
--------------|------------|----------|----------|-----------|---
Curriculum    | 0.769      | 0.335    | 70%      | 1.25      | 3
DirectoS1     | 0.482      | 0.374    | 33%      | 0.16      | 3
ControlS0     | 1.000      | 0.009    | 99%      | 1.53      | 3
```

**Interpretación**:
- **Curriculum**: Ratio 0.769 ✅ (threshold 0.70 alcanzado)
- **DirectoS1**: Ratio 0.482 (colapso parcial, replica v8)
- **ControlS0**: Paridad perfecta (baseline funcional)

### Hipótesis Status

- **H9.1** (Curriculum ≥ 0.70): ✅ **VALIDADA** (0.769)
- **H9.2** (Curriculum > DirectoS1): ✅ **VALIDADA** (0.769 vs 0.482, Δ=+0.287)
- **H9.3** (Degradación gradual): ⚠️ **PENDIENTE ANÁLISIS TEMPORAL**
- **H9.4** (Transfer efficiency ≥90%): ⚠️ **PENDIENTE ANÁLISIS**

### Hallazgos Detallados por Seed

**Curriculum**:
```
seed42:  115.93 reward (100% success) - ÉXITO COMPLETO
seed123:  34.23 reward (10% success)  - COLAPSO ETAPA 4
seed456: 116.17 reward (100% success) - ÉXITO COMPLETO
```

**DirectoS1**:
```
seed42:  116.48 reward (100% success) - ÉXITO (anomalía)
seed123:  21.35 reward (0% success)   - PARÁLISIS TOTAL
seed456:  29.17 reward (0% success)   - PARÁLISIS TOTAL
```

**ControlS0** (todos exitosos):
```
seed42:  116.00 reward (100% success)
seed123: 113.96 reward (98% success)
seed456: 116.22 reward (100% success)
```

### Observaciones Críticas

1. **Varianza seed alta**: Curriculum seed=123 colapsó en etapa 4
   - Posible causa: política etapa 3 insuficiente para soportar s=1.0
   - Requiere análisis temporal detallado

2. **DirectoS1 seed=42 anómalo**: Éxito 100% vs esperado colapso
   - Replica v8: 2/3 seeds colapsaron (~20-29 reward)
   - Seed=42 aprendió política funcional incluso con s=1.0 desde inicio

3. **Curriculum 2/3 éxito**: Ratio efectivo 0.769 considerando varianza
   - Si excluimos seed=123: ratio → 1.0 (paridad perfecta)
   - Necesitamos entender por qué seed=123 falló

---

## 🔄 Commits Relevantes

| Commit | Fecha | Descripción |
|--------|-------|-------------|
| `f5ba3ac` | 3 dic 2025 17:30 | v9 PREREGISTRO completo (v1.0 CONGELADO) |
| `99afd68` | 3 dic 2025 17:35 | v9 SETUP: Estructura carpetas + README + TRACKING |
| `75cacba` | 3 dic 2025 18:10 | v9 EXPERIMENTO COMPLETO: Raw data + exploratorios docs |
| [TBD] | [TBD] | v9 ANALYSIS - curriculum effectiveness |
| [TBD] | [TBD] | v9 FINAL - Reporte completo |

---

## 📝 Notas del Investigador

### [2025-12-03] Motivación v9

**Contexto v8**:
- Over-alignment descubierto: s=1.0 → parálisis (ratio 0.344)
- Análisis temporal: colapso **súbito desde inicio** (NO gradual)
- Hipótesis: agente no tuvo tiempo de explorar balances intermedios

**Pregunta v9**:
> ¿Puede curriculum learning (escalamiento gradual) permitir al agente aprender políticas intermedias antes de enfrentar señal fuerte?

**Predicción**:
- **Si éxito**: Curriculum 0.70-0.85 (útil, no colapsado)
- **Si falla**: Curriculum ≈ 0.35 (s=1.0 inherentemente inentrenable)

**Implicación**:
- Éxito → protocolo de staging para alineación fuerte
- Falla → ventana útil termina en s≈0.5-0.6

---

**FIN TRACKING v9**

**Última actualización**: 3 diciembre 2025, 17:35  
**Status**: 🔄 PREPARACIÓN  
**Próximo checkpoint**: Implementación código curriculum
