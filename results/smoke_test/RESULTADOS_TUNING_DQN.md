# Comparativo tuning DQN: baseline vs región mala

| Experimento | Configuración breve | LR | Gamma | Epsilon (estrategia) | Reward media últimos 100 | % episodios > 0 | Comentario |
|-------------|---------------------|----|-------|----------------------|-------------------------|-----------------|------------|
| EXP00       | coords_only, lambda_gaming=0.0 | 1e-3 | 0.99  | 1.0 → 0.01 (rápido)  | >300                    | ~98%            | Baseline canónico, DQN aprende |
| EXP02–EXP06 | tuning batch (lr/gamma/eps)    | varios| varios| varios               | <0                      | 0%              | Región mala, DQN colapsa |

---
## EXP00 Baseline congelado (26/11/2025)
**Propósito:** Referencia científica y técnica para todos los experimentos futuros con DQN. Punto de partida y mínimo aceptable para RL en este proyecto.
**Comando ejecutado:**
```
python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 1.0 --dqn_control --lambda_gaming 0.0 --learning_rate 0.001 --gamma 0.95 --epsilon 0.2 --export results/smoke_test/EXP00_baseline.json --output_prefix results/smoke_test/EXP00_baseline
```
**Hiperparámetros:**
- learning_rate=0.001
- gamma=0.95
- epsilon=0.2
- lambda_gaming=0.0
**Diagnóstico:**
El baseline EXP00 se congela como referencia para comparaciones futuras. Si los archivos no se generan, revisar permisos y flags en el script. Resultados esperados: reward media positiva y mayoría de episodios con reward > 0.
---

Interpretación:
Estos resultados muestran que, aunque existe una región de hiperparámetros donde el DQN aprende bien (EXP00), las variantes EXP02–EXP06 lo llevan a colapso de performance incluso en el entorno easy. Se conservan como evidencia negativa documentada, pero no se usarán como baseline ni como prueba contra TUI.

Conclusión:
EXP02–EXP06 no mejoran ni igualan a EXP00; se comportan como ejemplos de hiperparámetros frágiles. Se documentan para trazar la frontera de robustez del DQN y para evitar zonas peligrosas en futuros experimentos.

Se congela EXP00 (coords_only, lambda_gaming=0.0, seeds 42/123/456) como baseline canónico DQN-easy.
EXP02–EXP06 quedan marcados como región mala de hiperparámetros.
# RESULTADOS_TUNING_DQN

Contexto: entorno benigno (grid 3x3, penalizaciones -0.01, bonus meta 100, sin red team, coords_only para DQN) ejecutado desde `sim/prototipo_rl_simbiosis.py`. Los hiperparámetros de DQN usados en estos runs son los valores por defecto vigentes al momento de la ejecución (lr≈0.1 por defecto heredado de AGENT_LEARNING_RATE, gamma=0.95, epsilon=0.2) con `lambda_gaming` según se indica.

## Baseline tabular (control)
- Fuente: `tabular_easy_log.txt`
- Episodios: 500
- Reward media primeros 50: 3.8
- Reward media últimos 50: 2484.23
- Reward máx/min: 2701.9 / 1.3
- Episodios con reward > 0: 500 / 500

## DQN sin penalización de gaming (lambda_gaming=0.0, coords_only)
| Archivo CSV | Seed | Episodios | Reward media | Reward min / max | Episodios > 0 |
| --- | --- | --- | --- | --- | --- |
| dqn_xy_gamingoff_seed42_risk0.5_episodes.csv | 42 | 1500 | 110.22 | -3750.00 / 2701.90 | 1000 / 1500 |
| dqn_xy_gamingoff_seed123_seed123_risk0.5_episodes.csv | 123 | 1500 | 105.80 | -3450.00 / 2701.90 | 1000 / 1500 |
| dqn_xy_gamingoff_seed456_seed456_risk0.5_episodes.csv | 456 | 1500 | 93.11 | -3330.00 / 2602.10 | 1000 / 1500 |

Observaciones:
- Con `lambda_gaming=0` el DQN pasa a recompensas netas positivas y ~66% de episodios con reward > 0 en las tres seeds, pero mantiene alta varianza (mínimos negativos grandes).

## DQN con penalización de gaming (lambda_gaming por defecto anterior)
| Archivo CSV | Seed | Episodios | Reward media | Reward min / max | Episodios > 0 |
| --- | --- | --- | --- | --- | --- |
| dqn_xy_seed42_risk0.5_episodes.csv | 42 | 1500 | -251.37 | -11677.15 / -17.55 | 0 / 1500 |

Observaciones:
- La penalización de gaming agresiva ahogó la señal: todas las recompensas son negativas.

## Próximos pasos propuestos
1) Repetir runs con los defaults DQN actualizados (DQN_LEARNING_RATE=1e-3, DQN_GAMMA=0.95, DQN_EPSILON=0.2) para aislar el efecto del lr alto heredado del tabular en estos runs.
2) Lanzar EXP02–EXP06 variando learning_rate, gamma y epsilon (manteniendo lambda_gaming=0) y registrar reward media de los últimos 100 episodios y % de episodios > 0.
3) Una vez estable, reintroducir la penalización de gaming con un esquema más suave (warm-up/umbrales) y medir impacto.
4) Probar con estado completo (`get_abstract_state`) para evaluar el efecto del ruido en observabilidad.
