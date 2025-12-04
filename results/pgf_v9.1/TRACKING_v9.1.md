# 📋 TRACKING EXPERIMENTAL v9.1: Validación Estadística Robusta

**Experimento**: v9.1 - Validación Estadística (N=10) del Curriculum Learning  
**Inicio**: 4 de diciembre de 2025  
**Status**: 🔄 EN PREPARACIÓN  
**Investigador**: Sistema TUI v4.1

---

## 📅 Log de Actividades

### [2025-12-04 10:00] Preregistro Completado

**Acción**: Creación y congelamiento de PREREGISTRO_v9.1.md v1.0

**Contenido**:
- Diseño experimental: N=10 seeds (vs N=3 v9 original)
- 4 hipótesis actualizadas (H9.1.1-H9.4.1)
- Análisis potencia estadística: 60-80% vs 18% (v9)
- Predicciones pre-ejecución (optimista/pesimista)
- Criterios de éxito definidos

**Commit**: `089b258` - "PREREGISTROS v9.1 + v10: Validación robusta N=10 + Adaptive curriculum 8×8"

**Status**: ✅ CONGELADO - No se permiten cambios sin v9.2

---

### [2025-12-04 10:05] Estructura de Carpetas Creada

**Acción**: Creación de estructura base results/pgf_v9.1/

**Carpetas**:
```
pgf_v9.1/
├── resultados/      # 30 CSVs (3 grupos × 10 seeds)
├── analisis/        # JSONs estadísticos
├── figuras/         # Visualizaciones
├── exploratorios/   # Análisis adicionales
└── reportes/        # Reporte final
```

**Archivos base**:
- ✅ `PREREGISTRO_v9.1.md` - Diseño experimental (30 páginas)
- ✅ `README.md` - Documentación general
- ✅ `TRACKING_v9.1.md` - Este archivo

**Status**: ✅ COMPLETADO

---

### [PENDIENTE] Implementación Script

**Acción**: Adaptar `scripts/run_experiment_9_curriculum.py` → `run_experiment_9.1_robust.py`

**Cambios requeridos**:
1. **Seeds**: Añadir 7 nuevas [789, 101112, 131415, 161718, 192021, 222324, 252627]
2. **Checkpoints**: Cada 10 configs (3h aprox)
3. **Validación**: Test mode con 2 seeds × 30 eps

**Tiempo estimado**: ~15 min

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Test Mode

**Acción**: Ejecutar test mode (2 seeds × 30 eps)

**Validaciones esperadas**:
- ✅ 6 configs ejecutan sin errores (3 grupos × 2 seeds)
- ✅ CSV con columnas correctas (stage, shaping_scale_current, etc.)
- ✅ Transiciones curriculum visibles (s=0.0→0.25→0.5→1.0)
- ✅ Divergencia conductual entre grupos

**Tiempo estimado**: ~1 min

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Ejecución Completa

**Acción**: Ejecutar 30 configs × 300 eps = 9,000 eps

**Configuración**:
```python
# 3 grupos
GROUPS = ['Curriculum', 'DirectoS1', 'ControlS0']

# 10 seeds
SEEDS = [42, 123, 456, 789, 101112, 131415, 161718, 192021, 222324, 252627]

# Total
N_CONFIGS = 3 × 10 = 30
N_EPISODES = 30 × 300 = 9,000
```

**Checkpoints**:
- Cada 10 configs (3h aprox)
- Backup automático CSVs

**Tiempo estimado**: ~6 horas

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Análisis Estadístico

**Acción**: Ejecutar análisis comparativo N=3 vs N=10

**Análisis incluidos**:
1. **Estadísticas descriptivas**: Media, SD, CV por grupo
2. **Tests hipótesis**: H9.1.1-H9.4.1
3. **Comparación N=3 vs N=10**: Reducción incertidumbre (CI width)
4. **Clustering seeds**: K-means exitosas vs vulnerables
5. **Power analysis**: Potencia observada con N=10

**Outputs esperados**:
- `analisis/hypothesis_tests.json`
- `analisis/power_analysis.json`
- `analisis/seed_clustering.json`

**Tiempo estimado**: ~30 min

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Visualizaciones

**Acción**: Generar figuras comparativas

**Figuras clave**:
1. `ratio_comparison_n3_vs_n10.png` - Reducción incertidumbre
2. `reward_by_group_n10.png` - Boxplots 3 grupos
3. `success_rate_by_seed.png` - Identificar vulnerables
4. `curriculum_trajectory_by_seed.png` - 10 trayectorias
5. `hypothesis_tests_summary.png` - Visual p-values

