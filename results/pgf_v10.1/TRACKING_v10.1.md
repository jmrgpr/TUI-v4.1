# 📋 TRACKING EXPERIMENTAL v10.1: Adaptive Curriculum 8×8 Economía Calibrada

**Experimento**: v10.1 - Adaptive Curriculum 8×8 con balance=5.0  
**Inicio**: 4 de diciembre de 2025  
**Status**: 🔄 PREPARACIÓN  
**Investigador**: Sistema TUI v4.1  
**Predecesor**: v10 (8×8 trivial, balance=8.0 → saturación)

---

## 📅 Log de Actividades

### [2025-12-04 22:30] PREREGISTRO v10.1 Congelado

**Acción**: Creación y congelamiento PREREGISTRO_v10.1.md v1.0

**Motivación**: v10 resultó trivial (balance=8.0 → 470% margen → todas 100% success)

**Cambios clave vs v10**:
- INITIAL_BALANCE: 8.0 → **5.0** (margen 257%, mismo v9.1 exitoso)
- N seeds: 5 → **8** (potencia 45% → 65%)
- Hipótesis ajustadas: H10.1.1-H10.4.1
- Gates críticos: Control 70-90% success para proceder

**Commit**: `c68f8dd` - "PREREGISTRO v10.1: 8×8 economía ajustada (balance=5.0) - CONGELADO"

**Status**: ✅ CONGELADO - No cambios permitidos sin v10.1.1

---

### [2025-12-04 23:00] Estructura de Carpetas Creada

**Acción**: Creación estructura completa `results/pgf_v10.1/`

**Carpetas**:
```
pgf_v10.1/
├── resultados/      # 24 CSVs (3 grupos × 8 seeds)
├── analisis/        # Tests estadísticos, episodes_per_stage
├── figuras/         # Visualizaciones comparativas
├── exploratorios/   # Clustering seeds, análisis adicionales
└── reportes/        # Reporte final
```

**Archivos base**:
- ✅ `PREREGISTRO_v10.1.md` - Diseño experimental (CONGELADO)
- ✅ `README.md` - Documentación general
- ✅ `TRACKING_v10.1.md` - Este archivo

**Status**: ✅ COMPLETADO

---

### [PENDIENTE] Desarrollo Script v10.1

**Acción**: Crear `run_experiment_10.1_balanced.py`

**Derivación de v10**:
- Base: `scripts/run_experiment_10_adaptive.py` (757 líneas)
- Cambios mínimos:
  1. `INITIAL_BALANCE = 5.0` (línea ~54, era 8.0)
  2. `SEEDS = [42, 123, 456, 789, 101112, 131415, 161718, 192021]` (8 vs 5)
  3. `OUTPUT_DIR = 'results/pgf_v10.1/resultados'` (path correcto)
  4. Logging: mencionar v10.1, no v10

**Validaciones**:
- ✅ Mismo AdaptiveCurriculum (threshold 0.60, timeout 150)
- ✅ Mismo Fixed/Control logic
- ✅ CSV/JSON structure idéntica v10
- ✅ ResourceDensityEnv con API correcta

**Tiempo estimado**: ~1-2 horas

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Test Mode (Gate Crítico)

**Acción**: Ejecutar test mode con 2 seeds × 100 eps

```bash
python scripts/run_experiment_10.1_balanced.py --test_mode --seeds 42,789 --max_episodes 100
```

**Validaciones esperadas**:

#### Gate Crítico: Success Rate Control
- ✅ **70-90% success** → PROCEDER con batch completo
- ❌ **>95% success** → ABORTAR (aún trivial, balance debe bajar a 4.5)
- ❌ **<60% success** → AJUSTAR balance a 5.5 o 6.0

#### Otras validaciones:
- ✅ Adaptive transitions threshold-based (no solo timeout)
- ✅ Episodes/etapa Stage 0: 30-50 (vs 25-31 trivial v10)
- ✅ Resources recolectados (críticos con balance=5.0)
- ✅ Divergencia conductual visible (Adaptive vs Fixed vs Control)
- ✅ CSVs exportan correctamente

**Tiempo estimado**: ~10 min ejecución + 30 min análisis

**Status**: ⏳ PENDIENTE (requiere script completado)

---

### [PENDIENTE] Decisión GO/NO-GO

**Acción**: Analizar test mode → Decidir ejecución batch

**Criterios decisión**:

**🟢 GO (ejecutar batch completo)**:
- Control: 70-90% success ✓
- Adaptive personaliza (eps/etapa variable) ✓
- Fixed/Adaptive divergen (no convergen) ✓
- **Interpretación**: Balance calibrado correctamente

