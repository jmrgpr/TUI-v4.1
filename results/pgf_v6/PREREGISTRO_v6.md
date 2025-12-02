# PGF v6 - Preregistro Experimento 3: Caracterización de la Curva Goldilocks

**Título**: Mapping the Goldilocks Zone: Non-Linear Relationship Between Resource Density and Alignment Cost in RL

**Fecha preregistro**: 2025-12-02  
**Investigador principal**: TUI v4.3 Research Team  
**Versión**: PGF v6.0  
**Antecedentes**: PGF v5 (Exp2) refutó H-DR (ratio ∝ 1/D) y detectó patrón no lineal con máximo en D intermedia

---

## 1. Hipótesis y Predicciones

### 1.1 Hipótesis Nula (H0)
> **H0**: El ratio PGF/Control es independiente de la densidad efectiva de recursos.
> 
> Matemáticamente: $\text{ratio}(D) = c$ (constante)

**Si H0 es cierta**: 
- Correlación r ≈ 0
- Ajuste lineal R² < 0.1
- No diferencias significativas entre densidades

### 1.2 Hipótesis Alternativa (H1 - Goldilocks)
> **H1**: El ratio PGF/Control sigue una relación **no lineal** con máximo en densidad intermedia.
>
> Forma funcional propuesta: $\text{ratio}(D) = aD^2 + bD + c$ (parábola invertida)

**Predicciones cuantitativas** (basadas en PGF v5):

| Densidad | D_efectiva esperado | Ratio esperado | Intervalo 95% |
|----------|---------------------|----------------|---------------|
| **Muy baja** | 0.20 - 0.40 | 70 - 90% | [60, 100]% |
| **Baja** | 0.60 - 0.90 | 95 - 105% | [85, 115]% |
| **Intermedia** | 1.00 - 1.30 | **100 - 110%** | [90, 120]% ← **PICO** |
| **Alta** | 1.50 - 1.80 | 90 - 100% | [80, 110]% |
| **Muy alta** | 2.00 - 2.50 | 80 - 95% | [70, 105]% |

**Predicción del máximo**:
- Densidad óptima: $D^* \in [0.9, 1.4]$
- Ratio máximo: $\text{ratio}(D^*) \in [100\%, 110\%]$

### 1.3 Mecanismo Propuesto

**¿Por qué parábola invertida?**

1. **Régimen de escasez (D bajo)**:
   - Pocos recursos → competencia extrema
   - Prudencia no compensa: todos luchan por sobrevivir
   - PGF y Control convergen (~paridad o PGF peor)

2. **Régimen Goldilocks (D intermedio)**:
   - Recursos suficientes pero no abundantes
   - Prudencia maximiza eficiencia (evitar riesgos innecesarios)
   - step_cost=-0.3 penaliza vagabundeo → PGF aventaja
   - **Zona de máximo diferencial competitivo**

3. **Régimen de abundancia (D alto)**:
   - Recursos abundantes → margen de error amplio
   - Imprudencia de Control no se castiga tanto
   - Ambos agentes pueden "permitirse" errores
   - Diferencia se reduce (no desaparece, pero baja)

**Variables mediadoras**:
- Recursos recolectados por episodio
- Tripwires/shocks activados
- Step cost acumulado
- Tiempo hasta terminación

---

## 2. Diseño Experimental

### 2.1 Variables

**Variable independiente**: Densidad de recursos (spawn_rate)
- **Niveles**: 5 densidades en barrido fino
  - 0.05 (muy baja - escasez extrema)
  - 0.10 (baja)
  - 0.20 (intermedia-baja)
  - 0.30 (intermedia-alta)
  - 0.40 (alta - abundancia)

**Variable dependiente**: Ratio PGF/Control (%)
- **Definición**: $\text{ratio} = \frac{\bar{R}_{\text{PGF}}}{\bar{R}_{\text{Control}}} \times 100$
- Donde $\bar{R}$ = recompensa media en últimos 100 episodios

**Variables controladas**:
- Grid size: 4×4 (fijo)
- Risk scale: 1.5 (fijo)
- Entorno: ResourceDensityEnv v3 endurecido
  - resource_reward = 1.0
  - max_resources_on_grid = 3
  - step_cost = -0.3
  - resource_decay_steps = 5

### 2.2 Tamaño Muestral

**Configuración por densidad**:
- Seeds: 5 réplicas [42, 123, 456, 789, 101112]
- Episodios por agente: **300** (mejora vs 100 en v5)
- Total por config: 300 PGF + 300 Control = 600 episodios

