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

### [2025-12-03 17:40] Implementación - PENDIENTE

**Próxima acción**: Crear `scripts/run_experiment_9_curriculum.py`

**Requisitos implementación**:
1. **Función `train_curriculum()`**:
   - 4 etapas secuenciales
   - Transfer learning de pesos Q-network
   - Epsilon continuo (NO reset)
   - Actualizar `env.shaping_scale` por etapa

2. **Función `train_direct_s1()`**:
   - 300 episodios s=1.0 constante
   - Réplica v8 comportamiento

3. **Función `train_control_s0()`**:
   - 300 episodios s=0.0 (sin shaping)
   - Baseline funcional

4. **Validación CSV**:
   - Columna `stage` (1-4 para Curriculum, null otros)
   - Columna `shaping_scale_current`
   - Todas métricas v8 + específicas v9

**Tiempo estimado**: ~30 minutos

---

### [PENDIENTE] Test Mode

**Acción planeada**: Ejecutar 1 config Curriculum con 30 eps/etapa (120 total)

**Validaciones**:
- ✅ Transiciones etapas detectadas en CSV (stage 1→2→3→4)
- ✅ Shaping_scale actualizado correctamente
- ✅ Epsilon continúa decreciente (NO reset)
- ✅ Pesos Q-network se transfieren (verificar hash)

**Tiempo estimado**: ~2 minutos

---

### [PENDIENTE] Ejecución Completa

**Acción planeada**: 9 configs × 300 episodios = 2,700 episodios totales

**Orden ejecución**:
```
Grupos × Seeds:
1. Curriculum × seed42
2. Curriculum × seed123
3. Curriculum × seed456
4. DirectoS1 × seed42
5. DirectoS1 × seed123
6. DirectoS1 × seed456
7. ControlS0 × seed42
8. ControlS0 × seed123
9. ControlS0 × seed456
```

**Checkpoints**:
- 33% (3 configs): ~5 min
- 66% (6 configs): ~10 min
- 100% (9 configs): ~15 min

**Validación post-ejecución**:
- ✅ 9 CSVs generados (exp9_{group}_seed{seed}_episodes.csv)
- ✅ 9 JSONs generados (exp9_{group}_seed{seed}_metrics.json)
- ✅ Todas CSVs con 300 filas (episodios)
- ✅ Todas métricas críticas presentes

**Tiempo estimado**: ~15 minutos

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

*(Se completará post-ejecución)*

### Ratios Finales (episodios 250-300)

```
Grupo         | Ratio Mean | Ratio SD | Success% | Tripwires
--------------|------------|----------|----------|----------
Curriculum    | [TBD]      | [TBD]    | [TBD]    | [TBD]
DirectoS1     | [TBD]      | [TBD]    | [TBD]    | [TBD]
ControlS0     | [TBD]      | [TBD]    | [TBD]    | [TBD]
```

### Hipótesis Status

- **H9.1** (Curriculum > DirectoS1): [TBD]
- **H9.2** (Curriculum mantiene prudencia): [TBD]
- **H9.3** (Curriculum evita parálisis): [TBD]
- **H9.4** (Degradación gradual): [TBD]

---

## 🔄 Commits Relevantes

| Commit | Fecha | Descripción |
|--------|-------|-------------|
| `f5ba3ac` | 3 dic 2025 | v9 PREREGISTRO completo |
| [TBD] | [TBD] | v9 RAW DATA - 9 configs completos |
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
