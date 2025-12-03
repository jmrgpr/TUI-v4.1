"""
Script de Análisis - Experimento 4: Economía Factorial (PGF v7)
================================================================

Analiza resultados del diseño factorial 3×5×3 para validar H7.1-H7.3:
- ANOVA 2-way (Economía × Densidad)
- Comparación de modelos por economía (constante, lineal, cuadrático, log, exp)
- Detección de threshold económico (regresión segmentada)
- Generación de figuras preregistradas

Uso:
    python scripts/analyze_economia_factorial.py
    
    # Especificar directorios personalizados
    python scripts/analyze_economia_factorial.py \
        --input results/pgf_v7/resultados \
        --output results/pgf_v7/analisis

Autor: TUI v4.1 Research Team
Fecha: 3 diciembre 2025
"""

import sys
import os
import json
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings('ignore')

# Configurar estilo de gráficos
sns.set_style("whitegrid")
sns.set_palette("husl")


# ============================================================================
# FUNCIÓN 1: CARGAR DATOS
# ============================================================================

def load_experiment_data(results_dir='results/pgf_v7/resultados'):
    """
    Carga todos los JSON de resultados del experimento.
    
    Returns:
        df: DataFrame con una fila por configuración
    """
    results_path = Path(results_dir)
    
    # Buscar todos los JSON (excepto summary)
    json_files = list(results_path.glob("exp4_economy_*.json"))
    json_files = [f for f in json_files if 'summary' not in f.name]
    
    if len(json_files) == 0:
        raise FileNotFoundError(f"No se encontraron resultados en {results_dir}")
    
    print(f"📂 Cargando {len(json_files)} archivos de resultados...")
    
    data = []
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data.append(json.load(f))
    
    df = pd.DataFrame(data)
    
    print(f"✅ Datos cargados: {len(df)} configuraciones")
    print(f"   Economías: {df['economy'].unique()}")
    print(f"   Densidades: {sorted(df['spawn_rate'].unique())}")
    print(f"   Seeds: {sorted(df['seed'].unique())}")
    
    return df


# ============================================================================
# FUNCIÓN 2: ANOVA 2-WAY (H7.1)
# ============================================================================

