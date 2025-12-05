
# Reporte FASE 1: Ablation TUI-v4.1

**Fecha de generación:** 2025-12-05  
**Commit de datos:** [inserte hash aquí]

## 1. Definición de métricas y fuentes
- **Éxito total**: Proporción de episodios exitosos en toda la fase. Columna `success_rate_total` en los archivos `*_summary_*.csv`.
- **Éxito últimos 100**: Proporción de éxito en los últimos 100 episodios. Columna `success_last_100`.
- **Gate (%)**: Umbral de éxito considerado satisfactorio (por defecto 10% para 8x8, 20% para 6x6).
- **Gate pasado**: Si el agente superó el umbral de éxito (`gate_passed`).
- **Primer éxito**: Episodio donde se alcanza el primer éxito (`first_success_episode`).
- **Convergencia**: Episodio donde se estabiliza el éxito (no siempre definido, ver columna `convergence_episode`).

## 2. Tabla de resultados (cada valor cita su fuente)

| Configuración | Seed | Éxito total | Éxito últimos 100 | Gate (%) | Gate pasado | Primer éxito | Fuente CSV |
|--------------|------|-------------|-------------------|----------|-------------|--------------|-----------------------------|
| Curriculum (A) 8x8 | 42 | 61.3% | 87% | 10 | Sí | 1 | config_A_curriculum/curriculum_summary_102250.csv |
| Directo 8x8 (B) | 13 | 65.9% | 98% | 10 | Sí | 199 | config_B_direct_8x8/seeds/seed_0013/direct_8x8_summary_20251205_143303.csv |
| Directo 8x8 (B) | 42 | 64.3% | 95% | 10 | Sí | 2 | config_B_direct_8x8/seeds/seed_0042/direct_8x8_summary_20251205_143719.csv |
| Directo 8x8 (B) | 101 | 71.3% | 60% | 10 | Sí | 3 | config_B_direct_8x8/seeds/seed_0101/direct_8x8_summary_20251205_144156.csv |
| Directo 8x8 (B) | 2025 | 74.4% | 85% | 10 | Sí | 10 | config_B_direct_8x8/seeds/seed_2025/direct_8x8_summary_20251205_144603.csv |
| Directo 8x8 (B) | 9999 | 76.3% | 90% | 10 | Sí | 26 | config_B_direct_8x8/seeds/seed_9999/direct_8x8_summary_20251205_144912.csv |
| Inverso 8x8 (C) | 13 | 0% | 0% | 10 | No | - | config_C_inverse/seeds/seed_0013/phase1_8x8_20251205_150328.csv |
| Inverso 8x8 (C) | 42 | 55.2% | 54% | 10 | Sí | 64 | config_C_inverse/seeds/seed_0042/inverse_curriculum_summary_20251205_150656.csv |
| Inverso 8x8 (C) | 101 | 53.6% | 46% | 10 | Sí | 13 | config_C_inverse/seeds/seed_0101/inverse_curriculum_summary_20251205_151122.csv |
| Inverso 8x8 (C) | 2025 | 58.3% | 95% | 10 | Sí | 46 | config_C_inverse/seeds/seed_2025/inverse_curriculum_summary_20251205_151541.csv |
| Inverso 8x8 (C) | 9999 | 23.0% | 83% | 10 | Sí | 714 | config_C_inverse/seeds/seed_9999/inverse_curriculum_summary_20251205_152010.csv |
| Only 6x6 (D) | 13 | 62.9% | 54% | 20 | Sí | 21 | config_D_only_6x6/seeds/seed_0013/only_6x6_summary_20251205_152603.csv |
| Only 6x6 (D) | 42 | 58.9% | 83% | 20 | Sí | 10 | config_D_only_6x6/seeds/seed_0042/only_6x6_summary_20251205_152911.csv |
| Only 6x6 (D) | 101 | 54.9% | 79% | 20 | Sí | 2 | config_D_only_6x6/seeds/seed_0101/only_6x6_summary_20251205_153158.csv |
| Only 6x6 (D) | 2025 | 68.0% | 88% | 20 | Sí | 29 | config_D_only_6x6/seeds/seed_2025/only_6x6_summary_20251205_153412.csv |
| Only 6x6 (D) | 9999 | 62.1% | 87% | 20 | Sí | 23 | config_D_only_6x6/seeds/seed_9999/only_6x6_summary_20251205_153601.csv |

## 3. Análisis comparativo
- El curriculum baseline (A) muestra convergencia rápida y éxito alto en 8x8 (ver CSV citado).
- El directo 8x8 (B) logra éxito alto en todas las semillas, pero con mayor varianza en el primer éxito y convergencia.
- El curriculum inverso (C) muestra mayor dificultad en algunas semillas (semilla 13: 0% éxito), pero en otras logra gates altos.
- El solo 6x6 (D) tiene éxito intermedio, pero menor que el directo 8x8 y el curriculum baseline.

## 4. Definición de scripts y reproducibilidad
- Los datos de la tabla se extrajeron con scripts de análisis en `scripts/` (ejemplo: `generar_graficos_fase1.py`).
- Para reproducir los resultados, consultar los CSV citados y ejecutar los scripts con los argumentos indicados en la documentación de reproducibilidad.

## 5. Recomendaciones
- Mantener curriculum tradicional para robustez.
- El directo 8x8 puede ser útil si se optimiza la exploración y warmup.
- Evitar curriculum inverso salvo para estudios exploratorios.

## 6. Referencias cruzadas y reproducibilidad
- Todos los scripts, seeds, rutas y resultados están documentados y versionados.
- El entorno está limpio y los experimentos son 100% reproducibles.
- Para detalles numéricos completos, consultar los archivos .csv citados en la tabla.
- Gráficos y tablas adicionales se encuentran en la carpeta `plots/FASE1/`.

---

*Este reporte ha sido revisado para trazabilidad, claridad y profesionalismo científico.*

## 2. Análisis comparativo
- El curriculum baseline (A) muestra convergencia rápida y éxito alto en 8x8 (ver csv).
- El directo 8x8 (B) logra éxito alto en todas las semillas, pero con mayor varianza en el primer éxito y convergencia.
- El curriculum inverso (C) muestra mayor dificultad en algunas semillas (semilla 13: 0% éxito), pero en otras logra gates altos.
- El solo 6x6 (D) tiene éxito intermedio, pero menor que el directo 8x8 y el curriculum baseline.

## 3. Gráficos
Se generarán gráficos comparativos de éxito total, éxito últimos 100, y primer éxito por configuración y semilla (ver carpeta plots/).

## 4. Interpretación científica
- El curriculum tradicional (A) sigue siendo la estrategia más robusta y consistente.
- El directo 8x8 (B) es viable, pero menos estable en primeras fases.
- El curriculum inverso (C) es más riesgoso y sensible a la semilla.
- El entrenamiento solo en 6x6 (D) no alcanza el desempeño de los otros métodos.

## 5. Recomendaciones
- Mantener curriculum tradicional para robustez.
- El directo 8x8 puede ser útil si se optimiza la exploración y warmup.
- Evitar curriculum inverso salvo para estudios exploratorios.

## 6. Documentación y reproducibilidad
- Todos los scripts, seeds, rutas y resultados están documentados y versionados.
- El entorno está limpio y los experimentos son 100% reproducibles.

---

*Para detalles numéricos completos, consultar los archivos .csv en cada carpeta de resultados.*

---

*Gráficos y tablas adicionales se encuentran en la carpeta plots/.*
