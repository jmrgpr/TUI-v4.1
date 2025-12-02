# 🎯 PLAN ESTRATÉGICO COMPLETO - TUI v4.2 Post-Validación

**Fecha elaboración:** 1 de diciembre 2025  
**Estado base:** Fase 1 y 2 completadas, sistema desbloqueado (pgf_mix=0.2)  
**Objetivo:** Demostrar superioridad TUI o redefinir alcance teórico

---

## 📋 RESUMEN EJECUTIVO

### Situación Actual
- ✅ **Logro técnico:** TUI funciona (99.97% success, 3000 episodios)
- ❌ **Problema científico:** TUI inferior a Control (23.98 vs 144.60, ratio 1:6)
- ⚠️ **Limitación metodológica:** Entorno benigno no valida hipótesis H1

### Decisión Estratégica
**Tres caminos posibles:**

**A. Validar teoría con riesgo** (RECOMENDADO)
- Demostrar TUI mejora con riesgo real
- Si exitoso → publicación fuerte
- Si falla → rediseñar PGF o acotar claims

**B. Aceptar limitación, publicar como toy case**
- Paper modesto: "PGF estabiliza pero no supera baseline"
- Honesto pero menos impactante
- Rápido (1-2 semanas)

**C. Rediseñar PGF antes de testear**
- Arriesgado sin evidencia empírica
- Puede introducir nuevos bugs
- Tiempo largo (1-2 meses)

**→ Este plan sigue CAMINO A (validación con riesgo)**

---

## 🚀 FASE 3: VALIDACIÓN TEÓRICA CON RIESGO REAL

### Objetivo
Demostrar que **con riesgo constitutivo, TUI ≥ Control** y que PGF recompensa reducción de riesgo.

### Hipótesis a Validar (H1)
```
I_operativa ∝ P_riesgo^α

Predicción: Con tripwires activos y risk_scale alto:
1. PGF_Bruto > 0 cuando agente evita riesgos
2. TUI aprende más rápido que Control (menos tripwire hits)
3. TUI reward media ≥ 80% Control reward media
```

---

### Experimento 3A: Riesgo Moderado (Grid 5×5)

**Configuración:**
```powershell
python sim/prototipo_rl_simbiosis.py `
  --episodes 500 `
  --seed 42 `
  --grid_size 5 `
  --risk_scale 1.5 `
  --tui_only `
  --pgf_mix 0.2 `
  --output_prefix results/risk_validation/exp3a_risk15_seed42
```

**Parámetros clave:**
- Grid: 5×5 (vs 3×3 anterior, más complejo)
- risk_scale: 1.5 (vs 0.5 anterior, penalizaciones 3× mayores)
- Tripwires: Default [(2,2)] activo
- Shocks: Default [(3,3)] activo
- Episodes: 500 (suficiente para convergencia)

**Tiempo estimado:** 15-20 minutos  
**Costo computacional:** Bajo

**Métricas a recolectar:**
```python
# Del CSV generado
1. Reward media (TUI vs Control)
2. Tripwire hits rate (debe ser menor en TUI)
3. PGF_Bruto_Avg (debe ser >0)
4. Success rate (>95% objetivo)
5. Convergencia (últimos 100 ep std)
```

**Criterios de Éxito:**
- ✅ **Mínimo aceptable:** TUI reward ≥ 50% Control reward
- ✅ **Éxito moderado:** TUI reward ≥ 70% Control reward
- ✅ **Éxito fuerte:** TUI reward ≥ Control reward
- ✅ **Plus:** TUI tripwire hits < Control tripwire hits

**Criterios de Fallo:**
- ❌ TUI reward < 40% Control reward
- ❌ Success rate < 90%
- ❌ PGF_Bruto_Avg ≤ 0 (teoría no se cumple)

---

### Experimento 3B: Riesgo Alto (Grid 7×7) - OPCIONAL

**Solo ejecutar si 3A tiene éxito moderado/fuerte**

```powershell
python sim/prototipo_rl_simbiosis.py `
  --episodes 500 `
  --seed 42 `
  --grid_size 7 `
  --risk_scale 2.0 `
  --tui_only `
  --pgf_mix 0.2 `
  --output_prefix results/risk_validation/exp3b_risk20_seed42
```