**🟡 AJUSTAR (balance intermedio)**:
- Control: 60-70% success (muy al límite)
- **Acción**: Subir balance a 5.5, repetir test mode
- **Interpretación**: 5.0 un poco agresivo

**🟡 AJUSTAR (aún trivial)**:
- Control: 90-95% success (borderline)
- **Acción**: Bajar balance a 4.5, repetir test mode
- **Interpretación**: 5.0 aún generoso

**🔴 ABORT (extremos)**:
- Control >95% OR <60%
- **Acción**: Crear v10.2 con balance muy diferente (4.0 o 6.0)
- **Interpretación**: 5.0 no es punto dulce, requiere repreregistro

**Status**: ⏳ PENDIENTE (requiere test mode)

---

### [PENDIENTE] Ejecución Completa

**Acción**: Batch completo 24 configs

**Configuración**:
```python
# Grupos
GROUPS = ['ControlS0', 'FixedCurriculum', 'AdaptiveCurriculum']

# Seeds (N=8, vs N=5 en v10)
SEEDS = [42, 123, 456, 789, 101112, 131415, 161718, 192021]

# Total
N_CONFIGS = 3 × 8 = 24
N_EPISODES_APPROX = 24 × 400 = 9,600
```

**Checkpoints**:
- Cada 6 configs (~2.5h)
- Validar CSVs parciales, verificar no errores
- Backup automático

**Tiempo estimado**: ~10-12 horas

**Status**: ⏳ PENDIENTE (requiere GO decision)

---

### [PENDIENTE] Análisis Estadístico

**Acción**: Tests hipótesis + comparación v10 vs v10.1

**Análisis incluidos**:

1. **Tests H10.1.1 - H10.4.1**:
   - H10.1.1: Ratio ≥0.70 (bootstrap CI)
   - H10.2.1: Adaptive > Fixed (paired t-test)
   - H10.3.1: CV ratio < 0.80 (Levene's test)
   - H10.4.1: Seeds vulnerables ≥60%

2. **Episodes per stage (Adaptive)**:
   - Distribución por seed
   - Correlación eps_critical vs success
   - Comparación v10 trivial (25-31) vs v10.1 esperado (80-120)

3. **Comparación v10 vs v10.1**:
   - Efecto balance en discriminación
   - Success rates: 100% trivial → 70-90% funcional
   - Ratios: 0.995 paridad → 0.75-0.85 costo visible

4. **Clustering seeds**: Rápidas/lentas (K-means)

**Outputs esperados**:
- `analisis/hypothesis_tests_v10.1.json`
- `analisis/episodes_per_stage_adaptive.json`
- `analisis/comparison_v10_vs_v10.1.json`
- `analisis/final_metrics_v10.1.csv`

**Tiempo estimado**: ~2 horas

**Status**: ⏳ PENDIENTE (requiere batch completo)

---

### [PENDIENTE] Visualizaciones

**Acción**: Generar figuras comparativas v10 vs v10.1

**Figuras clave**:

1. **ratio_v10_vs_v10.1.png**: Barplot lado a lado
   - v10: ratio=0.995 (trivial)
   - v10.1: ratio esperado 0.75-0.85 (funcional)

2. **success_by_group_v10.1.png**: Boxplots 3 grupos
   - Mostrar dispersión
   - Identificar outliers

3. **episodes_per_stage_heatmap.png**: Heatmap seeds × stages (Adaptive)
   - Stage 0: 80-120 eps
   - Stages 1-3: 30-50 eps cada una
   - Stage 4: 50-80 eps

4. **cv_comparison.png**: Fixed vs Adaptive varianza
   - v10: CV ratio=12.6 (Adaptive MÁS variable)
   - v10.1 esperado: CV ratio=0.70 (Adaptive MENOS variable)

5. **seed_vulnerability_v10.1.png**: Trayectorias seeds débiles
   - Seed 123 rescate (vs colapso v9.1 4×4)

**Tiempo estimado**: ~1 hora

**Status**: ⏳ PENDIENTE (requiere análisis completo)

---

### [PENDIENTE] Reporte Final

**Acción**: Crear `reportes/REPORTE_FINAL_v10.1.md`

**Secciones**:
1. Resumen ejecutivo (discriminación recuperada?)
2. Motivación (v10 trivial → ajuste balance)
3. Resultados principales (hipótesis validadas/rechazadas)
4. Comparación v10 vs v10.1 (efecto balance)
5. Episodes per stage (personalización Adaptive)
6. Escalamiento 4×4→8×8 (v9.1 vs v10.1)
7. Limitaciones + próximos pasos

**Tiempo estimado**: ~3 horas

**Status**: ⏳ PENDIENTE (requiere análisis + figuras)

---

## 📊 Métricas de Progreso

### Desarrollo
- [ ] Script v10.1 creado
- [ ] Test mode ejecutado
- [ ] Gates validados

### Decisión
- [ ] Test mode analizado
- [ ] GO/NO-GO decidido

### Ejecución
- [ ] Configs completadas: 0/24
- [ ] Episodios completados: 0/9,600
- [ ] Tiempo transcurrido: 0/12 horas

### Análisis
- [ ] Tests estadísticos ejecutados
- [ ] Episodes_per_stage analizado
- [ ] Comparación v10 vs v10.1 completada
- [ ] Figuras generadas
- [ ] Reporte final escrito

---

## 🎯 Hitos Clave

| Hito | Fecha Objetivo | Status | Dependencia |
|------|----------------|--------|-------------|
| Preregistro congelado | 2025-12-04 22:30 | ✅ | - |
| Estructura carpetas | 2025-12-04 23:00 | ✅ | - |
| Script v10.1 completado | 2025-12-05 01:00 | ⏳ | - |
| Test mode ejecutado | 2025-12-05 02:00 | ⏳ | Script |
| **GO/NO-GO decidido** | **2025-12-05 03:00** | ⏳ | **Test mode** |
| Batch iniciado | 2025-12-05 09:00 | ⏳ | GO decision |
| Checkpoint 1 (6 configs) | 2025-12-05 12:00 | ⏳ | Batch |
| Checkpoint 2 (12 configs) | 2025-12-05 15:00 | ⏳ | Batch |
| Checkpoint 3 (18 configs) | 2025-12-05 18:00 | ⏳ | Batch |
| Batch completo | 2025-12-05 21:00 | ⏳ | Batch |
| Análisis estadístico | 2025-12-05 23:00 | ⏳ | Batch |
| Reporte final | 2025-12-06 02:00 | ⏳ | Análisis |

---

## 🔔 Notas y Observaciones

### Diferencias Metodológicas v10 vs v10.1

**v10 (balance=8.0)**:
- Margen: 470% (80 steps / 14 Manhattan)
- Resultado: TODAS 100% success (trivial)
- Hallazgo: Límite superior curriculum (saturación)
- Valor: Documenta cuándo curriculum es redundante

**v10.1 (balance=5.0)**:
- Margen: 257% (50 steps / 14 Manhattan)
- Predicción: Control 80-90%, Adaptive 70-80%, Fixed 60-70%
- Objetivo: Validar escalamiento con presión real
- Valor: Testear si curriculum ayuda bajo presión (como v9.1)

### Transparencia Científica

**v10.1 NO es "arreglo" de v10**:
- v10 es hallazgo válido (saturación documentada)
- v10.1 es NUEVO experimento con economía calibrada
- Preregistrado ANTES de ejecución (rigor)
- Justificación cuantitativa: v9.1 balance=5.0 funcionó en 4×4

### Riesgos Identificados

**Riesgo 1: Balance=5.0 aún trivial** (15% probabilidad)
- Síntoma: Control >95% success en test mode
- Mitigación: Abortar, crear v10.2 con balance=4.5

**Riesgo 2: Balance=5.0 muy duro** (25% probabilidad)
- Síntoma: Control <60% success en test mode
- Mitigación: Ajustar a balance=5.5, repetir test

**Riesgo 3: Arquitectura insuficiente** (30% probabilidad)
- Síntoma: Control >80% PERO Adaptive/Fixed colapsan igualmente
- Diagnóstico: DQN 2×64 límite para 8×8
- Mitigación: Plan B con DQN 3×128

---

## 📝 Decisiones Pendientes

### Si Test Mode Falla Gates

**Control >95% (aún trivial)**:
- OPCIÓN 1: Abortar v10.1, crear v10.2 balance=4.0 o 4.5
- OPCIÓN 2: Continuar pero documentar como "límite intermedio"

**Control <60% (muy difícil)**:
- OPCIÓN 1: Ajustar balance=5.5 o 6.0, repetir test
- OPCIÓN 2: Abortar, documentar que 8×8 requiere balance >5.0

### Si v10.1 Éxito Completo

**Curriculum escala exitosamente**:
- Paper story: "v9.1 validó 4×4, v10.1 valida 8×8 con economía calibrada"
- Siguiente: v11 IPG completo O cierre con reporte consolidado

### Si v10.1 Éxito Parcial

**Curriculum ayuda pero límite arquitectura**:
- Siguiente: v10.2 con DQN 3×128 (mayor capacidad)
- O simplificar: grid 6×6 o 7×7 intermedio

---

**FIN TRACKING v10.1**

**Última actualización**: 4 diciembre 2025, 23:00  
**Status**: 🔄 PREPARACIÓN (estructura completa, script pendiente)  
**Próximo paso**: Crear `run_experiment_10.1_balanced.py`
