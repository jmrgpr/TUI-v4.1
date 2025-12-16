# F2_redteam – Experimento Red Team y Ataques Adversariales (v11)

## Descripción
Este experimento corresponde a la fase F2 del plan v11, centrado en evaluar la resiliencia de TUI/Simbiosis, Control clásico y DQN-Control frente a ataques adversariales explícitos (red team) bajo condiciones de riesgo alto.

## Objetivos
- Validar la robustez y alineación de TUI/Simbiosis ante ataques de reward hacking, distributional shift y gaming de métricas.
- Comparar el desempeño de los tres agentes bajo escenarios adversariales.
- Documentar y analizar el impacto de los ataques en las métricas clave.

## Estructura de carpetas
- `raw/`: Resultados crudos por configuración (JSON y CSV).
- `analysis/`: Notebooks, scripts y reportes de análisis.
- `grid8/riskhigh/{control,simbiosis,dqn_control}/`: Resultados organizados por agente, grid y seed.
- `grid16/riskhigh/{control,simbiosis,dqn_control}/`: Idem para grid 16x16.

## Referencias
- Preregistro: `PREREGISTRO_F2_v11.md`
- Protocolo: `MEGA_PLAN_EVALUACION_v11.md`
- Scripts: `sim/prototipo_rl_simbiosis.py`, `sim/runner.py`

## Estado
- [ ] Preregistro completado
- [ ] Ejecución experimental
- [ ] Análisis y reporte
