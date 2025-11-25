# Plan de Desarrollo Futuro: TUI-v4.1

## 1. Estado Actual
- El entorno implementado es Gridworld discreto, sin soporte para entornos continuos (MuJoCo, etc.).
- El pipeline real de experimentos está en `scripts/run_full_experiment.py` y `scripts/consolidate_results.py`.
- La suite de tests pasa completa, con cobertura cercana al 99%. Los huecos principales están en `sim/prototipo_rl_simbiosis.py` y `sim/runner.py`.
- No existe `coverage_report.txt`, `run_fase2.py`, `run_sota_comparison.py`, ni `Dockerfile` en el repo actual.
- El módulo global de configuración es `sim/config.py`, pero no se han detectado problemas de race conditions dado el uso de procesos separados.
- La documentación es bilingüe y clara, pero faltan definiciones matemáticas formales de métricas clave.
- El roadmap de algoritmos SOTA está documentado, pero la integración actual es limitada (solo PPO/A2C/DQN en Gridworld).

## 2. Recomendaciones Útiles

### Corto Plazo (antes de Exp2)
- No realizar refactors grandes antes de correr Exp2. Priorizar la ejecución y consolidación de resultados.
- Documentar claramente las limitaciones actuales: solo Gridworld, sin SOTA adicionales, sin soporte para entornos continuos.
- Mantener la suite de tests y cobertura, intentando cubrir los huecos en `prototipo_rl_simbiosis.py` y `runner.py` si es posible.
- Solicitar peer review basado en artefactos presentes: ejecución de tests, revisión de scripts y documentación real.

### Medio Plazo (tras Exp2)
- Refactorizar `sim/prototipo_rl_simbiosis.py` para separar parser, ejecución y generación de gráficos, solo si se planea modificar el código.
- Crear un documento Markdown en `docs/` (ej. `METRICS_DEFINITION.md`) con definiciones matemáticas de las métricas principales (PGF_Bruto, PGF_Costo, etc.).
- Mejorar la documentación CITATION.cff para incluir versión y commit hash del software.
- Considerar la creación de un Dockerfile para facilitar la reproducibilidad en diferentes sistemas.

### Largo Plazo (escalabilidad y colaboración)
- Si se planea salir del Gridworld, definir una clase base abstracta para el entorno (ej. `BaseTUIEnv`) que permita inyectar dinámicas físicas distintas.
- Ampliar el roadmap de algoritmos SOTA y planificar la integración de nuevos métodos (SAC, TD3, DDPG, Rainbow, etc.) solo si hay recursos y necesidad científica.
- Mantener la documentación bilingüe y actualizada, facilitando la colaboración internacional.

## 3. Acciones Prioritarias
- Ejecutar Exp2 con los scripts actuales y consolidar resultados.
- Documentar las limitaciones y el estado real del repo antes de cualquier revisión externa.
- Revisar y actualizar el roadmap en función de los resultados y necesidades futuras.


Este plan integra recomendaciones útiles y observaciones técnicas adaptadas al estado real del repositorio. Se prioriza la ejecución y documentación sobre refactorizaciones especulativas, asegurando que el desarrollo futuro sea pragmático y alineado con los recursos y objetivos científicos.