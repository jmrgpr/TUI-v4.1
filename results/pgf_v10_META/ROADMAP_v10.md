# ROADMAP SERIE v10: De Baseline a Cierre Científico

**Objetivo**: Transformar v10_viable (N=1) en serie v10 completa y cerrada científicamente.

**Estado**: ✅ Fase 0 completada, ✅ Fase 1 completada, ✅ Fase 2 completada, ⏳ Fase 3 pendiente

---

## 📋 Visión General

```
v10_viable (seed=42) → Multi-Seed → Ablation → PGF Offline → [v11]
    ↓                      ↓            ↓           ↓
  Baseline           Robustez     Causalidad    Teoría
```

---

## 🎯 Fases del Roadmap

### ✅ FASE 0: Congelar y Blindar v10_viable [COMPLETADO]

**Objetivo**: Proteger baseline y documentar estado actual.

**Acciones completadas**:
- ✅ Sección v10_viable en README principal
- ✅ Estructura carpetas separadas (multiseed/ablation/pgf_offline/META)
- ✅ v10_viable intocable (inmutable)
- ✅ Backup externo recomendado

**Entregables**:
- README.md actualizado con sección v10
- Estructura `results/pgf_v10_*/` creada
- Documentación limitaciones explícitas (N=1, varianza 6×6)

**Gate**: ✅ v10_viable documentado y congelado

---

### ✅ FASE 1: Robustez Multi-Seed [COMPLETADA]

**Objetivo**: Validar reproducibilidad curriculum con N=5 seeds.

**Seeds**: `[13, 42, 101, 2025, 9999]`

**Archivos clave**:
- `results/pgf_v10_multiseed/README_MULTISEED.md`
- `results/pgf_v10_multiseed/PREREGISTRO_MULTISEED.md`
- `scripts/run_multiseed_v10.py` (runner)
- `scripts/analisis_multiseed_v10.py` (análisis agregado)

**Criterios de éxito**:
- 4×4: Media >85% ± 10%, ≥4 seeds pasan gate (>80%)
- 6×6: Media >50% ± 20%, ≥3 seeds pasan gate (>20%)
- 8×8: Media >70% ± 15%, ≥3 seeds pasan gate (>10%)

**Entregables esperados**:
- `seeds/seed_XXXX/` con CSVs y modelos (4 nuevas seeds)
- `analisis_agregado/multiseed_statistics.csv`
- `figuras/` (3 visualizaciones)
- `REPORTE_MULTISEED.md`

**Timeline**: 1-2 semanas (~8-10 horas cómputo)

**Gate Fase 1**:
- ✅ Pasar: Si ≥4 seeds cumplen criterios → PROCEDER Fase 2
- ❌ Fallar: Si ≥2 seeds fallan gate fase 2/3 → REDISEÑAR curriculum

**Ejecución**:
```bash
# Correr multi-seed
python scripts/run_multiseed_v10.py

# Analizar resultados
python scripts/analisis_multiseed_v10.py
```

---

### ✅ FASE 2: Ablation Study (Componentes) [COMPLETADA]

Estado: ablation de componentes en 8×8 ejecutada (baseline, regularización, reward_extra, shaping, curriculum). Ver `results/pgf_v10_ablation/REPORTE_ABLATION_COMPONENTES_v10.md` y `analisis_comparativo/ablation_componentes_summary_v10.csv`.

**Prerequisito**: ✅ Fase 1 completada exitosamente

**Objetivo**: Demostrar que curriculum es necesario, no opcional.

**Experimentos planeados**:

#### Config A: Curriculum (baseline)
- Reference a v10_viable
- Success 8×8: 87% (conocido)

#### Config B: Direct 8×8 (crítico)
- Entrenar 8×8 desde cero
- Mismo budget (2500 eps)
- Mismo hyperparameters base

#### Config C: Curriculum Inverso (opcional)
- 8×8 → 6×6 → 4×4
- Test si orden importa

#### Config D: Solo 6×6 (opcional)
- ¿Empezar en "crisol" es suficiente?

**Hipótesis**:
- H1: Config A > Config B (curriculum ayuda)
- H2: Config A > Config C (orden importa)
- H3: Config D < Config A (4×4 necesario para foundation)

**Archivos clave**:
- `scripts/run_ablation_v10.py` (runner configs B-D)
- `results/pgf_v10_ablation/config_X/` (estructura por config)
- `REPORTE_ABLATION.md`

**Timeline**: 1 semana (~3-4 días cómputo)

**Gate Fase 2**:
- ✅ Si Config A > Config B por ≥15% → Curriculum validado
- ⚠️ Si diferencia <10% → Curriculum nice-to-have, no esencial

