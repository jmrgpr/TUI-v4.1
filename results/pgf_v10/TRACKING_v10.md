# 📋 TRACKING EXPERIMENTAL v10: Adaptive Curriculum Learning 8×8

**Experimento**: v10 - Adaptive Curriculum Learning para Escalamiento 8×8  
**Inicio**: 4 de diciembre de 2025 (desarrollo), 5-6 dic (ejecución)  
**Status**: 🔄 EN PREPARACIÓN (desarrollo mientras v9.1 ejecuta)  
**Investigador**: Sistema TUI v4.1  
**Dependencia**: ⚠️ Analizar v9.1 resultados antes de ejecutar

---

## 📅 Log de Actividades

### [2025-12-04 10:00] Preregistro Completado

**Acción**: Creación y congelamiento de PREREGISTRO_v10.md v1.0

**Contenido**:
- Diseño experimental: 3 grupos (ControlS0, FixedCurriculum, AdaptiveCurriculum)
- Grid 8×8 (complejidad alta)
- 4 hipótesis preregistradas (H10.1-H10.4)
- Lógica adaptive threshold-based (success>0.75)
- N=5 seeds, balance cómputo/robustez

**Commit**: `089b258` - "PREREGISTROS v9.1 + v10: Validación robusta N=10 + Adaptive curriculum 8×8"

**Status**: ✅ CONGELADO - No se permiten cambios sin v10.1

---

### [2025-12-04 10:05] Estructura de Carpetas Creada

**Acción**: Creación de estructura base results/pgf_v10/

**Carpetas**:
```
pgf_v10/
├── resultados/      # 15 CSVs (3 grupos × 5 seeds)
├── analisis/        # JSONs estadísticos + episodes_per_stage
├── figuras/         # Visualizaciones Fixed vs Adaptive
├── exploratorios/   # Clustering, threshold sensitivity
└── reportes/        # Reporte final
```

**Archivos base**:
- ✅ `PREREGISTRO_v10.md` - Diseño experimental (30 páginas)
- ✅ `README.md` - Documentación general
- ✅ `TRACKING_v10.md` - Este archivo

**Status**: ✅ COMPLETADO

---

### [PENDIENTE] Desarrollo Lógica Adaptive

**Acción**: Implementar `scripts/run_experiment_10_adaptive.py`

**Componentes a desarrollar**:

1. **Clase `AdaptiveCurriculum`** ⏳:
   ```python
   class AdaptiveCurriculum:
       def __init__(self, stages=[0.0, 0.25, 0.5, 0.75, 1.0])
       def should_advance(self) → bool
       def update(self, goal_reached)
       def get_current_scale() → float
   ```
   - Threshold: success_rate_last_25 > 0.75
   - Timeout: episodes_in_stage > 150
   - Tracking: episodes_per_stage[stage]

2. **Función `train_adaptive_curriculum()`** ⏳:
   - Loop hasta stage==4 AND episodes_in_stage≥50
   - Máximo 500 eps (seguridad)
   - Logging transiciones

3. **Función `train_fixed_curriculum()`** (control) ⏳:
   - 4 etapas × 100 eps (fixed)
   - s=0.0→0.25→0.5→1.0

4. **Función `train_control_s0()`** (baseline) ⏳:
   - 400 eps s=0.0

5. **CSV extendido** ⏳:
   - Columnas: stage, episodes_in_stage, transition_triggered, success_rate_last_25

**Tiempo estimado**: ~2-3 días (mientras v9.1 ejecuta en background)

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Test Mode

**Acción**: Ejecutar test mode (1 seed × 100 eps, solo Adaptive)

**Validaciones esperadas**:
- ✅ Transiciones ocurren (logs muestran "Avanzando a stage X")
- ✅ Episodios/etapa razonables (50-120 rango esperado)
- ✅ Timeout funciona (si seed débil, usa 150 eps en etapa)
- ✅ CSV con todas columnas correctas
- ✅ Success_rate_last_25 se calcula bien

**Tiempo estimado**: ~5 min

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Decisión Ejecución (⚠️ GATE CRÍTICO)

**Acción**: Analizar resultados v9.1 → Decidir si ejecutar v10

**Criterios decisión**:

**🟢 GO (ejecutar v10)**:
- v9.1: H9.2.1 significativa (p<0.05)
- v9.1: ≥60% seeds exitosas
- **Interpretación**: Curriculum robusto en 4×4 → Escalar a 8×8 adaptive

**🟡 GO CON PRECAUCIÓN**:
- v9.1: H9.2.1 borderline (p=0.05-0.10)
- v9.1: 50-60% seeds exitosas
- **Interpretación**: Curriculum frágil → Adaptive es crítico en v10

**🔴 PAUSE (investigar antes)**:
- v9.1: H9.2.1 no significativa (p>0.10)
- v9.1: <50% seeds exitosas
- **Interpretación**: Problema fundamental → Analizar causas antes de v10

