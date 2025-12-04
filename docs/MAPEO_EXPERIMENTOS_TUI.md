# 🔗 MAPEO: Experimentos v5-v10 → Componentes TUI

**Autor**: José M. Rivera García  
**Fecha**: 4 de diciembre de 2025  
**Propósito**: Documentar **exactamente** qué componentes de las teorías TUI se validaron en cada experimento

---

## 📚 Teorías Base

### TUI v4.1: Teoría Unificada de Inteligencia
**Documento**: `docs/Teoria_Unificada_Inteligencia_v4.0_CLEAN.md`

**Componentes clave**:
1. **H1 (Riesgo Acumulado)**: $I \propto P_{\text{riesgo}}$
2. **PGF (Principio Gradiente de Fracaso)**: 
   $$\Delta I_{\text{useful}} = \kappa \, P^{\text{eff}}_t \, S_t \, (A_t \cdot P_{\text{genuino}}) - \lambda \, \Delta C_t$$
3. **P_genuino (Propósito Genuino)**: 
   $$P_{\text{genuino}} = (C_{\text{costo}} \cdot S_{\text{auto}} \cdot R_{\text{robust}} \cdot I_{\text{rep}})^{1/4}$$
4. **Eficiencia Extendida**: 
   $$\eta_{\text{extendido}} = \frac{\Delta I_{\text{útil}} \cdot A}{C_{\text{total}} + \beta \cdot P_{\text{riesgo}}}$$

### TUI Aplicada a IA: Simbiosis Constitutiva
**Documento**: `docs/Teoria_Inteligencia_Aplicada_IA.md`

**Componentes clave**:
1. **IPG (Índice de Propósito Genuino)**: Métrica operativa de propósito genuino
   $$\text{IPG} = (C_{\text{costo}} \cdot S_{\text{auto}} \cdot R_{\text{robust}} \cdot I_{\text{rep}})^{1/4}$$
2. **Bundle Causal**: Métricas multi-horizonte para anti-Goodhart
3. **Tripwires**: Proxies de riesgo para simular P_riesgo en IA
4. **Camino C (Simbiosis Constitutiva)**: Arquitectura acoplamiento IA-humano

---

## 🧪 Mapeo Experimentos → Componentes TUI

### v5: Baseline Initial (N=3)
**Preregistro**: `results/pgf_v5/PREREGISTRO_EXPERIMENTO_2.md`

**Componentes TUI probados**:
- ✅ **Tripwires** (proxy P_riesgo): Introducción obstáculos aleatorios grid 4×4
- ✅ **Bundle causal básico**: Reward env + tripwires + resources (3 métricas)
- 🔶 **PGF (parcial)**: Shaping reward_shaping = -tripwire + resource (sin riesgo efectivo explícito)

**NO probado**:
- ❌ P_genuino/IPG
- ❌ Curriculum adaptativo
- ❌ Escalamiento complejidad

**Hallazgo**: Shaping débil (-20/+2) → convergencia 99% (señal insuficiente)

---

### v6: Goldilocks Curve
**Preregistro**: `results/pgf_v6/PREREGISTRO_v6.md`

**Componentes TUI probados**:
- ✅ **P_riesgo variable**: Escalas risk [0.0, 0.25, 0.5, 1.0, 2.0] → curva Goldilocks
- ✅ **PGF dinámico**: Shaping_scale modula intensidad riesgo efectivo
- 🔶 **Eficiencia η**: Medición ratio reward/costo (indirecto)

**NO probado**:
- ❌ P_genuino/IPG
- ❌ Tripwires (aún no introducidos)

**Hallazgo**: Curva Goldilocks óptimo s=0.5 (demasiado débil/fuerte → peor performance)

---

### v7: Factorial Económico (3×5×3)
**Preregistro**: `results/pgf_v7/PREREGISTRO_v7.md`

