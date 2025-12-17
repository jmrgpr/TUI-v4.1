# REPORTE_PUBLICACION_F1_v11.md (DEPRECATED)

Este documento se conserva solo como **auditoria historica**. Fue redactado antes del cierre reproducible/canonico de la serie v11 y contiene claims/estadistica no alineados con los artefactos canonicos actuales.

Para la version vigente (serie v11 completa), usar:
- `results/v11/PUBLICACION_SERIE_V11.md`
- `results/v11/INFORME_CIENTIFICO_SERIE_V11.md`
- `results/v11/data/stats_report_v11.md`
- `results/v11/CANONICAL_DATASET_v11.md`

---

## Resumen Ejecutivo
Este trabajo presenta el experimento F1_highrisk v11, diseñado para evaluar la Teoría Unificada de Inteligencia (TUI/Simbiosis) bajo condiciones de alto riesgo. Se compara el desempeño de Simbiosis frente a Control clásico y DQN-Control en términos de recompensa, robustez, flexibilidad, riesgo efectivo y PGF.

## 1. Introducción
La TUI/PGF propone una arquitectura de inteligencia artificial alineada, robusta y segura. El objetivo de F1_highrisk es validar la teoría en entornos adversos, respondiendo a críticas de reproducibilidad y trazabilidad.

## 2. Preregistro y Diseño Experimental
- Protocolo: v11
- Preregistro: `PREREGISTRO_F1_v11.md`
- Grids: 8×8 y 16×16
- Seeds: 42, 101, 13, 7, 99
- Agentes: control, simbiosis, dqn_control
- Episodios: 200 por configuración
- Parámetros: `risk_scale = 1.2`, `risk_level = high`, `pgf_mix = 0.2`
- Sin red_team ni ataques adversariales

## 3. Ejecución Experimental
- Piloto GO/NO-GO: seed 42, 50 episodios, grid 8×8, criterio GO cumplido.
- Batch principal: 5 seeds, 200 episodios por configuración, todos los runs cumplen criterios.
- Comandos, scripts y parámetros documentados en `metadata.json`.

## 4. Resultados Clave
- Simbiosis logra mayor recompensa y menor riesgo efectivo que Control y DQN-Control.
- Longitudes de episodio: Simbiosis siempre alcanza el máximo (30/30), Control y DQN-Control presentan mínimos más bajos pero medias cercanas a 30.
- Flexibilidad y robustez: similares entre agentes, robustez media ≈ 1.
- Riesgo efectivo: Simbiosis reduce el riesgo medio frente a Control (p < 0.05, Bonferroni).
- PGF bruto: Simbiosis comparable a Control.
- Tripwires y surprise: tasas bajas, sin colapsos ni anomalías.

## 5. Validación Estadística
- Tests de normalidad (Shapiro), comparación de medias (Welch/Mann–Whitney), intervalos de confianza, tamaño de efecto (Cohen’s d), corrección de Bonferroni.
- Tablas exportadas en `analysis/` para auditoría.

## 6. Trazabilidad y Reproducibilidad
- Carpeta estructurada por grid, agente y seed.
- Preregistro, README y metadata detallados.
- Scripts y comandos archivados.
- Resultados exportados en CSV y notebook.

## 7. Discusión y Respuestas a Peer Review
- El diseño responde a críticas previas: trazabilidad total, preregistro, validación estadística, anexo técnico de métricas.
- Limitaciones: no se incluye red_team ni ataques adversariales (reservados para F2).
- Propuesta de F2: diseñar ataques explícitos y comparar resiliencia de TUI/Simbiosis.

## 8. Conclusión
La TUI/Simbiosis demuestra ventajas claras en recompensa y riesgo efectivo bajo condiciones adversas, sin sacrificar robustez ni seguridad. El experimento es reproducible, trazable y cumple los estándares científicos.

## 9. Próximos Pasos
- Ejecutar F2 (red team y ataques adversariales).
- Meta-análisis y comparación con otros experimentos.
- Publicar resultados extendidos y responder a nuevos peer reviews.

## 10. Anexos
- Preregistro completo
- Metadata y comandos
- Tablas de resultados y estadística
- Anexo técnico de métricas
- Glosario y diagramas

---

**Contacto:** jmrgpr | Proyecto TUI-v4.1 | 11 de diciembre de 2025