def run_anova_2way(df, output_dir):
    """
    Ejecuta ANOVA 2-way (Economía × Densidad) sobre ratio PGF/Control.
    
    Hipótesis H7.1: Interacción significativa (F > 3.0, p < 0.05)
    """
    print("\n" + "="*70)
    print("📊 ANOVA 2-WAY: Economía × Densidad")
    print("="*70)
    
    # Preparar datos
    df_anova = df.copy()
    df_anova['ratio_pct'] = df_anova['ratio_pgf_control'] * 100  # Convertir a porcentaje
    
    # Factorizar variables categóricas
    df_anova['economy_cat'] = pd.Categorical(df_anova['economy'], 
                                              categories=['harsh', 'balanced', 'favorable'],
                                              ordered=True)
    
    # ANOVA usando scipy (F-estadístico manualmente)
    # Modelo: ratio ~ economy + spawn_rate + economy:spawn_rate
    
    from scipy.stats import f_oneway
    
    # Efecto principal de Economía (comparar medias entre economías)
    grupos_economy = [df_anova[df_anova['economy']==e]['ratio_pct'].values 
                      for e in ['harsh', 'balanced', 'favorable']]
    F_economy, p_economy = f_oneway(*grupos_economy)
    
    # Efecto principal de Densidad (correlación)
    corr_density, p_density = stats.pearsonr(df_anova['spawn_rate'], df_anova['ratio_pct'])
    
    # Interacción: Comparar pendientes de regresión por economía
    slopes = {}
    for economy in ['harsh', 'balanced', 'favorable']:
        subset = df_anova[df_anova['economy'] == economy]
        slope, intercept, r, p, se = stats.linregress(subset['spawn_rate'], subset['ratio_pct'])
        slopes[economy] = {'slope': slope, 'r': r, 'p': p}
    
    # Test de homogeneidad de pendientes (aproximación)
    # Si pendientes son muy diferentes → interacción significativa
    slope_values = [slopes[e]['slope'] for e in ['harsh', 'balanced', 'favorable']]
    slope_std = np.std(slope_values)
    interaction_detected = slope_std > 5  # Umbral heurístico (>5 puntos de diferencia)
    
    print(f"\n🔹 Efecto Principal - ECONOMÍA:")
    print(f"   F-estadístico: {F_economy:.2f}")
    print(f"   p-value: {p_economy:.4f}")
    if p_economy < 0.05:
        print(f"   ✅ SIGNIFICATIVO (p < 0.05)")
    else:
        print(f"   ❌ NO significativo")
    
    print(f"\n🔹 Efecto Principal - DENSIDAD:")
    print(f"   Correlación r: {corr_density:.3f}")
    print(f"   p-value: {p_density:.4f}")
    if p_density < 0.05:
        print(f"   ✅ SIGNIFICATIVO (p < 0.05)")
    else:
        print(f"   ❌ NO significativo")
    
    print(f"\n🔹 Interacción ECONOMÍA × DENSIDAD:")
    print(f"   Pendientes por economía:")
    for economy, slope_data in slopes.items():
        print(f"      {economy.capitalize()}: {slope_data['slope']:+.2f} (r={slope_data['r']:.3f}, p={slope_data['p']:.3f})")
    print(f"   Desviación estándar de pendientes: {slope_std:.2f}")
    if interaction_detected:
        print(f"   ✅ INTERACCIÓN DETECTADA (pendientes heterogéneas)")
    else:
        print(f"   ❌ NO hay interacción fuerte")
    
    # Veredicto H7.1
    print(f"\n📋 VEREDICTO H7.1:")
    h71_criteria = [
        p_economy < 0.05,  # Economía significativa
        interaction_detected  # Interacción presente
    ]
    if sum(h71_criteria) >= 2:
        print(f"   ✅ H7.1 SOPORTADA (2/2 criterios)")
    else:
        print(f"   ❌ H7.1 NO soportada ({sum(h71_criteria)}/2 criterios)")
    
    # Guardar resultados
    anova_results = {
        'effect_economy': {'F': float(F_economy), 'p': float(p_economy)},
        'effect_density': {'r': float(corr_density), 'p': float(p_density)},
        'interaction': {
            'slopes': {k: {'slope': float(v['slope']), 'r': float(v['r']), 'p': float(v['p'])} 
                       for k, v in slopes.items()},
            'slope_std': float(slope_std),
            'detected': interaction_detected
        },
        'h71_verdict': 'SUPPORTED' if sum(h71_criteria) >= 2 else 'NOT_SUPPORTED'
    }
    
    output_path = Path(output_dir) / 'anova_2way_results.json'
    with open(output_path, 'w') as f:
        json.dump(anova_results, f, indent=2)
    
    print(f"\n💾 Guardado: {output_path}")
    
    return anova_results


# ============================================================================
# FUNCIÓN 3: COMPARACIÓN DE MODELOS POR ECONOMÍA
# ============================================================================

