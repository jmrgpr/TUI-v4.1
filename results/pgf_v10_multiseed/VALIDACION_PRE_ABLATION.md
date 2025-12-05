# VALIDACIÓN PRE-ABLATION: Estado del Repositorio

**Fecha**: 2025-12-05 13:15  
**Commit actual**: c6944a5  
**Branch**: main (3 commits ahead of origin)

---

## ✅ INTEGRIDAD DE DATOS VERIFICADA

### Estadísticas Finales Confirmadas

| Fase | N Seeds | Success Mean | Std | Min | Max | Gates Passed |
|------|---------|-------------|-----|-----|-----|--------------|
| **4×4** | 5 | 86.0% ± 7.2% | 7.2% | 75% | 93% | 4/5 (80%) |
| **6×6** | 4 | 68.5% ± 17.2% | 17.2% | 51% | 92% | 4/4 (100%) |
| **8×8** | 4 | 79.5% ± 8.7% | 8.7% | 67% | 87% | 4/4 (100%) |

**Nota Crítica**: N=4 en 6×6 y 8×8 porque seed 2025 falló gate 4×4 y no progresó.

### Seeds Individuales

```
Seed 13:   4×4=91%, 6×6=92%, 8×8=82% ✅
Seed 42:   4×4=93%, 6×6=68%, 8×8=87% ✅ (Baseline)
Seed 101:  4×4=83%, 6×6=63%, 8×8=82% ✅
Seed 2025: 4×4=75% ❌ (detenida)
Seed 9999: 4×4=88%, 6×6=51%, 8×8=67% ✅
```

### Archivos Críticos Validados

- ✅ `multiseed_summary.csv`: 13 registros (4 seeds × 3 fases + 1 seed × 1 fase)
- ✅ `multiseed_statistics.csv`: 3 fases con n_seeds correcto
- ✅ Curriculum summaries individuales: Todas las seeds completas tienen 3 fases
- ✅ Phase CSVs: Todos con 500/1000/1000 episodios esperados

---

## ⚠️ PROBLEMAS IDENTIFICADOS

### 1. Bloat de Repositorio: Checkpoints Versionados

**Problema**: 248 archivos `.pth` (18.5 MB) commiteados en c6944a5.

**Archivos**:
```
results/pgf_v10_multiseed/seeds/seed_0042/checkpoint_*.pth (múltiples timestamps)
results/pgf_v10_viable/resultados/checkpoint_*.pth (duplicados)
```

**Impacto**:
- Git repo inflado innecesariamente
- Múltiples corridas históricas mezcladas
- Dificulta tracking de cambios reales

**Recomendación**: 
```bash
# Opción 1: Remover checkpoints del historial (destructivo)
git filter-branch --tree-filter 'rm -rf results/*/seeds/*/checkpoint_*.pth results/*/resultados/checkpoint_*.pth' HEAD

# Opción 2: Agregar a .gitignore y limpiar en próximo commit
echo "**/*checkpoint*.pth" >> .gitignore
git rm --cached results/pgf_v10_multiseed/seeds/*/checkpoint_*.pth
```

**Decisión pendiente**: ¿Mantener solo modelos finales (model_*.pth)?

---

### 2. Documentos Eliminados Sin Explicación

**Eliminados en c6944a5**:
- `results/pgf_v10_multiseed/PREREGISTRO_MULTISEED.md`
- `results/pgf_v10_multiseed/README_MULTISEED.md`
- `results/pgf_v10_multiseed/RESUMEN_EJECUTIVO.md`

**Agregados**:
- `results/pgf_v10_multiseed/AUDITORIA_DATOS.md`
- `results/pgf_v10_multiseed/REPORTE_MULTISEED.md`

**Problema**: No hay mensaje de commit explicando la razón del borrado.

**Pregunta**: ¿Fueron reemplazados intencionalmente por AUDITORIA_DATOS.md?

**Recomendación**: Si fueron obsoletos, documentar en commit message. Si contenían info valiosa, recuperar.

---

### 3. Indexación Inconsistente: first_success_episode

**Problema**: Valores en `multiseed_summary.csv` usan indexación 0-based (Python) pero logs de terminal usan 1-based (humano).

**Evidencia**:
```
multiseed_summary.csv:
  seed 13, 8×8: first_success_episode=0
  seed 42, 8×8: first_success_episode=0
  seed 101, 8×8: first_success_episode=0
  seed 9999, 8×8: first_success_episode=4
```

**Log de terminal (corrida limpia)**:
```
Ep 1000: success= 92.0%, reward= +40.57, steps= 21.6
Primer éxito: Episodio 1
```

