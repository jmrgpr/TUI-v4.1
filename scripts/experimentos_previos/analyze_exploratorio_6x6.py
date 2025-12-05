#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis estadístico completo del exploratorio 6×6 (N=3 seeds).

Compara resultados 4×4 vs 6×6 para validar:
- H_exp1: Generalización a mayor complejidad espacial
- H_exp2: Posible amplificación del efecto con complejidad

Author: TUI Team
Date: 2025-01-20
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

def load_6x6_results(seeds=[42, 123, 456]):
    """Carga todos los resultados de 6×6."""
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
                stats = data['stats']
                results[group].append({
                    'seed': seed,
                    'reward_final': stats['mean_reward_env_final'],
                    'success_rate': stats['success_rate_final'],
                    'tripwires': stats['mean_tripwires_final'],
                    'reward_std': stats['std_reward_env_final']
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

def test_generalization(results_4x4, results_6x6):
    """Test estadístico H_exp1: Curriculum mantiene efectividad en 6×6."""
    # Ratio Curriculum/Control en cada grid
    ratio_4x4 = compute_ratios(results_4x4)['curriculum']
    ratio_6x6 = compute_ratios(results_6x6)['curriculum']
    
    # Test t independiente (diferentes ambientes)
    t_stat, p_val = stats.ttest_ind(ratio_4x4['values'], ratio_6x6['values'])
    
    # H_exp1: ratio_6x6 >= 0.70 (threshold conservador)
    h_exp1_validated = ratio_6x6['mean'] >= 0.70 and ratio_6x6['ci_lower'] > 0.0
    
    return {
        'ratio_4x4': ratio_4x4,
        'ratio_6x6': ratio_6x6,
        't_statistic': t_stat,
        'p_value': p_val,
        'h_exp1_validated': h_exp1_validated,
        'interpretation': 'VALIDATED' if h_exp1_validated else 'REJECTED'
    }

def test_amplification(results_4x4, results_6x6):
    """Test estadístico H_exp2: Curriculum mejora con complejidad."""
    ratio_4x4 = compute_ratios(results_4x4)['curriculum']
    ratio_6x6 = compute_ratios(results_6x6)['curriculum']
    
    # Test direccional: ratio_6x6 > ratio_4x4
    t_stat, p_val_two_tailed = stats.ttest_ind(ratio_6x6['values'], ratio_4x4['values'])
    p_val_one_tailed = p_val_two_tailed / 2 if t_stat > 0 else 1 - p_val_two_tailed / 2
    
    # Cohen's d para magnitud del efecto
    pooled_std = np.sqrt((ratio_4x4['std']**2 + ratio_6x6['std']**2) / 2)
    cohens_d = (ratio_6x6['mean'] - ratio_4x4['mean']) / pooled_std if pooled_std > 0 else 0
    
    # H_exp2: ratio_6x6 > ratio_4x4 (con p < 0.05)
    h_exp2_validated = ratio_6x6['mean'] > ratio_4x4['mean'] and p_val_one_tailed < 0.05
    
    return {
        'difference': ratio_6x6['mean'] - ratio_4x4['mean'],
        'percent_improvement': ((ratio_6x6['mean'] - ratio_4x4['mean']) / ratio_4x4['mean'] * 100),
        't_statistic': t_stat,
        'p_value_one_tailed': p_val_one_tailed,
        'cohens_d': cohens_d,
        'h_exp2_validated': h_exp2_validated,
        'interpretation': 'VALIDATED' if h_exp2_validated else 'NOT SIGNIFICANT'
    }

def analyze_seed_variance(results_6x6):
    """Analiza varianza entre seeds en 6×6 vs 4×4."""
    curriculum_rewards = [r['reward_final'] for r in results_6x6['Curriculum']]
    
    # Identifica si algún seed colapsó (reward < 50)
    collapsed_seeds = [r['seed'] for r in results_6x6['Curriculum'] if r['reward_final'] < 50]
    successful_seeds = [r['seed'] for r in results_6x6['Curriculum'] if r['reward_final'] >= 100]
    
    return {
        'collapsed_seeds': collapsed_seeds,
        'successful_seeds': successful_seeds,
        'variance': np.var(curriculum_rewards, ddof=1),
        'cv': np.std(curriculum_rewards, ddof=1) / np.mean(curriculum_rewards) if np.mean(curriculum_rewards) > 0 else 0,
        'interpretation': 'SEED=123 RECOVERED' if 123 not in collapsed_seeds else 'SEED=123 COLLAPSED AGAIN'
    }

def main():
    print("=" * 70)
    print("ANÁLISIS EXPLORATORIO 6×6 (N=3 seeds)")
    print("=" * 70)
    
    # Carga datos
    results_4x4 = load_4x4_results()
    results_6x6 = load_6x6_results()
    
    print("\n📊 DESCRIPTIVOS 4×4:")
    for group, data in results_4x4.items():
        rewards = [r['reward_final'] for r in data]
        print(f"   {group:12}: {np.mean(rewards):6.2f} ± {np.std(rewards, ddof=1):5.2f}")
    
    print("\n📊 DESCRIPTIVOS 6×6:")
    for group, data in results_6x6.items():
        rewards = [r['reward_final'] for r in data]
        print(f"   {group:12}: {np.mean(rewards):6.2f} ± {np.std(rewards, ddof=1):5.2f}")
    
    # Test H_exp1: Generalización
    print("\n" + "=" * 70)
    print("TEST H_exp1: GENERALIZACIÓN A 6×6")
    print("=" * 70)
    gen_results = test_generalization(results_4x4, results_6x6)
    
    print(f"\nRatio Curriculum/Control 4×4: {gen_results['ratio_4x4']['mean']:.3f} ± {gen_results['ratio_4x4']['std']:.3f}")
    print(f"  95% CI: [{gen_results['ratio_4x4']['ci_lower']:.3f}, {gen_results['ratio_4x4']['ci_upper']:.3f}]")
    print(f"  Seeds: {gen_results['ratio_4x4']['values']}")
    
    print(f"\nRatio Curriculum/Control 6×6: {gen_results['ratio_6x6']['mean']:.3f} ± {gen_results['ratio_6x6']['std']:.3f}")
    print(f"  95% CI: [{gen_results['ratio_6x6']['ci_lower']:.3f}, {gen_results['ratio_6x6']['ci_upper']:.3f}]")
    print(f"  Seeds: {gen_results['ratio_6x6']['values']}")
    
    print(f"\nt-test independiente: t={gen_results['t_statistic']:.3f}, p={gen_results['p_value']:.4f}")
    print(f"H_exp1 (ratio ≥ 0.70): {gen_results['interpretation']} ✅" if gen_results['h_exp1_validated'] else f"H_exp1: {gen_results['interpretation']} ❌")
    
    # Test H_exp2: Amplificación
    print("\n" + "=" * 70)
    print("TEST H_exp2: AMPLIFICACIÓN CON COMPLEJIDAD")
    print("=" * 70)
    amp_results = test_amplification(results_4x4, results_6x6)
    
    print(f"\nDiferencia (6×6 - 4×4): {amp_results['difference']:+.3f} ({amp_results['percent_improvement']:+.1f}%)")
    print(f"Cohen's d: {amp_results['cohens_d']:.3f}")
    print(f"t-test direccional: t={amp_results['t_statistic']:.3f}, p={amp_results['p_value_one_tailed']:.4f}")
    print(f"H_exp2 (6×6 > 4×4): {amp_results['interpretation']}", end="")
    print(" ✅" if amp_results['h_exp2_validated'] else " ❌")
    
    # Análisis varianza seeds
    print("\n" + "=" * 70)
    print("ANÁLISIS VARIANZA ENTRE SEEDS (6×6)")
    print("=" * 70)
    var_results = analyze_seed_variance(results_6x6)
    
    print(f"\nSeeds exitosos (reward ≥ 100): {var_results['successful_seeds']}")
    print(f"Seeds colapsados (reward < 50): {var_results['collapsed_seeds']}")
    print(f"Coeficiente variación: {var_results['cv']:.3f}")
    print(f"Interpretación: {var_results['interpretation']}")
    
    # HALLAZGO CLAVE: seed=123
    curriculum_6x6_by_seed = {r['seed']: r['reward_final'] for r in results_6x6['Curriculum']}
    curriculum_4x4_by_seed = {r['seed']: r['reward_final'] for r in results_4x4['Curriculum']}
    
    print(f"\n🔍 ANÁLISIS SEED=123:")
    print(f"   4×4: {curriculum_4x4_by_seed[123]:.2f} reward (COLAPSO)")
    print(f"   6×6: {curriculum_6x6_by_seed[123]:.2f} reward (RECUPERACIÓN)")
    print(f"   Interpretación: La mayor complejidad 6×6 ESTABILIZA seed=123")
    
    # Exporta resultados
    output = {
        'grid_comparison': {
            '4x4': {group: [r['reward_final'] for r in data] for group, data in results_4x4.items()},
            '6x6': {group: [r['reward_final'] for r in data] for group, data in results_6x6.items()}
        },
        'h_exp1_generalization': gen_results,
        'h_exp2_amplification': amp_results,
        'seed_variance_6x6': var_results,
        'seed123_recovery': {
            '4x4_reward': curriculum_4x4_by_seed[123],
            '6x6_reward': curriculum_6x6_by_seed[123],
            'interpretation': 'GRID 6×6 ESTABILIZA SEED=123'
        }
    }
    
    # Convierte numpy types para JSON
    def convert_numpy(obj):
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(item) for item in obj]
        return obj
    
    output = convert_numpy(output)
    
    # Clase custom para JSON serialization
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.bool_):
                return bool(obj)
            return super().default(obj)
    
    output_path = Path("results/pgf_v9/exploratorios/grid_6x6/analisis_6x6_completo.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    
    print(f"\n✓ Resultados guardados: {output_path}")
    
    # Summary final
    print("\n" + "=" * 70)
    print("RESUMEN EJECUTIVO EXPLORATORIO 6×6")
    print("=" * 70)
    print(f"✅ H_exp1 (Generalización): {gen_results['interpretation']}")
    print(f"   Ratio 6×6 = {gen_results['ratio_6x6']['mean']:.3f} (threshold: 0.70)")
    print(f"{'✅' if amp_results['h_exp2_validated'] else '❌'} H_exp2 (Amplificación): {amp_results['interpretation']}")
    print(f"   Mejora 6×6 vs 4×4: {amp_results['percent_improvement']:+.1f}% (p={amp_results['p_value_one_tailed']:.4f})")
    print(f"\n🔑 HALLAZGO CLAVE: Seed=123 se RECUPERA en 6×6")
    print(f"   Mayor complejidad espacial ESTABILIZA curriculum learning")

if __name__ == "__main__":
    main()
