# PGF v6 - Caracterización de la Curva Goldilocks

**Versión**: TUI v4.3 candidate (v6)  
**Estado**: 🔄 EN PREPARACIÓN  
**Objetivo**: Mapear relación no lineal ratio(D) con barrido fino de densidades

---

## Estructura de Directorios

```
results/pgf_v6/
├── README_PGF_v6.md                 # Este archivo - Estado del proyecto
├── PREREGISTRO_v6.md                # Hipótesis + diseño + criterios (preregistrado 2025-12-02)
│
├── resultados/                       # Datos crudos (pendiente - 50 archivos esperados)
│   ├── exp3_spawn{D}_seed{S}.json           # 25 configuraciones
│   ├── exp3_spawn{D}_seed{S}_episodes.csv   # 25 configuraciones  
│   └── experiment_3_summary.json            # Resumen agregado
│
├── figuras/                          # Visualizaciones (pendiente)
│   ├── goldilocks_curve_full.png            # Curva ratio(D) con 5 densidades
│   ├── model_comparison_aic.png             # Comparación modelos (lineal/cuadrático/log)
│   ├── mechanism_decomposition.png          # Recursos vs castigos vs D
│   └── regime_comparison_boxplot.png        # Distribución por régimen
│
└── reportes/                         # Análisis estadístico (pendiente)
    └── REPORTE_EXPERIMENTO_3.md
```

---

## Antecedentes (PGF v5)

**Resultados previos**:
- H-DR (ratio ∝ 1/D) refutada
- Patrón no lineal detectado con N=7 configs robustos
- Ecuación empírica: `ratio = -19.85D² + 44.58D + 74.38`
- Máximo detectado: D ≈ 1.12, ratio ≈ 99.4%

**Limitaciones v5**:
- Solo 3 densidades × 3 seeds (N pequeño)
- 100 episodios/agente (outliers DQN - seed 456)
- Resolución baja para caracterizar forma exacta

---

## Diseño v6 (Mejoras)

### Parámetros Experimentales

**Densidades (5 niveles)**:
- 0.05 - Muy baja (escasez extrema)
- 0.10 - Baja
- 0.20 - Intermedia-baja
- 0.30 - Intermedia-alta  
- 0.40 - Alta (abundancia)

**Réplicas**: 5 seeds [42, 123, 456, 789, 101112]

**Episodios**: 300 por agente (vs 100 en v5)
- Justificación: Reducir varianza DQN, evitar outliers

**Total**: 25 configs × 600 episodios = **15,000 episodios** (~6-8h)

### Entorno (congelado v3)

```python
ResourceDensityEnv(
    size=4,                      # Grid 4×4 (fijo)
    risk_scale=1.5,              # Nivel riesgo (fijo)
    resource_reward=1.0,         # Calibrado v5
    max_resources_on_grid=3,     # Escasez real
    step_cost=-0.3,              # Castigo fuerte vagabundeo
    resource_decay_steps=5       # Caducan rápido
)
```

---

## Hipótesis v6 (Preregistrada)

### H0 (Nula)
> Ratio PGF/Control es independiente de densidad (curva plana)

### H1 (Goldilocks)
> Ratio sigue **parábola invertida** con máximo en D intermedio

**Predicciones cuantitativas**:

| Densidad | D_eff esperado | Ratio esperado | Rango IC95% |
|----------|---------------|----------------|-------------|
| 0.05 | 0.20-0.40 | 70-90% | [60, 100]% |
| 0.10 | 0.60-0.90 | 95-105% | [85, 115]% |
| 0.20 | 1.00-1.30 | **100-110%** ← PICO | [90, 120]% |
| 0.30 | 1.50-1.80 | 90-100% | [80, 110]% |
| 0.40 | 2.00-2.50 | 80-95% | [70, 105]% |

### Criterios de Éxito (5 criterios)

H1 soportada SI:
1. ✅ |r| > 0.5, p < 0.01 (correlación significativa)
2. ✅ Modelo cuadrático gana (ΔAIC < -4 vs lineal)
3. ✅ Coeficiente a < 0, IC95% no cruza 0 (parábola invertida)
4. ✅ Máximo D* ∈ [0.7, 1.5] (zona Goldilocks)
5. ✅ Ratio pico > 95% (PGF competitivo)

**Mínimo para publicación**: 3/5 criterios

---

## Mecanismo Propuesto

**¿Por qué curva no lineal?**

1. **Escasez (D bajo)**: Supervivencia pura → prudencia no diferencia
2. **Goldilocks (D medio)**: Balance perfecto → prudencia maximiza eficiencia
3. **Abundancia (D alto)**: Margen amplio → imprudencia tolerable

**Mediadores**:
- Recursos recolectados (PGF > Control en D medio)
- Castigos acumulados (Control > PGF en D medio)
- Eficiencia (reward/step) maximiza en D óptimo

---

## Cronograma

| Fase | Estado | Tiempo |
|------|--------|--------|
| Preregistro | ✅ COMPLETO | - |
| Scripts preparación | 🔄 PENDIENTE | 1h |
| Ejecución batch | 🔄 PENDIENTE | 6-8h |
| Análisis estadístico | 🔄 PENDIENTE | 2h |
| Documentación final | 🔄 PENDIENTE | 1h |

**Total estimado**: 10-12h

---

## Próximos Pasos

1. Crear `scripts/run_experiment_3_goldilocks.py`
2. Validar con dry-run (1 config, 50 eps)
3. Ejecutar batch completo (puede ser overnight)
4. Análisis + figuras + reporte
5. Commit final + paper v6

---

## Referencias

- **v5 cerrado**: `results/pgf_v5/README_PGF_v5_FINAL.md`
- **Refutación H-DR**: `results/pgf_v5/INFORME_EXP2_REFUTACION.md`
- **Curva v5**: `results/pgf_v5/figuras/goldilocks_curve_analysis.png`
- **Preregistro v6**: `results/pgf_v6/PREREGISTRO_v6.md` (commit `fbabbbd`)

---

**Estado actual**: ✅ Estructura creada, preregistro timestamped, listo para ejecución
