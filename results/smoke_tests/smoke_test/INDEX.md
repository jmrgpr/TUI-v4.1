# 📚 ÍNDICE MAESTRO - Documentación Smoke Test TUI v4.2

**Carpeta:** `results/smoke_test/`  
**Última actualización:** 1 de diciembre 2025  
**Estado:** Problema crítico identificado y resuelto ✅

---

## 🎯 DOCUMENTOS POR PROPÓSITO

### 1. GUÍAS DE USO Y CONFIGURACIÓN

#### 📖 **README.md**
- **Propósito:** Guía rápida para ejecutar smoke tests
- **Contenido:** Comandos protocolizados, config benigna, flags de tuning
- **Audiencia:** Usuarios que ejecutan experimentos
- **Estado:** ✅ Actualizado con pgf_mix=0.2 recomendado

#### 📋 **EXP00_baseline_README.md**
- **Propósito:** Documentar experimento baseline EXP00
- **Contenido:** Configuración lambda_gaming=0.0, resultados
- **Estado:** ✅ Legacy, ver RESULTADOS_TUNING_DQN.md actualizado

---

### 2. SCRIPTS DE AUTOMATIZACIÓN ⚙️ NUEVO

#### 🔧 **scripts/run_validation_long.ps1** ⭐
- **Propósito:** Ejecución automatizada validación robusta
- **Contenido:** 1000 ep × 3 seeds (42, 123, 456), pgf_mix=0.2
- **Audiencia:** Automatización de experimentos Phase 2
- **Estado:** ✅ Listo para ejecutar (commit 2ca8159)

#### 📊 **scripts/analyze_validation_long.py** ⭐
- **Propósito:** Análisis estadístico automático de validación
- **Contenido:** Convergencia, intervalos confianza, t-tests, gráficos
- **Audiencia:** Análisis post-ejecución Phase 2
- **Estado:** ✅ Listo para usar (commit 2ca8159)

---

### 3. RESULTADOS Y ANÁLISIS

#### 📊 **RESULTADOS_TUNING_DQN.md** ⭐
- **Propósito:** Documento central de resultados y tuning
- **Contenido:**
  - Baselines disponibles (tabular, DQN legacy, protocolizados)
  - Tabla de tuning (EXP00-EXP06)
  - ⚠️ Sección diagnóstico problema pgf_mix
  - Próximos pasos actualizados
- **Audiencia:** Análisis técnico y planificación
- **Estado:** ✅ Actualizado con diagnóstico y solución

#### ✅ **RESULTADOS_FIX_PGF_MIX.md** ⭐ NUEVO
- **Propósito:** Documentar resolución problema agentes simbiosis/TUI
- **Contenido:**
  - Resultados EXP_FIX_01/02/03
  - Análisis comparativo pgf_mix (0.0, 0.2, 0.5)
  - Recomendaciones y warnings
  - Interpretación teoría TUI
- **Audiencia:** Validación técnica y publicación
- **Estado:** ✅ Completo, experimentos validados

#### 📄 **RESULTADOS_DESBLOQUEO.md**
- **Propósito:** Legacy - documenta desbloqueo inicial lambda_gaming
- **Contenido:** Auditoría, corrección crítica, tabla tuning, diagnóstico
- **Estado:** ⚠️ Legacy, referencia histórica (algunos datos mojibake)

---

### 3. PROTOCOLOS Y PLANIFICACIÓN

#### 🔬 **PROTOCOLO_COMPARATIVO_TUI_vs_DQN.md**
- **Propósito:** Define FASE 4 experimento comparativo
- **Contenido:** Comandos para comparar DQN-Control vs TUI/PGF Neural
- **Estado:** ⏳ Pendiente actualizar con pgf_mix=0.2

#### 📋 **PLAN_ACCION_SMOKE_TEST_V2.md** ⭐
- **Propósito:** Roadmap completo post-diagnóstico
- **Contenido:**
  - Soluciones A/B/C propuestas
  - Timeline de implementación
  - Criterios validación teoría TUI
  - Riesgos y mitigaciones
- **Audiencia:** Planificación estratégica
- **Estado:** ✅ Actualizado, guía de referencia

---

### 4. DIAGNÓSTICO Y ANÁLISIS TÉCNICO

#### 🔍 **DIAGNOSTICO_SMOKE_TEST.md** ⭐
- **Propósito:** Análisis técnico profundo del problema
- **Contenido:**
  - Datos reales verificados (seeds 123/456)
  - Bug identificado en runner.py
  - Hipótesis causa raíz confirmada
  - Impacto en teoría TUI
- **Audiencia:** Debugging técnico
- **Estado:** ✅ Completo, diagnóstico confirmado

#### 🐍 **analyze_smoke_test.py**
- **Propósito:** Script análisis automático métricas CSV
- **Contenido:** Lectura y resumen de todos los archivos de resultados
- **Uso:** `python results/smoke_test/analyze_smoke_test.py`
- **Estado:** ✅ Funcional

---

## 📂 ORGANIZACIÓN DE ARCHIVOS

