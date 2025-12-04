#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis estadístico completo del exploratorio 8×8 (N=3 seeds).

Compara resultados 4×4 vs 6×6 vs 8×8 para validar:
- H_exp1 extensión: Generalización a 8×8 (ratio ≥ 0.70)
- Análisis colapso: ¿Dónde falla curriculum learning?
- Límite arquitectural: ¿Es DQN 2×64 insuficiente?

Author: TUI Team
Date: 2025-12-03
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

def load_8x8_results(seeds=[42, 123, 456]):
    """Carga todos los resultados de 8×8."""
    base_dir = Path("results/pgf_v9/resultados")
    
    results = {
        'Curriculum': [],
        'DirectoS1': [],
        'ControlS0': []
    }
    
    for seed in seeds:
        for group in results.keys():
            json_path = base_dir / f"exp9_{group}_seed{seed}_metrics.json"
            with open(json_path) as f:
                data = json.load(f)
                stats_data = data['stats']
                results[group].append({
                    'seed': seed,
                    'reward_final': stats_data['mean_reward_env_final'],
                    'success_rate': stats_data['success_rate_final'],
                    'tripwires': stats_data['mean_tripwires_final'],
                    'reward_std': stats_data['std_reward_env_final']
                })
    
    return results

def load_6x6_results(seeds=[42, 123, 456]):
    """Carga resultados 6×6."""
    base_dir = Path("results/pgf_v9/exploratorios/grid_6x6/resultados")
    
    results = {
        'Curriculum': [],
        'DirectoS1': [],
        'ControlS0': []
    }
    
    for seed in seeds:
        for group in results.keys():
            json_path = base_dir / f"exp9_{group}_seed{seed}_metrics.json"
            with open(json_path) as f:
                data = json.load(f)
                stats_data = data['stats']
                results[group].append({
                    'seed': seed,
                    'reward_final': stats_data['mean_reward_env_final'],
                    'success_rate': stats_data['success_rate_final'],
                    'tripwires': stats_data['mean_tripwires_final'],
                    'reward_std': stats_data['std_reward_env_final']
                })
    
    return results

def load_4x4_results(seeds=[42, 123, 456]):
    """Carga resultados 4×4 del CSV de métricas finales."""
    csv_path = Path("results/pgf_v9/analisis/curriculum_metrics_final.csv")
    df = pd.read_csv(csv_path)
    
    results = {
        'Curriculum': [],
        'DirectoS1': [],
        'ControlS0': []
    }
    
    for seed in seeds:
        for group in results.keys():
            row = df[(df['group'] == group) & (df['seed'] == seed)]
            if len(row) > 0:
                results[group].append({
                    'seed': seed,
                    'reward_final': row.iloc[0]['mean_reward_env'],
                    'success_rate': row.iloc[0]['success_rate'],
                    'tripwires': row.iloc[0]['mean_tripwires'],
                    'reward_std': row.iloc[0]['std_reward_env']
                })
    
    return results

def compute_ratios(results):
    """Calcula ratios Curriculum/Control y DirectoS1/Control."""
    curriculum_rewards = [r['reward_final'] for r in results['Curriculum']]
    control_rewards = [r['reward_final'] for r in results['ControlS0']]
    directo_rewards = [r['reward_final'] for r in results['DirectoS1']]
    
    ratios_curriculum = [c/ctrl for c, ctrl in zip(curriculum_rewards, control_rewards)]
    ratios_directo = [d/ctrl for d, ctrl in zip(directo_rewards, control_rewards)]
    
    return {
        'curriculum': {
            'values': ratios_curriculum,
            'mean': np.mean(ratios_curriculum),
            'std': np.std(ratios_curriculum, ddof=1),
            'ci_lower': np.mean(ratios_curriculum) - 1.96 * np.std(ratios_curriculum, ddof=1) / np.sqrt(len(ratios_curriculum)),
            'ci_upper': np.mean(ratios_curriculum) + 1.96 * np.std(ratios_curriculum, ddof=1) / np.sqrt(len(ratios_curriculum))
        },
        'directo': {
            'values': ratios_directo,
            'mean': np.mean(ratios_directo),
            'std': np.std(ratios_directo, ddof=1)
        }
    }

