# Bootstrap No Paramétrico desde archivos de episodios — v11

Se generan estimaciones bootstrap no paramétricas (resampling per-run de la media de recompensa por archivo) para la diferencia de medias vs control, por `risk_group`.

      agent  risk_group  mean_diff   ci95_lo   ci95_hi  p_boot_nonparam  n_agent  n_control
dqn_control         1.0  -3.273449 -3.469566 -3.084105           0.4990       42         42
  simbiosis         1.0  42.760700 42.549619 42.968344           0.5002       42         42