#!/usr/bin/env python3
"""
analyze_risk_exp.py - Análisis científico riguroso Experimento 3A

Compara TUI vs Control en entorno con riesgo constitutivo (risk_scale=1.5)
para validar Hipótesis H1: I_operativa ∝ P_riesgo^α

Fecha: 2 de diciembre 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats

def load_and_validate_data(csv_path):
    """Carga CSV y valida estructura"""
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV no encontrado: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    required_cols = ['Episodio', 'Agente', 'Recompensa']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Columnas faltantes: {missing}")
    
    return df

def compute_agent_statistics(df, agent_name):
    """Calcula estadísticas completas por agente"""
    agent_data = df[df['Agente'] == agent_name]['Recompensa']
    
    if len(agent_data) == 0:
        return None
    
    return {
        'n': len(agent_data),
        'mean': agent_data.mean(),
        'std': agent_data.std(),
        'median': agent_data.median(),
        'min': agent_data.min(),
        'max': agent_data.max(),
        'q25': agent_data.quantile(0.25),
        'q75': agent_data.quantile(0.75),
        'success_count': (agent_data > 0).sum(),
        'success_rate': (agent_data > 0).mean() * 100,
        'mean_last100': agent_data.tail(100).mean(),
        'std_last100': agent_data.tail(100).std()
    }

def statistical_comparison(data_a, data_b):
    """Comparación estadística rigurosa entre dos agentes"""
    # T-test independiente
    t_stat, p_value = stats.ttest_ind(data_a, data_b)
    
    # Cohen's d (effect size)
    pooled_std = np.sqrt(((len(data_a)-1)*data_a.std()**2 + (len(data_b)-1)*data_b.std()**2) / (len(data_a) + len(data_b) - 2))
    cohens_d = (data_a.mean() - data_b.mean()) / pooled_std
    
    # Mann-Whitney U (non-parametric)
    u_stat, u_pvalue = stats.mannwhitneyu(data_a, data_b, alternative='two-sided')
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'significant': p_value < 0.05,
        'mann_whitney_u': u_stat,
        'mann_whitney_p': u_pvalue
    }

def check_pgf_bruto(df):
    """Verifica si PGF_Bruto > 0 (validación teoría)"""
    if 'PGF_Bruto' not in df.columns:
        return None
    
    tui_pgf = df[df['Agente'] == 'tui']['PGF_Bruto']
    simb_pgf = df[df['Agente'] == 'simbiosis']['PGF_Bruto']
    
    return {
        'tui_mean': tui_pgf.mean() if len(tui_pgf) > 0 else None,
        'tui_positive_pct': (tui_pgf > 0).mean() * 100 if len(tui_pgf) > 0 else None,
        'simb_mean': simb_pgf.mean() if len(simb_pgf) > 0 else None,
        'simb_positive_pct': (simb_pgf > 0).mean() * 100 if len(simb_pgf) > 0 else None
    }

def interpret_results(tui_stats, control_stats, comparison):
    """Interpretación científica de resultados"""
    ratio = tui_stats['mean'] / control_stats['mean'] if control_stats['mean'] != 0 else 0
    
    print("\n" + "="*70)
    print("📊 INTERPRETACIÓN CIENTÍFICA - EXPERIMENTO 3A")
    print("="*70 + "\n")
    
    # Criterio éxito según plan
    if ratio >= 0.7:
        verdict = "✅ ÉXITO FUERTE/MODERADO"
        action = "Proceder a Fase 4 (SOTA Comparison)"
        color = "VERDE"
    elif ratio >= 0.5:
        verdict = "⚠️ ÉXITO MÍNIMO"
        action = "Considerar Experimento 3C (sweep pgf_mix 0.3-0.5)"
        color = "AMARILLO"
    elif ratio >= 0.4:
        verdict = "⚠️ RESULTADO DÉBIL"
        action = "Evaluar rediseño PGF (Camino A2) o ajustar hiperparámetros"
        color = "NARANJA"
    else:
        verdict = "❌ FALLO"
        action = "OBLIGATORIO: Rediseñar PGF (Solución B) antes de continuar"
        color = "ROJO"
    
    print(f"Veredicto: {verdict}")
    print(f"Ratio TUI/Control: {ratio:.2%}")
    print(f"Acción recomendada: {action}\n")
    
    # Validación hipótesis H1
    print("Validación Hipótesis H1 (I ∝ P_riesgo^α):")
    if tui_stats['mean'] > control_stats['mean']:
        print("  ✅ TUI SUPERA Control: Hipótesis H1 VALIDADA")
        print(f"     Incremento: {(ratio-1)*100:.1f}%")
    elif ratio >= 0.7:
        print("  ⚠️ TUI cercano a Control: Hipótesis H1 PARCIALMENTE validada")
        print(f"     Déficit: {(1-ratio)*100:.1f}%")
    else:
        print("  ❌ TUI significativamente inferior: Hipótesis H1 NO validada")
        print(f"     Déficit: {(1-ratio)*100:.1f}%")
    
    # Significancia estadística
    print(f"\nSignificancia estadística:")
    print(f"  p-value: {comparison['p_value']:.6f} {'(significativo)' if comparison['significant'] else '(NO significativo)'}")
    print(f"  Cohen's d: {comparison['cohens_d']:.4f}", end="")
    if abs(comparison['cohens_d']) > 0.8:
        print(" (efecto GRANDE)")
    elif abs(comparison['cohens_d']) > 0.5:
        print(" (efecto MEDIANO)")
    elif abs(comparison['cohens_d']) > 0.2:
        print(" (efecto PEQUEÑO)")
    else:
        print(" (efecto TRIVIAL)")
    
    return verdict, action, ratio

def generate_convergence_plot(df, output_path):
    """Genera gráfico convergencia con rolling mean"""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    agents = ['control', 'simbiosis', 'tui']
    colors = ['blue', 'green', 'red']
    
    # Plot 1: Reward con rolling mean
    for agent, color in zip(agents, colors):
        data = df[df['Agente'] == agent]['Recompensa']
        if len(data) > 0:
            rolling = data.rolling(window=50, center=True).mean()
            axes[0].plot(rolling.index, rolling.values, label=agent, color=color, alpha=0.8, linewidth=2)
    
    axes[0].set_xlabel('Episodio', fontsize=12)
    axes[0].set_ylabel('Recompensa (rolling mean 50)', fontsize=12)
    axes[0].set_title('EXP 3A: Convergencia con Riesgo Real (risk_scale=1.5, grid 5×5)', fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=11)
    axes[0].grid(alpha=0.3)
    axes[0].axhline(0, color='black', linestyle='--', alpha=0.5, linewidth=1)
    
    # Plot 2: Success rate acumulativo
    for agent, color in zip(agents, colors):
        data = df[df['Agente'] == agent]['Recompensa']
        if len(data) > 0:
            cumsum_success = (data > 0).cumsum()
            cumsum_total = np.arange(1, len(data) + 1)
            success_rate = (cumsum_success / cumsum_total) * 100
            axes[1].plot(success_rate.index, success_rate.values, label=agent, color=color, alpha=0.8, linewidth=2)
    
    axes[1].set_xlabel('Episodio', fontsize=12)
    axes[1].set_ylabel('Success Rate Acumulativo (%)', fontsize=12)
    axes[1].set_title('Tasa de Éxito (reward > 0)', fontsize=14)
    axes[1].legend(fontsize=11)
    axes[1].grid(alpha=0.3)
    axes[1].axhline(95, color='green', linestyle='--', alpha=0.5, label='Criterio 95%')
    axes[1].set_ylim([0, 105])
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n📊 Gráfico guardado: {output_path}")
    plt.close()

def main():
    print("="*70)
    print("🔬 ANÁLISIS CIENTÍFICO EXPERIMENTO 3A")
    print("   Validación TUI con Riesgo Constitutivo (risk_scale=1.5)")
    print("="*70 + "\n")
    
    # Configuración
    csv_path = 'results/risk_validation/exp3a_risk15_seed42_episodes.csv'
    output_dir = Path('results/risk_validation')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Cargar datos
    print(f"📂 Cargando datos: {csv_path}")
    df = load_and_validate_data(csv_path)
    print(f"✅ Datos cargados: {len(df)} episodios\n")
    
    # Estadísticas por agente
    print("="*70)
    print("📈 ESTADÍSTICAS DESCRIPTIVAS")
    print("="*70 + "\n")
    
    agents = ['control', 'simbiosis', 'tui']
    stats_dict = {}
    
    for agent in agents:
        stats = compute_agent_statistics(df, agent)
        if stats:
            stats_dict[agent] = stats
            print(f"🤖 {agent.upper()}")
            print(f"   n episodios:        {stats['n']}")
            print(f"   Media:              {stats['mean']:.2f} ± {stats['std']:.2f}")
            print(f"   Mediana:            {stats['median']:.2f}")
            print(f"   Rango:              [{stats['min']:.2f}, {stats['max']:.2f}]")
            print(f"   Q25-Q75:            [{stats['q25']:.2f}, {stats['q75']:.2f}]")
            print(f"   Success rate:       {stats['success_rate']:.2f}% ({stats['success_count']}/{stats['n']})")
            print(f"   Media últimos 100:  {stats['mean_last100']:.2f} ± {stats['std_last100']:.2f}")
            print()
    
    # Comparación estadística TUI vs Control
    if 'tui' in stats_dict and 'control' in stats_dict:
        print("="*70)
        print("📊 COMPARACIÓN ESTADÍSTICA: TUI vs CONTROL")
        print("="*70 + "\n")
        
        tui_data = df[df['Agente'] == 'tui']['Recompensa']
        control_data = df[df['Agente'] == 'control']['Recompensa']
        
        comparison = statistical_comparison(tui_data, control_data)
        
        print(f"T-test independiente:")
        print(f"   t-statistic:  {comparison['t_statistic']:.4f}")
        print(f"   p-value:      {comparison['p_value']:.6f} {'***' if comparison['p_value'] < 0.001 else '**' if comparison['p_value'] < 0.01 else '*' if comparison['p_value'] < 0.05 else 'ns'}")
        print(f"\nEffect size:")
        print(f"   Cohen's d:    {comparison['cohens_d']:.4f}")
        print(f"\nMann-Whitney U (non-parametric):")
        print(f"   U statistic:  {comparison['mann_whitney_u']:.0f}")
        print(f"   p-value:      {comparison['mann_whitney_p']:.6f}")
        
        # PGF_Bruto check
        pgf_stats = check_pgf_bruto(df)
        if pgf_stats:
            print("\n" + "="*70)
            print("🔍 VALIDACIÓN PGF_BRUTO (Teoría TUI)")
            print("="*70 + "\n")
            
            if pgf_stats['tui_mean'] is not None:
                print(f"TUI:")
                print(f"   PGF_Bruto medio:     {pgf_stats['tui_mean']:.4f}")
                print(f"   % episodios PGF>0:   {pgf_stats['tui_positive_pct']:.2f}%")
                print(f"   Validación:          {'✅ POSITIVO' if pgf_stats['tui_mean'] > 0 else '❌ NEGATIVO/CERO'}")
            
            if pgf_stats['simb_mean'] is not None:
                print(f"\nSimbiosis:")
                print(f"   PGF_Bruto medio:     {pgf_stats['simb_mean']:.4f}")
                print(f"   % episodios PGF>0:   {pgf_stats['simb_positive_pct']:.2f}%")
                print(f"   Validación:          {'✅ POSITIVO' if pgf_stats['simb_mean'] > 0 else '❌ NEGATIVO/CERO'}")
        
        # Interpretación final
        verdict, action, ratio = interpret_results(stats_dict['tui'], stats_dict['control'], comparison)
        
        # Gráficos
        plot_path = output_dir / 'exp3a_convergence_analysis.png'
        generate_convergence_plot(df, plot_path)
        
        # Guardar resumen
        summary_path = output_dir / 'exp3a_summary.txt'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("EXPERIMENTO 3A - RESUMEN EJECUTIVO\n")
            f.write("="*70 + "\n\n")
            f.write(f"Fecha: 2 diciembre 2025\n")
            f.write(f"Configuración: grid 5×5, risk_scale=1.5, pgf_mix=0.2, 500 episodios\n\n")
            f.write(f"RESULTADOS:\n")
            f.write(f"  TUI media:       {stats_dict['tui']['mean']:.2f} ± {stats_dict['tui']['std']:.2f}\n")
            f.write(f"  Control media:   {stats_dict['control']['mean']:.2f} ± {stats_dict['control']['std']:.2f}\n")
            f.write(f"  Ratio TUI/Ctrl:  {ratio:.2%}\n")
            f.write(f"  p-value:         {comparison['p_value']:.6f}\n")
            f.write(f"  Cohen's d:       {comparison['cohens_d']:.4f}\n\n")
            f.write(f"VEREDICTO: {verdict}\n")
            f.write(f"ACCIÓN:    {action}\n")
        
        print(f"\n📄 Resumen guardado: {summary_path}")
        
    else:
        print("⚠️ No se encontraron datos de TUI o Control para comparar")
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)

if __name__ == '__main__':
    main()