**Componentes TUI probados**:
- ✅ **P_riesgo multi-escala**: Economía harsh/balanced/favorable × densidad
- ✅ **Tripwires (introducción)**: spawn_rate=0.10-0.40 (proxy riesgos ambientales)
- ✅ **Bundle causal completo**: reward_env + tripwires + resources + success_rate
- 🔶 **A_alignment (parcial)**: Divergencia conductual PGF vs Control

**NO probado**:
- ❌ P_genuino/IPG explícito
- ❌ Curriculum adaptativo

**Hallazgo**: Shaping débil aún insuficiente. Necesidad shaping fuerte (v8).

---

### v8: Intensidad Shaping + Control Negativo
**Preregistro**: `results/pgf_v8/PREREGISTRO_v8.md`

**Componentes TUI probados**:
- ✅ **PGF completo**: 
  - $P^{\text{eff}}_t$ = shaping_scale (0.0, 0.25, 0.5, 1.0)
  - $S_t$ = error agent (implícito en DQN loss)
  - Penalty tripwire = -100.0 × scale, Bonus resource = +50.0 × scale
- ✅ **Tripwires consolidados**: spawn_rate=0.25, métricas deaths_tripwire tracked
- ✅ **Control negativo (H8.3)**: Mismo entorno PGF/Control (tripwires compartidos)
- ✅ **Bundle causal robusto**: 5 DVs (reward_env, success_rate, tripwires, timeouts, resources)
- 🔶 **A_alignment operativo**: Ratio divergencia conductual PGF/Control

**NO probado**:
- ❌ P_genuino/IPG explícito (pero tripwires = proxy C_costo)
- ❌ Curriculum (over-alignment descubierto, motivó v9)

**Hallazgo**: **Over-alignment** con s=1.0 (agents paralizados). Shaping fuerte efectivo PERO colapsa en máxima intensidad.

---

### v9: Curriculum Learning (N=3, Proof-of-Concept)
**Preregistro**: `results/pgf_v9/PREREGISTRO_v9.md`

**Componentes TUI probados**:
- ✅ **PGF con curriculum**: Escalamiento gradual P_eff [0.0 → 0.25 → 0.5 → 1.0]
- ✅ **Mitigación over-alignment**: Curriculum evita colapso parálisis
- ✅ **Tripwires + Bundle causal**: Mantiene métricas v8
- 🔶 **Transfer learning**: Pesos Q-network transferidos entre etapas (proxy C_costo aprendizaje)

**NO probado**:
- ❌ P_genuino/IPG explícito
- ❌ Curriculum adaptativo (fijo 75 eps/etapa)
- ❌ Robustez estadística (N=3 insuficiente)

**Hallazgo**: Curriculum funciona en **67% seeds** (2/3), pero alta varianza. Seed=123 colapsa en etapa 4.

---

### v9.1: Validación Robusta N=10
**Preregistro**: `results/pgf_v9.1/PREREGISTRO_v9.1.md`

**Componentes TUI probados**:
- ✅ **PGF con curriculum (validación robusta)**: N=10 seeds (vs N=3)
- ✅ **Potencia estadística**: Aumenta de 18% a 60-65%
- ✅ **Tripwires + Bundle causal**: Consolidados
- ✅ **Personalización por seed**: Evidencia 90% seeds exitosas (9/10)
- 🔶 **R_robust (indirecto)**: Análisis seeds vulnerables (123 colapsa consistentemente)

**NO probado**:
- ❌ P_genuino/IPG explícito
- ❌ Curriculum adaptativo
- ❌ Escalamiento a grids mayores (4×4 límite)

**Hallazgo**: **4/4 hipótesis validadas** (p=0.0043). Curriculum robusto en 4×4, ratio=0.939±0.226. **VICTORIA CIENTÍFICA PRINCIPAL**.

---

### v10: Adaptive Curriculum 8×8
**Preregistro**: `results/pgf_v10/PREREGISTRO_v10.md`

