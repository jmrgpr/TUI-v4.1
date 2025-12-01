# PLAN DE ACCIÓN: Smoke Test v2 y Mejoras del Simulador TUI v4.2

**Fecha:** 1 de diciembre 2025  
**Objetivo:** Desbloquear agentes simbiosis/TUI y validar teoría TUI sin ambigüedades

---

## 1. PROBLEMA IDENTIFICADO

### 1.1 Síntomas
- Agentes `simbiosis` y `tui` tienen **0/2000 episodios con reward >0**
- Medias de recompensa: -84 a -88
- Agentes `control` (tabular) y `dqn_control` (DQN) funcionan perfectamente

### 1.2 Causa Raíz Confirmada
```
PGF_Neto = PGF_Bruto - PGF_Costo
         = (kappa * delta_P * A_t) - (lambda_c * delta_C_t)
         = 0.0 - X  (donde X > 0)
         = NEGATIVO
```

**En entorno 3×3 benigno:**
- Sin tripwires/shocks activos → `delta_P ≈ 0` → `PGF_Bruto ≈ 0`
- Consumo de recursos normal → `delta_C_t > 0` → `PGF_Costo > 0`
- Resultado: **señal PGF siempre ≤0**

Con `pgf_mix=1.0` (100% PGF), agentes ignoran `reward_env` positivo y solo ven señal negativa.

---

## 2. SOLUCIONES PROPUESTAS (Prioridad Descendente)

### SOLUCIÓN A: Ajustar pgf_mix (RÁPIDO, NO INVASIVO)
**Tiempo estimado:** 2 horas  
**Complejidad:** Baja

**Implementación:**
1. Modificar `sim/config.py`:
   ```python
   # Añadir en EXP_CONFIG
   "pgf_mix_default": 0.5,  # 50% PGF, 50% reward_env
   ```

2. Actualizar default en `sim/prototipo_rl_simbiosis.py`:
   ```python
   parser.add_argument('--pgf_mix', type=float, default=0.5, help='...')
   ```

3. Ejecutar experimentos de validación:
   ```bash
   # EXP_FIX_01: Mix 50/50
   python sim/prototipo_rl_simbiosis.py --episodes 100 --seed 42 --grid_size 3 --risk_scale 0.5 \
     --tui_only --pgf_mix 0.5 --output_prefix results/smoke_test/fix_pgfmix05_seed42

   # EXP_FIX_02: Mix 20/80 (más conservador)
   python sim/prototipo_rl_simbiosis.py --episodes 100 --seed 42 --grid_size 3 --risk_scale 0.5 \
     --tui_only --pgf_mix 0.2 --output_prefix results/smoke_test/fix_pgfmix02_seed42

   # EXP_FIX_03: Control (sin PGF)
   python sim/prototipo_rl_simbiosis.py --episodes 100 --seed 42 --grid_size 3 --risk_scale 0.5 \
     --tui_only --pgf_mix 0.0 --output_prefix results/smoke_test/fix_pgfmix00_seed42
   ```

**Criterio de éxito:**
- Media reward >0 en últimos 50 episodios
- Al menos 60% episodios con reward >0

**Pros:**
- No requiere cambios en evaluator_pgf.py
- Permite iterar rápidamente
- Mantiene señal PGF parcial

**Contras:**
- No valida PGF puro (solo mezcla)
- Puede enmascarar problemas de diseño PGF

---

### SOLUCIÓN B: Rediseñar PGF para Entornos Benignos (MEDIO, INVASIVO)
**Tiempo estimado:** 1-2 días  
**Complejidad:** Media

**Implementación:**
1. Modificar `sim/evaluator_pgf.py` líneas 50-65:
   ```python
   # NUEVO: Recompensa base por supervivencia
   survival_bonus = 0.1 if agent_resources > 0 else 0.0
   
   # NUEVO: Penalizar solo consumo excesivo
   efficient_usage = max(0.0, 1.0 - delta_C_t / env.resources)
   pgf_costo_adjusted = lambda_c * delta_C_t * (1.0 - efficient_usage)
   
   # PGF redesigned
   pgf_bruto = kappa * delta_P * A_t + survival_bonus
   pgf_costo = pgf_costo_adjusted
   self.PGF = pgf_bruto - pgf_costo
   ```

2. Añadir parámetros en `sim/config.py`:
   ```python
   EVAL_PGF_SURVIVAL_BONUS = 0.1
   EVAL_PGF_EFFICIENCY_WEIGHT = 0.5
   ```

