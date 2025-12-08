# REPORTE FINAL: v10.8 – Smoke test goal-oriented (grid 6×6)

**Fecha:** 2025-12-08  
**Datos:** `results/pgf_v10.8/resultados/smoke_test_v10.8_goal_oriented/episodes.csv|summary.json`  
**Config:** grid_size=6, balance=5.0, goal_reward=10.0, step_cost=-0.15, spawn_rate=0.4, num_episodes=1000, epsilon_decay=0.9995.

---

## 1. Resultados (summary.json)
- `success_rate_total`: 0.0  
- `success_rate_last_100`: 0.0  
- `reward_mean_total`: -32.31  
- `reward_mean_last_100`: -32.21  
- `resources_mean_total`: 0.984 (last_100: 0.94)  
- `goal_rewards_applied`: 0  
- Gates: pasa epsilon (0.01 < 0.1), falla success (0%), reward negativo y recursos marginales.

---

## 2. Interpretación
- El agente no alcanza ninguna meta en 1000 episodios; reward permanece negativo (~-32).  
- Aunque epsilon converge a 0.01, no hay señal de éxito → o el entorno es demasiado exigente con esta economía o la recompensa es insuficiente.  
- Recursos bajos (~1.0) sugieren que el agente apenas mantiene autonomía; sin goal_reward aplicado, no logra avanzar.

---

## 3. Limitaciones
- Single run (smoke test) sin replicación.  
- Solo métrica agregada; no se analizaron curvas ni eventos detallados.  
- No se ajustaron hyperparámetros ni shaping/reward_extra.

---

## 4. Recomendaciones
- Incrementar goal_reward o ajustar balance/step_cost para ofrecer señal de éxito.  
- Añadir shaping/reward_extra o curriculum/transfer para facilitar exploración en 6×6.  
- Repetir con más seeds y analizar las curvas de episodios (episodes.csv) para ver si hay progreso parcial.

