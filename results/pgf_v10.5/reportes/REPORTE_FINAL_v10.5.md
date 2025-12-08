# REPORTE FINAL: Experimento v10.5 – Adaptive Curriculum 8×8 (economía ajustada, N=2)

**Fecha:** 2025-12-08  
**Preregistro:** results/pgf_v10.5/PREREGISTRO_v10.5.md (si aplica)  
**Datos:** results/pgf_v10.5/resultados/*.csv|*.json  
**Grupos:** AdaptiveCurriculum vs ControlS0 (s=0.0)

---

## 1. Diseño experimental
- Entorno: `ResourceDensityEnv`, grid 8×8, economía ajustada (balance ~5.0).
- Agente: DQN serie 10.x.
- Grupos y episodios observados:
  - AdaptiveCurriculum: 2 seeds (42, 123), 170 episodios por run; curriculum adaptativo (transiciones en `curriculum_info`).
  - ControlS0: 2 seeds (42, 123), 400 episodios por run, shaping s=0.0.
- Métricas analizadas: `success_rate_final`, `mean_reward_env_final`, `mean_tripwires_final` del campo `final_window`.
- Limitación: N=2 y duración desigual entre grupos (170 vs 400 episodios).

---

## 2. Resultados (ventana final)
Valores por seed:
```
group               seed  success  reward   tripwires  n_episodes
AdaptiveCurriculum    42    0.00   48.40      0.04         170
AdaptiveCurriculum   123    0.00   49.15      0.04         170
ControlS0             42    0.00   29.76      2.98         400
ControlS0            123    0.00   29.73      5.94         400
```
Agregados (media ± sd):
- AdaptiveCurriculum (N=2): success = 0.00 ± 0.00; reward ≈48.8 ± 0.4; tripwires ≈0.04 ± 0.00.
- ControlS0 (N=2): success = 0.00 ± 0.00; reward ≈29.7 ± 0.02; tripwires ≈4.46 ± 3.51.

---

## 3. Interpretación
- Ningún grupo alcanzó éxito en la ventana final (success=0). El experimento no converge en las condiciones probadas.
- AdaptiveCurriculum obtiene mayor reward final y pisa menos tripwires que el control, pero sin lograr éxito.
- Probable insuficiencia de exploración o presión/objetivo mal calibrado; también puede influir la duración desigual (170 vs 400 episodios).

---

## 4. Limitaciones
- N muy bajo (2) y episodios desiguales entre grupos.
- Solo se analiza la ventana final; sin curvas de aprendizaje ni gates para detectar breakthroughs.
- Se requiere revisar si el entorno objetivo (goal) es alcanzable con esta economía y parametrización.

---

## 5. Recomendaciones
- Verificar cálculo de `success` desde los CSV completos para descartar error de logging.
- Igualar duración por grupo (≥400 episodios) y aumentar N (≥5).
- Ajustar economía o curriculum si se busca que el agente alcance metas; analizar también señal de shaping (si aplica) y políticas de exploración.

---

## 6. Archivos de referencia
- Datos crudos: `results/pgf_v10.5/resultados/exp10.5_*_episodes.csv|metrics.json`
- README/Tracking: `results/pgf_v10.5/README.md`, `TRACKING_v10.5.md` (si aplica)

