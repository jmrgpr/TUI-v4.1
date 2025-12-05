"""
Análisis Estadístico v9.1: Validación Estadística Robusta N=10
================================================================

Análisis preregistrado para validar Hipótesis H9.1.1-H9.4.1 con N=10:
- H9.1.1: Curriculum ≥ 0.70 ratio vs Control (threshold éxito con potencia 60-80%)
- H9.2.1: Curriculum ≈ Control (p<0.05, Cohen's d, adecuadamente powered)
- H9.3.1: Curriculum mantiene prudencia (tripwires ≤ Control)
- H9.4.1: Degradación gradual (0/10 seeds colapso súbito)

Mejoras vs v9 (N=3):
- N=10 seeds → Potencia 60-80% (vs 18%)
- Reducción CI width ~40%
- Detección d=0.8 con α=0.05, β=0.20-0.40

Métodos:
- t-tests pareados (paired samples por seed)
- Wilcoxon signed-rank (validación no-paramétrica)
- Effect sizes (Cohen's d)
- Confidence intervals (95%)
- Bootstrap CI (1000 resamples)

Uso:
    python scripts/analyze_curriculum_v9_1.py

Autor: TUI v4.1 Research Team
Fecha: 4 diciembre 2025
Preregistro: results/pgf_v9.1/PREREGISTRO_v9.1.md v1.0
"""

import sys
import os
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Agregar directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