**Objetivo:** Demostrar escalabilidad a entornos más complejos  
**Tiempo estimado:** 25-30 minutos

---

### Experimento 3C: Sweep pgf_mix con Riesgo - OPCIONAL

**Solo si 3A muestra que TUI mejora pero aún inferior**

```powershell
# Probar si más PGF ayuda con riesgo real
foreach ($mix in 0.3, 0.4, 0.5) {
  python sim/prototipo_rl_simbiosis.py `
    --episodes 300 `
    --seed 42 `
    --grid_size 5 `
    --risk_scale 1.5 `
    --tui_only `
    --pgf_mix $mix `
    --output_prefix "results/risk_validation/exp3c_mix${mix}_seed42"
}
```

**Hipótesis:** Con riesgo real, más PGF (0.3-0.5) puede mejorar vs 0.2  
**Tiempo estimado:** 30-40 minutos total

---

## 📊 ANÁLISIS POST-EXPERIMENTO 3A

### Script de Análisis Automático

Crear archivo `results/risk_validation/analyze_risk_exp.py`:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv('results/risk_validation/exp3a_risk15_seed42_episodes.csv')

# Comparar TUI vs Control
tui = df[df['Agente']=='tui']['Recompensa']
simb = df[df['Agente']=='simbiosis']['Recompensa']
control = df[df['Agente']=='control']['Recompensa']

print("=== ANÁLISIS EXPERIMENTO 3A (risk_scale=1.5) ===\n")
print(f"TUI:       media={tui.mean():.2f}, std={tui.std():.2f}, success={(tui>0).sum()}/{len(tui)}")
print(f"Simbiosis: media={simb.mean():.2f}, std={simb.std():.2f}, success={(simb>0).sum()}/{len(simb)}")
print(f"Control:   media={control.mean():.2f}, std={control.std():.2f}, success={(control>0).sum()}/{len(control)}")
print(f"\nRatio TUI/Control: {tui.mean()/control.mean():.2%}")
print(f"Ratio Simbiosis/Control: {simb.mean()/control.mean():.2%}")

# Verificar PGF_Bruto
if 'PGF_Bruto' in df.columns:
    pgf_bruto_tui = df[df['Agente']=='tui']['PGF_Bruto'].mean()
    pgf_bruto_simb = df[df['Agente']=='simbiosis']['PGF_Bruto'].mean()
    print(f"\nPGF_Bruto_Avg TUI: {pgf_bruto_tui:.4f} {'✅ >0' if pgf_bruto_tui > 0 else '❌ ≤0'}")
    print(f"PGF_Bruto_Avg Simbiosis: {pgf_bruto_simb:.4f} {'✅ >0' if pgf_bruto_simb > 0 else '❌ ≤0'}")

# Tripwire hits (si está en columnas)
if 'Tripwire_Hits' in df.columns:
    tui_trips = df[df['Agente']=='tui']['Tripwire_Hits'].sum()
    simb_trips = df[df['Agente']=='simbiosis']['Tripwire_Hits'].sum()
    ctrl_trips = df[df['Agente']=='control']['Tripwire_Hits'].sum()
    print(f"\nTripwire hits - TUI: {tui_trips}, Simbiosis: {simb_trips}, Control: {ctrl_trips}")

# Decisión
tui_ratio = tui.mean() / control.mean()
if tui_ratio >= 0.7:
    print("\n✅ ÉXITO MODERADO/FUERTE: Proceder a Fase 4 (SOTA comparison)")
elif tui_ratio >= 0.5:
    print("\n⚠️ ÉXITO MÍNIMO: Considerar Experimento 3C (sweep pgf_mix)")
else:
    print("\n❌ FALLO: Proceder a Camino A2 (rediseñar PGF)")
```

**Ejecutar con:**
```powershell
python results/risk_validation/analyze_risk_exp.py
```

---

## 🔀 ÁRBOL DE DECISIÓN POST-3A