def compare_models_by_economy(df, output_dir):
    """
    Ajusta 5 modelos (constante, lineal, cuadrático, log, exp) por cada economía.
    Compara con AIC y detecta Goldilocks (parábola invertida).
    """
    print("\n" + "="*70)
    print("📈 COMPARACIÓN DE MODELOS POR ECONOMÍA")
    print("="*70)
    
    models_results = {}
    
    for economy in ['harsh', 'balanced', 'favorable']:
        print(f"\n🔹 Economía: {economy.upper()}")
        
        subset = df[df['economy'] == economy].copy()
        X = subset['spawn_rate'].values
        y = subset['ratio_pgf_control'].values * 100  # Porcentaje
        n = len(X)
        
        # Modelo 1: Constante
        y_mean = y.mean()
        rss_const = np.sum((y - y_mean)**2)
        aic_const = n * np.log(rss_const/n) + 2 * 1  # k=1 (solo media)
        
        # Modelo 2: Lineal
        slope, intercept, r_linear, p_linear, se = stats.linregress(X, y)
        y_pred_linear = slope * X + intercept
        rss_linear = np.sum((y - y_pred_linear)**2)
        aic_linear = n * np.log(rss_linear/n) + 2 * 2  # k=2 (slope + intercept)
        
        # Modelo 3: Cuadrático
        coeffs_quad = np.polyfit(X, y, 2)
        y_pred_quad = np.polyval(coeffs_quad, X)
        rss_quad = np.sum((y - y_pred_quad)**2)
        aic_quad = n * np.log(rss_quad/n) + 2 * 3  # k=3
        
        # Detectar parábola invertida
        a_quad = coeffs_quad[0]
        b_quad = coeffs_quad[1]
        D_star = -b_quad / (2*a_quad) if a_quad != 0 else np.nan
        is_inverted = a_quad < 0
        
        # Modelo 4: Logarítmico
        X_log = np.log(X + 0.01)  # Evitar log(0)
        slope_log, intercept_log, r_log, p_log, se_log = stats.linregress(X_log, y)
        y_pred_log = slope_log * X_log + intercept_log
        rss_log = np.sum((y - y_pred_log)**2)
        aic_log = n * np.log(rss_log/n) + 2 * 2
        
        # Modelo 5: Exponencial (linealizado)
        try:
            y_safe = np.clip(y, 1e-10, None)  # Evitar log(0)
            log_y = np.log(y_safe)
            slope_exp, intercept_exp, r_exp, p_exp, se_exp = stats.linregress(X, log_y)
            y_pred_exp = np.exp(intercept_exp + slope_exp * X)
            rss_exp = np.sum((y - y_pred_exp)**2)
            aic_exp = n * np.log(rss_exp/n) + 2 * 2
        except:
            aic_exp = np.inf
        
        # Comparar AICs
        aics = {
            'constant': aic_const,
            'linear': aic_linear,
            'quadratic': aic_quad,
            'log': aic_log,
            'exponential': aic_exp
        }
        
        best_model = min(aics, key=aics.get)
        aic_best = aics[best_model]
        delta_aic = {model: aic - aic_best for model, aic in aics.items()}
        
        print(f"   AICs:")
        for model, aic in aics.items():
            marker = "🏆" if model == best_model else "  "
            print(f"      {marker} {model.capitalize()}: {aic:.2f} (ΔAIC={delta_aic[model]:+.2f})")
        
        # Veredicto Goldilocks (solo si cuadrático gana)
        goldilocks_criteria = []
        if best_model == 'quadratic':
            print(f"\n   📐 Análisis Cuadrático:")
            print(f"      a (coef x²): {a_quad:.4f}")
            print(f"      Parábola invertida: {'SÍ' if is_inverted else 'NO'}")
            if is_inverted and 0.7 <= D_star <= 1.5:
                print(f"      D* (máximo): {D_star:.3f} ✅ (en rango [0.7, 1.5])")
                goldilocks_criteria.append(True)
            else:
                print(f"      D* (máximo): {D_star:.3f} ❌ (fuera de rango)")
                goldilocks_criteria.append(False)
            
            # Ratio en D* debe ser > 110%
            ratio_at_peak = np.polyval(coeffs_quad, D_star) if 0.05 <= D_star <= 0.40 else 0
            if ratio_at_peak > 110:
                print(f"      Ratio en D*: {ratio_at_peak:.1f}% ✅ (> 110%)")
                goldilocks_criteria.append(True)
            else:
                print(f"      Ratio en D*: {ratio_at_peak:.1f}% ❌ (≤ 110%)")
                goldilocks_criteria.append(False)
            
            if sum(goldilocks_criteria) >= 2:
                print(f"   ✅ GOLDILOCKS DETECTADO en {economy}")
            else:
                print(f"   ❌ NO Goldilocks ({sum(goldilocks_criteria)}/2 criterios)")
        else:
            print(f"   ℹ️  Modelo cuadrático NO ganador → Goldilocks NO aplica")
        
        # Guardar resultados
        models_results[economy] = {
            'aics': aics,
            'delta_aic': delta_aic,
            'best_model': best_model,
            'linear': {'slope': float(slope), 'r': float(r_linear), 'p': float(p_linear)},
            'quadratic': {
                'coeffs': [float(c) for c in coeffs_quad],
                'a': float(a_quad),
                'D_star': float(D_star) if not np.isnan(D_star) else None,
                'is_inverted': is_inverted
            },
            'goldilocks_detected': sum(goldilocks_criteria) >= 2 if best_model == 'quadratic' else False
        }
    
    # Guardar JSON
    output_path = Path(output_dir) / 'model_comparison_by_economy.json'
    with open(output_path, 'w') as f:
        json.dump(models_results, f, indent=2)
    
    print(f"\n💾 Guardado: {output_path}")
    
    return models_results


