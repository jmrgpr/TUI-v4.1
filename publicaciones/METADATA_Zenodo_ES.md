# Metadata para Publicación en Zenodo

## Título

**Español (Principal)**:  
Función de Puerta Prudencial v3: Validación Multi-Semilla de un Mecanismo de Recompensa Sensible al Riesgo para Aprendizaje por Refuerzo

**Título corto**:  
PGF v3: Validación Multi-Semilla Sensible al Riesgo

---

## Autor

**Nombre completo**: Jose M Rivera Garcia  
**Afiliación**: Investigador Independiente  
**ORCID**: 0009-0000-3013-725X  
**Email**: jmrgpr@gmail.com  
**País**: Puerto Rico / Estados Unidos

---

## Resumen (máx. 250 palabras)

Presentamos una validación multi-semilla de la Función de Puerta Prudencial (PGF) v3, un mecanismo de modelado de recompensas diseñado para inducir comportamiento sensible al riesgo en agentes de aprendizaje por refuerzo en entornos estocásticos. En tres semillas aleatorias independientes en un grid de 5×5 con condiciones de riesgo moderado (risk_scale=1.5), PGF v3 logra una razón de desempeño promedio de 38.93% ± 0.59% respecto a un agente control sin sensibilidad al riesgo, con reproducibilidad estadística excepcional (coeficiente de variación = 1.52%). Esto representa una mejora acumulada de +131.7% sobre la implementación base inicial.

Aunque el ~39% pueda parecer bajo en términos absolutos, argumentamos que cuantifica el **impuesto de alineación**—el costo inherente de imponer restricciones de seguridad y sensibilidad al riesgo en entornos donde las estrategias óptimas maximizadoras de recompensa implican alta varianza. El agente control logra mayores recompensas medias pero con 192% de coeficiente de variación, mientras que el agente PGF mantiene 71% CV, demostrando el balance estabilidad-desempeño. En entornos simplificados (3×3), PGF permite superar al control (105%), validando la corrección funcional del mecanismo.

El análisis estadístico confirma mejora significativa sobre la iteración previa. Sin embargo, documentamos que ~70% de la señal PGF proviene de bonificaciones heurísticas y no de señales teóricas puras, indicando limitaciones impuestas por la complejidad. Este trabajo aporta datos empíricos al debate sobre seguridad-desempeño en IA y provee un marco reproducible para investigación en RL sensible al riesgo. Todo el código, datos y scripts de análisis son públicos.

**Palabras clave**: aprendizaje por refuerzo, modelado de recompensas, agentes sensibles al riesgo, impuesto de alineación, validación estadística, reproducibilidad multi-semilla, seguridad en IA, comportamiento prudencial

---

## Referencia BibTeX

@misc{rivera2025tui,
  title={Teoría Unificada de la Inteligencia v4.1: Un Marco Impulsado por el Riesgo},
  author={Rivera Garcia, Jose M},
  year={2025},
  doi={10.5281/zenodo.17702378},
  url={https://github.com/jmrgpr/TUI-v4.1},
  note={Versión 4.1}
}

---

## Nota sobre Asistencia de IA

 Nota: Se utilizaron herramientas basadas en IA únicamente como apoyo técnico (autocompletado, traducción, formato). Todas las decisiones científicas, análisis y conclusiones son responsabilidad exclusiva del autor. El uso de IA no influyó en la integridad científica ni en la originalidad del trabajo.
