# REPORTE_ABLATION_v10.md

## Resumen Ejecutivo
Este reporte presenta un análisis estadístico exhaustivo de la ablation FASE 1 (N=5 seeds) para TUI-v4.1, comparando las configuraciones: Curriculum (A), Direct 8×8 (B), Inverso (C) y Only 6×6 (D). Se incluyen promedios, desviaciones estándar, rangos, mecanismos de éxito/fallo y recomendaciones prácticas.

## Configuraciones Evaluadas
- **A:** Curriculum 4→6→8 (baseline)
- **B:** Direct 8×8 (sin curriculum)
- **C:** Inverso 8→6→4
- **D:** Only 6×6

## Resultados por Seed
| Config | Seed | Success Total | Success Last 100 | Primer Éxito | Gate | Gate Pass | Episodios |
|--------|------|--------------|------------------|--------------|------|-----------|-----------|
| B | 13   | 65.9% | 98% | 199 | 10 | Sí | 1500 |
| B | 42   | 64.3% | 95% | 2   | 10 | Sí | 1500 |
| B | 101  | 71.3% | 60% | 3   | 10 | Sí | 1500 |
| B | 2025 | 74.4% | 85% | 10  | 10 | Sí | 1500 |
| B | 9999 | 76.3% | 90% | 26  | 10 | Sí | 1500 |
| C | 13   | 0%    | 0%  | -   | 10 | No | 1000 |
| C | 42   | 55.2% | 54% | 64  | 10 | Sí | 1000 |
| C | 101  | 53.6% | 46% | 13  | 10 | Sí | 1000 |
| C | 2025 | 58.3% | 95% | 46  | 10 | Sí | 1000 |
| C | 9999 | 23.0% | 83% | 714 | 10 | Sí | 1000 |
| D | 13   | 62.9% | 54% | 21  | 20 | Sí | 1000 |
| D | 42   | 58.9% | 83% | 10  | 20 | Sí | 1000 |
| D | 101  | 54.9% | 79% | 2   | 20 | Sí | 1000 |
| D | 2025 | 68.0% | 88% | 29  | 20 | Sí | 1000 |
| D | 9999 | 62.1% | 87% | 23  | 20 | Sí | 1000 |
| A | 42   | 61.3% | 87% | 1   | 10 | Sí | 1000 |

## Estadísticas Consolidadas
| Config | Success Last 100 (mean±std) | Primer Éxito (mean±std) | Gate Pass | Fallos |
|--------|-----------------------------|------------------------|-----------|--------|
| B | 85.6% ± 15.2% | 48 ± 77 | 5/5 | 0 |
| C | 55.6% ± 37.8% | 167 ± 273 | 4/5 | 1 |
| D | 78.2% ± 13.6% | 17 ± 11 | 5/5 | 0 |
| A | 87%* | 1* | 1/1 | 0 |

## Ranking y Hallazgos Principales
1. **Config B (Direct 8×8)**: Mejor balance rendimiento/costo, 85.6% success, 0 fallos, eficiente y simple.
2. **Config D (Only 6×6)**: Alternativa estable (78.2%, std=13.6%), mejor ratio success/episodio.
3. **Config C (Inverso)**: Inestable, 1/5 seeds con fallo total, varianza inaceptable.
4. **Config A (Curriculum)**: Baseline robusto, pero no superior a B en eficiencia.

## Interpretación Científica
- **Max steps** es el factor crítico: 70 steps (B) = éxito, 42 steps (C) = fallo.
- **Curriculum** no es necesario para alto desempeño, pero sí para robustez máxima.
- **Orden del curriculum** importa: inverso es inestable.
- **Only 6×6** es viable para prototipado rápido y máxima estabilidad.

## Recomendaciones Prácticas
- **Producción**: Direct 8×8 (B) con max_steps=70.
- **Prototipado/Estabilidad**: Only 6×6 (D).
- **Evitar**: Curriculum inverso (C) por alta tasa de fallo.

## Tablas y Gráficos
- Ver `plots/FASE1/` para PNGs comparativos.
- CSVs crudos y scripts en `results/pgf_v10_ablation/`.

---

*Este reporte sigue el formato y profundidad sugeridos para análisis científico y toma de decisiones.*
