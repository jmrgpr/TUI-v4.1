# REPORTE MULTI-SEED VALIDATION

**Fecha**: 2025-12-05 12:57
**Seeds**: [13, 42, 101, 2025, 9999]
**N**: 5

---

## Resultados Agregados

| Fase | Grid | Gate | Success Mean ± Std | Rango | Seeds Pasaron |
|------|------|------|-------------------|-------|---------------|
| 4X4 | 4×4 | >80% | **86.0% ± 7.2%** | [75.0%, 93.0%] | 4/5 |
| 6X6 | 6×6 | >20% | **68.5% ± 17.2%** | [51.0%, 92.0%] | 4/4 |
| 8X8 | 8×8 | >10% | **79.5% ± 8.7%** | [67.0%, 87.0%] | 4/4 |

---

## Interpretación

### Hipótesis H1: Success Rates Reproducibles

✅ **VALIDADA**: Las success rates son reproducibles en N=5 seeds.

### Hipótesis H2: Breakthrough 6×6 Reproducible

⚠️ **PARCIAL**: Breakthrough variable (ep -1 ± 0)

### Hipótesis H3: Transfer 6×6→8×8 Superior

❌ **RECHAZADA**: Transfer no claramente superior

---

## Conclusión

**Estado v10_viable**: 

✅ **BASELINE VALIDADA** - Curriculum reproducible, proceder con ablation/PGF

---

## Archivos Generados

- `multiseed_summary.csv` (datos completos)
- `multiseed_statistics.csv` (estadísticas)
- `boxplot_success_rates_5seeds.png`
- `phase2_breakthrough_histogram.png`
- `transfer_effectiveness_comparison.png`
