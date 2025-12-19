# reporte_final_F0_v11.md (DEPRECATED)

Este reporte fue generado en una iteración temprana y **no** está alineado con el cierre canónico de la serie v11 (dataset con hashes + unidad primaria run/seed + métricas duales `reward_total`/`reward_env_total`).

Para el estado vigente de F0 dentro de la serie v11, usar:
- `results/v11/data/stats_report_v11.md`
- `results/v11/data/episodic_metrics_v11.md`
- `results/v11/CANONICAL_DATASET_v11.md`
- `results/v11/INFORME_CIENTIFICO_SERIE_V11.md`

Motivo: versiones anteriores de este reporte usaban `avg_reward` como “recompensa ambiental” sin distinguir `reward_total` vs `reward_env_total`, lo que induce a conclusiones incorrectas cuando `pgf_mix>0`.