def test_8x8_generalization(results_8x8):
    """Test H_exp1 extensión: ¿Se mantiene efectividad en 8×8?"""
    ratios_8x8 = compute_ratios(results_8x8)['curriculum']
    
    # H_exp1: ratio_8x8 >= 0.70 (threshold conservador)
    h_exp1_validated = ratios_8x8['mean'] >= 0.70 and ratios_8x8['ci_lower'] > 0.0
    
    # Clasificación resultado
    if ratios_8x8['mean'] >= 0.70:
        interpretation = 'SUCCESS: Curriculum mantiene efectividad'
    elif ratios_8x8['mean'] >= 0.50:
        interpretation = 'PARTIAL COLLAPSE: Degradación significativa'
    else:
        interpretation = 'COMPLETE COLLAPSE: Curriculum falla totalmente'
    
    return {
        'ratio_8x8': ratios_8x8,
        'h_exp1_validated': h_exp1_validated,
        'interpretation': interpretation
    }

def analyze_multiscale_trend(results_4x4, results_6x6, results_8x8):
    """Analiza tendencia ratio vs complejidad espacial."""
    ratio_4x4 = compute_ratios(results_4x4)['curriculum']
    ratio_6x6 = compute_ratios(results_6x6)['curriculum']
    ratio_8x8 = compute_ratios(results_8x8)['curriculum']
    
    # Tendencia ratio vs grid size
    grid_sizes = [16, 36, 64]  # 4×4, 6×6, 8×8
    ratios = [ratio_4x4['mean'], ratio_6x6['mean'], ratio_8x8['mean']]
    
    # Regresión lineal simple
    from scipy.stats import linregress
    slope, intercept, r_value, p_value, std_err = linregress(grid_sizes, ratios)
    
    trend = 'NEGATIVE (colapso con complejidad)' if slope < 0 else 'POSITIVE (mejora con complejidad)'
    
    return {
        'grid_sizes': grid_sizes,
        'ratios': ratios,
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value,
        'trend': trend,
        'interpretation': f'Pendiente={slope:.4f} por celda² (R²={r_value**2:.3f}, p={p_value:.4f})'
    }

def analyze_seed123_trajectory(results_4x4, results_6x6, results_8x8):
    """Tracking completo seed=123 a través de 4×4 → 6×6 → 8×8."""
    curriculum_4x4 = {r['seed']: r for r in results_4x4['Curriculum']}
    curriculum_6x6 = {r['seed']: r for r in results_6x6['Curriculum']}
    curriculum_8x8 = {r['seed']: r for r in results_8x8['Curriculum']}
    
    seed123_trajectory = {
        '4x4': curriculum_4x4[123]['reward_final'],
        '6x6': curriculum_6x6[123]['reward_final'],
        '8x8': curriculum_8x8[123]['reward_final']
    }
    
    # Clasificación trayectoria
    if seed123_trajectory['8x8'] >= 100:
        status_8x8 = 'RECOVERED: Mantiene estabilidad'
    elif seed123_trajectory['8x8'] >= 50:
        status_8x8 = 'DEGRADED: Pérdida parcial'
    else:
        status_8x8 = 'COLLAPSED: Falla completa'
    
    return {
        'trajectory': seed123_trajectory,
        'status_8x8': status_8x8,
        'interpretation': f"Seed=123: {seed123_trajectory['4x4']:.1f} → {seed123_trajectory['6x6']:.1f} → {seed123_trajectory['8x8']:.1f}"
    }

def analyze_variance_by_grid(results_4x4, results_6x6, results_8x8):
    """Analiza cómo evoluciona la varianza entre seeds con complejidad."""
    curriculum_rewards_4x4 = [r['reward_final'] for r in results_4x4['Curriculum']]
    curriculum_rewards_6x6 = [r['reward_final'] for r in results_6x6['Curriculum']]
    curriculum_rewards_8x8 = [r['reward_final'] for r in results_8x8['Curriculum']]
    
    cv_4x4 = np.std(curriculum_rewards_4x4, ddof=1) / np.mean(curriculum_rewards_4x4)
    cv_6x6 = np.std(curriculum_rewards_6x6, ddof=1) / np.mean(curriculum_rewards_6x6)
    cv_8x8 = np.std(curriculum_rewards_8x8, ddof=1) / np.mean(curriculum_rewards_8x8)
    
    # Interpretación
    if cv_8x8 > cv_6x6 and cv_6x6 > cv_4x4:
        trend = 'INCREASING: Inestabilidad crece con complejidad'
    elif cv_8x8 < cv_6x6:
        trend = 'STABILIZING: Complejidad reduce varianza'
    else:
        trend = 'MIXED: Sin tendencia clara'
    
    return {
        'cv_4x4': cv_4x4,
        'cv_6x6': cv_6x6,
        'cv_8x8': cv_8x8,
        'trend': trend,
        'interpretation': f'CV: {cv_4x4:.3f} (4×4) → {cv_6x6:.3f} (6×6) → {cv_8x8:.3f} (8×8)'
    }

