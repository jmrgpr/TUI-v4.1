# REPORTE FINAL: Experimento v10.1 – Adaptive Curriculum 8×8 (economía calibrada)

**Fecha:** 2025-12-08  
**Preregistro:** results/pgf_v10.1/PREREGISTRO_v10.1.md  
**Datos:** results/pgf_v10.1/resultados/*.csv|*.json  
**Grupos:** AdaptiveCurriculum vs ControlS0 (s=0.0)

---

## 1. Diseño experimental
- Entorno: `ResourceDensityEnv`, grid 8×8, economía v10 calibrada (balance=5.0 según métricas).
- Agente: DQN (parámetros serie 10.x), epsilon-greedy, replay.
- Grupos y episodios:
  - AdaptiveCurriculum: 2 seeds (42, 123), ~100–104 episodios por run (curriculum adaptativo, escalas de shaping 0→0.25→0.5→0.75, 4 transiciones documentadas en `curriculum_info`).
  - ControlS0: 2 seeds (42, 123), 400 episodios por run, shaping fijo s=0.0.
- Métricas: del campo `final_window` de los JSON (última ventana): `success_rate`, `mean_reward_env`, `mean_tripwires`.
- Limitación: N=2 por grupo y duración desigual (100 vs 400 episodios); resultados indicativos, no concluyentes.

---

## 2. Resultados (final_window, últimos episodios)
Valores por seed:
```
group               seed  success  reward   tripwires  n_episodes
AdaptiveCurriculum    42    1.00   126.43      0.00         100
AdaptiveCurriculum   123    1.00   125.83      0.00         104
ControlS0             42    1.00   130.51      0.00         400
ControlS0            123    1.00   131.86      0.00         400
```
Agregados (media ± sd):
- AdaptiveCurriculum (N=2): success = 1.00 ± 0.00; reward = 126.1 ± 0.4; tripwires = 0.00 ± 0.00.
- ControlS0 (N=2): success = 1.00 ± 0.00; reward = 131.2 ± 0.95; tripwires = 0.00 ± 0.00.

---

## 3. Interpretación
- Ambos grupos alcanzan 100% de éxito en la ventana final; el entorno es poco exigente con la economía usada (balance 5.0).
- ControlS0 obtiene reward final algo mayor (~131 vs ~126), pero con N=2 y diferente número de episodios no se puede concluir robustamente.
- Tripwires finales son 0 en ambos grupos; no hay presión de seguridad medible en esta ventana.
- Conclusión: el escenario es trivial; los resultados no permiten evaluar el beneficio del curriculum adaptativo frente al control.

---

## 4. Limitaciones
- N=2 por grupo y duración desigual (100 vs 400 episodios) → no hay potencia estadística ni comparabilidad directa.
- Sin análisis de curvas de aprendizaje completas (solo ventana final).
- No se evaluó sensibilidad a seeds ni variación de economía/presión.

---

## 5. Recomendaciones
- Para evaluar curriculum adaptativo en 8×8 con economía calibrada, usar N≥5 y misma duración por grupo; analizar curvas completas (no solo ventana final).
- Aumentar presión del entorno (menor balance, mayor costo) si se busca discriminar efectos del curriculum.

---

## 6. Archivos de referencia
- Datos crudos: `results/pgf_v10.1/resultados/exp10.1_*_episodes.csv|metrics.json`
- Preregistro: `results/pgf_v10.1/PREREGISTRO_v10.1.md`
- Tracking: `results/pgf_v10.1/TRACKING_v10.1.md`, `execution.log`

