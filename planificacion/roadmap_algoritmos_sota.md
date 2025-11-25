# Reporte de decisión sobre integración de algoritmos SOTA antes del Experimento 2

1. **Objetivo y contexto**

El Experimento 2 busca comparar TUI/PGF puro y variantes actuales (control, dqn_control, simbiosis, PPO/A2C/DQN) en el entorno gridworld. El pipeline y la infraestructura están listos para estos agentes, con alta reproducibilidad y cobertura.

2. **Evaluación de integrar nuevos algoritmos (SAC, TD3, DDPG, Rainbow, etc.)**

**Ventajas:**
- Permite una comparativa SOTA más completa y alineada con la literatura RL moderna.
- Fortalece la publicación y la revisión por pares.

**Desventajas:**
- Requiere integrar nuevas librerías, adaptar el entorno (posiblemente a continuo), crear wrappers y runners, y validar outputs.
- Puede introducir inestabilidad, retrasos y trabajo extra en reproducibilidad y testing.
- El entorno actual no está optimizado para algoritmos continuos/distribuidos.

3. **Recomendación combinada**

- Si el objetivo es cerrar el Experimento 2 pronto y validar TUI/PGF frente a los baselines actuales, no conviene implementar los algoritmos faltantes ahora.
- Ejecuta Exp2 con los agentes ya listos (control, dqn_control, simbiosis, PPO/A2C/DQN).
- Documenta explícitamente en el README y reporte qué algoritmos SOTA faltan y por qué, como trabajo futuro.
- Si tienes tiempo y buscas un benchmark más amplio, puedes añadir 1–2 algoritmos (SAC, TD3) como extensión, pero planifica el impacto en reproducibilidad y validación.
- La integración de nuevos algoritmos puede quedar para Experimento 3 o como línea de trabajo futuro, asegurando que la comparativa actual sea clara y reproducible.

4. **Acción recomendada**

- Corre el Experimento 2 con los agentes actuales.
- Añade una sección en la documentación y reporte indicando las ausencias y el plan de integración futura.
- Prioriza la estabilidad, reproducibilidad y cierre del experimento antes de ampliar el benchmark.
