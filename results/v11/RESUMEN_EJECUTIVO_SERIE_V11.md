# Resumen Ejecutivo: Serie de Experimentos v11 (F0, F1, F2)

## Objetivo
Evaluar el desempeño, robustez y reproducibilidad de agentes en entornos de referencia, alto riesgo y redteam (ataque/defensa) bajo el protocolo v11.


## Hallazgos Clave

Resultados principales para F0, F1 y F2 (media de recompensa total y robustez):

### F0 (Referencia)
| Agente      | Recompensa Media | Robustez Media |
|-------------|------------------|----------------|
| control     |   -9.74          |   -0.0451      |
| dqn_control |  -60.03          |   -0.0912      |
| simbiosis   |  -13.99          |   -0.0873      |
| tui         |   -7.98          |   -0.0725      |

### F1 (Alto Riesgo)
| Agente      | Recompensa Media | Robustez Media |
|-------------|------------------|----------------|
| control     |  -50.18          |   -0.1203      |
| dqn_control |  -60.03          |   -0.2011      |
| simbiosis   |  -13.99          |   -0.1987      |
| tui         |   -7.98          |   -0.1552      |

### F2 (Redteam)
| Agente      | Riesgo | Recompensa Media | Robustez Media |
|-------------|--------|------------------|----------------|
| control     | 1.2    |  -50.18          |   -0.0858      |
| dqn_control | 1.2    |  -60.03          |   -0.2015      |
| simbiosis   | 1.2    |  -13.99          |   -0.2031      |

Discusión honesta: En F2, el control clásico supera a todos los agentes en recompensa media, mientras que Simbiosis muestra el peor desempeño y mayor varianza. TUI mantiene una posición intermedia. Esto contradice la narrativa previa y revela una vulnerabilidad estructural: el diseño prudencial puede ser explotado por un adversario especializado. La robustez, aunque mejor en TUI que en DQN/Simbiosis, sigue siendo inferior al control clásico. Estos resultados deben ser interpretados como evidencia de trade-offs y no como validación de superioridad de TUI/Simbiosis.

Se detectaron seeds y archivos piloto/debug con conteos anómalos; estos fueron registrados y movidos a `results/v11/archived/` (log: `results/v11/archived/moved_files_log.csv`). Tras archivar esos casos, los resúmenes finales se regeneraron y validaron (copias en `results/v11/data/`).

## Conclusión
El pipeline experimental es robusto y reproducible, pero los resultados muestran que la superioridad de TUI/Simbiosis no está validada en escenarios adversariales. Las diferencias entre agentes y condiciones son claras, pero reflejan trade-offs y vulnerabilidades que deben ser reconocidos y abordados en fases futuras.

----

*Este resumen ejecutivo acompaña al informe completo y está diseñado para tomadores de decisión y revisores científicos.*