class NumpyEncoder(json.JSONEncoder):
    """Custom encoder para tipos numpy."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super(NumpyEncoder, self).default(obj)

RESULTS_DIR = Path('results/pgf_v9.1/resultados')
OUTPUT_DIR = Path('results/pgf_v9.1/analisis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GROUPS = ['Curriculum', 'DirectoS1', 'ControlS0']
SEEDS = [42, 123, 456, 789, 101112, 131415, 161718, 192021, 222324, 252627]

# Ventana final para análisis (últimos 50 episodios)
FINAL_WINDOW_SIZE = 50


# ============================================================================
# CARGA DE DATOS
# ============================================================================

def load_all_data():
    """
    Carga todos los CSVs generados en v9.1.
    
    Returns:
        dict: {group: {seed: DataFrame}}
    """
    data = {}
    
    for group in GROUPS:
        data[group] = {}
        for seed in SEEDS:
            csv_path = RESULTS_DIR / f"exp9_{group}_seed{seed}_episodes.csv"
            
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV no encontrado: {csv_path}")
            
            df = pd.read_csv(csv_path)
            
            # Validar estructura
            if len(df) != 300:
                raise ValueError(f"{csv_path.name}: esperado 300 filas, encontrado {len(df)}")
            
            data[group][seed] = df
            print(f"✓ Cargado: {csv_path.name} ({len(df)} episodios)")
    
    return data


def extract_final_metrics(data, window_size=50):
    """
    Extrae métricas de la ventana final de cada configuración.
    
    Args:
        data: dict {group: {seed: DataFrame}}
        window_size: Tamaño ventana final (default: 50)
    
    Returns:
        DataFrame con métricas agregadas por grupo y seed
    """
    metrics_list = []
    
    for group in GROUPS:
        for seed in SEEDS:
            df = data[group][seed]
            df_final = df.iloc[-window_size:]
            
            metrics_list.append({
                'group': group,
                'seed': seed,
                'mean_reward_env': df_final['total_reward_env'].mean(),
                'std_reward_env': df_final['total_reward_env'].std(),
                'mean_reward_shaped': df_final['total_reward_shaped'].mean(),
                'mean_tripwires': df_final['tripwires_triggered'].mean(),
                'total_tripwires': df_final['tripwires_triggered'].sum(),
                'mean_resources': df_final['resources_collected'].mean(),
                'mean_steps': df_final['steps_to_goal'].mean(),
                'success_rate': df_final['goal_reached'].mean(),
                'survival_rate': 1 - df_final['deaths_starvation'].mean(),
                'final_epsilon': df.iloc[-1]['epsilon']
            })
    
    return pd.DataFrame(metrics_list)


# ============================================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================================

def compute_cohens_d(group1, group2):
    """
    Calcula Cohen's d (effect size) entre dos grupos.
    
    Args:
        group1, group2: arrays de valores
    
    Returns:
        float: Cohen's d
    """
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    # Pooled standard deviation
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    # Cohen's d
    d = (np.mean(group1) - np.mean(group2)) / pooled_std
    
    return d


def bootstrap_ci(data, n_bootstrap=1000, ci=0.95):
    """
    Calcula bootstrap confidence interval.
    
    Args:
        data: array de valores
        n_bootstrap: número de resamples
        ci: nivel de confianza (default: 0.95)
    
    Returns:
        tuple: (lower, upper)
    """
    bootstrap_means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_means.append(np.mean(sample))
    
    alpha = 1 - ci
    lower = np.percentile(bootstrap_means, alpha/2 * 100)
    upper = np.percentile(bootstrap_means, (1 - alpha/2) * 100)
    
    return (lower, upper)


def paired_t_test(group1, group2, alternative='two-sided'):
    """
    Realiza t-test pareado (paired samples).
    
    Args:
        group1, group2: arrays de valores (mismo orden de seeds)
        alternative: 'two-sided', 'greater', 'less'
    
    Returns:
        dict con t-statistic, p-value, CI
    """
    if len(group1) != len(group2):
        raise ValueError("Grupos deben tener mismo tamaño para t-test pareado")
    
    # t-test pareado
    t_stat, p_value = stats.ttest_rel(group1, group2, alternative=alternative)
    
    # Confidence interval (95%)
    differences = np.array(group1) - np.array(group2)
    mean_diff = np.mean(differences)
    se_diff = stats.sem(differences)
    ci = stats.t.interval(0.95, len(differences) - 1, loc=mean_diff, scale=se_diff)
    
    return {
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'mean_difference': float(mean_diff),
        'ci_95_lower': float(ci[0]),
        'ci_95_upper': float(ci[1]),
        'significant': bool(p_value < 0.05)
    }


def wilcoxon_test(group1, group2, alternative='two-sided'):
    """
    Realiza Wilcoxon signed-rank test (no-paramétrico).
    
    Args:
        group1, group2: arrays de valores (mismo orden de seeds)
        alternative: 'two-sided', 'greater', 'less'
    
    Returns:
        dict con statistic, p-value
    """
    if len(group1) != len(group2):
        raise ValueError("Grupos deben tener mismo tamaño")
    
    # Wilcoxon signed-rank
    w_stat, p_value = stats.wilcoxon(group1, group2, alternative=alternative)
    
    return {
        'w_statistic': float(w_stat),
        'p_value': float(p_value),
        'significant': bool(p_value < 0.05)
    }


def analyze_h91_1_curriculum_threshold(metrics_df):
    """
    H9.1.1: Curriculum alcanza ratio ≥ 0.70 vs Control (N=10, powered).
    
    Args:
        metrics_df: DataFrame con métricas por grupo y seed
    
    Returns:
        dict con resultados H9.1.1
    """
    print("\n" + "="*70)
    print("H9.1.1: Curriculum ≥ 0.70 Threshold (N=10 Validación)")
    print("="*70)
    
    curriculum = metrics_df[metrics_df['group'] == 'Curriculum']['mean_reward_env'].values
    control = metrics_df[metrics_df['group'] == 'ControlS0']['mean_reward_env'].values
    
    # Calcular ratios por seed
    ratios = curriculum / control
    ratio_mean = np.mean(ratios)
    ratio_std = np.std(ratios, ddof=1)
    ratio_se = stats.sem(ratios)
    
    # Test one-sample t-test: ¿ratio > 0.70?
    t_stat, p_value = stats.ttest_1samp(ratios, 0.70, alternative='greater')
    
    # Confidence interval (parametric)
    ci = stats.t.interval(0.95, len(ratios) - 1, 
                          loc=ratio_mean, 
                          scale=ratio_se)
    
    # Bootstrap CI (robusto)
    bootstrap_ci_result = bootstrap_ci(ratios, n_bootstrap=1000)
    
    # % seeds exitosas (ratio ≥ 0.70)
    seeds_exitosas = np.sum(ratios >= 0.70)
    pct_exitosas = seeds_exitosas / len(ratios) * 100
    
    print(f"\nCurriculum rewards (N={len(curriculum)}): {curriculum}")
    print(f"Control rewards    (N={len(control)}):    {control}")
    print(f"\nRatios por seed: {ratios}")
    print(f"Ratio mean:      {ratio_mean:.3f} ± {ratio_std:.3f} (SE: {ratio_se:.3f})")
    print(f"95% CI param:    [{ci[0]:.3f}, {ci[1]:.3f}]")
    print(f"95% CI bootstrap:[{bootstrap_ci_result[0]:.3f}, {bootstrap_ci_result[1]:.3f}]")
    print(f"\nSeeds exitosas:  {seeds_exitosas}/{len(ratios)} ({pct_exitosas:.1f}%)")
    print(f"  Criterio:      ≥60% seeds con ratio≥0.70")
    
    print(f"\nt-test vs 0.70 (one-tailed):")
    print(f"  t-statistic:   {t_stat:.3f}")
    print(f"  p-value:       {p_value:.4f}")
    print(f"  Significant:   {p_value < 0.05}")
    
    # Interpretación
    threshold_met = ratio_mean >= 0.70 and ci[0] >= 0.70
    seeds_criterion = pct_exitosas >= 60
    
    if threshold_met and seeds_criterion:
        print(f"\n✅ H9.1.1 VALIDADA: Ratio {ratio_mean:.3f} ≥ 0.70, CI no cruza threshold, {pct_exitosas:.1f}% seeds exitosas")
    elif threshold_met:
        print(f"\n⚠️  H9.1.1 MARGINAL: Ratio {ratio_mean:.3f} ≥ 0.70 pero solo {pct_exitosas:.1f}% seeds exitosas")
    elif ratio_mean >= 0.70:
        print(f"\n⚠️  H9.1.1 MARGINAL: Ratio {ratio_mean:.3f} ≥ 0.70 pero CI cruza threshold")
    else:
        print(f"\n❌ H9.1.1 RECHAZADA: Ratio {ratio_mean:.3f} < 0.70")
    
    return {
        'hypothesis': 'H9.1.1',
        'description': 'Curriculum ≥ 0.70 ratio vs Control (N=10 powered)',
        'n_seeds': len(ratios),
        'curriculum_rewards': curriculum.tolist(),
        'control_rewards': control.tolist(),
        'ratios': ratios.tolist(),
        'ratio_mean': float(ratio_mean),
        'ratio_std': float(ratio_std),
        'ratio_se': float(ratio_se),
        'ci_95_parametric': [float(ci[0]), float(ci[1])],
        'ci_95_bootstrap': [float(bootstrap_ci_result[0]), float(bootstrap_ci_result[1])],
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'threshold': 0.70,
        'seeds_exitosas': int(seeds_exitosas),
        'pct_seeds_exitosas': float(pct_exitosas),
        'validated': threshold_met and seeds_criterion,
        'interpretation': 'VALIDATED' if (threshold_met and seeds_criterion) else 'MARGINAL' if threshold_met else 'REJECTED'
    }


def analyze_h92_1_curriculum_vs_control(metrics_df):
    """
    H9.2.1: Curriculum ≈ Control (equivalencia estadística, p<0.05).
    
    Args:
        metrics_df: DataFrame con métricas por grupo y seed
    
    Returns:
        dict con resultados H9.2.1
    """
    print("\n" + "="*70)
    print("H9.2.1: Curriculum ≈ Control (Equivalencia Estadística)")
    print("="*70)
    
    curriculum = metrics_df[metrics_df['group'] == 'Curriculum']['mean_reward_env'].values
    control = metrics_df[metrics_df['group'] == 'ControlS0']['mean_reward_env'].values
    
    # Paired t-test (two-tailed: diferencia significativa?)
    test_parametric = paired_t_test(curriculum, control, alternative='two-sided')
    
    # Wilcoxon (validación no-paramétrica)
    test_nonparametric = wilcoxon_test(curriculum, control, alternative='two-sided')
    
    # Effect size
    cohens_d = compute_cohens_d(curriculum, control)
    
    # Bootstrap CI para diferencia
    differences = curriculum - control
    bootstrap_ci_result = bootstrap_ci(differences, n_bootstrap=1000)
    
    print(f"\nCurriculum rewards: {curriculum}")
    print(f"Control rewards:    {control}")
    print(f"\nDifferences (Curr - Ctrl): {differences}")
    print(f"Mean difference:    {test_parametric['mean_difference']:.2f}")
    print(f"95% CI parametric:  [{test_parametric['ci_95_lower']:.2f}, {test_parametric['ci_95_upper']:.2f}]")
    print(f"95% CI bootstrap:   [{bootstrap_ci_result[0]:.2f}, {bootstrap_ci_result[1]:.2f}]")
    
    print(f"\nPaired t-test (two-tailed):")
    print(f"  t-statistic:      {test_parametric['t_statistic']:.3f}")
    print(f"  p-value:          {test_parametric['p_value']:.4f}")
    print(f"  Significant diff: {test_parametric['significant']}")
    
    print(f"\nWilcoxon signed-rank:")
    print(f"  W-statistic:      {test_nonparametric['w_statistic']:.1f}")
    print(f"  p-value:          {test_nonparametric['p_value']:.4f}")
    print(f"  Significant diff: {test_nonparametric['significant']}")
    
    print(f"\nEffect size:")
    print(f"  Cohen's d:        {cohens_d:.3f}")
    
    # Interpretación effect size
    if abs(cohens_d) < 0.2:
        effect_interpretation = "negligible"
    elif abs(cohens_d) < 0.5:
        effect_interpretation = "small"
    elif abs(cohens_d) < 0.8:
        effect_interpretation = "medium"
    else:
        effect_interpretation = "large"
    
    print(f"  Interpretation:   {effect_interpretation}")
    
    # Criterio equivalencia: p > 0.05 AND |d| < 0.5 (efecto pequeño)
    equivalence = not test_parametric['significant'] and abs(cohens_d) < 0.5
    
    if equivalence:
        print(f"\n✅ H9.2.1 VALIDADA: Curriculum ≈ Control (p={test_parametric['p_value']:.3f}, |d|={abs(cohens_d):.2f}<0.5)")
    elif not test_parametric['significant']:
        print(f"\n⚠️  H9.2.1 MARGINAL: No diferencia significativa (p={test_parametric['p_value']:.3f}) pero |d|={abs(cohens_d):.2f}≥0.5")
    else:
        print(f"\n❌ H9.2.1 RECHAZADA: Diferencia significativa (p={test_parametric['p_value']:.3f})")
    
    return {
        'hypothesis': 'H9.2.1',
        'description': 'Curriculum ≈ Control (equivalencia estadística)',
        'n_seeds': len(curriculum),
        'curriculum_rewards': curriculum.tolist(),
        'control_rewards': control.tolist(),
        'differences': differences.tolist(),
        'mean_difference': float(test_parametric['mean_difference']),
        'ci_95_parametric': [float(test_parametric['ci_95_lower']), float(test_parametric['ci_95_upper'])],
        'ci_95_bootstrap': [float(bootstrap_ci_result[0]), float(bootstrap_ci_result[1])],
        't_test': test_parametric,
        'wilcoxon_test': test_nonparametric,
        'cohens_d': float(cohens_d),
        'effect_interpretation': effect_interpretation,
        'validated': equivalence,
        'interpretation': 'VALIDATED' if equivalence else 'MARGINAL' if not test_parametric['significant'] else 'REJECTED'
    }


def analyze_h93_1_prudence(metrics_df):
    """
    H9.3.1: Curriculum mantiene prudencia (tripwires ≤ Control).
    
    Args:
        metrics_df: DataFrame con métricas por grupo y seed
    
    Returns:
        dict con resultados H9.3.1
    """
    print("\n" + "="*70)
    print("H9.3.1: Prudencia Mantenida (Tripwires)")
    print("="*70)
    
    curriculum = metrics_df[metrics_df['group'] == 'Curriculum']['mean_tripwires'].values
    control = metrics_df[metrics_df['group'] == 'ControlS0']['mean_tripwires'].values
    
    # Paired t-test (one-tailed: curriculum ≤ control)
    test_parametric = paired_t_test(curriculum, control, alternative='less')
    
    # Wilcoxon
    test_nonparametric = wilcoxon_test(curriculum, control, alternative='less')
    
    print(f"\nCurriculum tripwires: {curriculum}")
    print(f"Control tripwires:    {control}")
    print(f"\nCurriculum mean:      {np.mean(curriculum):.2f} ± {np.std(curriculum, ddof=1):.2f}")
    print(f"Control mean:         {np.mean(control):.2f} ± {np.std(control, ddof=1):.2f}")
    
    print(f"\nPaired t-test (curriculum < control):")
    print(f"  Mean difference:  {test_parametric['mean_difference']:.2f}")
    print(f"  t-statistic:      {test_parametric['t_statistic']:.3f}")
    print(f"  p-value:          {test_parametric['p_value']:.4f}")
    print(f"  Curriculum ≤ Ctrl:{test_parametric['significant']}")
    
    print(f"\nWilcoxon signed-rank:")
    print(f"  p-value:          {test_nonparametric['p_value']:.4f}")
    print(f"  Curriculum ≤ Ctrl:{test_nonparametric['significant']}")
    
    # Verificar prudencia mantenida
    prudence_maintained = test_parametric['mean_difference'] <= 0
    
    if prudence_maintained:
        print(f"\n✅ H9.3.1 VALIDADA: Curriculum prudente (tripwires ≤ Control)")
    else:
        print(f"\n❌ H9.3.1 RECHAZADA: Curriculum más tripwires que Control")
    
    return {
        'hypothesis': 'H9.3.1',
        'description': 'Curriculum mantiene prudencia (tripwires ≤ Control)',
        'curriculum_tripwires': curriculum.tolist(),
        'control_tripwires': control.tolist(),
        'curriculum_mean': float(np.mean(curriculum)),
        'control_mean': float(np.mean(control)),
        't_test': test_parametric,
        'wilcoxon_test': test_nonparametric,
        'validated': prudence_maintained,
        'interpretation': 'VALIDATED' if prudence_maintained else 'REJECTED'
    }


def analyze_h94_1_gradual_degradation(data):
    """
    H9.4.1: Degradación gradual, no colapso súbito (0/10 seeds colapsan).
    
    Args:
        data: dict {group: {seed: DataFrame}}
    
    Returns:
        dict con resultados H9.4.1
    """
    print("\n" + "="*70)
    print("H9.4.1: Degradación Gradual (No Colapso Súbito)")
    print("="*70)
    
    collapse_seeds = []
    
    for seed in SEEDS:
        df = data['Curriculum'][seed]
        
        # Analizar etapa 4 (s=1.0): episodios 225-300
        stage4 = df.iloc[225:300]
        success_rate_stage4 = stage4['goal_reached'].mean()
        
        # Criterio colapso: <10% success en etapa 4
        if success_rate_stage4 < 0.10:
            collapse_seeds.append(seed)
            print(f"  ⚠️  Seed {seed}: Success {success_rate_stage4:.1%} (COLAPSO)")
        else:
            print(f"  ✓ Seed {seed}: Success {success_rate_stage4:.1%}")
    
    n_collapses = len(collapse_seeds)
    pct_collapses = n_collapses / len(SEEDS) * 100
    
    print(f"\nTotal colapsos: {n_collapses}/{len(SEEDS)} ({pct_collapses:.1f}%)")
    print(f"  Criterio:     0/10 seeds colapsan (degradación gradual)")
    
    # Validación
    validated = n_collapses == 0
    
    if validated:
        print(f"\n✅ H9.4.1 VALIDADA: 0/10 seeds colapsan (degradación gradual)")
    elif n_collapses <= 2:
        print(f"\n⚠️  H9.4.1 MARGINAL: {n_collapses}/10 seeds colapsan (aceptable <20%)")
    else:
        print(f"\n❌ H9.4.1 RECHAZADA: {n_collapses}/10 seeds colapsan (≥20%)")
    
    return {
        'hypothesis': 'H9.4.1',
        'description': 'Degradación gradual, no colapso súbito',
        'n_seeds': len(SEEDS),
        'collapse_seeds': collapse_seeds,
        'n_collapses': n_collapses,
        'pct_collapses': float(pct_collapses),
        'validated': validated,
        'interpretation': 'VALIDATED' if validated else 'MARGINAL' if n_collapses <= 2 else 'REJECTED'
    }


def summary_decision_go_pause(results):
    """
    Decisión GO/PAUSE para v10 basada en resultados v9.1.
    
    Args:
        results: dict con resultados de todas las hipótesis
    
    Returns:
        dict con decisión y justificación
    """
    print("\n" + "="*70)
    print("⚠️  DECISIÓN CRÍTICA: GO/PAUSE v10")
    print("="*70)
    
    h91 = results['H9.1.1']
    h92 = results['H9.2.1']
    h93 = results['H9.3.1']
    h94 = results['H9.4.1']
    
    # Criterios GO
    ratio_ok = h91['ratio_mean'] >= 0.70
    seeds_ok = h91['pct_seeds_exitosas'] >= 60
    equivalence_ok = h92['validated'] or not h92['t_test']['significant']
    prudence_ok = h93['validated']
    no_collapse = h94['n_collapses'] <= 2
    
    print(f"\nCriterios evaluados:")
    print(f"  1. Ratio ≥ 0.70:           {'✅' if ratio_ok else '❌'} ({h91['ratio_mean']:.3f})")
    print(f"  2. ≥60% seeds exitosas:    {'✅' if seeds_ok else '❌'} ({h91['pct_seeds_exitosas']:.1f}%)")
    print(f"  3. Curriculum ≈ Control:   {'✅' if equivalence_ok else '❌'} (p={h92['t_test']['p_value']:.3f})")
    print(f"  4. Prudencia mantenida:    {'✅' if prudence_ok else '❌'}")
    print(f"  5. No colapso (≤2 seeds):  {'✅' if no_collapse else '❌'} ({h94['n_collapses']}/10)")
    
    # Decisión
    criteria_met = sum([ratio_ok, seeds_ok, equivalence_ok, prudence_ok, no_collapse])
    
    if criteria_met >= 4:
        decision = "GO"
        color = "🟢"
        justification = f"Criterios {criteria_met}/5 validados. Curriculum robusto, proceder con v10 Adaptive 8×8."
    elif criteria_met >= 3:
        decision = "GO_PRECAUCION"
        color = "🟡"
        justification = f"Criterios {criteria_met}/5 validados. Curriculum marginal, v10 adaptive crítico para rescate."
    else:
        decision = "PAUSE"
        color = "🔴"
        justification = f"Criterios {criteria_met}/5 validados. Insuficiente evidencia, investigar antes v10."
    
    print(f"\n{color} DECISIÓN: {decision}")
    print(f"   Justificación: {justification}")
    
    return {
        'decision': decision,
        'criteria_met': criteria_met,
        'criteria_total': 5,
        'ratio_ok': ratio_ok,
        'seeds_ok': seeds_ok,
        'equivalence_ok': equivalence_ok,
        'prudence_ok': prudence_ok,
        'no_collapse': no_collapse,
        'justification': justification
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Ejecuta análisis completo v9.1."""
    
    print("="*70)
    print("ANÁLISIS ESTADÍSTICO v9.1: Validación N=10 Curriculum Learning")
    print("="*70)
    print(f"Input:  {RESULTS_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"N seeds: {len(SEEDS)}")
    print(f"Grupos: {GROUPS}")
    
    # 1. Cargar datos
    print("\n[1/6] Cargando datos...")
    data = load_all_data()
    
    # 2. Extraer métricas finales
    print("\n[2/6] Extrayendo métricas finales (últimos 50 eps)...")
    metrics_df = extract_final_metrics(data, window_size=FINAL_WINDOW_SIZE)
    
    # Guardar métricas
    metrics_csv = OUTPUT_DIR / 'v9_1_final_metrics.csv'
    metrics_df.to_csv(metrics_csv, index=False)
    print(f"✓ Guardado: {metrics_csv}")
    
    # 3. Análisis hipótesis
    print("\n[3/6] Analizando hipótesis...")
    
    results = {}
    
    # H9.1.1: Threshold
    results['H9.1.1'] = analyze_h91_1_curriculum_threshold(metrics_df)
    
    # H9.2.1: Equivalencia
    results['H9.2.1'] = analyze_h92_1_curriculum_vs_control(metrics_df)
    
    # H9.3.1: Prudencia
    results['H9.3.1'] = analyze_h93_1_prudence(metrics_df)
    
    # H9.4.1: Degradación gradual
    results['H9.4.1'] = analyze_h94_1_gradual_degradation(data)
    
    # 4. Decisión GO/PAUSE
    print("\n[4/6] Evaluando decisión GO/PAUSE v10...")
    results['decision_v10'] = summary_decision_go_pause(results)
    
    # 5. Guardar resultados
    print("\n[5/6] Guardando resultados...")
    results_json = OUTPUT_DIR / 'v9_1_statistical_analysis.json'
    with open(results_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)
    print(f"✓ Guardado: {results_json}")
    
    # 6. Resumen final
    print("\n[6/6] Resumen final")
    print("="*70)
    print(f"Hipótesis validadas: {sum([r['validated'] for r in [results['H9.1.1'], results['H9.2.1'], results['H9.3.1'], results['H9.4.1']]])}/4")
    print(f"Decisión v10:        {results['decision_v10']['decision']}")
    print(f"Archivos generados:")
    print(f"  - {metrics_csv}")
    print(f"  - {results_json}")
    
    print("\n✅ Análisis v9.1 completado")
    
    return results


if __name__ == '__main__':
    main()
