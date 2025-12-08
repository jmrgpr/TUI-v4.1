# REPORTE FINAL: Experimento v10.6_exploratory_16x16 – Curriculum vs Control en grid 16×16

**Fecha:** 2025-12-08  
**Preregistro:** results/pgf_v10.6_exploratory_16x16/PREREGISTRO_v10.6_exploratory_16x16.md (si aplica)  
**Datos:** results/pgf_v10.6_exploratory_16x16/resultados/*.csv|*.json  
**Grupos:** AdaptiveCurriculum vs ControlS0 (s=0.0)

---

## 1. Diseño experimental
- Entorno: `ResourceDensityEnv`, grid 16×16, economía de la serie 10.x (balance ~5.0).
- Agente: DQN serie 10.x.
- Grupos y episodios observados:
  - AdaptiveCurriculum: 2 seeds (42, 123), 400 episodios por run; curriculum adaptativo (transiciones en `curriculum_info`).
  - ControlS0: 2 seeds (42, 123), 200 episodios por run, shaping s=0.0.
- Métricas analizadas: `success_rate_final`, `mean_reward_env_final`, `mean_tripwires_final` del campo `final_window`.
- Limitación: N=2 y episodios desiguales entre grupos (400 vs 200).

---

## 2. Resultados (ventana final)
Valores por seed:
```
group               seed  success  reward   tripwires  n_episodes
AdaptiveCurriculum    42    0.00   36.31      0.00         400
AdaptiveCurriculum   123    0.00   34.54      0.12         400
ControlS0             42    0.00   18.78      1.42         200
ControlS0            123    0.00   19.06      1.22         200
```
Agregados (media ± sd):
- AdaptiveCurriculum (N=2): success = 0.00 ± 0.00; reward ≈35.4 ± 1.3; tripwires ≈0.06 ± 0.09.
- ControlS0 (N=2): success = 0.00 ± 0.00; reward ≈18.9 ± 0.2; tripwires ≈1.32 ± 0.14.

---

## 3. Interpretación
- Ningún grupo alcanzó éxito en la ventana final; en 16×16 la tarea resulta demasiado difícil con la configuración actual.
- AdaptiveCurriculum logra mayor reward y pisa menos tripwires que el control, pero sin lograr metas.
- La diferencia de episodios entre grupos (400 vs 200) y N=2 limitan cualquier conclusión.

---

## 4. Limitaciones
- N muy bajo (2) y duración desigual entre grupos.
- Solo se analizó la ventana final; sin curvas de aprendizaje ni análisis de gates.
- El entorno 16×16 puede ser demasiado exigente con estos hiperparámetros; podría requerir más episodios, mayor shaping, o ajustes de economía/exploración.

---

## 5. Recomendaciones
- Verificar éxito a partir de los CSV completos para confirmar la ausencia total de éxitos.
+- Igualar episodios entre grupos y aumentar N (≥5); incrementar presupuesto de episodios (≥1000) en 16×16.
- Ajustar economía o incluir shaping/transfer si se busca que el agente alcance metas en 16×16.

---

## 6. Archivos de referencia
- Datos crudos: `results/pgf_v10.6_exploratory_16x16/resultados/exp10.6_exploratory_*_episodes.csv|metrics.json`
- README/Tracking: `results/pgf_v10.6_exploratory_16x16/README.md`, `TRACKING_v10.6_exploratory_16x16.md` (si aplica)

