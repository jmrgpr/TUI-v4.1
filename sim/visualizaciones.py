"""
visualizaciones.py — Funciones avanzadas de visualización para TUI v4.1
Advanced visualization functions for TUI v4.1

Incluye:
- Curvas de riesgo comparativas
- Boxplots y heatmaps por agente y risk_scale
- Evolución temporal de métricas
- Intervalos de confianza, t-test, ANOVA
- Interpretación automática bilingüe
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def curva_riesgo_comparativa(riesgo_control, riesgo_simbiosis, export_path=None):
    """
    Grafica curvas de riesgo comparativas entre agentes (Control vs Simbiosis).
    Plots comparative risk curves between agents (Control vs Symbiosis).

    Ejemplo / Example:
    >>> curva_riesgo_comparativa(riesgo_control, riesgo_simbiosis, export_path='results/risk_curves.png')
    """
    plt.figure(figsize=(10,6))
    plt.plot(np.nanmean(riesgo_control, axis=0), label='Control', color='blue')
    plt.plot(np.nanmean(riesgo_simbiosis, axis=0), label='Simbiosis', color='red')
    plt.fill_between(range(len(riesgo_control[0])),
                     np.nanmean(riesgo_control, axis=0) - stats.sem(riesgo_control, axis=0, nan_policy='omit'),
                     np.nanmean(riesgo_control, axis=0) + stats.sem(riesgo_control, axis=0, nan_policy='omit'),
                     color='blue', alpha=0.2)
    plt.fill_between(range(len(riesgo_simbiosis[0])),
                     np.nanmean(riesgo_simbiosis, axis=0) - stats.sem(riesgo_simbiosis, axis=0, nan_policy='omit'),
                     np.nanmean(riesgo_simbiosis, axis=0) + stats.sem(riesgo_simbiosis, axis=0, nan_policy='omit'),
                     color='red', alpha=0.2)
    plt.title('Curvas de riesgo comparativas / Comparative risk curves')
    plt.xlabel('Paso / Step')
    plt.ylabel('Riesgo / Risk')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    interp = 'Simbiosis supera a Control si la curva roja está por debajo de la azul. / Symbiosis outperforms Control if the red curve is below the blue.'
    plt.figtext(0.5, 0.01, interp, ha='center', fontsize=10, color='darkgreen')
    if export_path:
        plt.savefig(export_path, dpi=200)
    plt.close()

def boxplot_metricas(metricas_control, metricas_simbiosis, nombre, export_path=None):
    """
    Boxplot comparativo de métricas entre agentes.
    Comparative boxplot of metrics between agents.

    Ejemplo / Example:
    >>> boxplot_metricas(flex_control, flex_simbiosis, 'Flexibilidad', export_path='results/boxplot_flex.png')
    """
    plt.figure(figsize=(8,5))
    data = [metricas_control, metricas_simbiosis]
    plt.boxplot(data, labels=['Control','Simbiosis'])
    plt.title(f'Boxplot {nombre} / {nombre} Boxplot')
    plt.ylabel(nombre)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    interp = f'Mediana más alta indica mejor desempeño en {nombre}. / Higher median indicates better {nombre} performance.'
    plt.figtext(0.5, 0.01, interp, ha='center', fontsize=10, color='darkblue')
    if export_path:
        plt.savefig(export_path, dpi=200)
    plt.close()

def heatmap_metricas(matriz, etiquetas, nombre, export_path=None):
    """
    Heatmap de métricas agregadas por agente y risk_scale.
    Heatmap of aggregated metrics by agent and risk_scale.

    Ejemplo / Example:
    >>> heatmap_metricas(matriz_robustez, etiquetas, 'Robustez', export_path='results/heatmap_robust.png')
    """
    plt.figure(figsize=(10,6))
    sns.heatmap(matriz, annot=True, fmt='.2f', cmap='coolwarm', xticklabels=etiquetas['x'], yticklabels=etiquetas['y'])
    plt.title(f'Heatmap {nombre} / {nombre} Heatmap')
    plt.tight_layout()
    interp = f'Colores más intensos indican mayor {nombre}. / More intense colors indicate higher {nombre}.'
    plt.figtext(0.5, 0.01, interp, ha='center', fontsize=10, color='darkred')
    if export_path:
        plt.savefig(export_path, dpi=200)
    plt.close()

def analisis_estadistico(metricas_control, metricas_simbiosis, nombre):
    """
    Realiza t-test y ANOVA entre agentes, con interpretación bilingüe.
    Performs t-test and ANOVA between agents, with bilingual interpretation.

    Ejemplo / Example:
    >>> analisis_estadistico(flex_control, flex_simbiosis, 'Flexibilidad')
    """
    ttest = stats.ttest_ind(metricas_control, metricas_simbiosis, nan_policy='omit')
    anova = stats.f_oneway(metricas_control, metricas_simbiosis)
    print(f"t-test {nombre}: p={ttest.pvalue:.4f}")
    print(f"ANOVA {nombre}: p={anova.pvalue:.4f}")
    print('Interpretación: Si p < 0.05, la diferencia entre agentes es significativa. / If p < 0.05, difference between agents is significant.')

def dashboard_metricas(metricas_dict, export_path=None):
    """
    Muestra y exporta dashboard resumen de métricas agregadas (mean, std, CI) por agente y risk_scale.
    Shows and exports dashboard summary of aggregated metrics (mean, std, CI) by agent and risk_scale.

    Ejemplo / Example:
    >>> dashboard_metricas(metricas_dict, export_path='results/dashboard_metricas.csv')
    >>> dashboard_metricas(metricas_dict, export_path='results/dashboard_metricas.json')
    """
    import csv, json
    resumen = {}
    print("\n=== Dashboard de métricas agregadas / Aggregated metrics dashboard ===")
    for agente, metricas in metricas_dict.items():
        resumen[agente] = {}
        for nombre, valores in metricas.items():
            arr = np.array(valores)
            arr = arr[~np.isnan(arr)]
            mean = np.nanmean(arr)
            std = np.nanstd(arr)
            ci = stats.t.interval(0.95, len(arr)-1, loc=mean, scale=stats.sem(arr)) if len(arr) > 1 else (mean, mean)
            resumen[agente][nombre] = {'mean': mean, 'std': std, 'ci': ci}
            print(f"{agente} | {nombre}: media={mean:.2f}, std={std:.2f}, CI=({ci[0]:.2f}, {ci[1]:.2f})")
    print("Interpretación bilingüe: La media y el intervalo de confianza permiten comparar desempeño y robustez entre agentes. / Mean and confidence interval allow comparison of performance and robustness between agents.")
    if export_path:
        if export_path.endswith('.csv'):
            with open(export_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Agente','Métrica','Media','STD','CI_inf','CI_sup'])
                for agente, metricas in resumen.items():
                    for nombre, vals in metricas.items():
                        writer.writerow([agente, nombre, vals['mean'], vals['std'], vals['ci'][0], vals['ci'][1]])
        elif export_path.endswith('.json'):
            with open(export_path, 'w') as f:
                json.dump(resumen, f, indent=2)
