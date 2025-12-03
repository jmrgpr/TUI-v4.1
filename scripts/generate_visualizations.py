"""
Visualizaciones Preregistradas - Experimento v8
Generar figuras comprometidas en PREREGISTRO_v8.md §Visualizaciones

Figuras:
1. Heatmap ratio × shaping × densidad
2. Scatter safety-reward tradeoff
3. Learning curves por shaping
4. Threshold regression plot
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuración matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Paths
RESULTS_DIR = Path("results/pgf_v8/resultados")
ANALYSIS_DIR = Path("results/pgf_v8/analisis")
FIGURAS_DIR = Path("results/pgf_v8/figuras")
FIGURAS_DIR.mkdir(parents=True, exist_ok=True)

def load_aggregate_data():
    """Cargar datos agregados por config"""
    configs = []
    
    shaping_levels = [0.0, 0.25, 0.5, 1.0]
    spawn_rates = [0.25, 0.40]
    seeds = [42, 123, 456]
    
    for shaping in shaping_levels:
        for spawn in spawn_rates:
            for seed in seeds:
                csv_path = RESULTS_DIR / f"exp8_shaping{shaping}_spawn{spawn}_seed{seed}_episodes.csv"
                
                if not csv_path.exists():
                    continue
                
                df = pd.read_csv(csv_path)
                
                pgf = df[df['agent_type'] == 'PGF']
                ctrl = df[df['agent_type'] == 'Control']
                
                # Ratios
                ratio_reward = pgf['total_reward_env'].mean() / ctrl['total_reward_env'].mean()
                
                pgf_tripwires = pgf['tripwires_triggered'].mean()
                ctrl_tripwires = ctrl['tripwires_triggered'].mean()
                ratio_tripwires = pgf_tripwires / ctrl_tripwires if ctrl_tripwires > 0.1 else np.nan
                
                # Safety score
                max_tripwires = 20  # Estimado razonable
                safety_pgf = 1 - (pgf_tripwires / max_tripwires)
                safety_ctrl = 1 - (ctrl_tripwires / max_tripwires)
                
                configs.append({
                    'shaping_scale': shaping,
                    'spawn_rate': spawn,
                    'seed': seed,
                    'ratio_reward_env': ratio_reward,
                    'ratio_tripwires': ratio_tripwires,
                    'pgf_reward': pgf['total_reward_env'].mean(),
                    'ctrl_reward': ctrl['total_reward_env'].mean(),
                    'pgf_safety': safety_pgf,
                    'ctrl_safety': safety_ctrl,
                    'pgf_success_rate': pgf['goal_reached'].mean(),
                    'ctrl_success_rate': ctrl['goal_reached'].mean()
                })
    
    return pd.DataFrame(configs)

def fig1_heatmap_ratio_shaping_density():
    """Figura 1: Heatmap ratio × shaping × densidad"""
    print("\n📊 Generando Figura 1: Heatmap ratio × shaping × densidad...")
    
    df = load_aggregate_data()
    
    # Pivot para heatmap
    pivot = df.groupby(['shaping_scale', 'spawn_rate'])['ratio_reward_env'].mean().reset_index()
    pivot_table = pivot.pivot(index='spawn_rate', columns='shaping_scale', values='ratio_reward_env')
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.heatmap(pivot_table, annot=True, fmt='.3f', cmap='RdYlGn', center=1.0,
                vmin=0.3, vmax=1.1, cbar_kws={'label': 'Ratio PGF/Control'},
                linewidths=0.5, ax=ax)
    
    ax.set_xlabel('Shaping Scale', fontsize=12, fontweight='bold')
    ax.set_ylabel('Spawn Rate (Densidad)', fontsize=12, fontweight='bold')
    ax.set_title('v8: Ratio Reward Env × Shaping × Densidad\n(Promedio sobre 3 seeds)', 
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    output_path = FIGURAS_DIR / "fig1_heatmap_ratio_shaping_density.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Guardado: {output_path}")

def fig2_scatter_safety_reward():
    """Figura 2: Scatter safety-reward tradeoff"""
    print("\n📊 Generando Figura 2: Scatter safety-reward tradeoff...")
    
    df = load_aggregate_data()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot PGF
    for shaping in sorted(df['shaping_scale'].unique()):
        subset = df[df['shaping_scale'] == shaping]
        
        ax.scatter(subset['pgf_safety'], subset['pgf_reward'],
                  s=100, alpha=0.7, label=f'PGF s={shaping}',
                  marker='o', edgecolors='black', linewidths=0.5)
    
    # Plot Control (solo s=0.0 para referencia)
    ctrl_ref = df[df['shaping_scale'] == 0.0]
    ax.scatter(ctrl_ref['ctrl_safety'], ctrl_ref['ctrl_reward'],
              s=100, alpha=0.5, label='Control (s=0.0)',
              marker='X', color='gray', edgecolors='black', linewidths=0.5)
    
    ax.set_xlabel('Safety Score (1 - tripwires/max)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean Reward Env', fontsize=12, fontweight='bold')
    ax.set_title('v8: Safety-Reward Tradeoff\n(Frontera de Pareto PGF vs Control)', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', frameon=True, fancybox=True)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = FIGURAS_DIR / "fig2_scatter_safety_reward.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Guardado: {output_path}")

def fig3_learning_curves():
    """Figura 3: Learning curves por shaping"""
    print("\n📊 Generando Figura 3: Learning curves por shaping...")
    
    # Cargar temporal analysis
    temporal_path = ANALYSIS_DIR / "temporal_analysis.json"
    with open(temporal_path, 'r', encoding='utf-8') as f:
        temporal_data = json.load(f)
    
    temporal_df = pd.DataFrame(temporal_data['temporal_ratios_aggregated'])
    
    # Mapear tramos a tiempo central
    tramo_to_time = {
        'exploration': 50,
        'convergence': 150,
        'stability': 250
    }
    temporal_df['time'] = temporal_df['tramo'].map(tramo_to_time)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot por shaping level
    for shaping in sorted(temporal_df['shaping_scale'].unique()):
        subset = temporal_df[temporal_df['shaping_scale'] == shaping].sort_values('time')
        
        ax.plot(subset['time'], subset['ratio_reward_mean'],
               marker='o', linewidth=2, markersize=8,
               label=f's = {shaping}', alpha=0.8)
        
        # Error bands
        ax.fill_between(subset['time'],
                       subset['ratio_reward_mean'] - subset['ratio_reward_std'],
                       subset['ratio_reward_mean'] + subset['ratio_reward_std'],
                       alpha=0.2)
    
    ax.axhline(y=1.0, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Paridad')
    
    ax.set_xlabel('Episodios (tramo central)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Ratio PGF/Control', fontsize=12, fontweight='bold')
    ax.set_title('v8: Curvas de Aprendizaje por Intensidad de Shaping\n(Ratio promedio ± SD por tramo temporal)', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', frameon=True, fancybox=True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 300)
    
    plt.tight_layout()
    output_path = FIGURAS_DIR / "fig3_learning_curves_by_shaping.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Guardado: {output_path}")

def fig4_threshold_regression():
    """Figura 4: Threshold regression plot"""
    print("\n📊 Generando Figura 4: Threshold regression...")
    
    df = load_aggregate_data()
    
    # Cargar threshold analysis
    threshold_path = ANALYSIS_DIR / "threshold_detection.json"
    with open(threshold_path, 'r', encoding='utf-8') as f:
        threshold_data = json.load(f)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter individual configs
    colors = {0.25: 'blue', 0.40: 'green'}
    for spawn in sorted(df['spawn_rate'].unique()):
        subset = df[df['spawn_rate'] == spawn]
        ax.scatter(subset['shaping_scale'], subset['ratio_reward_env'],
                  s=80, alpha=0.6, label=f'spawn={spawn}',
                  color=colors[spawn], edgecolors='black', linewidths=0.5)
    
    # Plot modelo lineal
    linear = threshold_data['linear_model']
    x_line = np.array([0.0, 1.0])
    y_line = linear['slope'] * x_line + linear['intercept']
    ax.plot(x_line, y_line, 'r--', linewidth=2, alpha=0.7,
           label=f"Linear (AIC={linear['aic']:.1f})")
    
    # Plot modelo piecewise si existe
    if threshold_data['piecewise_model'] is not None:
        pw = threshold_data['piecewise_model']
        bp = pw['breakpoint']
        
        # Segmento 1
        x1 = np.array([0.0, bp])
        y1 = pw['segment1']['slope'] * x1 + pw['segment1']['intercept']
        
        # Segmento 2
        x2 = np.array([bp, 1.0])
        y2 = pw['segment2']['slope'] * x2 + pw['segment2']['intercept']
        
        ax.plot(x1, y1, 'orange', linewidth=2.5, alpha=0.8, label=f"Piecewise (AIC={pw['aic']:.1f})")
        ax.plot(x2, y2, 'orange', linewidth=2.5, alpha=0.8)
        
        # Marcar breakpoint
        y_bp = pw['segment1']['slope'] * bp + pw['segment1']['intercept']
        ax.axvline(x=bp, color='purple', linestyle=':', linewidth=2, alpha=0.6)
        ax.plot(bp, y_bp, 'D', color='purple', markersize=10, 
               label=f"s* = {bp:.2f}", zorder=5)
    
    ax.axhline(y=1.0, color='black', linestyle='--', linewidth=1, alpha=0.4)
    
    ax.set_xlabel('Shaping Scale', fontsize=12, fontweight='bold')
    ax.set_ylabel('Ratio Reward Env (PGF/Control)', fontsize=12, fontweight='bold')
    ax.set_title('v8: Detección de Threshold s*\n(Regresión Segmentada vs Lineal)', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', frameon=True, fancybox=True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.05, 1.05)
    
    plt.tight_layout()
    output_path = FIGURAS_DIR / "fig4_threshold_regression.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Guardado: {output_path}")

def generate_all():
    """Generar todas las visualizaciones"""
    print("="*60)
    print("GENERACIÓN DE VISUALIZACIONES - Experimento v8")
    print("="*60)
    
    fig1_heatmap_ratio_shaping_density()
    fig2_scatter_safety_reward()
    fig3_learning_curves()
    fig4_threshold_regression()
    
    print("\n" + "="*60)
    print("✅ TODAS LAS VISUALIZACIONES GENERADAS")
    print("="*60)
    print(f"\nDirectorio: {FIGURAS_DIR}")
    print("\nFiguras creadas:")
    print("  1. fig1_heatmap_ratio_shaping_density.png")
    print("  2. fig2_scatter_safety_reward.png")
    print("  3. fig3_learning_curves_by_shaping.png")
    print("  4. fig4_threshold_regression.png")
    print("="*60)

if __name__ == "__main__":
    generate_all()
