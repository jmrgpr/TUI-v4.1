# 📋 REPORTE CIENTÍFICO - EXPERIMENTO 3A

**Título:** Validación de TUI v4.2 con Riesgo Constitutivo  
**Fecha:** 2 de diciembre 2025  
**Investigador:** Sistema TUI v4.2  
**Estado:** ❌ EXPERIMENTO FALLIDO - Hipótesis H1 NO VALIDADA

---

## 1. OBJETIVO

Validar la Hipótesis H1 de la Teoría Unificada de Inteligencia (TUI v4.2):

```
H1: I_operativa ∝ P_riesgo^α

Predicción: Con riesgo constitutivo alto (risk_scale=1.5), los agentes 
TUI/Simbiosis deberían aprovechar la señal PGF para gestionar riesgo mejor 
que el agente Control baseline, resultando en reward ≥ 70% del Control.
```

---

## 2. METODOLOGÍA

### 2.1 Configuración Experimental

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| **Grid size** | 5×5 | Mayor complejidad vs smoke test (3×3) |
| **risk_scale** | 1.5 | Penalizaciones 3× mayores (vs 0.5 previo) |
| **pgf_mix** | 0.2 | Valor óptimo validado en Fase 2 |
| **Episodes** | 500 | Suficiente para convergencia (vs 1000 Fase 2) |
| **Seed** | 42 | Reproducibilidad |
| **Tripwires** | [(2,2)] | Activos (riesgo real) |
| **Shocks** | [(3,3)] | Activos (riesgo real) |
| **Penalty high** | -60.0 | Configuración estándar |
| **Penalty low** | -25.0 | Configuración estándar |

### 2.2 Agentes Evaluados

1. **Control (Baseline):** Agente tabular sin PGF
2. **Simbiosis:** DQN + PGF (pgf_mix=0.2)
3. **TUI:** DQN + PGF (pgf_mix=0.2) [idéntico a Simbiosis]

### 2.3 Métricas Primarias

