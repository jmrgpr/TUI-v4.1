"""
Análisis de descomposición de reward para PGF v5
Extrae métricas de rendimiento por componente (recursos, step_cost, castigos)
para entender MECANISMO del patrón Goldilocks
"""
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

# Configuración estética
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

def load_experiment_data(results_dir="results/pgf_v5/resultados"):
    """Carga todos los JSON de experimentos v5"""
    data = []
    
    for json_file in Path(results_dir).glob("exp2_*.json"):
        if "summary" in json_file.name:
            continue
            
        with open(json_file, 'r', encoding='utf-8') as f:
            exp = json.load(f)
            
        # Metadata
        config = exp['config']
        results = exp['results']
        
        data.append({
            'filename': json_file.name,
            'spawn_rate': config['spawn_rate'],
            'seed': config['seed'],
            'D_effective': results['D_effective_mean'],
            'ratio_pgf_control': results['ratio_pgf_control'],
            'mean_reward_pgf': results['mean_reward_pgf'],
            'mean_reward_control': results['mean_reward_control'],
            'n_episodes_pgf': results['n_episodes_pgf'],
            'n_episodes_control': results['n_episodes_control'],
        })
    
    return pd.DataFrame(data)

def load_episode_details(csv_file):
    """Carga CSV de episodios para análisis detallado"""
    df = pd.read_csv(csv_file)
    return df

def analyze_reward_components(results_dir="results/pgf_v5/resultados"):
    """
    Descompone reward en:
    - Recursos recolectados × resource_reward (1.0)
    - Steps × step_cost (-0.3)
    - Castigos de riesgo (tripwires/shocks)
    """
    print("🔬 ANÁLISIS DE DESCOMPOSICIÓN DE REWARD\n")
    print("="*80)
    
    # Cargar resumen
    df_summary = load_experiment_data(results_dir)
    
    # Detectar outliers (criterio: ratio > 500% o < 5%)
    df_summary['is_outlier'] = (df_summary['ratio_pgf_control'] > 500) | \
                                (df_summary['ratio_pgf_control'] < 5)
    
    print(f"\n📊 DATOS CARGADOS:")
    print(f"  Total configs: {len(df_summary)}")
    print(f"  Configs robustos: {(~df_summary['is_outlier']).sum()}")
    print(f"  Outliers detectados: {df_summary['is_outlier'].sum()}")
    
    # Análisis por densidad (excluyendo outliers)
    df_robust = df_summary[~df_summary['is_outlier']]
    
    print(f"\n📈 PATRÓN POR DENSIDAD (solo robustos):\n")
    
    density_groups = df_robust.groupby('spawn_rate').agg({
        'ratio_pgf_control': ['mean', 'std', 'count'],
        'D_effective': 'mean',
        'mean_reward_pgf': 'mean',
        'mean_reward_control': 'mean',
    }).round(2)
    
    print(density_groups)
    
    # Análisis detallado por episodio (ejemplo: spawn=0.15, seed=42)
    print(f"\n🔍 ANÁLISIS DETALLADO (spawn=0.15, seed=42):")
    
    csv_file = Path(results_dir) / "exp2_grid4x4_spawn0.15_seed42_episodes.csv"
    if csv_file.exists():
        df_eps = load_episode_details(csv_file)
        
        # Separar PGF vs Control
        df_pgf = df_eps[df_eps['agent'] == 'PGF']
        df_ctrl = df_eps[df_eps['agent'] == 'Control']
        
        print(f"\n  PGF:")
        print(f"    Mean reward: {df_pgf['total_reward'].mean():.2f}")
        print(f"    Mean resources: {df_pgf['resources_collected'].mean():.2f}")
        print(f"    Mean steps: {df_pgf['steps'].mean():.2f}")
        print(f"    Reward/step: {(df_pgf['total_reward'] / df_pgf['steps']).mean():.3f}")
        
        print(f"\n  Control:")
        print(f"    Mean reward: {df_ctrl['total_reward'].mean():.2f}")
        print(f"    Mean resources: {df_ctrl['resources_collected'].mean():.2f}")
        print(f"    Mean steps: {df_ctrl['steps'].mean():.2f}")
        print(f"    Reward/step: {(df_ctrl['total_reward'] / df_ctrl['steps']).mean():.3f}")
        
        # Estimación de componentes
        print(f"\n  DESCOMPOSICIÓN ESTIMADA (PGF):")
        resources = df_pgf['resources_collected'].mean()
        steps = df_pgf['steps'].mean()
        total_reward = df_pgf['total_reward'].mean()
        
        resource_contribution = resources * 1.0  # resource_reward=1.0
        step_cost_contribution = steps * -0.3     # step_cost=-0.3
        risk_penalty = total_reward - resource_contribution - step_cost_contribution
        
        print(f"    Recursos (+{resources:.1f} × 1.0) = +{resource_contribution:.1f}")
        print(f"    Steps ({steps:.1f} × -0.3) = {step_cost_contribution:.1f}")
        print(f"    Castigos riesgo (residual) = {risk_penalty:.1f}")
        print(f"    TOTAL = {total_reward:.1f}")
    
    return df_summary, df_robust