3. Ejecutar experimentos de validación:
   ```bash
   python sim/prototipo_rl_simbiosis.py --episodes 100 --seed 42 --grid_size 3 --risk_scale 0.5 \
     --tui_only --pgf_mix 1.0 --output_prefix results/smoke_test/redesign_pgf_seed42
   ```

**Criterio de éxito:**
- PGF_Bruto_Avg > 0 en episodios sin shocks
- Media reward >0 con pgf_mix=1.0
- Interpretación teórica TUI clara

**Pros:**
- Valida PGF puro en entorno benigno
- Más alineado con teoría TUI (supervivencia es éxito)
- Extensible a entornos complejos

**Contras:**
- Requiere validación teórica cuidadosa
- Puede introducir nuevos bugs
- Cambio arquitectónico significativo

---

### SOLUCIÓN C: Smoke Test con Riesgo Mínimo (MEDIO, NO INVASIVO)
**Tiempo estimado:** 4 horas  
**Complejidad:** Media

**Implementación:**
1. Crear configuración `smoke_test_minimal_risk` en `sim/config.py`:
   ```python
   SMOKE_TEST_CONFIGS = {
       "benigno": {
           "tripwires": [],
           "shocks": [],
           "risk_penalty_high": -60.0
       },
       "minimal_risk": {
           "tripwires": [(1, 1)],  # 1 tripwire
           "shocks": [],
           "risk_penalty_high": -10.0  # Penalización suave
       }
   }
   ```

2. Ejecutar experimentos con riesgo mínimo:
   ```bash
   python sim/prototipo_rl_simbiosis.py --episodes 100 --seed 42 --grid_size 3 --risk_scale 0.5 \
     --tui_only --pgf_mix 1.0 --config minimal_risk --output_prefix results/smoke_test/minrisk_seed42
   ```

**Criterio de éxito:**
- PGF_Bruto_Avg > 0 en episodios con tripwire evitado
- delta_P > 0 observable en CSV
- Media reward >0 con pgf_mix=1.0

**Pros:**
- Valida PGF en condiciones de riesgo real (aunque mínimo)
- No modifica evaluator_pgf.py
- Más representativo de escenarios TUI reales

**Contras:**
- Cambia definición de "smoke test benigno"
- Puede introducir varianza adicional
- Requiere ajuste cuidadoso de penalizaciones

---

## 3. EXPERIMENTOS DE TUNING (Post-Desbloqueo)

Una vez desbloqueados los agentes simbiosis/TUI, ejecutar sweeps:

### 3.1 Tuning DQN (Reducir Varianza)
```bash
# EXP02: Learning rate
for lr in 5e-4 1e-4; do
  python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --risk_scale 0.5 \
    --dqn_control --lambda_gaming 0.0 --learning_rate $lr \
    --output_prefix results/smoke_test/tune_lr${lr}_seed42
done

# EXP03: Epsilon decay
for decay in 0.999 0.9995; do
  python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --risk_scale 0.5 \
    --dqn_control --lambda_gaming 0.0 --epsilon_decay $decay \
    --output_prefix results/smoke_test/tune_decay${decay}_seed42
done
```

### 3.2 Tuning TUI/PGF
```bash
# EXP04: pgf_mix sweep
for mix in 0.3 0.5 0.7 0.9; do
  python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --risk_scale 0.5 \
    --tui_only --pgf_mix $mix \
    --output_prefix results/smoke_test/tune_pgfmix${mix}_seed42
done

# EXP05: kappa/lambda_c sweep (requiere modificar config.py)
```

---

## 4. ACTUALIZACIÓN DE DOCUMENTACIÓN

### 4.1 Archivos a actualizar
1. **`results/smoke_test/RESULTADOS_TUNING_DQN.md`**
   - Corregir tabla con datos reales verificados
   - Marcar proyecciones como "PENDIENTE" o eliminarlas
   - Añadir sección "Problema Identificado" con diagnóstico

2. **`results/smoke_test/RESULTADOS_DESBLOQUEO.md`**
   - Limpiar encoding/mojibake si persiste
   - Añadir referencia a DIAGNOSTICO_SMOKE_TEST.md
   - Actualizar conclusiones con hallazgos actuales

3. **`results/smoke_test/README.md`**
   - Actualizar comandos con pgf_mix recomendado
   - Añadir warning sobre pgf_mix=1.0 en entorno benigno

### 4.2 Nuevo archivo
- **`results/smoke_test/PROTOCOLO_SMOKE_TEST_V2.md`**
  - Definir protocolo final post-fixes
  - Especificar configuraciones validadas
  - Criterios de éxito claros

---

## 5. ROADMAP DE EJECUCIÓN

