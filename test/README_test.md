# Tests para TUI v4.1 Toy Model — RL Symbiosis

Esta carpeta contiene pruebas unitarias y de integración para el simulador TUI v4.1 Toy Model — RL Symbiosis.

## Objetivo
- Proteger la lógica científica y reproducibilidad del toy model.
- Detectar rápidamente errores al modificar el código.
- Validar métricas, comparación de agentes, exportación y visualizaciones.
- Facilitar colaboración y extensión segura.

## Estructura sugerida
- `test_agent.py`: Pruebas de inicialización y comportamiento de agentes (Control, Simbiosis, DQN).
- `test_experiment.py`: Pruebas de ejecución de experimentos, logging y comparación.
- `test_visualizaciones.py`: Pruebas de generación de gráficos y exportación.
- `test_utils.py`: Pruebas de utilidades científicas (intervalos de confianza, t-test, ANOVA).
- `test_gui.py`: Pruebas básicas de la GUI Streamlit (opcional).

## Ejecución
```bash
pytest test/
```

## Recomendaciones
- Mantener los tests actualizados tras cada cambio relevante.
- Documentar cada test con docstring bilingüe.
- Priorizar pruebas científicas y de reproducibilidad.

---
Todos los tests deben respetar la licencia CC BY-NC-SA 4.0 y la filosofía de ciencia abierta del proyecto.
