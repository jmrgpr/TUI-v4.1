# Experimento: TUI prudencia v2 (datos etiquetados y ablations PGF)

## Objetivo
Recolectar un set limpio y trazable para medir prudencia vs utilidad:
- Incluir TUI con `risk_scale` etiquetado (default/tuned).
- Ablation PGF (prudencia suave vs fuerte) sobre TUI.
- Comparar contra DQN-Control y PPO bajo riesgos escalables.
- Añadir métrica de utilidad ajustada por seguridad (`safety_adj_reward = reward_total * exp(-beta * tripwires)`, beta=1 por defecto).

## Matriz de corridas
- Riesgos: 0.5, 1.0, 1.5, 2.0, 3.0 (opcional: 5.0, 10.0).
- Seeds: 42, 123, 456.
- Episodios: 200 (opcional repetir con 500).
- Agentes:
  - `tui_default`
  - `tui_tuned`
  - `simbiosis_light` (kappa=1.0, lambda=0.1, mix=0.5)
  - `simbiosis_heavy` (kappa=2.0, lambda=0.05, mix=0.8)
  - `dqn_control`
  - `ppo`

## Convenciones de nombres (para que el consolidado detecte metadatos)
Formato sugerido para CSV por run:  
`risk{R}_seed{S}_agent{AG}_episodes{E}_kappa{K}_lambda{L}_mix{M}.csv`  
Ejemplo: `risk1.5_seed42_tui_tuned_episodes200_kappa2.0_lambda0.05_mix0.8.csv`

## Estructura recomendada
```
results/exp_tui_prudencia_v2/
  README.md                # este archivo
  results/                 # CSV crudos por run
  plots/                   # PNGs y CSVs agregados del notebook
  logs/                    # logs de ejecución
  experiment_log.txt       # bitácora breve (fecha, comando, semilla)
  analysis_phase2.ipynb    # copia adaptada que apunte a esta carpeta
```

## Pasos
1) Ejecutar corridas según la matriz (guardar CSVs en `results/exp_tui_prudencia_v2/results/` con nombres consistentes).  
2) Reconsolidar: `python scripts/consolidate_results.py` (ya incluye `safety_adj_reward` y detecta `tui_default/tui_tuned`).  
3) Ejecutar el notebook `analysis_phase2.ipynb` (versión adaptada a esta carpeta) para generar `plots/` y tablas.  
4) Revisar gráficos: heatmaps, frontera PGF vs tripwires, violines, correlación, estabilidad por seed, y cualquier “zoom” de reward para manejar outliers de PPO.  
5) Actualizar reporte/publicación con los hallazgos de este experimento.

## Parámetros PGF por variante
- simbiosis_light: kappa=1.0, lambda=0.1, mix=0.5  
- simbiosis_heavy: kappa=2.0, lambda=0.05, mix=0.8  
- tui_default/tui_tuned: ajustar aquí si difieren (documentar en experiment_log.txt)

## Notas
- Mantener el outlier de PPO (si aparece) documentado; generar versión “zoom” de reward para legibilidad.  
- Si se prueban riesgos altos (5.0, 10.0), documentar train vs test para evaluar generalización.  
- Ajustar `SAFETY_BETA` en `scripts/consolidate_results.py` si se desea penalización más dura de accidentes.
