# PGF v5: Optimal Foraging Paradox & Density-Dependent Alignment Cost

**Investigador:** Jose M Rivera Garcia  
**Fecha inicio:** 2 de diciembre de 2025  
**Estado:** 🔬 En diseño experimental

---

## 🎯 Objetivo Central

**Demostrar que el "Valle de Dificultad" observado en grid 4x4 NO refuta la TUI, sino que revela:**

> **"El costo de la alineación es inversamente proporcional a la densidad de recursos"**

O en términos científicos:

$$Tax_{align}(D) = \kappa \cdot \frac{1}{D + \epsilon}$$

Donde:
- $D$ = Densidad de recursos
- $Tax_{align}$ = Costo de oportunidad de la prudencia
- $\kappa$ = Factor de escala
- $\epsilon$ = Término de estabilización

---

## 🔬 Marco Teórico: Optimal Foraging Theory Meets AI Safety

### Hallazgo de PGF v4:
```
Grid 3x3 → Ratio: 105% (óptimo para PGF)
Grid 4x4 → Ratio:  32% (valle - Control gana) ← "PARADOJA"
Grid 5x5 → Ratio:  39% (recuperación parcial)
```

### Interpretación Errónea Inicial:
❌ "4x4 es más difícil que 5x5" → Sugiere refutación de TUI

### Interpretación Correcta (PGF v5):
✅ **"4x4 tiene densidad de recursos ÓPTIMA para imprudencia"**

| Grid | Densidad | Perdona errores | Ganador | Ratio |
|------|----------|-----------------|---------|-------|
| 3x3  | Baja     | NO              | PGF (cautela necesaria) | 105% |
| 4x4  | **ALTA** | **SÍ**          | Control (velocidad > prudencia) | 32% |
| 5x5  | Media    | Poco            | PGF recupera (dispersión) | 39% |

---

## 💡 La Hipótesis Revisada

### TUI v4.1 (original):
"La inteligencia útil emerge del gradiente de riesgo acumulado"

### TUI v4.2 (enriquecida):
"La ventaja evolutiva de la inteligencia (alineación/prudencia) **escala inversamente** con la densidad de recursos del entorno"

**Predicción matemática:**
$$\frac{Reward_{PGF}}{Reward_{Control}} \propto \frac{1}{D_{recursos}} \cdot P_{riesgo}$$

**Traducción:**
- Cuando $D$ es alta (4x4): Ratio bajo (imprudencia "barata")
- Cuando $D$ es baja (3x3, 5x5): Ratio alto (prudencia "necesaria")

---

## 🎓 Fundamento en Optimal Foraging Theory

De la ecología evolutiva (Charnov, 1976):

> "Cuando la densidad de presas aumenta, el depredador puede capturarlas más rápido. En cierto punto, la tasa de captura es tan alta que el depredador no tiene que comer cada presa que encuentra"

**Analogía a nuestro experimento:**
- **Control** = Depredador oportunista (come todo rápido)
- **PGF** = Depredador selectivo (evalúa riesgos antes de comer)
- **4x4** = Entorno con "presas" abundantes → Selectividad es COSTOSA

---

## 🧪 Diseño Experimental PGF v5

### Experimento 2: Manipulación de Densidad de Recursos

**Objetivo:** Demostrar que el ratio sigue la **densidad**, NO el grid size.

#### Configuraciones de prueba:

| Exp | Grid | Spawn Rate | Death Penalty | Predicción Ratio | Hipótesis |
|-----|------|------------|---------------|------------------|-----------|
| 2A  | 4x4  | 0.2 (baja) | -100          | ~60-70% | Escasez → PGF gana |
| 2B  | 4x4  | 0.5 (actual) | -100        | ~32% | Baseline (valle) |
| 2C  | 4x4  | 0.8 (muy alta) | -100       | ~20-25% | Abundancia → Control arrasa |
| 2D  | 4x4  | 0.5        | -200 (alto) | ~50-60% | Castigo → Prudencia paga |
| 2E  | 5x5  | 0.5        | -100        | ~39% | Control (baseline v4) |

**Criterio de éxito:**
Si Exp 2A (baja densidad) > Exp 2B (baseline) > Exp 2C (alta densidad), entonces:
✅ **El ratio sigue la densidad, confirmando TUI v4.2**

---

## 📊 Métricas Clave a Medir

### Primarias:
1. **Ratio PGF/Control** (variable dependiente principal)
2. **Densidad efectiva de recursos** ($D_{eff}$):
   $$D_{eff} = \frac{Resources_{collected}}{Steps_{total}} \cdot Grid_{size}^2$$

### Secundarias:
3. **Resource Utilization Rate** (RUR):
   $$RUR = \frac{Resources_{consumed}}{Resources_{available}}$$
