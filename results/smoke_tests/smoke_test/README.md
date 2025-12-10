# Smoke Test y Tuning (entorno 3x3 benigno)

Estado: entorno y reward validados; export protocolizado funcionando.

## Config benigna
- Grid 3x3, recursos 200, pasos máx. 30.
- Sin tripwires/shocks/distractores; red team off.
- Penalizaciones -0.01; riesgo alto/bajo -0.2/-0.1.
- Bonus meta 100; bonus avance +0.2 y episodio limpio +1.

## Cómo correr (nombres protocolizados)
- DQN-Control (coords_only, lambda_gaming=0):
```
$env:PYTHONPATH='.'
python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --grid_size 3 --risk_scale 0.5 \
  --dqn_control --lambda_gaming 0.0 --learning_rate 0.001 --gamma 0.95 --epsilon 0.2
```
Genera `results/smoke_test/dqn_control_easy_seed42.json` y `_episodes.csv`.

- TUI/PGF (**recomendado: pgf_mix=0.2**):
```
python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --grid_size 3 --risk_scale 0.5 \
  --tui_only --pgf_mix 0.2
```
Genera `results/smoke_test/tui_pgf_easy_seed42.json` y `_episodes.csv`.

⚠️ **IMPORTANTE:** En entorno 3×3 benigno, usar `pgf_mix ≤ 0.5`. El valor `pgf_mix=1.0` requiere entorno con riesgo real (tripwires/shocks activos) para funcionar correctamente. Ver `RESULTADOS_FIX_PGF_MIX.md` para detalles.

Si pasas `--output_prefix`, se usa ese prefijo (carpetas creadas automáticamente). El JSON incluye `dqn_params`.

## Flags de tuning DQN
`--learning_rate`, `--gamma`, `--epsilon`, `--epsilon_decay`, `--epsilon_end`, `--lambda_gaming`.

Ejemplos (todos con lambda_gaming=0.0):
- LR 5e-4:
```
python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --risk_scale 0.5 \
  --dqn_control --lambda_gaming 0.0 --learning_rate 0.0005
```
- Gamma 0.95:
```
python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --risk_scale 0.5 \
  --dqn_control --lambda_gaming 0.0 --gamma 0.95
```
- Epsilon alto + decay lento:
```
python sim/prototipo_rl_simbiosis.py --episodes 500 --seed 42 --risk_scale 0.5 \
  --dqn_control --lambda_gaming 0.0 --epsilon 1.0 --epsilon_decay 0.999 --epsilon_end 0.1
```

## Resultados de referencia (legacy)
- Tabular: últimos 50 ep ≈ 2484, 500/500 > 0.
- DQN coords, lambda_gaming=0 (seeds 42/123/456): medias 93–110, 1000/1500 > 0, varianza alta.
- Con penalización de gaming activa: reward negativa, 0/1500 > 0.

## Plan
1) Repetir runs protocolizados (seeds 42/123/456) para DQN y TUI y documentarlos.
2) Tuning EXP02–EXP06 con lambda_gaming=0.0 (lr/gamma/epsilon/decay).
3) Rediseñar penalización de gaming (warm-up/umbrales/caps) y medir impacto.
4) Comparar TUI/PGF vs DQN-Control en este entorno.

Nota: la teoría TUI no está falsificada; el bloqueo era el shaping y los hiperparámetros. El entorno y el RL funcionan bajo configuraciones razonables.
