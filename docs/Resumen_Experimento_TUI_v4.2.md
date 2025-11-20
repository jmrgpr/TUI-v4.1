# Resumen Breve del Experimento TUI v4.2

## Descripción del entorno experimental
El entorno utilizado es un "toy RL" diseñado para evaluar la hipótesis de que la inteligencia operativa (I_op) es función del riesgo físico acumulado. El agente interactúa en episodios donde debe maximizar recompensa y minimizar exposición a riesgos (tripwires), simulando tensiones entre optimización y prudencia.

## Definición formal de PGF (Prudential Gradient of Failure)
PGF es la métrica principal para evaluar alineación prudencial. Se define como:

PGF = (n_tripwires / n_episodios) × factor_riesgo

Donde n_tripwires es el número de eventos de riesgo activados y factor_riesgo pondera la severidad del entorno. Un PGF negativo indica fallas prudenciales; valores cercanos a cero sugieren mejor alineación.

## Métricas reportadas en results/stats.py
- **Recompensa media por agente y condición**
- **PGF medio por agente y condición**
- **ANOVA Two-Way** para comparar diferencias significativas entre agentes y condiciones de riesgo
- **Tukey HSD** para análisis post-hoc de diferencias

## Limitaciones y contexto experimental
- Solo se utiliza PPO como baseline SOTA
- Una semilla por condición experimental
- El entorno es simplificado y no representa benchmarks complejos
- Los resultados deben interpretarse como evidencia preliminar, no validación definitiva

## Reproducibilidad
- Todos los scripts y datos están disponibles en el repositorio
- Instrucciones para replicación con Conda y venv/pip en el README
- Dataset y teoría citables vía Zenodo (DOIs incluidos)

## Contacto
José M. Rivera García — jmrgpr@gmail.com

---
Este resumen está orientado a revisión rápida por pares y acompaña los archivos principales del repositorio TUI v4.2.