4. **Death Rate por inanición** vs **Death Rate por trampas**
5. **Exploration Efficiency**: Celdas únicas visitadas / Total steps

### Predicciones específicas:

| Métrica | Alta $D$ (2C) | Media $D$ (2B) | Baja $D$ (2A) |
|---------|---------------|----------------|---------------|
| Ratio   | < 30%         | ~32%           | > 60%         |
| RUR     | < 50%         | ~70%           | > 90%         |
| Death/trap | Baja      | Media          | Alta          |

---

## 🎯 Valor Científico de PGF v5

### Si se confirma la hipótesis:

1. **Para TUI:**
   - NO refuta la teoría original
   - Agrega dimensión crítica: **densidad de recursos como modulador**
   - Explica "cuándo" la alineación es costosa vs valiosa

2. **Para AI Safety:**
   - **Implicación práctica:** "En producción con datos limpios y abundantes (4x4), el agente 'malo' gana. En el mundo real con incertidumbre y escasez (5x5), el agente 'bueno' sobrevive"
   - Paper potencial: **"The Optimal Foraging Paradox in Aligned AI"**

3. **Para la ciencia en general:**
   - Conexión cross-disciplinaria: Ecología Evolutiva ↔ AI Alignment
   - Ley universal emergente: $Cost_{alignment} \propto 1/D_{resources}$

---

## 📋 Plan de Ejecución

### Fase 1: Validación de concepto (3-5 días)
- [ ] Experimento 2A: Grid 4x4, spawn_rate=0.2 (3 seeds)
- [ ] Experimento 2B: Replicar baseline 4x4 actual (validación)
- [ ] Experimento 2C: Grid 4x4, spawn_rate=0.8 (3 seeds)
- [ ] Análisis preliminar: ¿Ratio sigue densidad?

### Fase 2: Manipulación de castigo (2-3 días)
- [ ] Experimento 2D: Grid 4x4, death_penalty=-200 (3 seeds)
- [ ] Comparación con 2B: ¿Castigo mayor → Ratio mayor?

### Fase 3: Control con grid diferente (2 días)
- [ ] Experimento 2E: Grid 5x5 con spawn_rate=0.5 (validación v4)
- [ ] Confirmar que 5x5 con misma densidad ≠ 4x4

### Fase 4: Análisis y escritura (3-4 días)
- [ ] Análisis estadístico completo
- [ ] Visualizaciones: Ratio vs Densidad (scatter plot clave)
- [ ] Draft paper section: "Density-Dependent Cost of Alignment"

---

## 🏆 Criterios de Éxito

### Confirmación de hipótesis:
✅ $Ratio_{2A} > Ratio_{2B} > Ratio_{2C}$ (tendencia monotónica)
✅ Correlación $R^2 > 0.7$ entre densidad y ratio
✅ $Ratio_{2D} > Ratio_{2B}$ (castigo aumenta valor de prudencia)

### Descarte de hipótesis:
❌ Si ratio NO correlaciona con densidad → Grid size es factor dominante (problema para teoría)
❌ Si $Ratio_{2D} \leq Ratio_{2B}$ → Castigo no modula alineación (problema conceptual)

---

## 📚 Referencias Clave

1. **Charnov, E.L. (1976).** Optimal foraging, the marginal value theorem. *Theoretical Population Biology*, 9(2), 129-136.
2. **MacArthur, R.H., & Pianka, E.R. (1966).** On optimal use of a patchy environment. *The American Naturalist*, 100(916), 603-609.
3. **Stephens, D.W., & Krebs, J.R. (1986).** *Foraging Theory*. Princeton University Press.

---

## 🔗 Conexión con PGF v4

**PGF v4 descubrió:** El "valle" en 4x4 (32% < 5x5 39%)

**PGF v5 explica:** No es un valle de "dificultad", es un valle de "necesidad de alineación"

**Transición conceptual:**
```
v4: "Grid 4x4 es más difícil que 5x5" (fenomenología)
    ↓
v5: "Grid 4x4 perdona la imprudencia más que 5x5" (mecanismo)
```

---

## 🚀 Impacto Esperado

Si PGF v5 confirma la hipótesis de densidad:

1. **Paper de alta relevancia:** Nature AI, PNAS, o Science (cross-disciplinary gold)
2. **Contribución teórica:** TUI v4.2 con modulador de densidad
3. **Aplicación práctica:** Guía para deployment de IA alineada según "riqueza" del entorno

---

**Status actual:** Diseño experimental completo  
**Próximo paso:** Implementar manipulación de `spawn_rate` en código  
**Timeline estimado:** 2-3 semanas para resultados completos
