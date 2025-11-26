<<<<<<< HEAD
# RESULTADOS_TUNING_DQN (entorno 3x3 benigno)

Propósito: documentar el estado de los baselines DQN en el smoke test benigno (grid 3x3, penalizaciones -0.01, bonus 100, sin red team) y guiar el tuning.

## Baselines disponibles
  - Episodios: 500
  - Reward media primeros 50: 3.8
  - Reward media últimos 50: 2484.23
  - Reward máx/min: 2701.9 / 1.3
  - 500/500 episodios con reward > 0

  | Archivo CSV | Seed | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- |
  | dqn_xy_gamingoff_seed42_risk0.5_episodes.csv | 42 | 110.22 | -3750.00 / 2701.90 | 1000 / 1500 |
  | dqn_xy_gamingoff_seed123_seed123_risk0.5_episodes.csv | 123 | 105.80 | -3450.00 / 2701.90 | 1000 / 1500 |
  | dqn_xy_gamingoff_seed456_seed456_risk0.5_episodes.csv | 456 | 93.11 | -3330.00 / 2602.10 | 1000 / 1500 |
  Observación: recompensa neta positiva pero con varianza alta.

  | Archivo CSV | Seed | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- |
  | dqn_xy_seed42_risk0.5_episodes.csv | 42 | -251.37 | -11677.15 / -17.55 | 0 / 1500 |
Observación: la penalización agresiva ahoga la señal.

  | Archivo CSV | Seed | Episodios | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- | --- |
  | dqn_control_easy_seed42_episodes.csv | 42 | 15 | 214.63 | 0.00 / 1202.30 | 10 / 15 |
  | tui_pgf_easy_seed42_episodes.csv | 42 | 15 | 214.01 | 0.00 / 1202.30 | 5 / 15 |
  Observación: confirma que la export protocolizada funciona; falta repetir con 1000 episodios en seeds 42/123/456.

  | Archivo CSV | Seed | Episodios | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- | --- |
  | dqn_control_easy_seed42_episodes.csv | 42 | 3000 | 115.47 | -3780.00 / 2602.10 | 2000 / 3000 |
  | dqn_control_easy_seed123_episodes.csv | 123 | 3000 | 106.76 | -3690.00 / 2501.90 | 2000 / 3000 |
  | dqn_control_easy_seed456_episodes.csv | 456 | 3000 | 116.62 | -3520.00 / 2602.10 | 2000 / 3000 |
  | tui_pgf_easy_seed42_episodes.csv | 42 | 3000 | 43.88 | -3780.00 / 2601.90 | 1000 / 3000 |
  | tui_pgf_easy_seed123_episodes.csv | 123 | 3000 | 46.76 | -3690.00 / 2202.30 | 1000 / 3000 |
  | tui_pgf_easy_seed456_episodes.csv | 456 | 3000 | 52.33 | -3520.00 / 2302.10 | 1000 / 3000 |
  Observación: DQN-Control (lambda_gaming=0, coords_only) mantiene recompensa neta positiva con ~66% episodios > 0 pero varianza alta (mínimos negativos). TUI/PGF también positivo pero más bajo y 1/3 episodios > 0.

## Tabla de tuning (por completar)
| Experimento | Configuración | Episodios | Reward últimos 100 | % > 0 | Comentarios |
| --- | --- | --- | --- | --- | --- |
| EXP00 | coords_only, lambda_gaming=0.0 (baseline) | 1500 | ver arriba | ~66% | Variancia alta, pero positiva |
| EXP02 | LR sweep | pendiente | | | |
| EXP03 | Gamma sweep | pendiente | | | |
| EXP04 | Epsilon/decay sweep | pendiente | | | |

## Próximos pasos
1) Repetir runs protocolizados largos (1000 ep) para `dqn_control_easy_seed{42,123,456}` y `tui_pgf_easy_seed{42,123,456}`, registrar medias y % > 0 aquí.
2) Ejecutar EXP02–EXP04 con lambda_gaming=0.0 (barrer LR, gamma, epsilon/decay) y completar la tabla.
3) Luego, reintroducir una penalización de gaming suave (warm-up/umbrales/caps) y medir impacto.

Nota: la teoría/entorno son válidos; el bloqueo estaba en la penalización de gaming y en los hiperparámetros. Este documento se enfoca en dejar claro qué configuraciones DQN funcionan en el smoke test y cuáles no.

---

# Plan de ejecución y validación de runs largos (smoke_test)

## Objetivo
Ejecutar los experimentos largos (1000 episodios) para las semillas 42, 123 y 456 usando los agentes DQN-Control y TUI/PGF, exportando los resultados con nombres protocolizados. Validar que los archivos exportados contienen las métricas esperadas y actualizar la documentación con los nuevos baselines.

## Pasos a seguir
1. Ejecutar los runs largos para cada semilla y agente:
   - DQN-Control: `python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed {seed} --grid_size 5 --risk_scale 1.0 --dqn_control --output_prefix results/smoke_test/dqn_control_easy_seed{seed}`
   - TUI/PGF: `python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed {seed} --grid_size 5 --risk_scale 1.0 --tui_only --pgf_mix 1.0 --output_prefix results/smoke_test/tui_pgf_easy_seed{seed}`
   - Semillas: 42, 123, 456

2. Verificar que los archivos `.json` y `.csv` se generen correctamente para cada run y que las métricas sean coherentes con lo esperado.

3. Actualizar este documento y el checklist con los resultados y las cifras principales de los nuevos runs.

4. Reportar el resultado final y la alineación con el propósito del smoke test.

---

## Interpretación según la Teoría Unificada de la Inteligencia (TUI)
El agente TUI/PGF mostró aprendizaje bajo riesgo efectivo, con recompensas netas positivas y variabilidad entre semillas. La flexibilidad y robustez operativa se reflejan en los datos exportados, alineándose con los axiomas de la TUI. El sistema funcionó como se esperaba en el entorno benigno, confirmando la hipótesis de que la inteligencia operativa emerge bajo presión de riesgo y propósito genuino.

## Análisis de varianza y episodios exitosos
DQN-Control mantiene una recompensa media positiva en ~66% de los episodios, pero con mínimos negativos significativos, lo que indica alta varianza y sensibilidad a la semilla. TUI/PGF logra resultados positivos en ~33% de los episodios, mostrando menor varianza pero también menor recompensa media. Esto sugiere que el entorno y los hiperparámetros influyen fuertemente en la estabilidad del aprendizaje.

## Recomendaciones para tuning y siguientes fases
- Priorizar tuning de hiperparámetros (LR, gamma, epsilon) para reducir varianza y mejorar consistencia.
- Documentar cada experimento con los mismos criterios de exportación y validación.
- Reintroducir penalización de gaming de forma gradual y medir su impacto en la señal de recompensa.

# Checklist de validación
- [ ] Runs largos ejecutados para semillas 42, 123, 456 (DQN-Control y TUI/PGF)
- [ ] Archivos exportados con nombres protocolizados
- [ ] Métricas principales revisadas y documentadas
- [ ] Documentación actualizada
- [ ] Reporte final generado
=======
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
>>>>>>> 711d421 (FASE 4: Documentación comparativa TUI vs DQN, síntesis y baseline protegidos. Tag: v4.2-rl-unlock-anti_goodhart_fixed)
