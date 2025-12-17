# F2 Final Checks - Canonico (seeds y outliers)

Archivos inspeccionados (F2 canonico): 30

Exclusiones: `raw/` y `archived/`. Unidad primaria: archivo `*_episodes.csv` (seed/run).

Criterios: `low_n` si `n` < 90% de la mediana (mediana=200.0); outlier si |z(mean_reward)|>3 o |z(pct_tripwires)|>3 o `low_n`.

Tabla por run:

                                                                                            file       agent  seed  grid   n  mean_reward  std_reward  pct_tripwires  low_n    z_mean    z_trip  outlier
        results\v11\F2_redteam\grid8\riskhigh\control\grid8_riskhigh_r1p2_seed7_v11_episodes.csv     control     7     8 200   -71.364950    7.733487            0.0  False  0.182575 -0.732978    False
       results\v11\F2_redteam\grid8\riskhigh\control\grid8_riskhigh_r1p2_seed13_v11_episodes.csv     control    13     8 200   -72.138700    3.324545           12.0  False -1.093381  2.857118    False
       results\v11\F2_redteam\grid8\riskhigh\control\grid8_riskhigh_r1p2_seed42_v11_episodes.csv     control    42     8 200   -72.544350    2.303133            2.0  False -1.762319 -0.134629    False
       results\v11\F2_redteam\grid8\riskhigh\control\grid8_riskhigh_r1p2_seed99_v11_episodes.csv     control    99     8 200   -71.603800    5.268634            2.5  False -0.211302  0.014959    False
      results\v11\F2_redteam\grid8\riskhigh\control\grid8_riskhigh_r1p2_seed101_v11_episodes.csv     control   101     8 200   -71.928150    4.710830            0.5  False -0.746172 -0.583391    False
      results\v11\F2_redteam\grid16\riskhigh\control\grid16_riskhigh_r1p2_seed7_v11_episodes.csv     control     7    16 200   -71.853000    2.783583            1.0  False -0.622246 -0.433803    False
     results\v11\F2_redteam\grid16\riskhigh\control\grid16_riskhigh_r1p2_seed13_v11_episodes.csv     control    13    16 200   -70.680850    4.610438            2.5  False  1.310693  0.014959    False
     results\v11\F2_redteam\grid16\riskhigh\control\grid16_riskhigh_r1p2_seed42_v11_episodes.csv     control    42    16 200   -70.824200    4.393441            0.0  False  1.074301 -0.732978    False
     results\v11\F2_redteam\grid16\riskhigh\control\grid16_riskhigh_r1p2_seed99_v11_episodes.csv     control    99    16 200   -70.804000    4.759391            3.0  False  1.107612  0.164546    False
    results\v11\F2_redteam\grid16\riskhigh\control\grid16_riskhigh_r1p2_seed101_v11_episodes.csv     control   101    16 200   -71.014650    4.772192            1.0  False  0.760239 -0.433803    False
    results\v11\F2_redteam\grid8\riskhigh\dqn_control\grid8_riskhigh_r1p2_seed7_v11_episodes.csv dqn_control     7     8 200   -71.988600    2.505964            1.5  False -1.287682 -0.265511    False
   results\v11\F2_redteam\grid8\riskhigh\dqn_control\grid8_riskhigh_r1p2_seed13_v11_episodes.csv dqn_control    13     8 200   -70.018700    4.761429            6.0  False  0.359079  2.389599    False
   results\v11\F2_redteam\grid8\riskhigh\dqn_control\grid8_riskhigh_r1p2_seed42_v11_episodes.csv dqn_control    42     8 200   -71.010650    4.040031            1.0  False -0.470153 -0.560523    False
   results\v11\F2_redteam\grid8\riskhigh\dqn_control\grid8_riskhigh_r1p2_seed99_v11_episodes.csv dqn_control    99     8 200   -71.334650    3.830595            4.0  False -0.741005  1.209550    False
  results\v11\F2_redteam\grid8\riskhigh\dqn_control\grid8_riskhigh_r1p2_seed101_v11_episodes.csv dqn_control   101     8 200   -71.570000    3.055228            2.0  False -0.937748  0.029501    False
  results\v11\F2_redteam\grid16\riskhigh\dqn_control\grid16_riskhigh_r1p2_seed7_v11_episodes.csv dqn_control     7    16 200   -71.776850    2.702990            0.5  False -1.110667 -0.855535    False
 results\v11\F2_redteam\grid16\riskhigh\dqn_control\grid16_riskhigh_r1p2_seed13_v11_episodes.csv dqn_control    13    16 200   -68.814950    5.116092            2.0  False  1.365368  0.029501    False
 results\v11\F2_redteam\grid16\riskhigh\dqn_control\grid16_riskhigh_r1p2_seed42_v11_episodes.csv dqn_control    42    16 200   -69.845250    4.481549            1.5  False  0.504076 -0.265511    False
 results\v11\F2_redteam\grid16\riskhigh\dqn_control\grid16_riskhigh_r1p2_seed99_v11_episodes.csv dqn_control    99    16 200   -68.449500    5.227525            1.0  False  1.670870 -0.560523    False
