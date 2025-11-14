"""
Funciones científicas avanzadas para visualización y análisis en la GUI TUI v4.1
Incluye: intervalos de confianza, t-test, ANOVA, interpretación automática bilingüe, heatmaps, dashboards y resúmenes tabulares.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, f_oneway, sem

def confidence_interval(data, alpha=0.95):
    arr = np.array(data)
    arr = arr[~np.isnan(arr)]
    mean = np.nanmean(arr)
    s = sem(arr)
    from scipy.stats import t
    ci = t.interval(alpha, len(arr)-1, loc=mean, scale=s) if len(arr) > 1 else (mean, mean)
    return mean, ci

def plot_heatmap(data, row_labels, col_labels, title):
    fig, ax = plt.subplots(figsize=(8,4))
    sns.heatmap(data, cmap='coolwarm', annot=True, fmt='.1f', cbar=True, yticklabels=row_labels, xticklabels=col_labels)
    ax.set_title(title)
    return fig

def plot_dashboard(metrics_dict):
    df = pd.DataFrame(metrics_dict)
    fig, ax = plt.subplots(figsize=(10,4))
    df.plot(kind='bar', ax=ax)
    ax.set_title('Dashboard de métricas / Metrics dashboard')
    ax.set_ylabel('Valor / Value')
    return fig

def scientific_report(results_A, results_B, label_A='Control', label_B='Simbiosis'):
    report = []
    # Intervalos de confianza
    for metric in ['flex_recov', 'robust_evol', 'q_optimal_evol', 'total_rewards', 'tripwire_steps']:
        mean_A, ci_A = confidence_interval(results_A[metric])
        mean_B, ci_B = confidence_interval(results_B[metric])
        report.append(f"{metric}: {label_A} {mean_A:.2f} ± {ci_A[1]-mean_A:.2f} | {label_B} {mean_B:.2f} ± {ci_B[1]-mean_B:.2f}")
    # t-test y ANOVA
    for metric in ['flex_recov', 'robust_evol', 'q_optimal_evol']:
        t_res = ttest_ind(results_A[metric], results_B[metric])
        report.append(f"t-test {metric}: p={t_res.pvalue:.4f}")
        anova_res = f_oneway(results_A[metric], results_B[metric])
        report.append(f"ANOVA {metric}: p={anova_res.pvalue:.4f}")
    # Interpretación automática
    report.append('Si p < 0.05, la diferencia entre agentes es significativa. / If p < 0.05, difference is significant.')
    return '\n'.join(report)