def diagnose_architectural_limit(results_8x8):
    """Diagnóstico: ¿Es la arquitectura DQN 2×64 el límite?"""
    control_rewards = [r['reward_final'] for r in results_8x8['ControlS0']]
    curriculum_rewards = [r['reward_final'] for r in results_8x8['Curriculum']]
    
    control_mean = np.mean(control_rewards)
    curriculum_mean = np.mean(curriculum_rewards)
    
    # Diagnóstico
    if control_mean >= 100:
        if curriculum_mean >= 100:
            diagnosis = 'ARQUITECTURA SUFICIENTE: Ambos grupos resuelven 8×8'
        else:
            diagnosis = 'PROBLEMA CURRICULAR: Arquitectura OK, falla graduación'
    else:
        diagnosis = 'LÍMITE ARQUITECTURAL: DQN 2×64 insuficiente para 8×8'
    
    return {
        'control_mean': control_mean,
        'control_success': control_mean >= 100,
        'curriculum_mean': curriculum_mean,
        'curriculum_success': curriculum_mean >= 100,
        'diagnosis': diagnosis,
        'recommendation': 'Revisar etapas curriculum (75 eps insuficiente)' if 'CURRICULAR' in diagnosis else 'Upgrade arquitectura a DQN 3×128'
    }

