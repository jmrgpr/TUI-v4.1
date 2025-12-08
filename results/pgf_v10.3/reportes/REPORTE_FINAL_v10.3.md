# REPORTE FINAL: Experimento v10.3 – Adaptive Curriculum 8×8 (economía ajustada)

**Fecha:** 2025-12-08  
**Preregistro:** results/pgf_v10.3/PREREGISTRO_v10.3.md (si aplica)  
**Datos:** results/pgf_v10.3/resultados/*.csv|*.json  
**Grupos:** AdaptiveCurriculum vs ControlS0 (s=0.0)

---

## 1. Diseño experimental
- Entorno: `ResourceDensityEnv`, grid 8×8, economía ajustada (balance ~5.0).
- Agente: DQN serie 10.x.
- Grupos y episodios observados:
  - AdaptiveCurriculum: 2 seeds (42, 123), 91–98 episodios por run; curriculum adaptativo con transiciones de shaping registradas en `curriculum_info`.
  - ControlS0: 2 seeds (42, 123), 400 episodios por run, shaping s=0.0.
- Métricas analizadas: `success_rate_final`, `mean_reward_env_final`, `mean_tripwires_final` de `final_window` (últimos episodios).
- Limitación: N=2 por grupo, duración desigual (Adaptive <100 eps, Control 400 eps) → resultados indicativos, no concluyentes.

---

## 2. Resultados (ventana final)
Valores por seed:
```
group               seed  success  reward   tripwires  n_episodes
AdaptiveCurriculum    42    0.29   77.42      1.14          98
AdaptiveCurriculum   123    0.00   69.65      0.59          91
ControlS0             42    1.00  108.25      5.05         400
ControlS0            123    1.00  106.83      2.72         400
```
Agregados (media ± sd):
- AdaptiveCurriculum (N=2): success = 0.14 ± 0.17; reward ≈73.5 ± 5.5; tripwires ≈0.86 ± 0.37.
- ControlS0 (N=2): success = 1.00 ± 0.00; reward ≈107.5 ± 0.71; tripwires ≈3.89 ± 1.63.

---

## 3. Interpretación
- El curriculum adaptativo no converge en <100 episodios: éxito final bajo (14%) y reward menor al control.
- ControlS0 alcanza 100% de éxito con reward alto; mayor exposición a tripwires (≈3.9) pero cumple el objetivo.
- Con episodios y N desiguales, no hay base para comparar con rigor; la señal sugiere que el adaptativo falló en estas condiciones.

---

## 4. Limitaciones
- N=2 por grupo; episodios muy desiguales (Adaptive <100 vs Control 400).
- Solo se analiza la ventana final; sin curvas de aprendizaje ni gates.
- Economía/parametrización pueden no ser suficientemente exigentes o el adaptativo no tuvo tiempo de aprender.

---

## 5. Recomendaciones
- Igualar duración por grupo y aumentar N (≥5) para evaluar el curriculum adaptativo.
- Ajustar economía o lógica adaptativa si se busca presión y convergencia.
- Incluir análisis de curvas completas para entender el fracaso de convergencia.

---

## 6. Archivos de referencia
- Datos crudos: `results/pgf_v10.3/resultados/exp10.3_*_episodes.csv|metrics.json`
- README/Tracking: `results/pgf_v10.3/README.md`, `TRACKING_v10.3.md` (si aplica)