**Status**: ⏳ PENDIENTE (esperar v9.1)

---

### [PENDIENTE] Ejecución Completa

**Acción**: Ejecutar 15 configs × ~400 eps = 6,000 eps

**Configuración**:
```python
# 3 grupos
GROUPS = ['ControlS0', 'FixedCurriculum', 'AdaptiveCurriculum']

# 5 seeds
SEEDS = [42, 123, 456, 789, 101112]

# Grid
GRID_SIZE = 8  # 8×8 = 64 celdas
SPAWN_RATE = 0.25  # ~16 tripwires

# Total
N_CONFIGS = 3 × 5 = 15
N_EPISODES_APPROX = 15 × 400 = 6,000
```

**Checkpoints**:
- Cada 5 configs (2.5h aprox)
- Validar episodios/etapa para Adaptive

**Tiempo estimado**: ~8 horas

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Análisis Estadístico

**Acción**: Ejecutar análisis Fixed vs Adaptive en 8×8

**Análisis incluidos**:

1. **Tests hipótesis**: H10.1-H10.4
2. **Episodes per stage (Adaptive)**:
   - Distribución por seed
   - Correlación eps_critical vs success
3. **Comparación Fixed vs Adaptive**:
   - Ratios, success rates, CVs
4. **Clustering seeds**: Rápidas vs lentas (K-means)
5. **Caso seed=123**: ¿Se rescata con adaptive?

**Outputs esperados**:
- `analisis/hypothesis_tests.json`
- `analisis/episodes_per_stage_adaptive.json`
- `analisis/correlation_eps_vs_success.json`
- `exploratorios/seed_clustering_adaptive.json`

**Tiempo estimado**: ~1 hora

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Visualizaciones

**Acción**: Generar figuras comparativas

**Figuras clave**:
1. `ratio_fixed_vs_adaptive_8x8.png` - Barplot comparativo
2. `episodes_per_stage_by_seed.png` - Stacked bar (Adaptive)
3. `success_vs_eps_critical.png` - Scatterplot correlación
4. `scaling_4x4_vs_8x8.png` - v9 vs v10, Fixed vs Adaptive
5. `seed123_rescue.png` - Trayectoria específica seed vulnerable

**Narrativa visual**:
- Fixed colapsa en 8×8 (como proyección v9)
- Adaptive recupera paridad mediante personalización
- Seeds vulnerables usan más tiempo en etapas críticas

**Tiempo estimado**: ~30 min

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Reporte Final

**Acción**: Crear REPORTE_FINAL_v10.md

**Secciones**:
1. Resumen ejecutivo (hallazgos principales)
2. Metodología (diferencias vs Fixed, 4×4 vs 8×8)
3. Resultados principales (hipótesis + métricas)
4. Análisis adaptive-specific (episodes_per_stage, threshold effectiveness)
5. Comparación scaling (v9 4×4 → v10 8×8)
6. Caso seed=123 (rescate vs colapso)
7. Limitaciones + próximos pasos

**Tiempo estimado**: ~2 horas

**Status**: ⏳ PENDIENTE

---

## 📊 Métricas de Progreso

### Desarrollo

- [ ] Clase AdaptiveCurriculum implementada
- [ ] Test mode exitoso (transiciones OK)
- [ ] Validaciones pasadas

### Decisión Ejecución

- [ ] Resultados v9.1 analizados
- [ ] Criterio decisión evaluado (verde/amarillo/rojo)
- [ ] GO/PAUSE decidido

### Ejecución

- [ ] Configs completadas: 0/15
- [ ] Episodios completados: 0/6,000
- [ ] Tiempo transcurrido: 0/8 horas

### Análisis

- [ ] Tests estadísticos ejecutados
- [ ] Episodes_per_stage analizado
- [ ] Figuras generadas
- [ ] Reporte final escrito

---

## 🎯 Hitos Clave

| Hito | Fecha Objetivo | Status | Dependencia |
|------|----------------|--------|-------------|
| Preregistro congelado | 2025-12-04 10:00 | ✅ | - |
| Clase Adaptive implementada | 2025-12-04 18:00 | ⏳ | - |
| Test mode exitoso | 2025-12-04 19:00 | ⏳ | Implementación |
| **v9.1 resultados disponibles** | **2025-12-04 20:30** | ⏳ | **CRÍTICO** |
| Decisión GO/PAUSE v10 | 2025-12-04 21:00 | ⏳ | v9.1 completo |
| Ejecución iniciada | 2025-12-05 09:00 | ⏳ | GO decision |
| Checkpoint 1 (5 configs) | 2025-12-05 11:30 | ⏳ | Ejecución |
| Checkpoint 2 (10 configs) | 2025-12-05 14:00 | ⏳ | Ejecución |
| Ejecución completa | 2025-12-05 17:00 | ⏳ | Ejecución |
| Análisis estadístico | 2025-12-05 18:00 | ⏳ | Ejecución |
| Reporte final | 2025-12-05 20:00 | ⏳ | Análisis |

