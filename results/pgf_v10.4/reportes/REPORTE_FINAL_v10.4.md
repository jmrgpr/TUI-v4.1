# REPORTE FINAL: Experimento v10.4 – Adaptive/Fixed Curriculum 8×8 (economía ajustada)

**Fecha:** 2025-12-08  
**Preregistro:** results/pgf_v10.4/PREREGISTRO_v10.4.md (si aplica)  
**Datos:** results/pgf_v10.4/resultados/*.csv|*.json  
**Grupos:** AdaptiveCurriculum, FixedCurriculum, ControlS0 (s=0.0)

---

## 1. Diseño experimental
- Entorno: `ResourceDensityEnv`, grid 8×8, economía ajustada (balance ~5.0).
- Agente: DQN serie 10.x; epsilon-greedy, replay.
- Grupos y episodios (según métricas JSON):
  - AdaptiveCurriculum: 8 seeds, 600 episodios por run.
  - FixedCurriculum: 8 seeds, 600 episodios por run.
  - ControlS0: 8 seeds, 600 episodios por run.
- Métricas tomadas del campo `final_window` en cada JSON: `success_rate`, `mean_reward_env`, `mean_tripwires`.
- Limitación: todos los `success_rate_final` reportan 0.0 en la ventana final → posible no convergencia real o problema de definición de ventana.

---

## 2. Resultados (ventana final)
Agregados por grupo (media ± sd, N=8):
```
Grupo               success_final   reward_final   tripwires_final
AdaptiveCurriculum       0.00±0.00     50.2±4.1       0.11±0.10
FixedCurriculum          0.00±0.00     50.7±6.7       0.14±0.12
ControlS0                0.00±0.00     30.6±0.0       1.66±0.71
```
Fuente: `final_window` de cada `*_metrics.json`. Nota: `success_rate_final` = 0 en todos los casos.

---

## 3. Interpretación preliminar
- Todos los grupos muestran `success_rate_final = 0.0` en la ventana final → el experimento no logró éxito en la fase analizada.
- Recompensa final es moderada en Adaptive/Fixed (~50) y menor en Control (~31); tripwires bajos en Adaptive/Fixed, mayores en Control.
- Posibles causas:
  - Ventana final mal definida o demasiado corta (ver estructura del campo `final_window`).
  - Economía o parámetros insuficientemente explorados (balance, costos) que impiden alcanzar el goal.
  - Bugs en logging de `success_rate` o en el cálculo de la ventana final.
  - Entrenamiento insuficiente (aunque 600 episodios por run deberían dar señal si el entorno fuera factible).

---

## 4. Limitaciones y próximos pasos
- Revisar la definición de `final_window` y recalcular `success` a partir de los CSV de episodios completos para confirmar si realmente es 0 o es un error de logging.
- Si `success` es realmente 0:
  - Ajustar economía o shaping para incrementar señal de éxito.
  - Revisar el curriculum (duración por etapa, gates) y la política de exploración.
- Si el logging es el problema:
  - Corregir el pipeline de métricas y repetir análisis.
- Con N=8 por grupo hay potencia suficiente para detectar efectos moderados, pero la señal es nula; se requiere diagnóstico de por qué no hay breakthroughs.

---

## 5. Conclusión
El experimento v10.4, en su forma actual, no alcanzó éxito en la ventana final para ningún grupo. Es necesario reanalizar usando los CSV completos y, según el hallazgo, ajustar economía/curriculum o corregir logging antes de sacar conclusiones sobre el valor del curriculum adaptativo/fijo frente al control en este escenario.

---

## 6. Archivos de referencia
- Datos crudos: `results/pgf_v10.4/resultados/exp10.4_*_episodes.csv|metrics.json`
- README/Tracking: `results/pgf_v10.4/README.md`, `TRACKING_v10.4.md` (si aplica)