- Reward medio (μ) y desviación estándar (σ)
- Success rate (% episodios reward >0)
- Ratio TUI/Control
- Significancia estadística (t-test, p-value, Cohen's d)

---

## 3. RESULTADOS

### 3.1 Estadísticas Descriptivas

| Agente | n | Media (μ) | Std (σ) | Mediana | Rango | Success Rate |
|--------|---|-----------|---------|---------|-------|--------------|
| **Control** | 500 | **145.04** | 285.90 | 27.00 | [-16.80, 1527.80] | 99.80% (499/500) |
| **Simbiosis** | 500 | **24.43** | 44.68 | 21.28 | [-82.68, 854.08] | 99.80% (499/500) |
| **TUI** | 500 | **24.43** | 44.68 | 21.28 | [-82.68, 854.08] | 99.80% (499/500) |

**Observaciones clave:**
- TUI/Simbiosis son idénticos (esperado, mismo agente)
- Control supera TUI por **5.94×** (factor crítico)
- Success rates similares (99.8% todos), problema no es estabilidad sino magnitud reward

### 3.2 Comparación Estadística (TUI vs Control)

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Ratio TUI/Control** | **16.84%** | ❌ Muy inferior (objetivo: ≥70%) |
| **Déficit** | **83.16%** | TUI obtiene solo 1/6 del reward Control |
| **t-statistic** | -9.3203 | Diferencia muy significativa |
| **p-value** | <0.000001 *** | Probabilidad nula de azar |
| **Cohen's d** | -0.5895 | Efecto mediano (negativo para TUI) |
| **Mann-Whitney U** | 7646 | Confirma diferencia (non-parametric) |

### 3.3 Convergencia (Últimos 100 Episodios)

| Agente | Media últimos 100 | Std últimos 100 | Estabilidad |
|--------|-------------------|-----------------|-------------|
| Control | 118.52 | 264.21 | Alta varianza |
| TUI | 25.44 | 40.27 | Baja varianza (más estable) |

**Nota:** TUI más estable pero en nivel inferior (no es ventaja)

---

## 4. VALIDACIÓN HIPÓTESIS H1

### 4.1 Predicciones vs Realidad

| Predicción H1 | Resultado Real | Validado |
|---------------|----------------|----------|
| PGF_Bruto > 0 con riesgo | NO DISPONIBLE (columna ausente CSV) | ❌ No verificable |
| TUI aprende más rápido | TUI 6× más lento | ❌ FALSO |
| TUI reward ≥ 80% Control | TUI reward = 16.8% Control | ❌ FALSO |
| Menos tripwire hits TUI | Control: 0.00, Simbiosis: 0.04 | ❌ FALSO (Control mejor) |

**Conclusión:** **Hipótesis H1 NO VALIDADA**. El aumento de riesgo (risk_scale 0.5→1.5) no mejoró el performance relativo de TUI.

### 4.2 Análisis Comparativo con Fase 2

| Métrica | Fase 2 (risk=0.5) | Fase 3A (risk=1.5) | Cambio |
|---------|-------------------|---------------------|--------|
| TUI media | 23.98 | 24.43 | +1.9% (insignificante) |
| Control media | 144.60 | 145.04 | +0.3% (insignificante) |
| Ratio TUI/Ctrl | 16.6% | 16.8% | Sin cambio |

**Hallazgo crítico:** Aumentar el riesgo 3× **NO mejoró la ventaja relativa de TUI**. Ambos agentes mantuvieron performance similar, sugiriendo que **PGF no está capturando la señal de riesgo correctamente**.

---

## 5. DIAGNÓSTICO DEL FALLO

### 5.1 Causa Raíz Probable: PGF_Costo Dominante

Con pgf_mix=0.2, la señal de recompensa es:

```
reward_total = 0.8 * reward_env + 0.2 * PGF_Neto

Donde:
PGF_Neto = PGF_Bruto - PGF_Costo
         = (kappa * delta_P * A_t) - (lambda_c * delta_C_t)
```

**Problema identificado:**
1. **PGF_Bruto** depende de `delta_P` (reducción de riesgo entre pasos)
2. En grid 5×5, incluso con tripwires, `delta_P` puede ser pequeño o errático
3. **PGF_Costo** penaliza consumo normal de recursos (`delta_C_t > 0` siempre)
4. Resultado: `PGF_Neto` sigue siendo mayormente negativo, **penalizando** en lugar de **guiar**

### 5.2 Evidencia Circunstancial

- **Tripwire hits:** Control 0.00 vs Simbiosis 0.04 → Control **evita mejor** los riesgos
- **Success rate idéntico:** 99.8% ambos → No es problema de estabilidad
- **TUI más estable (σ menor):** Sugiere que PGF está "aplanando" la señal, no mejorándola

### 5.3 Teoría Alternativa: Control Privilegiado

El agente Control (tabular, Q-learning) puede tener ventajas arquitectónicas:
- Estado discreto perfecto (grid coords)
- Convergencia más directa sin ruido neural
- Sin señal PGF "contaminante"

**Pero:** Esto no explica por qué TUI no mejoró **nada** con más riesgo.

---

## 6. VEREDICTO CIENTÍFICO

### 6.1 Clasificación del Resultado

Según criterios del Plan Estratégico:

| Ratio TUI/Control | Clasificación | Acción |
|-------------------|---------------|--------|
| ≥ 70% | ✅ Éxito fuerte | SOTA comparison |
| 50-70% | ⚠️ Éxito mínimo | Sweep pgf_mix |
| 40-50% | ⚠️ Débil | Evaluar rediseño |
| **< 40%** | **❌ FALLO** | **Rediseñar PGF obligatorio** |

**Nuestro resultado: 16.84%** → **FALLO CRÍTICO**

### 6.2 Implicaciones Teóricas

1. **TUI v4.2 no es superior a baseline** en gridworld con/sin riesgo
2. **PGF no captura ventaja** de gestión de riesgo como se hipotetizó
3. **pgf_mix=0.2 es un workaround**, no una validación de la teoría
4. **H1 (I ∝ P_riesgo^α) NO se sostiene** empíricamente en este dominio

---

## 7. PRÓXIMOS PASOS (OBLIGATORIOS)

### 7.1 Camino A2: Rediseño PGF (Solución B)

**Objetivo:** Hacer que PGF recompense supervivencia y eficiencia, no solo reducción de riesgo.

**Cambios propuestos:**

```python
# En sim/evaluator_pgf.py

def _compute_pgf_components_v2(self, agent_resources, delta_C_t, delta_P, A_t, env):
    kappa = 1.0
    lambda_c = 0.1
    
    # NUEVO: Bonus supervivencia (siempre positivo)
    survival_bonus = 0.2 if agent_resources > 0 else 0.0
    
    # NUEVO: Penalizar solo consumo excesivo (>50% recursos)
    resource_ratio = delta_C_t / max(env.resources, 1.0)
    if resource_ratio < 0.5:
        pgf_costo = lambda_c * delta_C_t * 0.3  # Penalización suave
    else:
        pgf_costo = lambda_c * delta_C_t  # Penalización completa
    
    # PGF_Bruto: riesgo + supervivencia
    pgf_bruto = kappa * delta_P * A_t + survival_bonus
    
    return pgf_bruto, pgf_costo, (pgf_bruto - pgf_costo)
```

**Experimento 3-ALT-A:** Validar PGF v2 en entorno benigno (grid 3×3, risk=0.5, episodes=200)
- Criterio: Media >0, success >90% con **pgf_mix=1.0** (PGF puro)

**Experimento 3-ALT-B:** Validar PGF v2 con riesgo (grid 5×5, risk=1.5, episodes=500)
- Criterio: TUI ≥ 70% Control

**Tiempo estimado:** 4-8 horas (implementación + testing)

### 7.2 Alternativa: Publicar "Negative Result"

Si rediseño PGF también falla, considerar:
- Paper: "Challenges in Prudential Gating Functions for RL Alignment"
- Contribución: Documentación rigurosa de por qué PGF no funciona como esperado
- Target: Workshop (ICLR Safe RL, NeurIPS Alignment)
- Valor: Evitar que otros cometan el mismo error

---

## 8. ARTEFACTOS GENERADOS

### 8.1 Datos
- `exp3a_risk15_seed42_episodes.csv` (1500 episodios, 3 agentes)
- `exp3a_risk15_seed42.json` (metadata experimento)

### 8.2 Análisis
- `exp3a_summary.txt` (resumen ejecutivo)
- `exp3a_convergence_analysis.png` (gráfico convergencia)
- `analyze_risk_exp.py` (script análisis reproducible)
- `REPORTE_EXP3A.md` (este documento)

### 8.3 Código
- Sin cambios en código fuente (experimento usó config existente)

---

## 9. CONCLUSIÓN

**El Experimento 3A demostró que aumentar el riesgo constitutivo (risk_scale 1.5) NO mejora el performance relativo de agentes TUI con PGF respecto a un baseline simple.**

**Ratio TUI/Control = 16.84%** es un fallo inaceptable que invalida la Hipótesis H1 de la teoría TUI v4.2 en su formulación actual.

**Acción obligatoria:** Implementar Solución B (rediseño PGF) antes de cualquier comparación SOTA o publicación. Si Solución B también falla, replantear fundamentalmente el enfoque PGF o aceptar que TUI no es superior a métodos estándar en este dominio.

**Honestidad científica:** Este resultado negativo es tan valioso como uno positivo. Documenta limitaciones reales de un enfoque teórico y guía investigación futura.

---

**Documento generado:** 2 diciembre 2025, 10:30 AM  
**Próxima sesión:** Implementar Solución B (rediseño PGF v2)  
**Status proyecto:** Fase 3 FALLIDA → Redirigir a Camino A2