---

## 🔔 Notas y Observaciones

### Decisión Metodológica: Por Qué Adaptive

**Diagnóstico v9 falla 8×8**:
- Curriculum fijo: 4 etapas × 75 eps
- Seed=123 colapsó en etapa 4 (s=1.0) → necesitaba **más tiempo** en s=0.5
- 8×8: Complejidad mayor (Manhattan 14 vs 6) → requiere consolidación

**Solución adaptive**:
- Seeds fuertes: avanzan rápido (~80 eps/etapa)
- Seeds vulnerables: usan timeout (~150 eps en s=0.5)
- Personalización: cada seed a su ritmo

### Validación Threshold (success>0.75)

**¿Por qué 0.75?**:
- Balance: No muy estricto (0.90 estancaría), no muy laxo (0.60 prematura)
- Literatura: Bengio et al. sugieren "mastery" ~75-80%
- Empírico: v9 mostró seeds exitosas tenían >80% en etapas intermedias

**Sensibilidad** (exploratorio):
- Si seeds se estancan mucho: considerar 0.70
- Si avanzan muy rápido y colapsan: considerar 0.80

### Seeds Seleccionadas (N=5)

**Incluye seed=123** (vulnerable en v9 4×4):
- Test clave: ¿Adaptive la rescata en 8×8?
- Predicción: Usa ~200 eps en s=0.5+s=0.75, alcanza 70% success

**Balance N=5**:
- Compromiso cómputo (15 configs × 400 = 6,000 eps, ~8h)
- Suficiente para patrones (80% power con N=5 si d>0.8)

---

## 🚦 Predicciones Específicas

### Episodios por Etapa (Adaptive)

**Seed fuerte (e.g., 42)**:
- s=0.0: 80 eps (domina rápido)
- s=0.25: 90 eps
- s=0.5: 100 eps
- s=0.75: 70 eps
- s=1.0: 60 eps
- **Total**: 400 eps

**Seed vulnerable (e.g., 123)**:
- s=0.0: 100 eps
- s=0.25: 120 eps
- s=0.5: **150 eps** (usa timeout, no alcanza 0.75)
- s=0.75: 80 eps
- s=1.0: 50 eps
- **Total**: 500 eps

**Correlación esperada**: r>0.70 entre eps_critical (s=0.5+s=0.75) y success_final

---

## 📝 Decisiones Pendientes

### Si v9.1 Falla (🔴 Escenario Rojo)

**Opciones**:
1. **PAUSE v10**: Investigar por qué curriculum fijo falla incluso en 4×4 con N=10
2. **Simplificar v10**: Testar 6×6 primero (complejidad intermedia)
3. **Cambiar arquitectura**: DQN 3×128 en lugar de 2×64

### Si v9.1 Éxito Parcial (🟡 Escenario Amarillo)

**v10 se vuelve crítico**:
- Curriculum fijo funciona pero es frágil
- Adaptive es la solución para robustez
- Ejecutar v10 para demostrar escalamiento

### Si v9.1 Éxito Completo (🟢 Escenario Verde)

**v10 demuestra escalamiento**:
- Paper story: "Curriculum fijo 4×4 validado, escalamos a 8×8 con adaptive"
- High impact: NeurIPS/ICML submission

---

## 📈 Plan B (Si v10 Falla)

### Plan B1: Arquitectura Mayor

**Acción**: Re-ejecutar v10 con DQN 3×128 (vs 2×64)

**Justificación**:
- 8×8 = 64 celdas (vs 16 en 4×4)
- Política más compleja (Manhattan 14 vs 6)
- Red mayor puede ser necesaria

**Tiempo adicional**: ~10h cómputo

### Plan B2: Simplificar Ambiente

**Acción**: v10.1 con grid 7×7 (complejidad intermedia)

**Justificación**:
- Evitar salto 4×4 → 8×8 (demasiado abrupto)
- 7×7: ~12 tripwires, Manhattan 12
- Validar si problema es tamaño o schedule

### Plan B3: Incrementar Etapas

**Acción**: 6 etapas en lugar de 5

**Nuevas escalas**: [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

**Justificación**: Transiciones más suaves (Δ=0.2 vs 0.25)

---

**FIN TRACKING v10**

**Última actualización**: 4 diciembre 2025, 10:05  
**Status**: 🔄 PREPARACIÓN (desarrollo)  
**Dependencia crítica**: ⚠️ Esperar v9.1 resultados antes de ejecutar  
**Próximo paso**: Implementar clase AdaptiveCurriculum
