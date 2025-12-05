#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualizaciones comparativas 4×4 vs 6×6.

Genera 2 figuras clave:
- Fig A: Ratios Curriculum/Control por grid size (con seed=123 destacado)
- Fig B: Varianza entre seeds por grid size

Author: TUI Team
Date: 2025-01-20
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Configuración estética
sns.set_context("paper", font_scale=1.3)
sns.set_style("whitegrid")
COLORS = {'Curriculum': '#2E86AB', 'DirectoS1': '#A23B72', 'ControlS0': '#F18F01'}

def load_results():
    """Carga resultados de análisis 6×6."""
    json_path = Path("results/pgf_v9/exploratorios/grid_6x6/analisis_6x6_completo.json")
    with open(json_path) as f:
        return json.load(f)

def plot_ratios_comparison(data):
    """Fig A: Ratios Curriculum/Control por grid size."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Datos
    grids = ['4×4', '6×6']
    ratios_4x4 = data['h_exp1_generalization']['ratio_4x4']['values']
    ratios_6x6 = data['h_exp1_generalization']['ratio_6x6']['values']
    
    # Scatter con seeds identificados
    seeds = [42, 123, 456]
    colors_4x4 = ['red' if s == 123 else 'steelblue' for s in seeds]
    colors_6x6 = ['green' if s == 123 else 'steelblue' for s in seeds]
    
    x_4x4 = np.random.normal(0, 0.04, size=len(ratios_4x4))
    x_6x6 = np.random.normal(1, 0.04, size=len(ratios_6x6))
    
    ax.scatter(x_4x4, ratios_4x4, s=150, c=colors_4x4, alpha=0.7, edgecolors='black', zorder=3)
    ax.scatter(x_6x6, ratios_6x6, s=150, c=colors_6x6, alpha=0.7, edgecolors='black', zorder=3)
    
    # Medias y CI
    mean_4x4 = data['h_exp1_generalization']['ratio_4x4']['mean']
    mean_6x6 = data['h_exp1_generalization']['ratio_6x6']['mean']
    ci_4x4 = [data['h_exp1_generalization']['ratio_4x4']['ci_lower'],
              data['h_exp1_generalization']['ratio_4x4']['ci_upper']]
    ci_6x6 = [data['h_exp1_generalization']['ratio_6x6']['ci_lower'],
              data['h_exp1_generalization']['ratio_6x6']['ci_upper']]
    
    ax.errorbar([0], [mean_4x4], yerr=[[mean_4x4 - ci_4x4[0]], [ci_4x4[1] - mean_4x4]], 
                fmt='D', color='black', markersize=10, capsize=8, capthick=2, zorder=4, label='Media ± 95% CI')
    ax.errorbar([1], [mean_6x6], yerr=[[mean_6x6 - ci_6x6[0]], [ci_6x6[1] - mean_6x6]], 
                fmt='D', color='black', markersize=10, capsize=8, capthick=2, zorder=4)
    
    # Línea threshold H9.1
    ax.axhline(y=0.70, color='gray', linestyle='--', linewidth=2, alpha=0.7, label='Threshold H9.1 (0.70)')
    
    # Anotaciones seed=123
    ax.annotate('seed=123\n(COLAPSO)', xy=(x_4x4[1], ratios_4x4[1]), 
                xytext=(x_4x4[1]-0.15, ratios_4x4[1]+0.15), fontsize=11, color='darkred',
                arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5))
    ax.annotate('seed=123\n(RECUPERACIÓN)', xy=(x_6x6[1], ratios_6x6[1]), 
                xytext=(x_6x6[1]+0.08, ratios_6x6[1]+0.15), fontsize=11, color='darkgreen',
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5))
    
    # Estética
    ax.set_xticks([0, 1])
    ax.set_xticklabels(grids, fontsize=14, fontweight='bold')
    ax.set_ylabel('Ratio Curriculum/Control', fontsize=14, fontweight='bold')
    ax.set_xlabel('Grid Size', fontsize=14, fontweight='bold')
    ax.set_title('Generalización del Curriculum Learning a Mayor Complejidad\n(N=3 seeds por condición)', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.set_ylim(-0.1, 1.3)
    ax.legend(loc='upper right', fontsize=12, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar
    output_path = Path("results/pgf_v9/exploratorios/grid_6x6/figA_ratios_4x4_vs_6x6.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Guardado: {output_path}")
    plt.close()

def plot_variance_comparison(data):
    """Fig B: Varianza Curriculum entre seeds por grid size."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Extraer rewards Curriculum por grid
    rewards_4x4 = data['grid_comparison']['4x4']['Curriculum']
    rewards_6x6 = data['grid_comparison']['6x6']['Curriculum']
    
    seeds = [42, 123, 456]
    
    # Barplot con seeds identificados
    x = np.arange(2)
    width = 0.25
    
    for i, seed in enumerate(seeds):
        color = 'red' if seed == 123 else 'steelblue'
        alpha = 1.0 if seed == 123 else 0.7
        ax.bar(x + i*width, [rewards_4x4[i], rewards_6x6[i]], width, 
               label=f'seed={seed}', color=color, alpha=alpha, edgecolor='black', linewidth=1.5)
    
    # Línea de paridad (100 reward)
    ax.axhline(y=100, color='green', linestyle='--', linewidth=2, alpha=0.6, label='Paridad (~100 reward)')
    
    # Estética
    ax.set_xticks(x + width)
    ax.set_xticklabels(['4×4', '6×6'], fontsize=14, fontweight='bold')
    ax.set_ylabel('Reward Final (últimos 50 episodios)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Grid Size', fontsize=14, fontweight='bold')
    ax.set_title('Varianza Entre Seeds: Curriculum Learning\n(Recuperación de seed=123 en 6×6)', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.set_ylim(0, 140)
    ax.legend(loc='upper left', fontsize=12, framealpha=0.95, ncol=2)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Anotación varianza
    cv_4x4 = np.std(rewards_4x4, ddof=1) / np.mean(rewards_4x4)
    cv_6x6 = np.std(rewards_6x6, ddof=1) / np.mean(rewards_6x6)
    ax.text(0.02, 0.98, f'CV 4×4: {cv_4x4:.2f}\nCV 6×6: {cv_6x6:.2f}', 
            transform=ax.transAxes, fontsize=12, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    # Guardar
    output_path = Path("results/pgf_v9/exploratorios/grid_6x6/figB_variance_seeds_4x4_vs_6x6.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Guardado: {output_path}")
    plt.close()

def main():
    print("=" * 70)
    print("VISUALIZACIONES COMPARATIVAS 4×4 vs 6×6")
    print("=" * 70)
    
    # Cargar datos
    data = load_results()
    
    # Generar figuras
    plot_ratios_comparison(data)
    plot_variance_comparison(data)
    
    print("\n" + "=" * 70)
    print("✅ VISUALIZACIONES COMPLETADAS")
    print("=" * 70)
    print("  Fig A: Ratios Curriculum/Control por grid")
    print("  Fig B: Varianza entre seeds por grid")

if __name__ == "__main__":
    main()
