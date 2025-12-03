"""
Generación de Visualizaciones v9
=================================

Genera 4 figuras preregistradas para v9:
1. Learning curves por grupo (ratios × episodios)
2. Barplot ratios finales (comparación grupos)
3. Temporal stages (reward por etapa Curriculum)
4. Scatter safety-reward tradeoff

Uso:
    python scripts/generate_visualizations_v9.py

Autor: TUI v4.1 Research Team
Fecha: 3 diciembre 2025
"""

import sys
import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Agregar directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

RESULTS_DIR = Path('results/pgf_v9/resultados')
OUTPUT_DIR = Path('results/pgf_v9/figuras')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GROUPS = ['Curriculum', 'DirectoS1', 'ControlS0']
SEEDS = [42, 123, 456]

# Estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11


# ============================================================================
# CARGA DATOS
# ============================================================================

def load_all_data():
    """Carga todos los CSVs generados en v9."""
    data = {}
    
    for group in GROUPS:
        data[group] = {}
        for seed in SEEDS:
            csv_path = RESULTS_DIR / f"exp9_{group}_seed{seed}_episodes.csv"
            
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                data[group][seed] = df
    
    return data


# ============================================================================
# FIGURA 1: LEARNING CURVES
# ============================================================================

def generate_fig1_learning_curves(data):
    """
    Figura 1: Learning curves por grupo (ratio PGF/Control × episodios).
    
    Args:
        data: dict {group: {seed: DataFrame}}
    
    Returns:
        Path al archivo guardado
    """
    print("\n[1/4] Generando Figura 1: Learning Curves...")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = {
        'Curriculum': '#2ecc71',  # Verde
        'DirectoS1': '#e74c3c',   # Rojo
        'ControlS0': '#95a5a6'    # Gris
    }
    
    # Calcular ratios vs Control para cada grupo
    for group in ['Curriculum', 'DirectoS1']:
        for seed in SEEDS:
            if seed in data[group] and seed in data['ControlS0']:
                df_group = data[group][seed]
                df_control = data['ControlS0'][seed]
                
                # Calcular ratio (ventana deslizante suavizada)
                window = 10
                rewards_group = df_group['total_reward_env'].rolling(window, min_periods=1).mean()
                rewards_control = df_control['total_reward_env'].rolling(window, min_periods=1).mean()
                
                ratios = rewards_group / rewards_control
                
                # Plot con alpha bajo para seeds individuales
                ax.plot(df_group['episode'], ratios, 
                       color=colors[group], alpha=0.3, linewidth=1)
        
        # Plot promedio grueso
        all_ratios = []
        for seed in SEEDS:
            if seed in data[group] and seed in data['ControlS0']:
                df_group = data[group][seed]
                df_control = data['ControlS0'][seed]
                
                rewards_group = df_group['total_reward_env'].rolling(window, min_periods=1).mean()
                rewards_control = df_control['total_reward_env'].rolling(window, min_periods=1).mean()
                ratios = rewards_group / rewards_control
                all_ratios.append(ratios.values)
        
        if all_ratios:
            mean_ratios = np.mean(all_ratios, axis=0)
            ax.plot(range(1, len(mean_ratios)+1), mean_ratios,
                   color=colors[group], linewidth=3, label=group)
    
    # Línea referencia threshold H9.1
    ax.axhline(y=0.70, color='black', linestyle='--', linewidth=1.5, 
               label='H9.1 Threshold (0.70)', alpha=0.7)
    
    # Línea referencia paridad
    ax.axhline(y=1.0, color='gray', linestyle=':', linewidth=1.5, 
               label='Paridad', alpha=0.5)
    
    ax.set_xlabel('Episodio', fontsize=13, fontweight='bold')
    ax.set_ylabel('Ratio Reward (PGF / Control)', fontsize=13, fontweight='bold')
    ax.set_title('v9: Learning Curves por Grupo Experimental', 
                fontsize=15, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1.5])
    
    # Guardar
    fig_path = OUTPUT_DIR / "fig1_learning_curves_by_group.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Guardada: {fig_path.name}")
    return fig_path


# ============================================================================
# FIGURA 2: BARPLOT RATIOS FINALES
# ============================================================================