**Tamaño total**:
- Configs: 5 densidades × 5 seeds = **25 configuraciones**
- Episodios totales: 25 × 600 = **15,000 episodios**
- Tiempo estimado: ~6-8 horas (asumiendo 2 min/config)

**Justificación N=300**:
- PGF v5 con N=100 mostró outliers (seed 456)
- Literatura RL sugiere N>200 para convergencia DQN estable
- N=300 balancea robustez vs costo computacional

### 2.3 Procedimiento

**Secuencia de ejecución**:
1. Configurar entorno con spawn_rate específico
2. Inicializar agentes PGF y Control (arquitectura idéntica)
3. **Fase 1**: Entrenar agente PGF (300 episodios)
   - Registro: reward, recursos, steps, D_eff por episodio
4. **Fase 2**: Entrenar agente Control (300 episodios)
   - Registro: mismas métricas
5. Calcular ratio y métricas agregadas
6. Guardar metadata completa (JSON + CSV)

**Criterios de exclusión**:
- Configs donde agente colapsa (reward medio < 50)
- Seeds que generen >2 colapsos (outliers sistemáticos)
- Documentar exclusiones con justificación

---

## 3. Análisis Estadístico

### 3.1 Análisis Primario

**Test de hipótesis**:

1. **H0 vs H1**: ¿Existe relación no trivial?
   - Correlación Pearson: r entre D_eff y ratio
   - Criterio rechazo H0: |r| > 0.5 y p < 0.01

2. **Forma funcional**: ¿Es parábola invertida?
   - Ajustar modelos:
     - M0: Constante (H0)
     - M1: Lineal ($a + bD$)
     - M2: Cuadrático ($a + bD + cD^2$)
     - M3: Logarítmico ($a + b\log(D)$)
     - M4: Exponencial ($ae^{bD}$)
   - Selección: AIC/BIC (penaliza complejidad)
   - Criterio: ΔAIC < -4 para preferir modelo complejo

3. **Goldilocks confirmado**: ¿Existe máximo?
   - Si M2 (cuadrático) gana: calcular vértice $D^* = -b/(2a)$
   - Validar: $a < 0$ (parábola invertida)
   - Bootstrap IC95% para $D^*$ y $\text{ratio}(D^*)$

### 3.2 Análisis Secundario

**Descomposición de mecanismo**:
- Regresión: $\text{ratio} \sim \text{recursos} + \text{castigos} + \text{steps}$
- Mediación: ¿D afecta ratio vía recursos o vía castigos?
- ANOVA: Comparar regímenes (baja/intermedia/alta)

**Robustez**:
- Análisis con/sin outliers
- Validación cruzada (leave-one-out por seed)
- Análisis de sensibilidad a N (100 vs 200 vs 300 eps)

### 3.3 Criterios de Éxito

**H1 (Goldilocks) es soportada SI**:

1. ✅ Correlación |r| > 0.5 (p < 0.01)
2. ✅ Modelo cuadrático gana (ΔAIC < -4 vs lineal)
3. ✅ Parábola invertida ($a < 0$, IC95% no cruza 0)
4. ✅ Máximo en rango [0.7, 1.5] (basado en v5)
5. ✅ Ratio pico > 95% (PGF competitivo o superior)

**Mínimo para publicación**: 3/5 criterios cumplidos

---

## 4. Metadatos y Trazabilidad

### 4.1 Versionado

- **Entorno**: `environment_v2.py` (commit: `03214bc`)
- **Scripts**: `run_experiment_3_goldilocks.py` (nuevo)
- **Análisis**: `analyze_goldilocks_curve.py` (nuevo)

### 4.2 Datos Abiertos

**Repositorio**: https://github.com/jmrgpr/TUI-v4.1/tree/main/results/pgf_v6

**Estructura**:
```
results/pgf_v6/
├── PREREGISTRO_v6.md          # Este documento
├── resultados/
│   ├── exp3_spawn{D}_seed{S}.json  (25 archivos)
│   ├── exp3_spawn{D}_seed{S}_episodes.csv (25 archivos)
│   └── experiment_3_summary.json
├── figuras/
│   ├── goldilocks_curve_full.png
│   ├── model_comparison_aic.png
│   ├── mechanism_decomposition.png
│   └── regime_comparison_boxplot.png
├── reportes/
│   └── REPORTE_EXPERIMENTO_3.md
└── README_PGF_v6.md
```

### 4.3 Timestamp y Firma

**Git commit de preregistro**: (pendiente tras guardar)  
**Fecha límite ejecución**: 2025-12-05  
**Análisis ciego**: No (investigador conoce patrón v5, sesgo minimizado con preregistro)

---