results\v11\F2_redteam\grid16\riskhigh\dqn_control\grid16_riskhigh_r1p2_seed101_v11_episodes.csv dqn_control   101    16 200   -69.673250    5.174276            0.0  False  0.647862 -1.150548    False
      results\v11\F2_redteam\grid8\riskhigh\simbiosis\grid8_riskhigh_r1p2_seed7_v11_episodes.csv   simbiosis     7     8 200   -55.009475   10.225992            0.5  False -1.309855 -0.557086    False
     results\v11\F2_redteam\grid8\riskhigh\simbiosis\grid8_riskhigh_r1p2_seed13_v11_episodes.csv   simbiosis    13     8 200   -42.113361   16.117018            5.0  False  0.566125  2.785430    False
     results\v11\F2_redteam\grid8\riskhigh\simbiosis\grid8_riskhigh_r1p2_seed42_v11_episodes.csv   simbiosis    42     8 200   -47.436570   15.188639            0.5  False -0.208235 -0.557086    False
     results\v11\F2_redteam\grid8\riskhigh\simbiosis\grid8_riskhigh_r1p2_seed99_v11_episodes.csv   simbiosis    99     8 200   -49.986691   14.643469            1.5  False -0.579198  0.185695    False
    results\v11\F2_redteam\grid8\riskhigh\simbiosis\grid8_riskhigh_r1p2_seed101_v11_episodes.csv   simbiosis   101     8 200   -53.567329   12.975783            2.0  False -1.100068  0.557086    False
    results\v11\F2_redteam\grid16\riskhigh\simbiosis\grid16_riskhigh_r1p2_seed7_v11_episodes.csv   simbiosis     7    16 200   -54.668690   11.018384            0.5  False -1.260282 -0.557086    False
   results\v11\F2_redteam\grid16\riskhigh\simbiosis\grid16_riskhigh_r1p2_seed13_v11_episodes.csv   simbiosis    13    16 200   -38.197249   17.537300            0.5  False  1.135797 -0.557086    False
   results\v11\F2_redteam\grid16\riskhigh\simbiosis\grid16_riskhigh_r1p2_seed42_v11_episodes.csv   simbiosis    42    16 200   -45.027045   17.270203            0.5  False  0.142275 -0.557086    False
   results\v11\F2_redteam\grid16\riskhigh\simbiosis\grid16_riskhigh_r1p2_seed99_v11_episodes.csv   simbiosis    99    16 200   -35.819982   17.528023            1.0  False  1.481614 -0.185695    False
  results\v11\F2_redteam\grid16\riskhigh\simbiosis\grid16_riskhigh_r1p2_seed101_v11_episodes.csv   simbiosis   101    16 200   -38.224540   17.022769            0.5  False  1.131827 -0.557086    False

Runs marcados como potencialmente problematicos:

Ninguno.