### Estructura actual:
```
results/smoke_test/
├── 📚 DOCUMENTACIÓN
│   ├── INDEX.md (este archivo)
│   ├── README.md (guía de uso)
│   ├── RESULTADOS_TUNING_DQN.md (central)
│   ├── RESULTADOS_FIX_PGF_MIX.md (solución)
│   ├── DIAGNOSTICO_SMOKE_TEST.md (análisis técnico)
│   ├── PLAN_ACCION_SMOKE_TEST_V2.md (roadmap)
│   ├── PROTOCOLO_COMPARATIVO_TUI_vs_DQN.md
│   ├── RESULTADOS_DESBLOQUEO.md (legacy)
│   └── EXP00_baseline_README.md (legacy)
│
├── 🧪 ARTEFACTOS EXPERIMENTALES
│   ├── JSON files (configuración + métricas agregadas)
│   └── CSV files (datos por episodio)
│
├── 🔧 SCRIPTS
│   └── analyze_smoke_test.py
│
└── 📊 LOGS
    └── tabular_easy_log.txt
```

---

## 🗂️ ARCHIVOS DE RESULTADOS (CSV/JSON)

### Runs Protocolizados Completos (1000 ep, 3 seeds)
```
dqn_control_easy_seed{42,123,456}.{json,csv}
tui_pgf_easy_seed{42,123,456}.{json,csv}
```
⚠️ **Nota:** Seeds 123/456 muestran problema bloqueado (pgf_mix=1.0)

### Experimentos Fix (100 ep, seed 42)
```
fix_pgfmix05_seed42.{json,csv}  # pgf_mix=0.5 → media 14.66 ✅
fix_pgfmix02_seed42.{json,csv}  # pgf_mix=0.2 → media 29.71 ✅
fix_pgfmix00_seed42.{json,csv}  # pgf_mix=0.0 → media 39.74 ✅
```

### Legacy runs (referencias históricas)
```
dqn_xy_gamingoff_seed{42,123,456}_*.csv
dqn_xy_seed42_risk0.5.csv
easy_seed42_risk0.5.csv
patched_seed42_risk0.5.csv
dqn_control_easy_seed42_rerun*.csv
```

---

## 🚀 FLUJO DE TRABAJO RECOMENDADO

### Para ejecutar nuevos experimentos:
1. Leer **README.md** para comandos básicos
2. Consultar **RESULTADOS_FIX_PGF_MIX.md** para configuración óptima
3. Usar `pgf_mix=0.2` como default
4. Documentar en **RESULTADOS_TUNING_DQN.md**

### Para entender el problema resuelto:
1. **DIAGNOSTICO_SMOKE_TEST.md** - análisis técnico
2. **RESULTADOS_FIX_PGF_MIX.md** - solución y validación
3. **PLAN_ACCION_SMOKE_TEST_V2.md** - contexto estratégico

### Para planificar próximos pasos:
1. **PLAN_ACCION_SMOKE_TEST_V2.md** - roadmap completo
2. **RESULTADOS_TUNING_DQN.md** - tabla de experimentos pendientes
3. **PROTOCOLO_COMPARATIVO_TUI_vs_DQN.md** - comparación TUI vs DQN

---

## 📌 ESTADO ACTUAL DEL PROYECTO

### ✅ Completado:
- Diagnóstico completo del problema pgf_mix
- 3 experimentos de validación (EXP_FIX_01/02/03)
- Solución confirmada: pgf_mix=0.2
- Documentación actualizada

### ⏳ En Progreso:
- Ninguno (todos los experimentos fix completados)

### 📋 Próximos Pasos (Prioridad):
1. **Runs largos con pgf_mix=0.2** (1000 ep × seeds 42/123/456)
2. **Comparación TUI vs DQN-Control** (arquitectura justa)
3. **Tuning hiperparámetros** (EXP02-05)
4. **Implementar Solución B** (rediseño PGF con survival_bonus)

---

## 🎓 LECCIONES APRENDIDAS

### Problema Identificado:
- **pgf_mix=1.0 NO funciona** en entorno benigno sin delta_P
- Causa: PGF_Bruto ≈ 0, PGF_Costo > 0 → señal negativa

### Solución:
- **pgf_mix=0.2** (80% reward_env + 20% PGF)
- Mantiene lógica TUI con señal de aprendizaje fuerte

### Aplicabilidad:
- Entornos benignos: pgf_mix ≤ 0.5
- Entornos con riesgo: pgf_mix puede ser ≥ 0.7
- Validación pura TUI: requiere entorno con delta_P > 0

---

## 📞 CONTACTO Y MANTENIMIENTO

**Proyecto:** TUI v4.2 - Smoke Test  
**Repositorio:** TUI-v4.1  
**Branch:** main  
**Última actualización:** 1 diciembre 2025

**Para preguntas o issues:**
- Consultar documentación en orden:
  1. README.md (comandos rápidos)
  2. RESULTADOS_FIX_PGF_MIX.md (solución actual)
  3. PLAN_ACCION_SMOKE_TEST_V2.md (roadmap)

---

## 📊 MÉTRICAS CLAVE (Resumen)

| Métrica | Valor Actual | Objetivo | Estado |
|---------|--------------|----------|--------|
| DQN-Control media | 92-109 | >0 | ✅ |
| Simbiosis pgf_mix=0.2 | 29.71 | >0 | ✅ |
| Success rate (fix) | 100% | >70% | ✅ |
| Documentación | 9 archivos | Completa | ✅ |
| Experimentos validación | 3/3 | 3 | ✅ |

---

**Fin del índice maestro**  
**Documento generado:** 1 dic 2025  
**Versión:** 1.0  
**Mantenedor:** Sistema de análisis automático TUI v4.2