**Impacto**: 
- Confusión al interpretar "Episodio 0" vs "Episodio 1"
- Inconsistencia con reportes previos que usan 1-based

**Solución**:
```python
# En reconstruct_curriculum_summaries.py línea 48:
'first_success_episode': df[df['success']==1].index[0] + 1 if len(df[df['success']==1]) > 0 else None
                                                        ^^^^
```

**Acción**: Decidir si corregir a 1-based o documentar explícitamente que es 0-based.

---

### 4. Mezcla de Timestamps en Seed 42

**Problema**: Seed 42 (baseline) contiene archivos de MÚLTIPLES corridas:

```
phase1_4x4_20251205_093829.csv (9:38 AM)
phase1_4x4_20251205_100627.csv (10:06 AM)
phase1_4x4_20251205_101537.csv (10:15 AM)
phase1_4x4_20251205_102250.csv (10:23 AM) ← USADA EN ANÁLISIS
```

**Causa**: Seed 42 es junction/symlink a `results/pgf_v10_viable/resultados/` que acumula histórico.

**Estado actual**: Script `fix_seed42_summary.py` fuerza uso de timestamp `102250` (correcto).

**Riesgo futuro**: Nuevas corridas agregarán más archivos, causando confusión.

**Solución permanente**:
1. NO usar junctions para baselines
2. COPIAR archivos finales con timestamp único
3. O limpiar histórico después de cada validación

---

### 5. Representatividad N=4 vs N=5

**Problema**: Análisis reporta "N=5 seeds" pero 6×6 y 8×8 tienen N=4.

**Evidencia**:
```
multiseed_statistics.csv:
  4×4: n_seeds=5
  6×6: n_seeds=4  ← Seed 2025 excluida
  8×8: n_seeds=4  ← Seed 2025 excluida
```

**Impacto**: 
- Confusión al leer "Multi-Seed N=5" en títulos
- Estadísticas de 8×8 menos robustas (N=4 vs N=5)

**Documentación actual**: AUDITORIA_DATOS.md menciona esto, pero no está en abstract/conclusión.

**Recomendación**: Siempre especificar N por fase en reportes finales.

---

## 📋 CHECKLIST PRE-ABLATION

### Datos Científicos
- [x] Estadísticas validadas: 86%/68%/79% correctas
- [x] Seeds individuales completas: 13, 42, 101, 9999
- [x] Seed 42 baseline representativa (Z<1.5)
- [x] Phase CSVs con episodios completos
- [x] Curriculum summaries reconstruidos correctamente
- [x] Análisis agregado sin NaNs ni outliers

### Limpieza Técnica
- [ ] **PENDIENTE**: Decidir sobre checkpoints (remover o mantener)
- [ ] **PENDIENTE**: Agregar `**/*checkpoint*.pth` a .gitignore
- [ ] **PENDIENTE**: Corregir first_success_episode a 1-based
- [ ] **PENDIENTE**: Documentar eliminación de docs previos
- [ ] **PENDIENTE**: Limpiar histórico seed 42 o cambiar a copia

### Documentación
- [x] AUDITORIA_DATOS.md completa
- [x] REPORTE_MULTISEED.md generado
- [ ] **PENDIENTE**: Agregar nota N=4 en conclusiones
- [ ] **PENDIENTE**: Changelog explicando cambios de docs

---

## 🎯 DECISIÓN: ¿Proceder con Ablation?

### Opción A: PROCEDER AHORA (Recomendado)
**Justificación**: 
- Datos científicos validados y correctos
- Problemas técnicos NO afectan resultados experimentales
- Limpieza puede hacerse en paralelo

**Acción**:
1. Proceder con Fase 2 (Ablation) usando datos actuales
2. Limpiar repo en commit separado después
3. Documentar issues pendientes en TODO.md

### Opción B: LIMPIAR PRIMERO
**Justificación**:
- Repo más limpio antes de generar nuevos datos
- Evita propagar problemas de indexación

**Acción**:
1. Corregir first_success_episode a 1-based
2. Remover checkpoints del historial
3. Limpiar seed 42 histórico
4. Luego ejecutar ablation

---

## 📊 CONCLUSIÓN

**Estado de Datos**: ✅ **VALIDADOS Y LISTOS**

**Problemas Técnicos**: ⚠️ **NO BLOQUEAN ABLATION** pero deben corregirse

**Recomendación**: **PROCEDER CON OPCIÓN A** - Los problemas identificados son de housekeeping, no científicos. Los datos de multi-seed están correctos y certificados. La limpieza del repo puede hacerse en paralelo sin afectar experimentos.

---

**Validación completada**: 2025-12-05 13:20  
**Aprobado para Fase 2**: ✅  
**Issues pendientes**: 5 (documentados arriba)
