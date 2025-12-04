#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualización comparativa multiescala: 4×4 vs 6×6 vs 8×8.

Genera figura de 3 paneles:
- Panel A: Ratios Curriculum/Control por grid size
- Panel B: Coeficiente de variación (CV) por grid size
- Panel C: Trayectoria seed=123 (4×4 → 6×6 → 8×8)

Author: TUI Team
Date: 2025-12-03
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_analysis_results():
    """Carga resultados de análisis 6×6 y 8×8."""
    # 6×6
    with open("results/pgf_v9/exploratorios/grid_6x6/analisis_6x6_completo.json") as f:
        results_6x6 = json.load(f)
    
    # 8×8
    with open("results/pgf_v9/exploratorios/grid_8x8/analisis_8x8_completo.json") as f:
        results_8x8 = json.load(f)
    
    return results_6x6, results_8x8

def extract_multiscale_data(results_6x6, results_8x8):
    """Extrae datos para comparación multiescala."""
    # Ratios
    ratio_4x4 = results_6x6['h_exp1_generalization']['ratio_4x4']['mean']
    ratio_6x6 = results_6x6['h_exp1_generalization']['ratio_6x6']['mean']
    ratio_8x8 = results_8x8['h_exp1_extension_8x8']['ratio_8x8']['mean']
    
    ratio_4x4_std = results_6x6['h_exp1_generalization']['ratio_4x4']['std']
    ratio_6x6_std = results_6x6['h_exp1_generalization']['ratio_6x6']['std']
    ratio_8x8_std = results_8x8['h_exp1_extension_8x8']['ratio_8x8']['std']
    
    # CV
    cv_4x4 = results_8x8['variance_analysis']['cv_4x4']
    cv_6x6 = results_8x8['variance_analysis']['cv_6x6']
    cv_8x8 = results_8x8['variance_analysis']['cv_8x8']
    
    # Seed=123 trajectory
    seed123_4x4 = results_6x6['seed123_recovery']['4x4_reward']
    seed123_6x6 = results_6x6['seed123_recovery']['6x6_reward']
    seed123_8x8 = results_8x8['seed123_trajectory']['trajectory']['8x8']
    
    return {
        'ratios': {
            'values': [ratio_4x4, ratio_6x6, ratio_8x8],
            'stds': [ratio_4x4_std, ratio_6x6_std, ratio_8x8_std]
        },
        'cvs': [cv_4x4, cv_6x6, cv_8x8],
        'seed123': [seed123_4x4, seed123_6x6, seed123_8x8]
    }

def create_comparison_figure(data):
    """Genera figura de 3 paneles."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    grid_labels = ['4×4\n(16 cells)', '6×6\n(36 cells)', '8×8\n(64 cells)']
    grid_sizes = [16, 36, 64]
    
    # Panel A: Ratios Curriculum/Control
    ax1 = axes[0]
    ratios = data['ratios']['values']
    stds = data['ratios']['stds']
    
    bars = ax1.bar(grid_labels, ratios, yerr=stds, capsize=5, 
                   color=['#2ecc71', '#3498db', '#e74c3c'], alpha=0.7)
    ax1.axhline(y=0.70, color='red', linestyle='--', linewidth=2, label='Threshold (0.70)')
    ax1.axhline(y=1.0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    
    ax1.set_ylabel('Ratio Curriculum/Control', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Grid Size', fontsize=12)
    ax1.set_title('A. Efectividad Curriculum por Complejidad', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_ylim([0, 1.2])
    
    # Anotaciones
    for i, (r, s) in enumerate(zip(ratios, stds)):
        ax1.text(i, r + s + 0.05, f'{r:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Panel B: Coeficiente de Variación
    ax2 = axes[1]
    cvs = data['cvs']
    
    ax2.plot(grid_sizes, cvs, marker='o', markersize=10, linewidth=2.5, 
             color='#9b59b6', label='CV Curriculum')
    ax2.fill_between(grid_sizes, cvs, alpha=0.2, color='#9b59b6')
    
    ax2.set_ylabel('Coeficiente de Variación (CV)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Grid Size (cells)', fontsize=12)
    ax2.set_title('B. Varianza entre Seeds vs Complejidad', fontsize=13, fontweight='bold')
    ax2.grid(alpha=0.3)
    ax2.legend(loc='upper left')
    
    # Anotaciones
    for gs, cv in zip(grid_sizes, cvs):
        ax2.text(gs, cv + 0.05, f'{cv:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Panel C: Trayectoria seed=123
    ax3 = axes[2]
    seed123 = data['seed123']
    
    ax3.plot(grid_sizes, seed123, marker='s', markersize=12, linewidth=3, 
             color='#e67e22', label='Seed=123')
    ax3.fill_between(grid_sizes, seed123, alpha=0.2, color='#e67e22')
    
    # Threshold éxito
    ax3.axhline(y=100, color='green', linestyle='--', linewidth=2, label='Éxito (>100)', alpha=0.7)
    ax3.axhline(y=50, color='red', linestyle='--', linewidth=2, label='Colapso (<50)', alpha=0.7)
    
    ax3.set_ylabel('Reward Final (mean)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Grid Size (cells)', fontsize=12)
    ax3.set_title('C. Tracking Seed=123 (4×4 → 6×6 → 8×8)', fontsize=13, fontweight='bold')
    ax3.legend(loc='lower left')
    ax3.grid(alpha=0.3)
    ax3.set_ylim([0, 140])
    
    # Anotaciones
    for gs, s123 in zip(grid_sizes, seed123):
        ax3.text(gs, s123 + 5, f'{s123:.1f}', ha='center', va='bottom', 
                fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    return fig

def main():
    print("=" * 70)
    print("VISUALIZACIÓN COMPARATIVA MULTIESCALA (4×4 vs 6×6 vs 8×8)")
    print("=" * 70)
    
    # Carga análisis
    print("\n📊 Cargando resultados análisis...")
    results_6x6, results_8x8 = load_analysis_results()
    
    # Extrae datos
    data = extract_multiscale_data(results_6x6, results_8x8)
    
    print("\n📈 Datos extraídos:")
    print(f"   Ratios: {data['ratios']['values']}")
    print(f"   CVs: {data['cvs']}")
    print(f"   Seed=123: {data['seed123']}")
    
    # Crea figura
    print("\n🎨 Generando figura...")
    fig = create_comparison_figure(data)
    
    # Guarda
    output_dir = Path("plots/v9")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "multiescala_4x4_6x6_8x8_comparison.png"
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Figura guardada: {output_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("HALLAZGOS CLAVE")
    print("=" * 70)
    print(f"📉 Ratio Curriculum/Control:")
    print(f"   4×4: {data['ratios']['values'][0]:.3f} (MARGINAL)")
    print(f"   6×6: {data['ratios']['values'][1]:.3f} (ÉXITO)")
    print(f"   8×8: {data['ratios']['values'][2]:.3f} (COLAPSO PARCIAL)")
    print(f"\n📊 Coeficiente de Variación:")
    print(f"   4×4: {data['cvs'][0]:.3f}")
    print(f"   6×6: {data['cvs'][1]:.3f} (menor varianza)")
    print(f"   8×8: {data['cvs'][2]:.3f} (inestabilidad máxima)")
    print(f"\n🔑 Seed=123:")
    print(f"   Trayectoria: {data['seed123'][0]:.1f} → {data['seed123'][1]:.1f} → {data['seed123'][2]:.1f}")
    print(f"   Interpretación: RECUPERACIÓN en 6×6, ESTABILIDAD en 8×8")

if __name__ == "__main__":
    main()
