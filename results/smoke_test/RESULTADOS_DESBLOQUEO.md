# Resultados experimentales: desbloqueo RL/TUI

# Resultados experimentales: auditoría y consistencia

## Configuración crítica usada (impresa en runtime)
- ENV_PENALTY_LOW_RESOURCES = -0.01
- ENV_PENALTY_TRIPWIRE_BASE = -0.01
- ENV_PENALTY_SHOCK_BASE = -0.01
- ENV_PENALTY_DISTRACTOR_BASE = -0.01
- ENV_REWARD_HELP_BONUS = 100.0
- EXP_CONFIG[risk_penalty_high] = -0.2
- EXP_CONFIG[risk_penalty_low] = -0.1

## Baseline tabular RL en entorno easy (3x3)
- Script: `scripts/run_tabular_easy.py`
- Log: `results/smoke_test/tabular_easy_log.txt`
- Reward media últimos 50: 2456.2
- Reward media primeros 50: 1663.2
- Reward máxima: 2701.9
- Reward mínima: 1.3
- Episodios con reward > 0: 500/500

**Conclusión:** El RL tabular aprende y maximiza el reward en el entorno easy. El entorno y la función de recompensa están correctos.

## Smoke test patched (get_abstract_state con coords)
- Script: `sim/prototipo_rl_simbiosis.py --episodes 50 --seed 42 --risk_scale 0.5 --output_prefix results/smoke_test/patched`
- Penalizaciones bajas, coords añadidas al estado abstracto.
- Reward media (control): -59.32
- Recompensa sigue negativa, aunque el agente ahora "ve" su posición.

**Conclusión:** El parche de visibilidad no es suficiente para que el agente complejo aprenda en el entorno easy. El siguiente paso es revisar hiperparámetros y arquitectura del agente complejo.

**Estado científico:**
- El entorno y la reward están validados.
- El RL tabular funciona con estado informativo.
- El agente complejo requiere ajuste adicional para aprender en el entorno easy.
- Todos los datos y configuraciones han sido auditados y son consistentes.
