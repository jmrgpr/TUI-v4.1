# Bootstrap confirmatorio (parametric approx) — v11

Se generaron estimaciones bootstrap paramétricas (muestreo normal) para la diferencia de medias vs control por `risk_scale`. Esto es confirmatorio y asume distribución aproximadamente normal de reward_total por run; recomendamos bootstrap no paramétrico si se dispone de raw per-run reward_total.

      agent  risk_scale  mean_diff    ci95_lo   ci95_hi  p_boot
dqn_control         1.2  -9.827161 -11.864926 -7.837436  0.4966
  simbiosis         1.2  36.175980  34.160799 38.202384  0.5042