---

### ⏳ FASE 3: PGF Offline (Teoría) [PENDIENTE]

**Prerequisito**: ✅ Fase 1 completada (datos multi-seed disponibles)

**Objetivo**: Conectar datos empíricos con teoría TUI/PGF.

**Approach**: Análisis sobre datos **ya existentes** (no nuevas ejecuciones).

**Métricas a calcular**:
- **I_op** (Información Operacional): f(complejidad_espacial, recursos, riesgo)
- **PGF** (Potencial Guiado Fractal): I_op + cost_penalty

**Preguntas a responder**:
1. ¿I_op aumenta de 4×4 a 8×8? (esperado: sí)
2. ¿Episodios alto PGF tienen mayor success rate?
3. ¿Breakthrough 6×6 tiene firma PGF detectable?
4. ¿Transfer learning correlaciona con optimización PGF?

**Archivos clave**:
- `scripts/compute_pgf_offline_v10.py` (enrichment CSVs)
- `results/pgf_v10_pgf_offline/datos_enriquecidos/` (CSVs + columnas PGF)
- `figuras/` (correlaciones, evolución PGF)
- `REPORTE_PGF_OFFLINE.md`

**Figuras planeadas**:
1. Evolución PGF por fase (líneas temporales)
2. I_op vs success rate (scatter)
3. Breakthrough 6×6 en espacio PGF (análisis ep 500-650)
4. Comparación overhead vs PGF (eficiencia)

**Timeline**: 1 semana (sin cómputo, solo análisis datos)

**Gate Fase 3**:
- ✅ Si PGF correlaciona con éxito → Teoría soportada empíricamente
- ⚠️ Si no hay correlación → PGF requiere refinamiento teórico

---

### ⏳ FASE 4: Escalabilidad 16×16 (Opcional) [FUTURO]

**Prerequisito**: ✅ Fases 1-3 completadas

**Objetivo**: Test límite arquitectura actual.

**Approach conservador**:
1. Smoke test (50 eps) antes de full run
2. Gate modesto: >20% últimos 100 eps
3. Transfer desde 8×8

**Criterio go/no-go**:
- Si smoke test <10% success → Abortar 16×16
- Si smoke ≥10% → Proceder full run (1000 eps)

**Resultado esperado**:
- ✅ Funciona: Validación escalabilidad, paper más fuerte
- ❌ Falla: Define límite, motivación para v11 (arquitectura jerárquica)

**Timeline**: 2 semanas (si se ejecuta)

---

## 📊 Criterios de Cierre Serie v10

### La serie v10 se considera **científicamente cerrada** cuando:

1. ✅ Multi-seed (Fase 1) completada con N≥3
2. ✅ Ablation (Fase 2) demuestra curriculum necesario
3. ✅ PGF offline (Fase 3) conecta teoría-experimento
4. ✅ Documentación completa (reportes, figuras, READMEs)
5. ✅ MASTER_SUMMARY.csv consolidado

### Solo entonces arranca v11

---

## 🚀 v11: Próxima Generación (Post-v10)

**No iniciar hasta cerrar v10**

**Ideas preliminares**:
- Curriculum adaptativo (gates dinámicos)
- Arquitecturas jerárquicas (solución 16×16)
- PGF en el loop (no solo análisis offline)
- Multi-agent scenarios
- Ablation hyperparameters sistemático

**Baseline v11**: Serie v10 completa (N≥3, ablation, PGF)

---

## 📈 Timeline Realista

| Fase | Duración | Bloqueadores | Output Crítico |
|------|----------|--------------|----------------|
| **0** | 2 horas | - | README, estructura |
| **1** | 1-2 sem | Cómputo | multiseed_statistics.csv |
| **2** | 1 sem | Fase 1 OK | Ablation comparison |
| **3** | 1 sem | Fase 1 datos | PGF correlaciones |
| **4** | 2 sem | Fases 1-3 OK | 16×16 (opcional) |
| **TOTAL** | **3-5 sem** | - | Serie v10 cerrada |

**Paper timeline**:
- Workshop: 4-5 semanas (Fases 0-2)
- Journal: 3-4 meses (Fases 0-4 completas)

---

## 🔍 Estructura Final Esperada