def plot_goldilocks_curve(df_robust, output_dir="results/pgf_v5/figuras"):
    """Genera figura clave: curva ratio(D) con ajuste cuadrático"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Panel 1: Scatter + fit cuadrático
    x = df_robust['D_effective'].values
    y = df_robust['ratio_pgf_control'].values
    
    # Fit cuadrático: ratio = a*D² + b*D + c
    coeffs = np.polyfit(x, y, 2)
    poly = np.poly1d(coeffs)
    
    x_smooth = np.linspace(x.min(), x.max(), 100)
    y_smooth = poly(x_smooth)
    
    # Encontrar máximo
    vertex_x = -coeffs[1] / (2 * coeffs[0])
    vertex_y = poly(vertex_x)
    
    ax1.scatter(x, y, s=100, alpha=0.6, c='steelblue', edgecolors='black')
    ax1.plot(x_smooth, y_smooth, 'r--', linewidth=2, alpha=0.7, 
             label=f'Fit cuadrático: {coeffs[0]:.1f}D² + {coeffs[1]:.1f}D + {coeffs[2]:.1f}')
    ax1.axvline(vertex_x, color='green', linestyle=':', linewidth=2, alpha=0.7,
                label=f'Máximo en D={vertex_x:.2f}')
    ax1.scatter([vertex_x], [vertex_y], s=200, marker='*', c='gold', 
                edgecolors='red', linewidths=2, zorder=5, label=f'Peak ratio={vertex_y:.1f}%')
    
    ax1.set_xlabel('Densidad Efectiva (D)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Ratio PGF/Control (%)', fontsize=13, fontweight='bold')
    ax1.set_title('Curva de Goldilocks: Zona Óptima de Alineación', fontsize=14, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Barras por densidad
    density_means = df_robust.groupby('spawn_rate')['ratio_pgf_control'].agg(['mean', 'std'])
    density_labels = ['Escasez\n(0.05)', 'Intermedia\n(0.15)', 'Abundancia\n(0.30)']
    
    bars = ax2.bar(range(len(density_means)), density_means['mean'], 
                   yerr=density_means['std'], capsize=10, 
                   color=['#d62728', '#2ca02c', '#1f77b4'], alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax2.axhline(100, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Paridad (100%)')
    ax2.set_xticks(range(len(density_means)))
    ax2.set_xticklabels(density_labels, fontsize=12)
    ax2.set_ylabel('Ratio PGF/Control (%)', fontsize=13, fontweight='bold')
    ax2.set_title('Rendimiento por Régimen de Densidad', fontsize=14, fontweight='bold')
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    
    # Anotar valores
    for i, (bar, val) in enumerate(zip(bars, density_means['mean'])):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    
    output_path = Path(output_dir) / "goldilocks_curve_analysis.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Figura guardada: {output_path}")
    
    plt.show()
    
    return coeffs, vertex_x, vertex_y

def main():
    print("="*80)
    print("📊 PGF v5 - ANÁLISIS DE DESCOMPOSICIÓN Y MECANISMO")
    print("="*80)
    
    # Análisis de componentes
    df_summary, df_robust = analyze_reward_components()
    
    # Generar figura clave
    print("\n" + "="*80)
    print("📈 GENERANDO FIGURA: CURVA DE GOLDILOCKS")
    print("="*80)
    
    coeffs, vertex_x, vertex_y = plot_goldilocks_curve(df_robust)
    
    print(f"\n🎯 HALLAZGO CLAVE:")
    print(f"  La curva ratio(D) tiene un MÁXIMO en D ≈ {vertex_x:.2f}")
    print(f"  En ese punto, PGF alcanza {vertex_y:.1f}% del rendimiento de Control")
    print(f"  Ecuación: ratio = {coeffs[0]:.2f}D² + {coeffs[1]:.2f}D + {coeffs[2]:.2f}")
    
    print(f"\n✅ ANÁLISIS COMPLETO - Ver figuras en results/pgf_v5/figuras/")

if __name__ == "__main__":
    main()