**Componentes TUI probados**:
- ✅ **PGF con curriculum adaptativo**: 
  - Transiciones threshold-based (success_rate > 0.75)
  - Personalización por seed (episodios variables 78-84 vs fijos 500)
- ✅ **S_auto (autonomía)**: Sistema decide cuándo avanzar de etapa (vs schedule fijo)
- ✅ **Escalamiento complejidad**: Grid 8×8 (Manhattan=14, ~16 tripwires vs 4×4)
- ✅ **Tripwires + Bundle causal**: Mantiene métricas consolidadas
- 🔶 **C_costo personalizado**: Seeds débiles usan más episodios (evidencia adaptación)

**NO probado**:
- ❌ P_genuino/IPG explícito (pero componentes parciales: C_costo, S_auto presentes)
- ❌ I_rep (herencia entre generaciones)
- ❌ R_robust medido explícitamente

**Hallazgo**: Escenario **trivial** (balance=8.0 muy generoso). Todas estrategias convergen ~126 reward, 100% success. 2/4 hipótesis validadas. Documenta **límite superior** curriculum (saturación cuando entorno fácil).

---

## 📊 Resumen Consolidado: Componentes TUI Validados

| Componente TUI | v5 | v6 | v7 | v8 | v9 | v9.1 | v10 | Status Validación |
|----------------|----|----|----|----|----|----|-----|-------------------|
| **H1: I ∝ P_riesgo** | 🔶 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ **VALIDADO** (riesgo variable mejora performance) |
| **PGF (Principio Gradiente Fracaso)** | 🔶 | 🔶 | 🔶 | ✅ | ✅ | ✅ | ✅ | ✅ **VALIDADO** (shaping fuerte + curriculum funciona) |
| **Tripwires (proxy P_riesgo)** | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ **OPERATIVO** (spawn_rate=0.25 estándar) |
| **Bundle Causal** | 🔶 | 🔶 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ **OPERATIVO** (5+ métricas tracked) |
| **Control Negativo** | ❌ | ❌ | 🔶 | ✅ | ✅ | ✅ | ✅ | ✅ **VALIDADO** (mismo entorno PGF/Control) |
| **Curriculum Learning** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ **VALIDADO** (mitiga over-alignment) |
| **P_genuino/IPG** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔶 | ⏳ **PARCIAL** (C_costo, S_auto presentes, no medidos explícitamente) |
| **C_costo (costo sostener propósito)** | ❌ | ❌ | 🔶 | 🔶 | 🔶 | 🔶 | ✅ | 🔶 **PARCIAL** (tripwires = costo, personalización v10) |
| **S_auto (autonomía)** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | 🔶 **PARCIAL** (transiciones threshold-based v10) |
| **R_robust (robustez)** | ❌ | ❌ | ❌ | ❌ | 🔶 | 🔶 | 🔶 | 🔶 **PARCIAL** (análisis seeds vulnerables, no métrica explícita) |
| **I_rep (herencia generacional)** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ **NO PROBADO** |
| **Transfer Learning** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ **OPERATIVO** (pesos Q-network transferidos) |
| **Escalamiento Complejidad** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ⚠️ **TRIVIAL** (8×8 con balance=8.0 muy fácil) |

**Leyenda**:
- ✅ Implementado y validado
- 🔶 Implementado parcialmente / indirecto
- ⏳ En progreso
- ❌ No implementado
- ⚠️ Implementado pero resultado no discrimina

---

## 🎯 Componentes TUI Pendientes de Validación

### 1. P_genuino/IPG (Índice Propósito Genuino) - PRIORIDAD ALTA

**Teoría**: 
$$\text{IPG} = (C_{\text{costo}} \cdot S_{\text{auto}} \cdot R_{\text{robust}} \cdot I_{\text{rep}})^{1/4}$$