```
results/
├── pgf_v10_viable/              ✅ INMUTABLE (baseline seed=42)
│   ├── README.md
│   ├── PREREGISTRO_v10_viable.md
│   ├── RESUMEN_EJECUTIVO.md
│   ├── resultados/ (CSVs, modelos)
│   ├── reportes/ (2 documentos)
│   ├── figuras/ (6 PNG)
│   └── analisis/ (scripts)
│
├── pgf_v10_multiseed/           🔄 EN PROGRESO
│   ├── README_MULTISEED.md
│   ├── PREREGISTRO_MULTISEED.md
│   ├── seeds/ (5 subdirs, seed_0042 es symlink)
│   ├── analisis_agregado/ (CSVs)
│   ├── figuras/ (3 PNG)
│   └── REPORTE_MULTISEED.md
│
├── pgf_v10_ablation/            ⏳ PENDIENTE (Fase 2)
│   ├── README_ABLATION.md
│   ├── config_A_curriculum/ (reference)
│   ├── config_B_direct_8x8/ (datos nuevos)
│   ├── config_C_inverse/ (opcional)
│   ├── config_D_only_6x6/ (opcional)
│   ├── analisis_comparativo/
│   ├── figuras/
│   └── REPORTE_ABLATION.md
│
├── pgf_v10_pgf_offline/         ⏳ PENDIENTE (Fase 3)
│   ├── README_PGF.md
│   ├── datos_enriquecidos/ (CSVs + columnas PGF)
│   ├── analisis_correlaciones/
│   ├── figuras/ (4 PNG)
│   └── REPORTE_PGF_OFFLINE.md
│
├── pgf_v10_scalability/         ⏳ OPCIONAL (Fase 4)
│   ├── README_16x16.md
│   ├── phase4_16x16/
│   └── REPORTE_16x16.md
│
└── pgf_v10_META/                📋 ESTE ARCHIVO
    ├── ROADMAP_v10.md           (este documento)
    └── MASTER_SUMMARY.csv       (consolidado final)
```

---

## ⚠️ Red Flags y Contingencias

### Si Multi-Seed Falla (Fase 1):
1. **NO proceder** a Fases 2-3
2. Opciones:
   - Ajustar hyperparameters (epsilon, max_steps)
   - Redefinir gates (más conservadores)
   - Fase intermedia 5×5
3. v10_viable queda como "resultado preliminar N=1"

### Si Ablation Muestra Curriculum Innecesario (Fase 2):
1. No es tragedia, aprendes algo
2. Paper angle: "Direct training competitivo en economía viable"
3. Refocus en PGF como diferenciador

### Si PGF No Correlaciona (Fase 3):
1. PGF necesita refinamiento teórico
2. Puedes seguir con paper RL puro (Fases 1-2)
3. TUI/PGF requiere más trabajo conceptual

---

## 📖 Referencias Clave

### Documentos Base
- **v10_viable baseline**: `results/pgf_v10_viable/`
- **Preregistro v10_viable**: commit `e099ab9`
- **Resultados v10_viable**: commit `cf1438c`

### Scripts Ejecutables
- **Baseline**: `scripts/run_curriculum_complete_viable.py`
- **Multi-seed**: `scripts/run_multiseed_v10.py`
- **Análisis multi-seed**: `scripts/analisis_multiseed_v10.py`

### Configuración Economía Viable
```python
INITIAL_RESOURCES = 8.0
STEP_COST = -0.15
RESOURCE_SPAWN_RATE = 0.40
GOAL_REWARD = 20.0
```

### Hyperparameters Fijos
```python
LEARNING_RATE = 0.001
GAMMA = 0.99
EPSILON_DECAY = 0.995
HIDDEN_DIM = 128
BATCH_SIZE = 32
MEMORY_SIZE = 10000
```

---

## 🎯 Próximo Paso Inmediato

**AHORA**: Ejecutar Fase 1 (Multi-Seed)

```bash
# 1. Ejecutar multi-seed (8-10 horas)
python scripts/run_multiseed_v10.py

# 2. Analizar resultados
python scripts/analisis_multiseed_v10.py

# 3. Revisar REPORTE_MULTISEED.md

# 4. Decisión:
#    - Si pasa → Fase 2 (ablation)
#    - Si falla → Rediseñar curriculum
```

---

## ✅ Checklist de Cierre v10

- [ ] **Fase 0**: README actualizado, estructura creada
- [ ] **Fase 1**: Multi-seed N=5 ejecutado y analizado
- [ ] **Fase 2**: Ablation curriculum vs directo completado
- [ ] **Fase 3**: PGF offline análisis completado
- [ ] **Fase 4** (opcional): 16×16 explorado
- [ ] **MASTER_SUMMARY.csv** generado
- [ ] **README_SERIE_v10.md** escrito
- [ ] **Zenodo** v10 completa (DOI)
- [ ] **Paper draft** iniciado

---

**Última actualización**: 5 de diciembre de 2025  
**Status**: Fase 0 completada, Fase 1 lista para ejecutar  
**Mantenedor**: Sistema Autónomo TUI v4.1
