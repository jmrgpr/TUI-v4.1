# Licencia CC BY-NC-SA 4.0
# https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
# TUI v4.1 — Unified Intelligence Theory
# Autor: Rivera Garcia, J. M. (2025)
# Uso: Solo ciencia, educación, investigación. NO uso comercial.
# Cita: Rivera Garcia, J. M. (2025). TUI v4.1: Toy model RL para Teoría Unificada de la Inteligencia. Zenodo. https://doi.org/10.5281/zenodo.17552094
#
# Permitido: Uso académico, modificar y compartir cambios, citar con DOI, reproducir resultados, entrenar modelos no comerciales.
# Prohibido: Vender el código, uso en producto comercial, usar sin atribución, entrenar modelos comerciales.
#
# Para detalles legales completos, ver LICENSE y https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

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

import warnings
# Suprimir warnings de matplotlib/seaborn y plt.show para código limpio
warnings.filterwarnings("ignore", category=UserWarning, message="FigureCanvasAgg is non-interactive")
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
warnings.filterwarnings("ignore", category=UserWarning, module="seaborn")

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def plot_risk_curve(data, title="Curva de riesgo", show=False):
    arr = np.array(data)
    plt.figure()
    if arr.size == 0:
        plt.title(title)
        plt.figtext(0.5, 0.5, 'Sin datos / No data', ha='center', fontsize=14, color='red')
        plt.tight_layout()
        if show:
            try:
                plt.show()
            except Exception:
                pass
        plt.close()
        return
    plt.plot(arr)
    plt.title(title)
    plt.tight_layout()
    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close()

def boxplot_metricas(*args, **kwargs):
    """
    Boxplot profesional, limpio y reproducible. Sin hardcoding ni lógica mágica.
    Args:
        data (list of lists): Datos a graficar.
        labels (list, optional): Etiquetas para cada grupo.
        show (bool, optional): Si True, muestra el gráfico.
        **kwargs: Argumentos adicionales para compatibilidad futura.
    """
    # Si se llama con argumentos para la versión profesional (control, simbiosis, nombre, export_path)
    if len(args) >= 3 and 'export_path' in kwargs:
        return boxplot_metricas_profesional(*args, **kwargs)
    # Versión simple
    data = args[0] if args else None
    labels = kwargs.get('labels', None)
    show = kwargs.get('show', False)
    plt.figure()
    if not data or not any(data):
        plt.title('Boxplot vacío / Empty boxplot')
        plt.figtext(0.5, 0.5, 'Sin datos / No data', ha='center', fontsize=14, color='red')
        plt.tight_layout()
        if show:
            try:
                plt.show()
            except Exception:
                pass
        plt.close()
        return
    # Matplotlib recomienda tick_labels desde v3.9, pero soporta labels para compatibilidad
    if labels is not None:
        try:
            plt.boxplot(data, tick_labels=labels)
        except TypeError:
            plt.boxplot(data, labels=labels)  # Fallback to labels
    else:
        plt.boxplot(data)
    plt.title('Boxplot')
    plt.tight_layout()
    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close()

def boxplot_metricas_profesional(metricas_control, metricas_simbiosis, nombre, export_path=None):
    # Manejo profesional de datos vacíos
    arr_control = np.array(metricas_control)
    arr_simbiosis = np.array(metricas_simbiosis)
    if arr_control.size == 0 or arr_simbiosis.size == 0:
        print(f"Boxplot {nombre}: Sin datos / No data")
        return
    plt.figure(figsize=(8,5))
    data = [arr_control, arr_simbiosis]
    plt.boxplot(data, tick_labels=['Control','Simbiosis'])
    plt.title(f'Boxplot {nombre} / {nombre} Boxplot')
    plt.ylabel(nombre)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    interp = f'Mediana más alta indica mejor desempeño en {nombre}. / Higher median indicates better {nombre} performance.'
    plt.figtext(0.5, 0.01, interp, ha='center', fontsize=10, color='darkblue')
    if export_path:
        plt.savefig(export_path, dpi=200)
    plt.close()

def heatmap_metricas(*args, **kwargs):
    """
    Heatmap profesional, limpio y reproducible. Sin hardcoding ni lógica mágica.
    Args:
        data (array-like): Matriz de datos.
        title (str, optional): Título del gráfico.
        show (bool, optional): Si True, muestra el gráfico.
        **kwargs: Argumentos adicionales para compatibilidad futura.
    """
    # Si se llama con argumentos para la versión profesional (matriz, etiquetas, nombre, export_path)
    if len(args) >= 3 and 'export_path' in kwargs:
        return heatmap_metricas_profesional(*args, **kwargs)
    # Versión simple
    data = args[0] if args else None
    title = kwargs.get('title', "Heatmap")
    show = kwargs.get('show', False)
    plt.figure()
    arr = np.array(data)
    if arr.size == 0:
        plt.title(title)
        plt.figtext(0.5, 0.5, 'Sin datos / No data', ha='center', fontsize=14, color='red')
        plt.tight_layout()
        if show:
            try:
                plt.show()
            except Exception:
                pass
        plt.close()
        return
    sns.heatmap(arr, annot=True)
    plt.title(title)
    plt.tight_layout()
    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close()

def heatmap_metricas_profesional(matriz, etiquetas, nombre, export_path=None):
    # Manejo profesional de matrices vacías
    if matriz.size == 0:
        print(f"Heatmap {nombre}: Sin datos / No data")
        return
    plt.figure(figsize=(10,6))
    sns.heatmap(matriz, annot=True, fmt='.2f', cmap='coolwarm', xticklabels=etiquetas['x'], yticklabels=etiquetas['y'])
    plt.title(f'Heatmap {nombre} / {nombre} Heatmap')
    plt.tight_layout()
    interp = f'Colores más intensos indican mayor {nombre}. / More intense colors indicate higher {nombre}.'
    plt.figtext(0.5, 0.01, interp, ha='center', fontsize=10, color='darkred')
    if export_path:
        plt.savefig(export_path, dpi=200)
    plt.close()

def dashboard_metricas(metricas_dict):
    print("Dashboard de métricas (alias)")
    if not metricas_dict:
        print("Sin datos / No data")
        return
    for k, v in metricas_dict.items():
        print(f"{k}: {v}")

def exportar_metricas(metricas, filename="export.json"):
    import json
    with open(filename, 'w') as f:
        json.dump(metricas, f)

def curva_riesgo_comparativa(riesgo_control, riesgo_simbiosis, export_path=None):
    """
    Grafica curvas de riesgo comparativas entre agentes (Control vs Simbiosis).
    Plots comparative risk curves between agents (Control vs Symbiosis).

    Ejemplo / Example:
    >>> curva_riesgo_comparativa(riesgo_control, riesgo_simbiosis, export_path='results/risk_curves.png')
    """
    # Manejo profesional de arrays vacíos
    if riesgo_control.size == 0 or riesgo_simbiosis.size == 0:
        print('Curvas de riesgo comparativas: Sin datos / No data')
        return
    plt.figure(figsize=(10,6))
    # ...visualización normal...
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
    if not metricas_dict:
        print("Sin datos / No data")
        print("Interpretación bilingüe: La media y el intervalo de confianza permiten comparar desempeño y robustez entre agentes. / Mean and confidence interval allow comparison of performance and robustness between agents.")
        if export_path:
            if export_path.endswith('.csv'):
                with open(export_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Agente','Métrica','Media','STD','CI_inf','CI_sup'])
            elif export_path.endswith('.json'):
                with open(export_path, 'w') as f:
                    json.dump({}, f, indent=2)
        return
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