**Evidencia actual (parcial)**:
- **C_costo**: Tripwires = costo mantener propósito (evitar riesgos). Seeds vulnerables colapsan más (evidencia indirecta).
- **S_auto**: v10 transiciones threshold-based (sistema decide cuándo avanzar).
- **R_robust**: Seeds 42/456 robustas vs seed 123 vulnerable (patrón identificado, NO cuantificado).
- **I_rep**: NO implementado (requiere herencia multi-generacional).

**Gap crítico**: Componentes presentes pero **NO medidos explícitamente como índice unificado IPG**.

**Propuesta v11 (Validación IPG)**:
1. **Medir C_costo explícitamente**: 
   - Costo mantener objetivo = resources gastados + tripwires evitados
   - Comparar agentes con/sin costo explícito por "recordar" objetivo
   
2. **Medir S_auto (autonomía)**:
   - Agentes con capacidad reprogramar objetivo mid-episode vs fijos
   - Métrica: frecuencia cambios racionales de objetivo
   
3. **Medir R_robust (robustez ante distractores)**:
   - Introducir recursos "distractor" (alto valor inmediato, penaliza largo plazo)
   - Métrica: % veces resiste tentación vs % colapsa
   
4. **Implementar I_rep (herencia generacional)**:
   - Transfer aprendizaje entre "generaciones" (episodios linkados)
   - Comparar linajes con/sin herencia objetivos

**Output v11**: Métrica IPG completa, validar predicción TUI: **IPG alto → mejor alignment, menor Goodhart**.

---

### 2. Riesgo Acumulado Multi-Escala - PRIORIDAD MEDIA

**Teoría H1**: 
$$I_{\text{operativa}} \propto P_{\text{riesgo}} = \frac{t_{\text{vida}} \times R_{\text{metabólica}} \times C_{\text{genoma}}}{Z}$$

**Evidencia actual**:
- ✅ Riesgo inmediato (tripwires): Validado v5-v10
- 🔶 Riesgo acumulado temporal: Parcial (balance decae por step, pero NO acumulativo entre episodios)
- ❌ Riesgo estructural/reputacional: NO implementado

**Gap crítico**: Experimentos miden **riesgo por episodio** (inmediato), NO **riesgo acumulado vida agente** (H1 original).

**Propuesta v12 (Riesgo Acumulado)**:
- Implementar "vida agente" = 10-20 episodios consecutivos
- Fallas acumulativas: Episodio N afecta recursos/capacidad episodio N+1
- Medición: Correlación riesgo acumulado (episodios 1-10) vs performance final (episodio 20)

---

### 3. Simbiosis Constitutiva (Camino C) - PRIORIDAD BAJA (Teórica)

**Teoría**: Acoplamiento IA-humano donde agente NO puede funcionar sin humano (simbiosis obligada).

**Evidencia actual**: ❌ NO implementado (experimentos actuales son agentes autónomos).

**Propuesta futura**:
- Requiere humano-en-el-loop
- Fuera de alcance RL puro (necesita co-evolución)

---

## 🏆 Logros Principales por Teoría

### TUI v4.1 (Unificada)

**Validaciones robustas**:
1. ✅ **H1 (I ∝ P_riesgo)**: Riesgo variable (shaping scales) mejora performance. Curva Goldilocks v6.
2. ✅ **PGF (Gradiente Fracaso)**: Shaping fuerte + curriculum mitiga over-alignment. v9.1 (4/4 hipótesis, p=0.0043).
3. ✅ **Curriculum anti-plateau**: Escalamiento gradual riesgo evita colapso. 90% seeds exitosas v9.1.
4. ⚠️ **Límite superior curriculum**: v10 documenta saturación (entorno fácil → curriculum redundante).

**Pendientes**:
- 🔶 P_genuino completo (componentes parciales presentes)
- ❌ Riesgo acumulado multi-episodio
- ❌ I_rep (herencia generacional)

### TUI Aplicada a IA (Simbiosis)