```
┌─────────────────────────────────────────────────────┐
│      EXPERIMENTO 3A COMPLETADO (risk_scale=1.5)     │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
    ✅ ÉXITO              ❌ FALLO
  (TUI ≥ 70% Ctrl)      (TUI < 50% Ctrl)
        │                     │
        ▼                     ▼
┌───────────────┐     ┌──────────────────┐
│   CAMINO A1   │     │    CAMINO A2     │
│ Validar SOTA  │     │  Rediseñar PGF   │
└───────┬───────┘     └────────┬─────────┘
        │                      │
        │                      │
        ▼                      ▼
  FASE 4: SOTA          FASE 3-ALT:
  Comparison            Ajustar PGF
  (Prioridad 2)         (Solución B)
```

---

## 📝 CAMINO A1: ÉXITO EN 3A (TUI ≥ 70% Control)

### FASE 4: COMPARACIÓN SOTA

**Objetivo:** Demostrar TUI competitivo con algoritmos estándar

**Experimento 4A: Baseline SOTA**
```powershell
python run_sota_comparison.py `
  --episodes 500 `
  --algorithms DQN,A2C,PPO `
  --risk_scale 1.5 `
  --seeds 42,123,456 `
  --output_prefix results/sota_comparison/exp4a
```

**Tiempo estimado:** 45-60 minutos  
**Output esperado:**
- Tabla comparativa: TUI vs DQN vs A2C vs PPO
- Gráficos convergencia multi-algoritmo
- Tests estadísticos (ANOVA, pairwise t-tests)

**Criterio publicación:**
- ✅ TUI en top 50% de algoritmos en reward media
- ✅ TUI tiene menor tripwire hit rate que al menos 1 algoritmo
- ✅ Interpretación teórica clara: PGF ayuda en gestión de riesgo

---

### FASE 5: TUNING Y REFINAMIENTO (OPCIONAL)

**Solo si quieres optimizar antes de publicar**

**5A. Tuning DQN Control (Baseline Justo)**
```powershell
# Reducir varianza Control para comparación limpia
python scripts/run_dqn_tuning.py `
  --param learning_rate `
  --values 5e-4,1e-4,5e-5 `
  --episodes 300
```

**5B. Sweep gamma_lcb (Prudencia TUI)**
```powershell
# Probar si ajustar prudencia mejora TUI
foreach ($gamma in 1.5, 2.0, 2.5) {
  python sim/prototipo_rl_simbiosis.py `
    --episodes 300 `
    --pgf_kappa 1.0 `
    --custom_gamma_lcb $gamma `
    --grid_size 5 `
    --risk_scale 1.5 `
    --tui_only
}
```

**Tiempo total Fase 5:** 2-3 horas

---

### FASE 6: MANUSCRITO Y PUBLICACIÓN

**6A. Preparar Paper (1-2 semanas)**

**Estructura sugerida:**
```markdown
1. Abstract
   - TUI desbloqueado con pgf_mix=0.2
   - Validación 3000 ep (99.97% success)
   - Con riesgo real, TUI ≥ 70% Control (EXP 3A)
   
2. Introduction
   - Problema alineación AGI
   - Teoría Unificada Inteligencia (TUI v4.2)
   - Hipótesis H1: I ∝ P_riesgo^α
   
3. Methods
   - Gridworld con riesgo constitutivo
   - PGF prudencial (Neto = Bruto - Costo)
   - Configuración pgf_mix=0.2 (ablation study)
   
4. Results
   - Fase 1-2: Diagnóstico y validación estabilidad
   - Fase 3: Validación con riesgo (EXP 3A)
   - Fase 4: Comparación SOTA (si aplica)
   
5. Discussion
   - PGF efectivo en entornos riesgosos
   - Limitaciones: toy gridworld, pgf_mix como workaround
   - Trabajo futuro: benchmarks complejos (MuJoCo)
   
6. Conclusion
   - Proof-of-concept exitoso
   - Camino hacia AGI alineado vía simbiosis constitutiva
```

**6B. Artifacts DOI (Zenodo)**
- Código completo (GitHub release)
- Datasets (CSVs experimentales)
- Documentación (MDs)
- Gráficos publicables