def main():
    print("=" * 70)
    print("ANÁLISIS EXPLORATORIO 8×8 (N=3 seeds)")
    print("=" * 70)
    
    # Carga datos multiescala
    results_4x4 = load_4x4_results()
    results_6x6 = load_6x6_results()
    results_8x8 = load_8x8_results()
    
    print("\n📊 DESCRIPTIVOS 4×4:")
    for group, data in results_4x4.items():
        rewards = [r['reward_final'] for r in data]
        print(f"   {group:12}: {np.mean(rewards):6.2f} ± {np.std(rewards, ddof=1):5.2f}")
    
    print("\n📊 DESCRIPTIVOS 6×6:")
    for group, data in results_6x6.items():
        rewards = [r['reward_final'] for r in data]
        print(f"   {group:12}: {np.mean(rewards):6.2f} ± {np.std(rewards, ddof=1):5.2f}")
    
    print("\n📊 DESCRIPTIVOS 8×8:")
    for group, data in results_8x8.items():
        rewards = [r['reward_final'] for r in data]
        seeds_detail = [(r['seed'], r['reward_final']) for r in data]
        print(f"   {group:12}: {np.mean(rewards):6.2f} ± {np.std(rewards, ddof=1):5.2f}")
        print(f"                 Seeds: {seeds_detail}")
    
    # Test H_exp1 extensión
    print("\n" + "=" * 70)
    print("TEST H_exp1 EXTENSIÓN: GENERALIZACIÓN A 8×8")
    print("=" * 70)
    gen_8x8 = test_8x8_generalization(results_8x8)
    
    print(f"\nRatio Curriculum/Control 8×8: {gen_8x8['ratio_8x8']['mean']:.3f} ± {gen_8x8['ratio_8x8']['std']:.3f}")
    print(f"  95% CI: [{gen_8x8['ratio_8x8']['ci_lower']:.3f}, {gen_8x8['ratio_8x8']['ci_upper']:.3f}]")
    print(f"  Seeds: {gen_8x8['ratio_8x8']['values']}")
    
    print(f"\nH_exp1 (ratio ≥ 0.70): {'VALIDATED ✅' if gen_8x8['h_exp1_validated'] else 'REJECTED ❌'}")
    print(f"Interpretación: {gen_8x8['interpretation']}")
    
    # Análisis tendencia multiescala
    print("\n" + "=" * 70)
    print("ANÁLISIS TENDENCIA MULTIESCALA (4×4 → 6×6 → 8×8)")
    print("=" * 70)
    trend = analyze_multiscale_trend(results_4x4, results_6x6, results_8x8)
    
    print(f"\nGrid sizes: {trend['grid_sizes']}")
    print(f"Ratios Curriculum/Control:")
    print(f"  4×4: {trend['ratios'][0]:.3f}")
    print(f"  6×6: {trend['ratios'][1]:.3f}")
    print(f"  8×8: {trend['ratios'][2]:.3f}")
    print(f"\nTendencia: {trend['trend']}")
    print(f"{trend['interpretation']}")
    
    # Tracking seed=123
    print("\n" + "=" * 70)
    print("TRACKING SEED=123 (4×4 → 6×6 → 8×8)")
    print("=" * 70)
    seed123 = analyze_seed123_trajectory(results_4x4, results_6x6, results_8x8)
    
    print(f"\n{seed123['interpretation']}")
    print(f"Status en 8×8: {seed123['status_8x8']}")
    
    # Análisis varianza
    print("\n" + "=" * 70)
    print("ANÁLISIS VARIANZA ENTRE SEEDS")
    print("=" * 70)
    variance = analyze_variance_by_grid(results_4x4, results_6x6, results_8x8)
    
    print(f"\n{variance['interpretation']}")
    print(f"Tendencia: {variance['trend']}")
    
    # Diagnóstico arquitectural
    print("\n" + "=" * 70)
    print("DIAGNÓSTICO LÍMITE ARQUITECTURAL")
    print("=" * 70)
    arch_diag = diagnose_architectural_limit(results_8x8)
    
    print(f"\nControl (s=0.0) en 8×8: {arch_diag['control_mean']:.2f} reward")
    print(f"  ¿Resuelve 8×8?: {'SÍ ✅' if arch_diag['control_success'] else 'NO ❌'}")
    print(f"\nCurriculum en 8×8: {arch_diag['curriculum_mean']:.2f} reward")
    print(f"  ¿Resuelve 8×8?: {'SÍ ✅' if arch_diag['curriculum_success'] else 'NO ❌'}")
    
    print(f"\n🔍 DIAGNÓSTICO: {arch_diag['diagnosis']}")
    print(f"💡 RECOMENDACIÓN: {arch_diag['recommendation']}")
    
    # Exporta resultados
    output = {
        'grid_comparison': {
            '4x4': {group: [r['reward_final'] for r in data] for group, data in results_4x4.items()},
            '6x6': {group: [r['reward_final'] for r in data] for group, data in results_6x6.items()},
            '8x8': {group: [r['reward_final'] for r in data] for group, data in results_8x8.items()}
        },
        'h_exp1_extension_8x8': gen_8x8,
        'multiscale_trend': trend,
        'seed123_trajectory': seed123,
        'variance_analysis': variance,
        'architectural_diagnosis': arch_diag
    }
    
    # Convierte numpy types
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.bool_):
                return bool(obj)
            return super().default(obj)
    
    output_path = Path("results/pgf_v9/exploratorios/grid_8x8/analisis_8x8_completo.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    
    print(f"\n✓ Resultados guardados: {output_path}")
    
    # Summary final
    print("\n" + "=" * 70)
    print("RESUMEN EJECUTIVO EXPLORATORIO 8×8")
    print("=" * 70)
    print(f"❌ H_exp1 extensión: {gen_8x8['interpretation']}")
    print(f"   Ratio 8×8 = {gen_8x8['ratio_8x8']['mean']:.3f} (threshold: 0.70)")
    print(f"\n📉 Tendencia multiescala: {trend['trend']}")
    print(f"   Ratios: 0.766 (4×4) → 0.859 (6×6) → {gen_8x8['ratio_8x8']['mean']:.3f} (8×8)")
    print(f"\n🔑 Seed=123: {seed123['status_8x8']}")
    print(f"   {seed123['interpretation']}")
    print(f"\n🏗️  Diagnóstico: {arch_diag['diagnosis']}")
    print(f"   {arch_diag['recommendation']}")

if __name__ == "__main__":
    main()