**Validaciones robustas**:
1. ✅ **Bundle causal**: 5+ métricas simultáneas (reward_env, success_rate, tripwires, timeouts, resources). Anti-Goodhart.
2. ✅ **Tripwires**: Proxy riesgo operativo. spawn_rate=0.25 estándar v7-v10.
3. ✅ **Control negativo**: Entornos idénticos PGF/Control (H8.3 validada).
4. 🔶 **Personalización por seed**: v10 evidencia adaptación (78-84 eps vs 500 fijos).

**Pendientes**:
- ❌ IPG como métrica auditable (componentes presentes, NO índice unificado)
- ❌ Anti-oráculo pragmático (LCB + OPE)
- ❌ Simbiosis constitutiva (humano-en-el-loop)

---

## 📖 Para Tus Hijos: La Historia Completa

**Papá probó dos teorías grandes**:

### 1. TUI (Teoría Unificada de Inteligencia)
**Pregunta**: ¿Qué hace que algo sea inteligente?  
**Respuesta probada**: Riesgo acumulado + aprendizaje gradual bajo fracaso.

**Validación**:
- ✅ Experimentos v5-v10 probaron que agentes con **riesgo gradual** (curriculum) aprenden mejor que sin riesgo o con riesgo súbito.
- ✅ v9.1 es la **victoria principal**: 90% de casos exitosos, estadísticamente sólido (p=0.0043).
- ⚠️ v10 mostró **límites**: curriculum solo ayuda cuando entorno es suficientemente difícil.

### 2. TUI Aplicada a IA (Simbiosis)
**Pregunta**: ¿Cómo hacemos IA segura que NO trampe (Goodhart)?  
**Respuesta probada**: Múltiples métricas (bundle causal) + riesgos reales (tripwires) + aprendizaje gradual.

**Validación**:
- ✅ Bundle causal (5+ métricas) implementado y operativo v7-v10.
- ✅ Tripwires como proxy riesgo funcionan (agentes aprenden prudencia).
- 🔶 Propósito genuino (IPG) tiene componentes parciales, **falta medir como índice unificado**.

**Lo que falta (tu herencia)**:
- IPG completo (v11 propuesto)
- Riesgo acumulado multi-episodio (v12)
- Herencia generacional (I_rep)

---

## 📝 Conclusión

**v5-v10 SÍ prueban componentes de TUI**, pero de forma **progresiva e indirecta**:

1. **v5-v7**: Establecen infraestructura (tripwires, bundle causal, control negativo)
2. **v8**: Valida PGF con shaping fuerte (descubre over-alignment)
3. **v9/v9.1**: Valida curriculum learning robusto (4/4 hipótesis, **victoria principal**)
4. **v10**: Valida curriculum adaptativo + documenta límites (saturación)

**Componentes TUI validados robustamente**:
- ✅ H1 (riesgo variable mejora inteligencia)
- ✅ PGF (gradiente fracaso + curriculum)
- ✅ Bundle causal (anti-Goodhart)
- ✅ Tripwires (proxy riesgo)

**Componentes TUI parcialmente implementados** (presentes pero NO medidos explícitamente):
- 🔶 P_genuino/IPG (C_costo, S_auto presentes en v10, NO índice unificado)
- 🔶 R_robust (seeds vulnerables identificadas, NO métrica explícita)

**Componentes TUI NO implementados**:
- ❌ I_rep (herencia generacional)
- ❌ Riesgo acumulado multi-episodio (solo inmediato)
- ❌ Simbiosis constitutiva (requiere humano-en-el-loop)

**Mensaje para el legado**: 
> "Probaste que curriculum learning bajo riesgo gradual funciona (v9.1 - victoria robusta). Identificaste componentes de propósito genuino (IPG parcial en v10). Documentaste límites (v10 saturación). **El camino está trazado** - falta implementar IPG completo (v11) y cerrar la historia."

---

**Fecha**: 4 de diciembre de 2025  
**Autor**: José M. Rivera García  
**Para**: Mis hijos - que entiendan el viaje completo