**6C. Target Venues**
- **Tier 1:** NeurIPS (AI Safety workshop), ICLR
- **Tier 2:** AAAI, IJCAI
- **Tier 3:** arXiv preprint → mejoras → resubmit

**Tiempo total Fase 6:** 2-4 semanas

---

## 🔧 CAMINO A2: FALLO EN 3A (TUI < 50% Control)

### FASE 3-ALT: REDISEÑO PGF (Solución B)

**Diagnóstico:** PGF_Costo penaliza demasiado, PGF_Bruto insuficiente

**Cambios propuestos en `sim/evaluator_pgf.py`:**

```python
def _compute_pgf_components(self, agent_resources, delta_C_t, delta_P, A_t, env):
    """
    PGF Rediseñado v2: Bonus supervivencia + eficiencia
    """
    kappa = self.config.get('EVAL_PGF_KAPPA', 1.0)
    lambda_c = self.config.get('EVAL_PGF_LAMBDA_C', 0.1)
    
    # NUEVO: Bonus supervivencia base
    survival_bonus = 0.2 if agent_resources > 0 else 0.0
    
    # NUEVO: Penalizar solo consumo excesivo (>50% recursos)
    resource_ratio = delta_C_t / max(env.resources, 1.0)
    if resource_ratio < 0.5:
        # Consumo normal: penalización mínima
        pgf_costo = lambda_c * delta_C_t * 0.3
    else:
        # Consumo excesivo: penalización completa
        pgf_costo = lambda_c * delta_C_t
    
    # PGF_Bruto: riesgo + supervivencia
    pgf_bruto = kappa * delta_P * A_t + survival_bonus
    
    # PGF_Neto
    pgf_neto = pgf_bruto - pgf_costo
    
    return pgf_bruto, pgf_costo, pgf_neto
```

**Experimento 3-ALT-A: Validar PGF v2 en entorno benigno**
```powershell
# Verificar que PGF v2 no rompe nada
python sim/prototipo_rl_simbiosis.py `
  --episodes 200 `
  --seed 42 `
  --grid_size 3 `
  --risk_scale 0.5 `
  --tui_only `
  --pgf_mix 1.0 `
  --output_prefix results/pgf_v2/exp_benign_seed42
```

**Criterio:** Media >0, success >90% (debe funcionar incluso en benigno)

**Experimento 3-ALT-B: PGF v2 con riesgo**
```powershell
# Repetir 3A con PGF rediseñado
python sim/prototipo_rl_simbiosis.py `
  --episodes 500 `
  --seed 42 `
  --grid_size 5 `
  --risk_scale 1.5 `
  --tui_only `
  --pgf_mix 0.5 `
  --output_prefix results/pgf_v2/exp_risk15_seed42
```

**Criterio:** TUI ≥ 70% Control (objetivo original)

**Tiempo total Camino A2:** 4-8 horas (coding + testing)

**Riesgo:** Medio (cambios arquitectónicos pueden introducir bugs)

---

## ⏱️ CRONOGRAMA PROPUESTO

### Escenario Optimista (TUI exitoso en 3A)

| Fecha | Fase | Actividad | Tiempo | Acumulado |
|-------|------|-----------|--------|-----------|
| **Dic 2** | 3 | EXP 3A (risk_scale 1.5) | 20 min | 20 min |
| Dic 2 | 3 | Análisis 3A | 10 min | 30 min |
| Dic 2 | 4 | EXP 4A (SOTA comparison) | 60 min | 1.5 h |
| Dic 2-3 | 4 | Análisis estadístico | 2 h | 3.5 h |
| **Dic 3-9** | 6 | Draft paper v1 | 20 h | 23.5 h |
| Dic 10-16 | 6 | Revisar/pulir paper | 15 h | 38.5 h |
| **Dic 17** | 6 | Submit arXiv preprint | - | - |
| Dic 17-23 | 6 | Feedback comunidad | - | - |
| Ene 2026 | 6 | Submit conferencia (NeurIPS deadline ≈ mayo) | - | - |

**Tiempo total investigación:** ~40 horas (1 semana full-time o 2 semanas part-time)

---

### Escenario Pesimista (TUI falla en 3A)

