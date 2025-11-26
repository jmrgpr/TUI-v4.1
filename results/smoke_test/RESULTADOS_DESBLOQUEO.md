# Resultados experimentales: desbloqueo RL/TUI

## Baseline tabular RL en entorno easy (3x3)
- Script: `scripts/run_tabular_easy.py`
- Episodios: 500
- Reward media últimos 50: 2456.2
- Reward media primeros 50: 1663.2
- Reward máxima: 2701.9
- Reward mínima: 1.3
- Episodios con reward > 0: 500/500

**Conclusión:** El RL tabular aprende y maximiza el reward en el entorno easy. El entorno y la función de recompensa están correctos.

## Smoke test con parche de visibilidad (get_abstract_state)
- Script: `sim/prototipo_rl_simbiosis.py --episodes 50 --seed 42 --risk_scale 0.5 --output_prefix results/smoke_test/patched`
- Penalizaciones bajas, coords añadidas al estado abstracto.
- Reward media (control): -59.32
- Recompensa sigue negativa, aunque el agente ahora "ve" su posición.

**Conclusión:** El parche de visibilidad no es suficiente para que el agente complejo aprenda en el entorno easy. El siguiente paso es revisar hiperparámetros y arquitectura del agente complejo.

**Estado científico:**
- El entorno y la reward están validados.
- El RL tabular funciona con estado informativo.
- El agente complejo requiere ajuste adicional para aprender en el entorno easy.