## 5. Limitaciones Reconocidas

### 5.1 Conocidas

1. **Sesgo de conocimiento previo**: 
   - v5 mostró patrón → predicciones influenciadas
   - Mitigación: Criterios cuantitativos a priori

2. **N relativamente pequeño**:
   - 5 seeds por densidad (mínimo estadístico)
   - Outliers individuales pueden influir
   - Mitigación: Análisis con/sin outliers

3. **DQN vanilla**:
   - No es estado del arte (no Double DQN, no prioritized replay)
   - Convergencia puede ser subóptima
   - Justificación: Simplicidad + comparabilidad con v5

4. **Dominio limitado**:
   - Solo grid 4×4, solo risk_scale=1.5
   - Generalización a otros contextos incierta

### 5.2 Posibles Resultados No Anticipados

**Si H0 (plano) gana**:
- Patrón v5 fue artefacto de bajo N
- Documentar como "resultado no replicado"
- Análisis post-hoc de diferencias v5 vs v6

**Si forma es diferente a parábola**:
- Explorar M3 (logarítmico) o M4 (exponencial)
- Describir forma empíricamente
- No forzar interpretación de "Goldilocks" si datos no apoyan

**Si máximo es inesperado**:
- Ej: D* < 0.5 o D* > 2.0 (fuera de rango v5)
- Validar con análisis de sensibilidad
- Considerar experimento v7 para explorar extremos

---

## 6. Plan de Contingencia

### Si tiempo es limitado (<8h disponibles)

**Opción reducida**:
- 3 densidades [0.10, 0.20, 0.30] × 5 seeds × 300 eps = 9,000 eps (~4h)
- Suficiente para confirmar máximo, pero menos resolución

### Si aparecen >4 outliers (colapsos)

**Protocolo**:
1. Identificar patrón: ¿Es seed específico? ¿Densidad específica?
2. Re-ejecutar configs problemáticas con seed diferente
3. Si persiste: documentar como "régimen inestable"

### Si resultados contradicen v5

**No es fracaso**:
- Mayor N puede revelar patrón diferente (esperado en ciencia)
- Documentar ambos resultados con honestidad
- Paper enfoca en "importancia de N robusto en RL"

---

## 7. Contribuciones Esperadas

### 7.1 Científicas

1. **Caracterización cuantitativa**: Primera ley empírica de costo de alineación vs densidad en RL
2. **Zona Goldilocks validada**: Confirmar que existe régimen óptimo para alineación
3. **Mecanismo causal**: Descomponer por qué D modula diferencia PGF/Control

### 7.2 Metodológicas

1. **Protocolo replicable**: Barrido fino de densidad + análisis robusto
2. **Manejo de outliers RL**: Documentar varianza DQN + estrategias mitigación
3. **Transparencia total**: Preregistro + datos abiertos + código reproducible

### 7.3 Prácticas (IA Safety)

1. **Diseño de entornos**: No todos los contextos favorecen alineación por igual
2. **Resource engineering**: Manipular D para maximizar ventaja de agentes alineados
3. **Implicación para sistemas reales**: Escasez extrema o abundancia extrema pueden dificultar alineación

---

## 8. Cronograma

| Fase | Duración | Tareas |
|------|----------|--------|
| **Preparación** | 1h | Crear scripts, validar entorno, test dry-run |
| **Ejecución** | 6-8h | Batch 25 configs (puede correr overnight) |
| **Análisis** | 2h | Estadística + figuras + reporte |
| **Documentación** | 1h | README v6, commit final |
| **TOTAL** | ~10-12h | Completable en 1-2 días |

---

## 9. Referencias

- **PGF v5**: `results/pgf_v5/README_PGF_v5_FINAL.md`
- **Exp2 refutación**: `results/pgf_v5/INFORME_EXP2_REFUTACION.md`
- **Curva v5**: `results/pgf_v5/figuras/goldilocks_curve_analysis.png`
- **Ecuación v5**: $\text{ratio} = -19.85D^2 + 44.58D + 74.38$ (N=7, máximo D≈1.12)

---

## 10. Firma Científica

**Preregistro creado**: 2025-12-02  
**Investigador**: [Nombre del equipo]  
**Revisores consultados**: Gemini, Codex  
**Commit para timestamp**: (siguiente commit tras guardar este archivo)

**Declaración**: Este preregistro establece hipótesis, predicciones y análisis ANTES de ejecutar Experimento 3. Cualquier desviación será documentada con justificación. Los datos serán publicados independientemente del resultado.

---

**Estado**: ✅ PREREGISTRADO - Listo para ejecución PGF v6