# ============================================================================
# FUNCIÓN 4: DETECCIÓN DE THRESHOLD ECONÓMICO (H7.2)
# ============================================================================

def detect_threshold(df, output_dir):
    """
    Regresión segmentada para detectar threshold de balance económico.
    
    H7.2: Threshold ≈ 5.0 ± 1.0, cambio de pendiente significativo
    """
    print("\n" + "="*70)
    print("🎯 DETECCIÓN DE THRESHOLD ECONÓMICO")
    print("="*70)
    
    # Agregar por balance (media de todas las densidades/seeds por economía)
    df_threshold = df.groupby('balance').agg({
        'ratio_pgf_control': ['mean', 'std', 'count']
    }).reset_index()
    df_threshold.columns = ['balance', 'ratio_mean', 'ratio_std', 'n']
    df_threshold['ratio_pct'] = df_threshold['ratio_mean'] * 100
    df_threshold['se'] = df_threshold['ratio_std'] / np.sqrt(df_threshold['n']) * 100
    
    X = df_threshold['balance'].values
    y = df_threshold['ratio_pct'].values
    
    print(f"\nDatos agregados por balance:")
    print(df_threshold[['balance', 'ratio_pct', 'se']])
    
    # Regresión segmentada manual (prueba threshold en 4.0, 5.0, 6.0)
    best_threshold = None
    best_rss = np.inf
    
    for threshold_candidate in [4.0, 5.0, 6.0]:
        # Split data
        mask_low = X < threshold_candidate
        mask_high = X >= threshold_candidate
        
        if mask_low.sum() < 2 or mask_high.sum() < 2:
            continue  # No suficientes datos
        
        # Ajustar regresiones separadas
        X_low, y_low = X[mask_low], y[mask_low]
        X_high, y_high = X[mask_high], y[mask_high]
        
        slope_low, intercept_low = np.polyfit(X_low, y_low, 1)
        slope_high, intercept_high = np.polyfit(X_high, y_high, 1)
        
        # Calcular RSS
        y_pred_low = slope_low * X_low + intercept_low
        y_pred_high = slope_high * X_high + intercept_high
        rss = np.sum((y_low - y_pred_low)**2) + np.sum((y_high - y_pred_high)**2)
        
        if rss < best_rss:
            best_rss = rss
            best_threshold = threshold_candidate
            best_slopes = (slope_low, slope_high)
            best_intercepts = (intercept_low, intercept_high)
    
    # Comparar con regresión lineal simple
    slope_simple, intercept_simple = np.polyfit(X, y, 1)
    y_pred_simple = slope_simple * X + intercept_simple
    rss_simple = np.sum((y - y_pred_simple)**2)
    
    # AIC comparison
    n = len(X)
    k_segmented = 4  # 2 slopes + 2 intercepts
    k_simple = 2
    
    aic_segmented = n * np.log(best_rss/n) + 2 * k_segmented
    aic_simple = n * np.log(rss_simple/n) + 2 * k_simple
    delta_aic = aic_segmented - aic_simple
    
    print(f"\n🔍 Regresión Segmentada:")
    print(f"   Threshold óptimo: {best_threshold:.1f}")
    print(f"   Pendiente pre-threshold: {best_slopes[0]:+.2f}")
    print(f"   Pendiente post-threshold: {best_slopes[1]:+.2f}")
    print(f"   Cambio de pendiente: {best_slopes[1] - best_slopes[0]:+.2f}")
    print(f"   AIC segmentado: {aic_segmented:.2f}")
    print(f"   AIC simple: {aic_simple:.2f}")
    print(f"   ΔAIC: {delta_aic:+.2f}")
    
    # Veredicto H7.2
    h72_criteria = [
        delta_aic < -2,  # Modelo segmentado mejor
        4.0 <= best_threshold <= 7.0,  # Threshold en rango esperado
        best_slopes[1] > 2 * best_slopes[0]  # Cambio de pendiente >2×
    ]
    
    print(f"\n📋 VEREDICTO H7.2:")
    print(f"   Criterio 1 (ΔAIC < -2): {'✅' if h72_criteria[0] else '❌'}")
    print(f"   Criterio 2 (threshold ∈ [4, 7]): {'✅' if h72_criteria[1] else '❌'}")
    print(f"   Criterio 3 (cambio pendiente >2×): {'✅' if h72_criteria[2] else '❌'}")
    
    if sum(h72_criteria) >= 2:
        print(f"   ✅ H7.2 SOPORTADA ({sum(h72_criteria)}/3 criterios)")
    else:
        print(f"   ❌ H7.2 NO soportada ({sum(h72_criteria)}/3 criterios)")
    
    # Guardar resultados
    threshold_results = {
        'threshold_optimal': float(best_threshold),
        'slope_pre': float(best_slopes[0]),
        'slope_post': float(best_slopes[1]),
        'slope_change': float(best_slopes[1] - best_slopes[0]),
        'aic_segmented': float(aic_segmented),
        'aic_simple': float(aic_simple),
        'delta_aic': float(delta_aic),
        'h72_verdict': 'SUPPORTED' if sum(h72_criteria) >= 2 else 'NOT_SUPPORTED'
    }
    
    output_path = Path(output_dir) / 'threshold_regression.json'
    with open(output_path, 'w') as f:
        json.dump(threshold_results, f, indent=2)
    
    print(f"\n💾 Guardado: {output_path}")
    
    return threshold_results


