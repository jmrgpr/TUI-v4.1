# To Do: Mejoras y Publicación TUI-v4.1 Fase 2

## Inmediato
- **Taggear release v0.1 y agregar CI/CD**
  - Crear un release v0.1 en GitHub y agregar workflow YAML de GitHub Actions para ejecutar tests automáticos en cada push/PR.
- **Pinnear dependencias y agregar Dockerfile**
  - Actualizar requirements.txt con versiones fijas (e.g., torch==2.1.0) y crear Dockerfile para reproducibilidad extrema.
- **Subir PDF teórico y notebook quickstart**
  - Agregar el paper completo en docs/ y crear un notebook quickstart en notebooks/ para onboarding y demostración rápida.

## Semana
- **Implementar script stats.py para ANOVA y p-values**
  - Crear script en results/ para análisis estadístico formal (ANOVA, p-values) sobre los resultados globales.
- **Comparar con baseline SOTA y discutir resultados**
  - Implementar y comparar al menos un algoritmo de referencia (PPO, A2C) y discutir los resultados frente a los agentes actuales.
- **Unificar idioma y mejorar narrativa Control**
  - Revisar y unificar idioma en comentarios/prints y mejorar la explicación sobre el agente Control en README/código.

## Mes
- **Escalar el experimento y agregar demo interactiva**
  - Aumentar el número de episodios/agentes, agregar demo interactiva (Streamlit/HuggingFace Spaces) y badges dinámicos (coverage, runs).

---

Este To Do resume las recomendaciones integradas de las revisiones Grok y Gemini Pro. Prioriza acciones para fortalecer la publicación y el impacto internacional del proyecto.