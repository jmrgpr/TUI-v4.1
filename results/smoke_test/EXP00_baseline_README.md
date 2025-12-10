# EXP00 Baseline DQN (defaults, lambda_gaming=0.0)

**Fecha de ejecución:** 26/11/2025
**Comando:**
```
python sim/prototipo_rl_simbiosis.py --episodes 1000 --seed 42 --grid_size 5 --risk_scale 1.0 --dqn_control --lambda_gaming 0.0 --learning_rate 0.001 --gamma 0.95 --epsilon 0.2 --export results/smoke_test/EXP00_baseline.json --output_prefix results/smoke_test/EXP00_baseline
```

## Resultados esperados
- Hiperparámetros: lr=1e-3, gamma=0.95, epsilon=0.2, lambda_gaming=0.0
- El archivo `EXP00_baseline.json` debe contener la sección `dqn_params` con los valores anteriores.
- El archivo `EXP00_baseline_episodes.csv` debe registrar recompensas por episodio, tripwires, flexibilidad, robustez, Q-optimal, PGF promedio y costo.
- Se espera que la recompensa media sea positiva y que la mayoría de episodios tengan reward > 0.

## Diagnóstico
Si los archivos no se generan:
- Verifica permisos de escritura en la carpeta `results/smoke_test`.
- Revisa la consola por errores de exportación.
- Asegúrate de que los flags `--export` y `--output_prefix` están correctamente implementados en el script.

## Siguiente paso
Actualizar `RESULTADOS_TUNING_DQN.md` con los resultados obtenidos y marcar EXP00 como baseline congelado para futuras comparaciones.
