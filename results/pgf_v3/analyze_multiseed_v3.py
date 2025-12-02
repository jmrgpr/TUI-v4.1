"""
Análisis Multi-Seed PGF v3 - Experimento 3A
Multi-Seed Analysis PGF v3 - Experiment 3A

Analiza los resultados de 3 seeds (42, 123, 456) para validar
robustez estadística de PGF v3.
"""
import pandas as pd
import numpy as np
from scipy import stats

# Seeds experimentales
seeds = [42, 123, 456]
ratios = []
simb_means = []
ctrl_means = []
pgf_bruto_means = []

print("=" * 70)
print("ANÁLISIS MULTI-SEED PGF v3 - Experimento 3A")
print("MULTI-SEED ANALYSIS PGF v3 - Experiment 3A")
print("=" * 70)
print()

# Análisis por seed
print("Resultados por Seed / Results by Seed:")
print("-" * 70)
for seed in seeds:
    df = pd.read_csv(f'results/pgf_v3/exp3a_pgfv3_risk15_seed{seed}_episodes.csv')
    
    simb = df[df['Agente'] == 'simbiosis']['Recompensa'].mean()
    ctrl = df[df['Agente'] == 'control']['Recompensa'].mean()
    ratio = 100 * simb / ctrl
    
    # PGF_Bruto
    pgf_bruto = df[df['Agente'] == 'simbiosis']['PGF_Bruto_Avg'].mean()
    
    ratios.append(ratio)
    simb_means.append(simb)
    ctrl_means.append(ctrl)
    pgf_bruto_means.append(pgf_bruto)
    
    print(f"Seed {seed}:")
    print(f"  Simbiosis: {simb:.2f} ± {df[df['Agente']=='simbiosis']['Recompensa'].std():.2f}")
    print(f"  Control:   {ctrl:.2f} ± {df[df['Agente']=='control']['Recompensa'].std():.2f}")
    print(f"  Ratio:     {ratio:.1f}%")
    print(f"  PGF_Bruto: {pgf_bruto:.4f}")
    print()

# Estadísticas agregadas
print("=" * 70)
print("ESTADÍSTICAS AGREGADAS / AGGREGATE STATISTICS")
print("=" * 70)
print()

ratio_mean = np.mean(ratios)
ratio_std = np.std(ratios, ddof=1)
ratio_se = ratio_std / np.sqrt(len(ratios))
ratio_ci_lower = ratio_mean - 1.96 * ratio_se
ratio_ci_upper = ratio_mean + 1.96 * ratio_se

simb_mean = np.mean(simb_means)
simb_std = np.std(simb_means, ddof=1)
ctrl_mean = np.mean(ctrl_means)
ctrl_std = np.std(ctrl_means, ddof=1)

pgf_mean = np.mean(pgf_bruto_means)
pgf_std = np.std(pgf_bruto_means, ddof=1)

print(f"Ratio Simbiosis/Control:")
print(f"  Media:      {ratio_mean:.2f}%")
print(f"  Std:        {ratio_std:.2f}%")
print(f"  SE:         {ratio_se:.2f}%")
print(f"  IC95%:      [{ratio_ci_lower:.2f}%, {ratio_ci_upper:.2f}%]")
print()

print(f"Recompensa Simbiosis:")
print(f"  Media:      {simb_mean:.2f}")
print(f"  Std:        {simb_std:.2f}")
print()

print(f"Recompensa Control:")
print(f"  Media:      {ctrl_mean:.2f}")
print(f"  Std:        {ctrl_std:.2f}")
print()

print(f"PGF_Bruto:")
print(f"  Media:      {pgf_mean:.4f}")
print(f"  Std:        {pgf_std:.4f}")
print()

# Comparación con v2.1
print("=" * 70)
print("COMPARACIÓN CON PGF v2.1 / COMPARISON WITH PGF v2.1")
print("=" * 70)
print()

v2_1_ratio = 26.7
v3_ratio = ratio_mean
improvement = ((v3_ratio - v2_1_ratio) / v2_1_ratio) * 100

print(f"PGF v2.1 Ratio:  {v2_1_ratio:.2f}%")
print(f"PGF v3 Ratio:    {v3_ratio:.2f}%")
print(f"Mejora:          +{improvement:.1f}%")
print(f"Diferencia abs:  +{v3_ratio - v2_1_ratio:.2f} puntos porcentuales")
print()

# Prueba t de mejora
v2_1_ratios = [27.2, 26.4, 26.4]  # Seeds 42, 123, 456 de v2.1
t_stat, p_val = stats.ttest_ind(ratios, v2_1_ratios)
cohen_d = (np.mean(ratios) - np.mean(v2_1_ratios)) / np.sqrt((np.std(ratios, ddof=1)**2 + np.std(v2_1_ratios, ddof=1)**2) / 2)

print(f"Prueba t (v3 vs v2.1):")
print(f"  t-statistic:  {t_stat:.4f}")
print(f"  p-value:      {p_val:.4e}")
print(f"  Cohen's d:    {cohen_d:.4f}")
print(f"  Significancia: {'SÍ (p<0.05)' if p_val < 0.05 else 'NO (p>=0.05)'}")
print()

# Comparación completa v1 -> v2.1 -> v3
print("=" * 70)
print("EVOLUCIÓN COMPLETA / COMPLETE EVOLUTION")
print("=" * 70)
print()

v1_ratio = 16.8
print(f"PGF v1:      {v1_ratio:.1f}%")
print(f"PGF v2.1:    {v2_1_ratio:.1f}%  (+{((v2_1_ratio-v1_ratio)/v1_ratio)*100:.1f}%)")
print(f"PGF v3:      {v3_ratio:.1f}%  (+{((v3_ratio-v2_1_ratio)/v2_1_ratio)*100:.1f}%)")
print(f"Mejora total v1→v3: +{((v3_ratio-v1_ratio)/v1_ratio)*100:.1f}%")
print()

# Resumen de robustez
print("=" * 70)
print("ROBUSTEZ ESTADÍSTICA / STATISTICAL ROBUSTNESS")
print("=" * 70)
print()

cv = (ratio_std / ratio_mean) * 100
print(f"Coeficiente de Variación (CV): {cv:.2f}%")
print(f"Interpretación: {'EXCELENTE (CV<5%)' if cv < 5 else 'BUENA (CV<10%)' if cv < 10 else 'MODERADA'}")
print()
print(f"Reproducibilidad: {len(seeds)} seeds experimentales")
print(f"Intervalo observado: [{min(ratios):.1f}%, {max(ratios):.1f}%]")
print(f"Rango: {max(ratios) - min(ratios):.1f} puntos porcentuales")
print()

# Guardar resultados
summary_data = {
    'Seed': seeds,
    'Simbiosis_Mean': simb_means,
    'Control_Mean': ctrl_means,
    'Ratio': ratios,
    'PGF_Bruto': pgf_bruto_means
}
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('results/pgf_v3/multiseed_summary_v3.csv', index=False)
print("Resultados guardados en: results/pgf_v3/multiseed_summary_v3.csv")
print("Results saved to: results/pgf_v3/multiseed_summary_v3.csv")
