# REPORTE FINAL: Experimento v10.2 – Adaptive Curriculum 8×8 (economía ajustada)

**Fecha:** 2025-12-08  
**Preregistro:** results/pgf_v10.2/PREREGISTRO_v10.2.md (si aplica)  
**Datos:** results/pgf_v10.2/resultados/*.csv|*.json  
**Grupos:** AdaptiveCurriculum vs ControlS0 (s=0.0)

---

## 1. Diseño experimental
- Entorno: `ResourceDensityEnv`, grid 8×8, economía ajustada (balance ~5.0 según configs).
- Agente: DQN serie 10.x; epsilon-greedy, replay.
- Grupos y episodios observados:
  - AdaptiveCurriculum: 2 seeds (42: 170 eps; 123: 78 eps), curriculum adaptativo con escalas de shaping (transiciones en `curriculum_info` de los JSON).
  - ControlS0: 2 seeds (42, 123), 400 episodios por run, shaping s=0.0.
- Métricas usadas: `success_rate_final`, `mean_reward_env_final`, `mean_tripwires_final` del campo `final_window` de cada JSON.
- Limitación: N=2 por grupo y distinto número de episodios entre grupos → resultados indicativos, no concluyentes.

---

## 2. Resultados (ventana final)
Valores por seed:
```
group               seed  success  reward   tripwires  n_episodes
AdaptiveCurriculum    42    0.14   68.42      1.46         170
AdaptiveCurriculum   123    0.02   76.14      0.32          78
ControlS0             42    1.00  109.35      4.42         400
ControlS0            123    1.00  108.42      1.04         400
```
Agregados (media ± sd):
- AdaptiveCurriculum (N=2): success = 0.08 ± 0.06; reward ≈72.3 ± 5.5; tripwires ≈0.89 ± 0.81.
- ControlS0 (N=2): success = 1.00 ± 0.00; reward ≈108.9 ± 0.66; tripwires ≈2.73 ± 2.45.

---

## 3. Interpretación
- El curriculum adaptativo, en esta configuración y con episodios reducidos, **no converge**: éxito final bajo (≈8%) y reward menor que el control.
- ControlS0 (s=0.0, 400 eps) alcanza 100% de éxito con reward elevado, aunque pisa más tripwires.
- Diferencia de episodios y N=2 → la comparación no es robusta. El escenario parece sencillo para el control, pero el curriculum adaptativo no tuvo tiempo suficiente o configuración adecuada para converger.

---

## 4. Limitaciones
- N=2 por grupo; distinto número de episodios (Adaptive 78/170 vs Control 400). No hay potencia estadística ni comparabilidad directa.
- Solo se reporta la ventana final; no se analizan curvas completas ni gates.
- Los parámetros de economy y curriculum podrían requerir ajuste para que el adaptativo tenga oportunidad de converger.

---

## 5. Recomendaciones
- Igualar duración por grupo (ej. 400–500 episodios) y aumentar N (≥5) para evaluar curriculum adaptativo con rigor.
- Incrementar presión del entorno o refinar la lógica adaptativa para evitar estancamientos tempranos.
- Analizar curvas de aprendizaje completas y eventos (tripwires, recursos) para entender la falta de convergencia.

---

## 6. Archivos de referencia
- Datos crudos: `results/pgf_v10.2/resultados/exp10.2_*_episodes.csv|metrics.json`
- Tracking/README: `results/pgf_v10.2/README.md`, `TRACKING_v10.2.md` (si existe)