### Fase 1: Validación Rápida ✅ COMPLETADA (1 dic 2025)
1. ✅ Diagnóstico completo (COMPLETADO)
2. ✅ Ejecutar EXP_FIX_01, 02, 03 (pgf_mix sweep) - **100% éxito**
3. ✅ Analizar resultados y confirmar desbloqueo - **Validado**
4. ✅ Documentar en RESULTADOS_FIX_PGF_MIX.md y RESULTADOS_TUNING_DQN.md

**Resultado:** Solución A validada, pgf_mix=0.2 óptimo (commit f9b8972)

### Fase 2: Implementación Robusta 🔄 EN PROGRESO (1 dic 2025)
1. ✅ Decidir entre Solución A, B o C → **Solución A seleccionada**
2. ✅ Implementar solución → **Default pgf_mix=0.2 (commit 2ca8159)**
3. ⏳ Ejecutar runs completos (1000 ep, seeds 42/123/456) - **Scripts creados**
4. ⏳ Validar métricas cumplen criterios de éxito - **Pendiente ejecución**

### Fase 3: Tuning y Optimización (2-3 días)
1. ⏳ Ejecutar EXP02-05 (sweeps hiperparámetros)
2. ⏳ Identificar configuración óptima DQN-Control y TUI/PGF
3. ⏳ Comparar TUI vs DQN con arquitectura justa

### Fase 4: Smoke Test Final (1 día)
1. ⏳ Ejecutar protocolo smoke test v2 completo
2. ⏳ Generar visualizaciones y análisis estadístico
3. ⏳ Actualizar toda la documentación
4. ⏳ Commit y push de artefactos validados

---

## 6. CRITERIOS DE VALIDACIÓN TEORÍA TUI

Para considerar la teoría TUI **validada sin dudas** en gridworld 3×3:

### 6.1 Criterios Técnicos
- ✅ **Convergencia:** Media reward >0 en últimos 100 episodios
- ✅ **Estabilidad:** Varianza reward < 50% de la media
- ✅ **Success rate:** >70% episodios con reward >0
- ✅ **Interpretabilidad:** PGF_Bruto correlaciona con reducción de riesgo

### 6.2 Criterios Comparativos
- ✅ **Paridad arquitectónica:** TUI/PGF usa DQN (no tabular vs neural)
- ✅ **Entorno justo:** Mismo grid, seeds, hiperparámetros base
- ✅ **Ventaja TUI observable:** TUI ≥ DQN-Control en alguna métrica clave
  - Gaming hits menores
  - Robustez mayor
  - Eficiencia en recursos

### 6.3 Criterios Teóricos
- ✅ **PGF validado:** PGF_Neto positivo en episodios exitosos
- ✅ **H1 observable:** I_op correlaciona con P_riesgo^α
- ✅ **Problema P3:** Tensión PGF_Bruto vs PGF_Costo medible

---

## 7. PRÓXIMOS PASOS INMEDIATOS

### HOY (1 dic 2025)
1. Ejecutar EXP_FIX_01, 02, 03 (mix sweep)
2. Analizar si pgf_mix=0.5 desbloquea aprendizaje
3. Decidir solución definitiva (A, B o C)

### MAÑANA (2 dic 2025)
1. Implementar solución elegida
2. Ejecutar runs completos seeds 42/123/456
3. Actualizar documentación con datos reales

### ESTA SEMANA
1. Completar tuning (EXP02-05)
2. Smoke test v2 final con protocolo validado
3. Preparar análisis para publicación/reporte

---

## 8. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| pgf_mix no resuelve el problema | Media | Alto | Implementar Solución B (rediseño PGF) |
| Rediseño PGF introduce nuevos bugs | Media | Medio | Tests unitarios exhaustivos |
| TUI sigue sin superar DQN | Baja | Alto | Aceptar resultado, ajustar teoría |
| Varianza DQN no se reduce | Media | Medio | Probar arquitectura diferente (A2C/PPO) |

---

## 9. CONCLUSIÓN

El smoke test actual **no puede validar TUI** porque el entorno benigno genera PGF negativo sistemáticamente. 

**Recomendación:** Implementar **Solución A (pgf_mix)** primero por rapidez, luego **Solución B (rediseño PGF)** para validación teórica robusta.

**Timeline optimista:** 3-5 días para smoke test v2 completo y validado.

**Criterio de éxito principal:** Agentes TUI/PGF aprenden y son comparables (no necesariamente superiores) a DQN-Control en entorno justo.

---

**Documento generado:** 1 dic 2025  
**Próxima revisión:** Post-EXP_FIX_01/02/03  
**Responsable:** Sistema de análisis automático TUI v4.2