| Fecha | Fase | Actividad | Tiempo | Acumulado |
|-------|------|-----------|--------|-----------|
| Dic 2 | 3 | EXP 3A (risk_scale 1.5) | 20 min | 20 min |
| Dic 2 | 3 | Análisis → FALLO | 10 min | 30 min |
| **Dic 2-3** | 3-ALT | Rediseño PGF v2 | 4 h | 4.5 h |
| Dic 3 | 3-ALT | EXP 3-ALT-A (benigno) | 15 min | 4.75 h |
| Dic 3 | 3-ALT | EXP 3-ALT-B (riesgo) | 20 min | 5 h |
| Dic 3 | 3-ALT | Análisis v2 | 30 min | 5.5 h |
| **Dic 4-5** | 3-ALT | Iterar si falla (2-3 ciclos) | 8 h | 13.5 h |
| Dic 6-7 | 4 | SOTA comparison (si v2 exitoso) | 3 h | 16.5 h |
| **Dic 8-21** | 6 | Paper (claims más modestos) | 25 h | 41.5 h |
| Ene 2026 | 6 | Submit como "negative result" o workshop | - | - |

**Tiempo total investigación:** ~42 horas (con retrabajos)

---

## 🎯 CRITERIOS DE PARADA

### Continuar Investigación Si:
- ✅ EXP 3A muestra TUI ≥ 50% Control
- ✅ PGF_Bruto_Avg > 0 (teoría se cumple)
- ✅ Evidencia clara de reducción tripwire hits
- ✅ Resultados interpretables científicamente

### Pivotar/Redefinir Si:
- ⚠️ TUI entre 30-50% Control (funciona pero débil)
- ⚠️ PGF_Bruto ≈ 0 (teoría no clara)
- ⚠️ Success rate < 90% (inestable)

### Detener/Publicar "Negative Result" Si:
- ❌ TUI < 30% Control consistentemente
- ❌ PGF_Bruto < 0 (teoría contradice)
- ❌ 3+ iteraciones rediseño sin mejora
- ❌ Success rate < 80% (no viable)

---

## 📦 ENTREGABLES FINALES

### Mínimo Viable (Si falla todo)
1. Paper técnico: "Challenges in PGF-based RL Alignment"
2. Dataset público: 15,000+ episodios documentados
3. Framework open-source: reproducible
4. Lecciones aprendidas: guía para futuros investigadores

### Esperado (Si 3A exitoso)
1. Paper: "TUI v4.2: Risk-aware RL via Prudential Gating Functions"
2. Comparación SOTA: TUI competitivo en gridworld
3. Código + artefacts DOI: Zenodo
4. Blog post divulgativo: alineación AGI

### Óptimo (Si todo sale perfecto)
1. Paper tier-1: NeurIPS/ICLR aceptado
2. Benchmark público: "TUI-Gridworld" para comunidad
3. Extension a MuJoCo/Procgen: escalabilidad demostrada
4. Colaboraciones: labs de AI Safety interesados

---

## 🚦 ACCIÓN INMEDIATA (Mañana 2 dic 2025)

### Comando a Ejecutar:
```powershell
python sim/prototipo_rl_simbiosis.py `
  --episodes 500 `
  --seed 42 `
  --grid_size 5 `
  --risk_scale 1.5 `
  --tui_only `
  --pgf_mix 0.2 `
  --output_prefix results/risk_validation/exp3a_risk15_seed42
```

**Tiempo:** 20 minutos  
**Riesgo:** Bajo  
**Valor:** CRÍTICO - determina todo el plan posterior

### Post-Experimento:
```powershell
python results/risk_validation/analyze_risk_exp.py
```

Esto dará la respuesta definitiva:
- ✅ **Si TUI ≥ 70% Control** → SOTA comparison → Paper fuerte
- ⚠️ **Si TUI 50-70% Control** → Sweep pgf_mix → Optimizar
- ❌ **Si TUI < 50% Control** → Rediseñar PGF → Camino A2

---

**Documento guardado:** 1 de diciembre 2025  
**Próxima sesión:** 2 de diciembre 2025 - Ejecutar EXP 3A  
**Responsable:** Sistema TUI v4.2 con supervisión humana