def generate_fig2_barplot_ratios(data):
    """
    Figura 2: Barplot ratios finales por grupo (últimos 50 episodios).
    
    Args:
        data: dict {group: {seed: DataFrame}}
    
    Returns:
        Path al archivo guardado
    """
    print("\n[2/4] Generando Figura 2: Barplot Ratios Finales...")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Calcular ratios finales (últimos 50 eps)
    window_size = 50
    ratios_by_group = {}
    
    for group in ['Curriculum', 'DirectoS1']:
        ratios_seeds = []
        for seed in SEEDS:
            if seed in data[group] and seed in data['ControlS0']:
                df_group = data[group][seed].iloc[-window_size:]
                df_control = data['ControlS0'][seed].iloc[-window_size:]
                
                ratio = df_group['total_reward_env'].mean() / df_control['total_reward_env'].mean()
                ratios_seeds.append(ratio)
        
        ratios_by_group[group] = ratios_seeds
    
    # Agregar ControlS0 (siempre 1.0 por definición)
    ratios_by_group['ControlS0'] = [1.0] * len(SEEDS)
    
    # Crear barplot
    groups_plot = ['Curriculum', 'DirectoS1', 'ControlS0']
    means = [np.mean(ratios_by_group[g]) for g in groups_plot]
    stds = [np.std(ratios_by_group[g], ddof=1) for g in groups_plot]
    
    colors_bar = ['#2ecc71', '#e74c3c', '#95a5a6']
    
    x_pos = np.arange(len(groups_plot))
    bars = ax.bar(x_pos, means, yerr=stds, capsize=10,
                  color=colors_bar, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Scatter puntos individuales (seeds)
    for i, group in enumerate(groups_plot):
        ratios = ratios_by_group[group]
        x_scatter = np.random.normal(i, 0.04, len(ratios))
        ax.scatter(x_scatter, ratios, color='black', s=60, alpha=0.6, zorder=3)
    
    # Línea threshold
    ax.axhline(y=0.70, color='black', linestyle='--', linewidth=2, 
               label='H9.1 Threshold (0.70)', alpha=0.7)
    
    # Línea paridad
    ax.axhline(y=1.0, color='gray', linestyle=':', linewidth=2, 
               label='Paridad', alpha=0.5)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(groups_plot, fontsize=12, fontweight='bold')
    ax.set_ylabel('Ratio Reward Final (PGF / Control)', fontsize=13, fontweight='bold')
    ax.set_title('v9: Comparación Ratios Finales por Grupo\n(Últimos 50 Episodios)', 
                fontsize=15, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax.grid(True, axis='y', alpha=0.3)
    ax.set_ylim([0, 1.3])
    
    # Anotar valores
    for i, (mean, std) in enumerate(zip(means, stds)):
        ax.text(i, mean + std + 0.05, f'{mean:.2f}±{std:.2f}',
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Guardar
    fig_path = OUTPUT_DIR / "fig2_barplot_ratios_final.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Guardada: {fig_path.name}")
    return fig_path


# ============================================================================
# FIGURA 3: TEMPORAL STAGES (CURRICULUM)
# ============================================================================

def generate_fig3_temporal_stages(data):
    """
    Figura 3: Reward por etapa (solo Curriculum).
    
    Args:
        data: dict {group: {seed: DataFrame}}
    
    Returns:
        Path al archivo guardado
    """
    print("\n[3/4] Generando Figura 3: Temporal Stages (Curriculum)...")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Colores por seed
    seed_colors = {42: '#3498db', 123: '#e74c3c', 456: '#f39c12'}
    
    # Plot por seed
    for seed in SEEDS:
        if seed in data['Curriculum']:
            df = data['Curriculum'][seed]
            
            # Agregar por etapa
            stage_rewards = []
            stage_nums = []
            
            for stage_num in [1, 2, 3, 4]:
                df_stage = df[df['stage'] == stage_num]
                if len(df_stage) > 0:
                    stage_rewards.append(df_stage['total_reward_env'].mean())
                    stage_nums.append(stage_num)
            
            # Plot
            ax.plot(stage_nums, stage_rewards, marker='o', markersize=10,
                   linewidth=2.5, label=f'Seed {seed}', color=seed_colors[seed])
    
    # Líneas de referencia
    ax.axhline(y=115, color='green', linestyle='--', linewidth=1.5, 
               label='Control Baseline (~115)', alpha=0.6)
    
    ax.set_xlabel('Etapa Curriculum', fontsize=13, fontweight='bold')
    ax.set_ylabel('Reward Env (Mean)', fontsize=13, fontweight='bold')
    ax.set_title('v9: Evolución Temporal por Etapas (Curriculum)', 
                fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(['Etapa 1\n(s=0.0)', 'Etapa 2\n(s=0.25)', 
                       'Etapa 3\n(s=0.5)', 'Etapa 4\n(s=1.0)'],
                       fontsize=11)
    ax.legend(loc='best', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 130])
    
    # Guardar
    fig_path = OUTPUT_DIR / "fig3_temporal_stages_curriculum.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Guardada: {fig_path.name}")
    return fig_path


# ============================================================================
# FIGURA 4: SCATTER SAFETY-REWARD
# ============================================================================

def generate_fig4_scatter_safety_reward(data):
    """
    Figura 4: Scatter safety score (tripwires) vs reward (últimos 50 eps).
    
    Args:
        data: dict {group: {seed: DataFrame}}
    
    Returns:
        Path al archivo guardado
    """
    print("\n[4/4] Generando Figura 4: Scatter Safety-Reward Tradeoff...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    window_size = 50
    colors_group = {
        'Curriculum': '#2ecc71',
        'DirectoS1': '#e74c3c',
        'ControlS0': '#95a5a6'
    }
    
    # Scatter por grupo
    for group in GROUPS:
        x_data = []  # tripwires (safety score invertido)
        y_data = []  # reward
        
        for seed in SEEDS:
            if seed in data[group]:
                df_final = data[group][seed].iloc[-window_size:]
                
                mean_tripwires = df_final['tripwires_triggered'].mean()
                mean_reward = df_final['total_reward_env'].mean()
                
                x_data.append(mean_tripwires)
                y_data.append(mean_reward)
        
        # Plot
        ax.scatter(x_data, y_data, s=200, alpha=0.7, 
                  color=colors_group[group], edgecolor='black', linewidth=2,
                  label=group, zorder=3)
        
        # Anotar seeds
        for i, seed in enumerate(SEEDS):
            ax.annotate(f'{seed}', (x_data[i], y_data[i]), 
                       fontsize=9, ha='center', va='center', 
                       fontweight='bold', color='white')
    
    ax.set_xlabel('Tripwires Triggered (Mean, últimos 50 eps)', 
                 fontsize=13, fontweight='bold')
    ax.set_ylabel('Reward Env (Mean, últimos 50 eps)', 
                 fontsize=13, fontweight='bold')
    ax.set_title('v9: Tradeoff Safety-Reward por Grupo\n(Mayor tripwires = Menor prudencia)', 
                fontsize=15, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=12, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    # Añadir zonas conceptuales
    ax.axhline(y=80, color='red', linestyle=':', alpha=0.3, linewidth=1)
    ax.text(0.95, 75, 'Zona colapso', transform=ax.get_yaxis_transform(),
           ha='right', fontsize=10, style='italic', alpha=0.6)
    
    ax.axhline(y=110, color='green', linestyle=':', alpha=0.3, linewidth=1)
    ax.text(0.95, 112, 'Zona funcional', transform=ax.get_yaxis_transform(),
           ha='right', fontsize=10, style='italic', alpha=0.6)
    
    # Guardar
    fig_path = OUTPUT_DIR / "fig4_scatter_safety_reward.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Guardada: {fig_path.name}")
    return fig_path


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*70)
    print("GENERACIÓN VISUALIZACIONES v9")
    print("="*70)
    print(f"\nOutput: {OUTPUT_DIR}")
    
    # Cargar datos
    print("\nCargando datos...")
    data = load_all_data()
    print(f"✓ Datos cargados: {len(GROUPS)} grupos × {len(SEEDS)} seeds")
    
    # Generar figuras
    print("\nGenerando figuras...")
    
    fig1 = generate_fig1_learning_curves(data)
    fig2 = generate_fig2_barplot_ratios(data)
    fig3 = generate_fig3_temporal_stages(data)
    fig4 = generate_fig4_scatter_safety_reward(data)
    
    # Resumen
    print("\n" + "="*70)
    print("✅ VISUALIZACIONES COMPLETADAS")
    print("="*70)
    print(f"\n📁 Archivos generados:")
    print(f"   {fig1.name}")
    print(f"   {fig2.name}")
    print(f"   {fig3.name}")
    print(f"   {fig4.name}")
    
    print(f"\n🎨 Figuras listas para reporte v9 y paper.")


if __name__ == '__main__':
    main()