**Tiempo estimado**: ~20 min

**Status**: ⏳ PENDIENTE

---

### [PENDIENTE] Reporte Final

**Acción**: Crear REPORTE_FINAL_v9.1.md

**Secciones**:
1. Resumen ejecutivo (hallazgos principales)
2. Metodología (diferencias vs v9)
3. Resultados principales (hipótesis + métricas)
4. Análisis comparativo N=3 vs N=10
5. Identificación seeds vulnerables
6. Limitaciones reconocidas
7. Próximos pasos (v10 adaptive)

**Tiempo estimado**: ~1 hora

**Status**: ⏳ PENDIENTE

---

## 📊 Métricas de Progreso

### Implementación

- [ ] Script adaptado con 10 seeds
- [ ] Test mode ejecutado exitosamente
- [ ] Validaciones pasadas

### Ejecución

- [ ] Configs completadas: 0/30
- [ ] Episodios completados: 0/9,000
- [ ] Tiempo transcurrido: 0/6 horas

### Análisis

- [ ] Tests estadísticos ejecutados
- [ ] Figuras generadas
- [ ] Reporte final escrito

---

## 🎯 Hitos Clave

| Hito | Fecha Objetivo | Status |
|------|----------------|--------|
| Preregistro congelado | 2025-12-04 10:00 | ✅ COMPLETADO |
| Script adaptado | 2025-12-04 11:00 | ⏳ PENDIENTE |
| Test mode exitoso | 2025-12-04 11:15 | ⏳ PENDIENTE |
| Ejecución iniciada | 2025-12-04 11:30 | ⏳ PENDIENTE |
| Checkpoint 1 (10 configs) | 2025-12-04 14:30 | ⏳ PENDIENTE |
| Checkpoint 2 (20 configs) | 2025-12-04 17:30 | ⏳ PENDIENTE |
| Ejecución completa | 2025-12-04 20:30 | ⏳ PENDIENTE |
| Análisis estadístico | 2025-12-04 21:00 | ⏳ PENDIENTE |
| Reporte final | 2025-12-04 22:00 | ⏳ PENDIENTE |

---

## 🔔 Notas y Observaciones

### Diseño Metodológico

**Seeds seleccionadas**:
- Mantener {42, 123, 456} de v9 (continuidad)
- Añadir 7 nuevas distribuidas uniformemente
- Evitar patrones obvios (no múltiplos de 10)

**Checkpoints críticos**:
- Config 10: Validar patrones iniciales
- Config 20: Confirmar tendencias
- Config 30: Análisis completo

### Predicciones Pre-Ejecución

**Escenario optimista (70% prob)**:
- 7-8/10 seeds exitosas
- Ratio: 0.75 ± 0.20
- H9.2.1: p<0.01

**Escenario pesimista (30% prob)**:
- 5-6/10 seeds exitosas
- Ratio: 0.65 ± 0.30
- H9.2.1: p=0.03-0.06

**Identificación vulnerables**:
- Esperamos 2-3 seeds tipo-123 (colapsan en etapa 4)

---

## 📝 Decisiones Metodológicas

### Por Qué N=10 (no N=23)

**N=23 óptimo** (potencia 80%), **PERO**:
- Tiempo cómputo: 23×3×300 = 20,700 eps (~14h)
- Balance factibilidad: N=10 da potencia 60-65% (~3.3× mejora vs N=3)
- Compromiso razonable para timeline proyecto

**Justificación**: N=10 suficiente para publicación workshop/ArXiv, responde crítica peer review directamente

### Por Qué Mismo Grid 4×4

**Mantener 4×4 (no escalar a 6×6/8×8 en v9.1)**:
- Continuidad metodológica con v9
- Aislar efecto N (no confundir con efecto complejidad)
- Escalamiento es objetivo v10 (adaptive curriculum)

---

## 🚦 Criterios de Avance a v10

**Verde (GO v10)**: 
- H9.2.1 significativa (p<0.05)
- ≥60% seeds exitosas
- CV reduce <0.40

**Amarillo (GO v10 con precaución)**:
- H9.2.1 borderline (p=0.05-0.10)
- 50-60% seeds exitosas
- v10 adaptive es crítico

**Rojo (PAUSE, investigar)**:
- H9.2.1 no significativa (p>0.10)
- <50% seeds exitosas
- Analizar causas antes de v10

---

**FIN TRACKING v9.1**

**Última actualización**: 4 diciembre 2025, 10:05  
**Status**: 🔄 PREPARACIÓN  
**Próximo paso**: Implementar script run_experiment_9.1_robust.py
