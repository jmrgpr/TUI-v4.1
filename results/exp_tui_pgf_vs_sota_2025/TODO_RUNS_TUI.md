# Plan de corridas faltantes (fase 2)

Objetivo: generar datos etiquetados para TUI y ablations PGF, reconsolidar y replotear.

1) Runs TUI etiquetados por riesgo  
   - Variantes: `tui_default`, `tui_tuned` (y si aplica, `tui` base).  
   - Seeds: 42, 123, 456.  
   - Riesgos: 0.5, 1.0, 1.5, 2.0, 3.0.  
   - Episodios: 200 (y si es posible repetir con 500).  
   - Asegurar que el CSV de cada run escriba `risk_scale`, `episodes`, `kappa`, `lambda`, `mix` y lleve estos tokens en el nombre/path para que el consolidado los detecte (ej.: `risk1.0_seed42_tui_tuned_kappa2.0_lambda0.05_mix0.8.csv`).

2) Ablation PGF mínima  
   - `simbiosis_light`: kappa=1.0, lambda=0.1, mix=0.5 (prudencia suave).  
   - `simbiosis_heavy`: kappa=2.0, lambda=0.05, mix=0.8 (prudencia fuerte).  
   - Misma matriz de seeds/risks/episodios y nomenclatura consistente para que el consolidado marque el agente.

3) PPO controlado  
   - Repetir PPO con normalización consistente; si persiste el outlier en riesgo 0.5, mantenerlo documentado pero generar gráfica “zoom” de reward sin perder el punto.

4) Reconsolidar y replotear  
   - Ejecutar `python scripts/consolidate_results.py` (ya añade `safety_adj_reward`).  
   - Reejecutar `results/exp_tui_pgf_vs_sota_2025/analysis_phase2.ipynb` para regenerar CSVs y PNGs (incluyendo la métrica nueva y versiones con zoom si aplica).

5) Publicación  
   - Actualizar `REPORTE_PRELIMINAR.md` con los nuevos hallazgos/figuras en la rama `publicaciones-fase2`.

Notas: el consolidado ya detecta `tui_tuned`/`tui_default`, extrae `risk_scale`/episodios/kappa/lambda/mix` desde el path y calcula `safety_adj_reward = reward_total * exp(-beta * tripwires)` con beta=1. Ajustar beta si se quiere penalización más dura.
