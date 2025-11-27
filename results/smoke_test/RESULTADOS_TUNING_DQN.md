# RESULTADOS_TUNING_DQN (entorno 3x3 benigno)

Propósito: documentar el estado de los baselines DQN en el smoke test benigno (grid 3x3, penalizaciones -0.01, bonus 100, sin red team) y guiar el tuning.

## Baselines disponibles
- Tabular (control): `tabular_easy_log.txt`
  - Episodios: 500
  - Reward media primeros 50: 3.8
  - Reward media últimos 50: 2484.23
  - Reward máx/min: 2701.9 / 1.3
  - 500/500 episodios con reward > 0

- DQN coords_only, lambda_gaming=0 (legacy runs, 1500 ep, nombres dqn_xy_gamingoff_*):
  | Archivo CSV | Seed | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- |
  | dqn_xy_gamingoff_seed42_risk0.5_episodes.csv | 42 | 110.22 | -3750.00 / 2701.90 | 1000 / 1500 |
  | dqn_xy_gamingoff_seed123_seed123_risk0.5_episodes.csv | 123 | 105.80 | -3450.00 / 2701.90 | 1000 / 1500 |
  | dqn_xy_gamingoff_seed456_seed456_risk0.5_episodes.csv | 456 | 93.11 | -3330.00 / 2602.10 | 1000 / 1500 |
  Observación: recompensa neta positiva pero con varianza alta.

- DQN con penalización de gaming activa (legacy):
  | Archivo CSV | Seed | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- |
  | dqn_xy_seed42_risk0.5_episodes.csv | 42 | -251.37 | -11677.15 / -17.55 | 0 / 1500 |
  Observación: la penalización agresiva ahoga la señal.

- Sanity check con nombres protocolizados (corrida corta 15 ep):
  | Archivo CSV | Seed | Episodios | Reward media | Min / Max | Episodios > 0 |
  | --- | --- | --- | --- | --- | --- |
  | dqn_control_easy_seed42_episodes.csv | 42 | 15 | 214.63 | 0.00 / 1202.30 | 10 / 15 |
  | tui_pgf_easy_seed42_episodes.csv | 42 | 15 | 214.01 | 0.00 / 1202.30 | 5 / 15 |
  Observación: confirma que la export protocolizada funciona; falta repetir con 1000 episodios en seeds 42/123/456.

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

# Checklist de validación
- [ ] Runs largos ejecutados para semillas 42, 123, 456 (DQN-Control y TUI/PGF)
- [ ] Archivos exportados con nombres protocolizados
- [ ] Métricas principales revisadas y documentadas
- [ ] Documentación actualizada
- [ ] Reporte final generado