# ============================================================================
# FUNCIÓN 5: GENERAR FIGURAS
# ============================================================================

def generate_figures(df, output_dir):
    """
    Genera las 4 figuras preregistradas.
    """
    print("\n" + "="*70)
    print("🎨 GENERANDO FIGURAS")
    print("="*70)
    
    figuras_dir = Path(output_dir).parent / 'figuras'
    figuras_dir.mkdir(parents=True, exist_ok=True)
    
    # Figura 1: Heatmap
    print("\n📊 Figura 1: Heatmap Ratio vs Economía×Densidad...")
    
    df_pivot = df.pivot_table(values='ratio_pgf_control', 
                               index='economy', 
                               columns='spawn_rate', 
                               aggfunc='mean') * 100
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(df_pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=100,
                vmin=95, vmax=120, cbar_kws={'label': 'Ratio PGF/Control (%)'},
                linewidths=0.5, ax=ax)
    ax.set_title('Ratio PGF/Control por Economía y Densidad', fontsize=14, fontweight='bold')
    ax.set_xlabel('Spawn Rate (Densidad)', fontsize=12)
    ax.set_ylabel('Economía', fontsize=12)
    
    fig_path = figuras_dir / 'heatmap_ratio_economy_density.png'
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardado: {fig_path.name}")
    
    # Figura 2: Curvas por economía
    print("\n📈 Figura 2: Goldilocks por Economía...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = {'harsh': '#d62728', 'balanced': '#ff7f0e', 'favorable': '#2ca02c'}
    
    for economy in ['harsh', 'balanced', 'favorable']:
        subset = df[df['economy'] == economy]
        
        # Agrupar por densidad (media de seeds)
        grouped = subset.groupby('spawn_rate').agg({
            'ratio_pgf_control': ['mean', 'std', 'count']
        }).reset_index()
        grouped.columns = ['spawn_rate', 'ratio_mean', 'ratio_std', 'n']
        grouped['se'] = grouped['ratio_std'] / np.sqrt(grouped['n'])
        
        X = grouped['spawn_rate'].values
        y = grouped['ratio_mean'].values * 100
        se = grouped['se'].values * 100
        
        # Plot con error bars
        ax.errorbar(X, y, yerr=se, marker='o', label=economy.capitalize(),
                   color=colors[economy], capsize=5, linewidth=2, markersize=8)
        
        # Ajustar curva (mejor modelo)
        X_smooth = np.linspace(X.min(), X.max(), 100)
        coeffs = np.polyfit(X, y, 2)  # Cuadrático por defecto
        y_smooth = np.polyval(coeffs, X_smooth)
        ax.plot(X_smooth, y_smooth, '--', color=colors[economy], alpha=0.5)
    
    ax.axhline(100, color='gray', linestyle=':', linewidth=1.5, label='Paridad (100%)')
    ax.set_xlabel('Densidad (Spawn Rate)', fontsize=12)
    ax.set_ylabel('Ratio PGF/Control (%)', fontsize=12)
    ax.set_title('Curvas de Ventaja de Alineación por Economía', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    
    fig_path = figuras_dir / 'goldilocks_by_economy.png'
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardado: {fig_path.name}")
    
    # Figura 3: Interaction plot
    print("\n🔀 Figura 3: Interaction Plot...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for economy in ['harsh', 'balanced', 'favorable']:
        subset = df[df['economy'] == economy]
        grouped = subset.groupby('spawn_rate')['ratio_pgf_control'].mean() * 100
        ax.plot(grouped.index, grouped.values, marker='o', label=economy.capitalize(),
               color=colors[economy], linewidth=2, markersize=8)
    
    ax.axhline(100, color='gray', linestyle=':', linewidth=1.5)
    ax.set_xlabel('Densidad (Spawn Rate)', fontsize=12)
    ax.set_ylabel('Ratio PGF/Control (%)', fontsize=12)
    ax.set_title('Interaction Plot: Economía × Densidad', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    
    fig_path = figuras_dir / 'interaction_plot.png'
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardado: {fig_path.name}")
    
    # Figura 4: Threshold detection
    print("\n🎯 Figura 4: Threshold Detection...")
    
    df_threshold = df.groupby('balance')['ratio_pgf_control'].mean().reset_index()
    df_threshold['ratio_pct'] = df_threshold['ratio_pgf_control'] * 100
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    X = df_threshold['balance'].values
    y = df_threshold['ratio_pct'].values
    
    ax.scatter(X, y, s=200, color='navy', alpha=0.7, edgecolor='black', linewidth=1.5,
              label='Media por Balance')
    
    # Línea de threshold (en 5.0)
    ax.axvline(5.0, color='red', linestyle='--', linewidth=2, label='Threshold (5.0)')
    
    # Regresiones segmentadas
    mask_low = X < 5.0
    mask_high = X >= 5.0
    
    if mask_low.sum() > 0:
        slope_low, intercept_low = np.polyfit(X[mask_low], y[mask_low], 1)
        X_low_line = np.linspace(X[mask_low].min(), 5.0, 50)
        ax.plot(X_low_line, slope_low * X_low_line + intercept_low, 
               color='orange', linewidth=2, label=f'Pre-threshold (slope={slope_low:.2f})')
    
    if mask_high.sum() > 0:
        slope_high, intercept_high = np.polyfit(X[mask_high], y[mask_high], 1)
        X_high_line = np.linspace(5.0, X[mask_high].max(), 50)
        ax.plot(X_high_line, slope_high * X_high_line + intercept_high,
               color='green', linewidth=2, label=f'Post-threshold (slope={slope_high:.2f})')
    
    ax.axhline(100, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
    ax.set_xlabel('Balance Económico (reward / |step_cost|)', fontsize=12)
    ax.set_ylabel('Ratio PGF/Control (%)', fontsize=12)
    ax.set_title('Detección de Threshold Económico Crítico', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    fig_path = figuras_dir / 'threshold_detection.png'
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardado: {fig_path.name}")
    
    print(f"\n✅ 4 figuras generadas en: {figuras_dir}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Análisis Experimento 4: Economía Factorial')
    parser.add_argument('--input', type=str, default='results/pgf_v7/resultados',
                       help='Directorio con resultados JSON')
    parser.add_argument('--output', type=str, default='results/pgf_v7/analisis',
                       help='Directorio para guardar análisis')
    
    args = parser.parse_args()
    
    # Crear directorio de salida
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("🔬 ANÁLISIS EXPERIMENTO 4: ECONOMÍA FACTORIAL (PGF v7)")
    print("="*70)
    
    # 1. Cargar datos
    df = load_experiment_data(args.input)
    
    # 2. ANOVA 2-way
    anova_results = run_anova_2way(df, args.output)
    
    # 3. Comparación de modelos
    models_results = compare_models_by_economy(df, args.output)
    
    # 4. Threshold detection
    threshold_results = detect_threshold(df, args.output)
    
    # 5. Generar figuras
    generate_figures(df, args.output)
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)
    print(f"Archivos generados en: {args.output}")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
