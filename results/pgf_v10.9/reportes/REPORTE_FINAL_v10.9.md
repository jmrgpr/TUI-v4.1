# REPORTE FINAL: v10.9 – Smoke test rápido (grid 6×6, max_steps=20)

**Fecha:** 2025-12-08  
**Datos:** `results/pgf_v10.9/resultados/smoke_test_v10.9_rapid/episodes.csv|summary.json`  
**Config:** grid_size=6, initial_balance=5.0, goal_reward=20.0, step_cost=-0.25, threshold_low=1.0, spawn_rate=0.4, max_steps=20, num_episodes=500.

---

## 1. Resultados (summary.json)
- `success_rate_total`: 0.0 (también 0.0 en últimos 100)  
- `reward_mean_total`: -28.33 (últimos 100: -28.87)  
- `steps_mean`: 19.73 (últimos 100: 19.96) sobre max_steps=20  
- `resources_mean`: 0.72 (últimos 100: 0.67)  
- `goal_rewards_applied`: 0  
- Gates: solo pasa epsilon (0.01 < 0.1); falla success (0%), reward negativo, recursos bajos y pasos al límite de max_steps.

---

## 2. Interpretación
- Ningún éxito en 500 episodios; el agente agota casi todos los pasos (≈20/20) sin alcanzar la meta.  
- Reward permanece negativo; recursos cercanos a umbral bajo (0.7).  
- Probablemente la combinación de max_steps=20, step_cost=-0.25 y economía no deja margen para explorar y alcanzar el goal.

---

## 3. Limitaciones
- Single smoke test (N=1); sin replicación ni variantes.  
- Solo métricas agregadas; no se inspeccionaron trayectorias ni episodios individuales.

---

## 4. Recomendaciones
- Aumentar max_steps o ajustar step_cost/goal_reward para permitir trayectorias viables.  
- Considerar curriculum/shaping/transfer para facilitar exploración en 6×6 con este presupuesto.  
- Repetir con más seeds y analizar episodios.csv para confirmar si hay intentos cercanos al goal.

