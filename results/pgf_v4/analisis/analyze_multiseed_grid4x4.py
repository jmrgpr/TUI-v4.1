"""
Análisis Multi-Semilla para Grid 4x4 - PGF v4 Experimento 1

Autor: Jose M Rivera Garcia
Fecha: 2 de diciembre de 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

RESULTS_DIR = Path("results/pgf_v4/resultados")
FIGURES_DIR = Path("results/pgf_v4/figuras")
ANALYSIS_DIR = Path("results/pgf_v4/analisis")
SEEDS = [42, 123, 456]

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

def load_episode_data(seed):
    file_path = RESULTS_DIR / f"exp1_grid4x4_seed{seed}_episodes.csv"
    return pd.read_csv(file_path)

def calculate_statistics(df, agent_type):
    agent_data = df[df['Agente'] == agent_type]['Recompensa']
    return {
        'mean': agent_data.mean(),
        'std': agent_data.std(),
        'cv': (agent_data.std() / agent_data.mean()) * 100 if agent_data.mean() != 0 else np.nan,
        'min': agent_data.min(),
        'max': agent_data.max(),
        'median': agent_data.median(),
        'q25': agent_data.quantile(0.25),
        'q75': agent_data.quantile(0.75),
        'count': len(agent_data),
        'mean_last100': agent_data.tail(100).mean(),
        'std_last100': agent_data.tail(100).std()
    }

def calculate_pgf_statistics(df):
    simbiosis_data = df[df['Agente'] == 'simbiosis']
    if 'PGF_Bruto_Avg' not in simbiosis_data.columns:
        return {}
    pgf_data = simbiosis_data['PGF_Bruto_Avg']
    return {
        'pgf_mean': pgf_data.mean(),
        'pgf_std': pgf_data.std(),
        'pgf_min': pgf_data.min(),
        'pgf_max': pgf_data.max(),
        'pgf_negative_count': (pgf_data < 0).sum(),
        'pgf_zero_count': (pgf_data == 0).sum(),
        'pgf_positive_count': (pgf_data > 0).sum()
    }

def analyze_single_seed(seed):
    print(f"\n{'='*60}")
    print(f"Analizando semilla {seed}...")
    print(f"{'='*60}")
    
    df = load_episode_data(seed)
    control_stats = calculate_statistics(df, 'control')
    simbiosis_stats = calculate_statistics(df, 'simbiosis')
    pgf_stats = calculate_pgf_statistics(df)
    ratio = (simbiosis_stats['mean'] / control_stats['mean']) * 100 if control_stats['mean'] != 0 else np.nan
    
    print(f"\nAgente Control:")
    print(f"  Recompensa: {control_stats['mean']:.2f} ± {control_stats['std']:.2f}")
    print(f"  CV: {control_stats['cv']:.2f}%")
    print(f"  Rango: [{control_stats['min']:.2f}, {control_stats['max']:.2f}]")
    
    print(f"\nAgente Simbiosis:")
    print(f"  Recompensa: {simbiosis_stats['mean']:.2f} ± {simbiosis_stats['std']:.2f}")
    print(f"  CV: {simbiosis_stats['cv']:.2f}%")
    print(f"  Rango: [{simbiosis_stats['min']:.2f}, {simbiosis_stats['max']:.2f}]")
    
    print(f"\n📊 RATIO DE DESEMPEÑO: {ratio:.2f}%")
    
    if pgf_stats:
        print(f"\nSeñal PGF:")
        print(f"  Media: {pgf_stats['pgf_mean']:.4f}")
        print(f"  Std: {pgf_stats['pgf_std']:.4f}")
        print(f"  Positivos: {pgf_stats['pgf_positive_count']}/{simbiosis_stats['count']}")
    
    return {
        'seed': seed,
        'control': control_stats,
        'simbiosis': simbiosis_stats,
        'pgf': pgf_stats,
        'ratio': ratio
    }

def analyze_multiseed():
    print(f"\n{'='*60}")
    print("ANÁLISIS MULTI-SEMILLA - GRID 4x4 REAL")
    print(f"{'='*60}")
    
    results = []
    ratios = []
    
    for seed in SEEDS:
        result = analyze_single_seed(seed)
        results.append(result)
        ratios.append(result['ratio'])
    
    ratios_array = np.array(ratios)
    mean_ratio = ratios_array.mean()
    std_ratio = ratios_array.std()
    cv_ratio = (std_ratio / mean_ratio) * 100 if mean_ratio != 0 else np.nan
    
    print(f"\n{'='*60}")
    print("RESUMEN MULTI-SEMILLA")
    print(f"{'='*60}")
    print(f"\nRatio de desempeño:")
    print(f"  Media: {mean_ratio:.2f}%")
    print(f"  Std: {std_ratio:.2f}%")
    print(f"  CV: {cv_ratio:.2f}%")
    print(f"  IC95%: [{mean_ratio - 1.96*std_ratio:.2f}%, {mean_ratio + 1.96*std_ratio:.2f}%]")
    print(f"  Rango: [{ratios_array.min():.2f}%, {ratios_array.max():.2f}%]")
    
    print(f"\n{'='*60}")
    print("EVALUACIÓN DE HIPÓTESIS")
    print(f"{'='*60}")
    
    if 60 <= mean_ratio <= 75:
        print("✅ HIPÓTESIS CONFIRMADA: Ratio en rango esperado (60-75%)")
    elif mean_ratio > 75:
        print("⚠️ Ratio superior al esperado. 4x4 es más favorable de lo previsto.")
    else:
        print("⚠️ Ratio inferior al esperado. Similitud con 5x5 o problemas de convergencia.")
    
    if cv_ratio < 5:
        print("✅ Reproducibilidad EXCELENTE (CV < 5%)")
    elif cv_ratio < 10:
        print("✅ Reproducibilidad BUENA (CV < 10%)")
    else:
        print("⚠️ Reproducibilidad MODERADA (CV > 10%)")
    
    summary_data = []
    for result in results:
        summary_data.append({
            'Seed': result['seed'],
            'Control_Mean': result['control']['mean'],
            'Control_Std': result['control']['std'],
            'Control_CV': result['control']['cv'],
            'Simbiosis_Mean': result['simbiosis']['mean'],
            'Simbiosis_Std': result['simbiosis']['std'],
            'Simbiosis_CV': result['simbiosis']['cv'],
            'Ratio_%': result['ratio'],
            'PGF_Mean': result['pgf'].get('pgf_mean', np.nan)
        })
    
    summary_df = pd.DataFrame(summary_data)
    output_file = ANALYSIS_DIR / "multiseed_summary_grid4x4.csv"
    summary_df.to_csv(output_file, index=False)
    print(f"\n✅ Resumen guardado en: {output_file}")
    
    return results, summary_df

def create_visualizations(results):
    print(f"\n{'='*60}")
    print("GENERANDO VISUALIZACIONES...")
    print(f"{'='*60}")
    
    all_data = []
    for seed in SEEDS:
        df = load_episode_data(seed)
        df['Seed'] = seed
        all_data.append(df)
    
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Figura 1: Barras
    fig, ax = plt.subplots(figsize=(10, 6))
    summary_data = []
    for result in results:
        summary_data.append({
            'Seed': f"Seed {result['seed']}",
            'Control': result['control']['mean'],
            'Simbiosis': result['simbiosis']['mean']
        })
    
    summary_df = pd.DataFrame(summary_data)
    x = np.arange(len(summary_df))
    width = 0.35
    
    ax.bar(x - width/2, summary_df['Control'], width, label='Control', alpha=0.8, color='steelblue')
    ax.bar(x + width/2, summary_df['Simbiosis'], width, label='Simbiosis (PGF)', alpha=0.8, color='coral')
    
    ax.set_xlabel('Semilla')
    ax.set_ylabel('Recompensa Media')
    ax.set_title('Grid 4x4: Comparación Control vs Simbiosis (Multi-Semilla)')
    ax.set_xticks(x)
    ax.set_xticklabels(summary_df['Seed'])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    fig1_path = FIGURES_DIR / "figure1_barras_grid4x4.png"
    plt.savefig(fig1_path, dpi=300, bbox_inches='tight')
    print(f"✅ Figura 1 guardada: {fig1_path}")
    plt.close()
    
    # Figura 2: Boxplots
    fig, ax = plt.subplots(figsize=(10, 6))
    control_data = combined_df[combined_df['Agente'] == 'control']['Recompensa']
    simbiosis_data = combined_df[combined_df['Agente'] == 'simbiosis']['Recompensa']
    
    ax.boxplot([control_data, simbiosis_data], tick_labels=['Control', 'Simbiosis (PGF)'])
    ax.set_ylabel('Recompensa')
    ax.set_title('Grid 4x4: Distribución de Recompensas (3 semillas, 1500 episodios)')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    fig2_path = FIGURES_DIR / "figure2_boxplot_grid4x4.png"
    plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
    print(f"✅ Figura 2 guardada: {fig2_path}")
    plt.close()
    
    # Figura 3: Evolución temporal
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    for idx, seed in enumerate(SEEDS):
        df = load_episode_data(seed)
        control_rewards = df[df['Agente'] == 'control']['Recompensa'].values
        simbiosis_rewards = df[df['Agente'] == 'simbiosis']['Recompensa'].values
        episodes = range(1, len(control_rewards) + 1)
        
        axes[idx].plot(episodes, control_rewards, alpha=0.3, color='steelblue', label='Control')
        axes[idx].plot(episodes, simbiosis_rewards, alpha=0.3, color='coral', label='Simbiosis')
        
        window = 50
        control_ma = pd.Series(control_rewards).rolling(window).mean()
        simbiosis_ma = pd.Series(simbiosis_rewards).rolling(window).mean()
        
        axes[idx].plot(episodes, control_ma, color='navy', linewidth=2, label='Control (MA50)')
        axes[idx].plot(episodes, simbiosis_ma, color='darkred', linewidth=2, label='Simbiosis (MA50)')
        
        axes[idx].set_title(f'Seed {seed}')
        axes[idx].set_xlabel('Episodio')
        axes[idx].set_ylabel('Recompensa')
        axes[idx].legend(loc='best')
        axes[idx].grid(alpha=0.3)
    
    plt.suptitle('Grid 4x4: Evolución Temporal por Semilla', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    fig3_path = FIGURES_DIR / "figure3_evolucion_grid4x4.png"
    plt.savefig(fig3_path, dpi=300, bbox_inches='tight')
    print(f"✅ Figura 3 guardada: {fig3_path}")
    plt.close()

def compare_with_previous_results():
    print(f"\n{'='*60}")
    print("COMPARACIÓN CON EXPERIMENTOS PREVIOS")
    print(f"{'='*60}")
    
    comparison_data = {
        'Grid_Size': ['3x3', '4x4', '5x5'],
        'Complexity': [9, 16, 25],
        'Ratio_%': [105.0, np.nan, 38.93],
        'Control_CV': [np.nan, np.nan, 192.0],
        'Simbiosis_CV': [np.nan, np.nan, 71.0]
    }
    
    try:
        summary_4x4 = pd.read_csv(ANALYSIS_DIR / "multiseed_summary_grid4x4.csv")
        ratio_4x4 = summary_4x4['Ratio_%'].mean()
        comparison_data['Ratio_%'][1] = ratio_4x4
        
        print(f"\n3x3: 105.0% (benign, PGF > Control)")
        print(f"4x4: {ratio_4x4:.2f}% (NUEVO - DATOS REALES)")
        print(f"5x5: 38.93% (baseline v3)")
        
        if 60 <= ratio_4x4 <= 75:
            print(f"\n✅ Tendencia lineal CONFIRMADA")
        elif abs(ratio_4x4 - 38.93) < 5:
            print(f"\n⚠️ UMBRAL ABRUPTO: 4x4 ≈ 5x5, colapso entre 3x3 y 4x4")
        else:
            print(f"\n❓ Resultado inesperado, requiere análisis adicional")
        
    except FileNotFoundError:
        print("\n⚠️ No se encontraron resultados de 4x4.")
    
    comparison_df = pd.DataFrame(comparison_data)
    output_file = ANALYSIS_DIR / "tabla_comparativa_grid4x4.csv"
    comparison_df.to_csv(output_file, index=False)
    print(f"\n✅ Tabla comparativa guardada: {output_file}")

def main():
    print("\n" + "="*60)
    print("ANÁLISIS MULTI-SEMILLA - GRID 4x4 REAL - PGF v4")
    print("="*60)
    
    results, summary_df = analyze_multiseed()
    create_visualizations(results)
    compare_with_previous_results()
    
    print(f"\n{'='*60}")
    print("✅ ANÁLISIS COMPLETADO")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
