# Experimento v10.1: Adaptive Curriculum 8×8 con Economía Ajustada

**Versión**: v10.1 ("Economía Calibrada")  
**Fecha inicio**: 4 de diciembre de 2025  
**Status**: 🔄 PREPARACIÓN  
**Predecesor**: v10 (8×8 trivial, balance=8.0)

---

## 📋 Documentos Principales

- **PREREGISTRO_v10.1.md** (v1.0, CONGELADO): Diseño experimental, hipótesis, criterios éxito
- **TRACKING_v10.1.md**: Log de ejecución en tiempo real
- **reportes/REPORTE_FINAL_v10.1.md**: Reporte post-ejecución (pendiente)

---

## 🎯 Objetivo

**Reintroducir presión selectiva en 8×8** para validar escalamiento de curriculum adaptativo.

**Motivación**: v10 con balance=8.0 resultó trivial (470% margen → todas estrategias 100% success). v10.1 ajusta balance a 5.0 (257% margen, mismo que v9.1 exitoso en 4×4).

---

## 🔬 Cambios vs v10

| Parámetro | v10 (Trivial) | v10.1 (Ajustado) | Justificación |
|-----------|---------------|------------------|---------------|
| **INITIAL_BALANCE** | 8.0 | **5.0** | Reducir margen 470%→257% |
| **N seeds** | 5 | **8** | Aumentar potencia 45%→65% |
| Grid size | 8×8 | 8×8 | Mantener complejidad |
| Spawn rate | 0.25 | 0.25 | Mantener densidad |
| Arquitectura | DQN 2×64 | DQN 2×64 | Mantener capacidad |

**Seeds**: {42, 123, 456, 789, 101112, 131415, 161718, 192021}

---

## 📊 Hipótesis Preregistradas

### H10.1.1: Adaptive Mantiene Paridad Funcional
- **Test**: Ratio Adaptive/Control ≥ 0.70, IC NO cruza 0.65
- **Predicción**: 0.75-0.85 (vs 0.995 trivial en v10)

### H10.2.1: Adaptive Supera Fixed
- **Test**: t-test pareado, p < 0.05, d > 0.3
- **Predicción**: Δ=+10, p=0.02 (vs Δ=-0.90, p=0.89 en v10)

### H10.3.1: Adaptive Reduce Varianza
- **Test**: CV ratio < 0.80
- **Predicción**: 0.70 (vs 12.6 en v10)

### H10.4.1: Seeds Vulnerables ≥60% Success
- **Test**: Percentil inferior 25% mantiene ≥60% con Adaptive
- **Predicción**: 62-68% (vs 100% trivial en v10)

---

## 🚦 Gates Críticos (Test Mode)

**Proceder si**:
- ✅ Control: 70-90% success

**Abortar si**:
- ❌ Control >95% success (aún trivial) → requiere balance más bajo
- ❌ Control <60% success (muy difícil) → requiere balance más alto

---

## 📁 Estructura de Resultados

```
pgf_v10.1/
├── PREREGISTRO_v10.1.md          # Diseño experimental (CONGELADO)
├── README.md                      # Este archivo
├── TRACKING_v10.1.md              # Log ejecución
├── resultados/
│   ├── adaptive_seed42_episodes.csv    # 24 CSVs (3 grupos × 8 seeds)
│   ├── adaptive_seed42_summary.json
│   └── ...
├── analisis/
│   ├── hypothesis_tests_v10.1.json
│   ├── episodes_per_stage_adaptive.json
│   ├── comparison_v10_vs_v10.1.json
│   └── final_metrics_v10.1.csv
├── figuras/
│   ├── ratio_v10_vs_v10.1.png
│   ├── success_by_group_v10.1.png
│   └── episodes_per_stage_heatmap.png
├── exploratorios/
│   └── seed_clustering.json
└── reportes/
    └── REPORTE_FINAL_v10.1.md
```

---

## ⏱️ Timeline Estimado

| Fase | Duración | Dependencias |
|------|----------|--------------|
| **Desarrollo script** | ~2h | PREREGISTRO congelado ✅ |
| **Test mode** | ~10 min | Script completo |
| **Decisión GO/NO-GO** | ~30 min | Test mode validado |
| **Batch completo** | ~10-12h | GO decision |
| **Análisis** | ~2h | Batch completo |
| **Reporte final** | ~3h | Análisis completo |

---

## 📚 Referencias

- **v10 (predecesor)**: `results/pgf_v10/reportes/REPORTE_FINAL_v10.md`
- **v9.1 (balance=5.0 éxito 4×4)**: `results/pgf_v9.1/reportes/REPORTE_FINAL_v9.1.md`
- **Mapeo TUI**: `docs/MAPEO_EXPERIMENTOS_TUI.md`

---

**Última actualización**: 4 de diciembre de 2025, 23:00  
**Status**: 🔄 PREPARACIÓN (estructura creada, script pendiente)
