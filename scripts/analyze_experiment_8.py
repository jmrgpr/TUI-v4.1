"""
Análisis Estadístico Experimento v8: Efectos de Intensidad de Reward Shaping

Este script implementa el plan de análisis preregistrado en PREREGISTRO_v8.md:
- ANOVA 2-way: Shaping × Densidad
- Post-hoc: Tukey HSD para comparaciones pareadas
- Effect sizes: η² (eta-squared)
- Análisis de ratios: reward_env (principal), tripwires, steps

Autor: TUI v4.1
Fecha: 3 diciembre 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import f_oneway
import json
from pathlib import Path
from itertools import combinations
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

# Configuración
RESULTS_DIR = Path("results/pgf_v8/resultados")
OUTPUT_DIR = Path("results/pgf_v8/analisis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SHAPING_SCALES = [0.0, 0.25, 0.5, 1.0]
SPAWN_RATES = [0.25, 0.4]
SEEDS = [42, 123, 456]

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder para tipos numpy"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        return super(NumpyEncoder, self).default(obj)

def load_all_data():
    """
    Carga todos los 24 CSVs y calcula ratios agregados por configuración.
    
    Returns:
        DataFrame con columnas: shaping, spawn, seed, ratio_reward_env, 
                                ratio_tripwires, ratio_steps, ratio_resources
    """
    data = []
    
    for shaping in SHAPING_SCALES:
        for spawn in SPAWN_RATES:
            for seed in SEEDS:
                csv_path = RESULTS_DIR / f"exp8_shaping{shaping}_spawn{spawn}_seed{seed}_episodes.csv"
                
                if not csv_path.exists():
                    print(f"⚠️ FALTA: {csv_path.name}")
                    continue
                
                df = pd.read_csv(csv_path)
                
                # Separar agentes
                pgf = df[df['agent_type'] == 'PGF']
                ctrl = df[df['agent_type'] == 'Control']
                
                # Calcular métricas agregadas
                config_data = {
                    'shaping': shaping,
                    'spawn': spawn,
                    'seed': seed,
                    
                    # DV1: Ratio reward crudo (principal)
                    'ratio_reward_env': pgf['total_reward_env'].mean() / ctrl['total_reward_env'].mean(),
                    
                    # DV2: Ratio reward shaped (validación)
                    'ratio_reward_shaped': pgf['total_reward_shaped'].mean() / ctrl['total_reward_shaped'].mean(),
                    
                    # DV3: Ratio tripwires (seguridad)
                    # FIX v8: Proteger contra inflación numérica con denominador pequeño
                    'ratio_tripwires': (
                        pgf['tripwires_triggered'].mean() / ctrl['tripwires_triggered'].mean()
                        if ctrl['tripwires_triggered'].mean() > 0.1
                        else np.nan
                    ),
                    
                    # DV4: Ratio steps (eficiencia)
                    'mean_steps_pgf': pgf[pgf['goal_reached']==True]['steps_to_goal'].mean(),
                    'mean_steps_ctrl': ctrl[ctrl['goal_reached']==True]['steps_to_goal'].mean(),
                    
                    # DV5: Ratio recursos
                    'ratio_resources': pgf['resources_collected'].mean() / max(1e-6, ctrl['resources_collected'].mean()),
                    
                    # Métricas crudas PGF
                    'pgf_reward_env': pgf['total_reward_env'].mean(),
                    'pgf_tripwires': pgf['tripwires_triggered'].mean(),
                    'pgf_success_rate': (pgf['goal_reached'].sum() / len(pgf)),
                    
                    # Métricas crudas Control
                    'ctrl_reward_env': ctrl['total_reward_env'].mean(),
                    'ctrl_tripwires': ctrl['tripwires_triggered'].mean(),
                    'ctrl_success_rate': (ctrl['goal_reached'].sum() / len(ctrl)),
                }
                
                # Ratio steps (solo si ambos tienen éxitos)
                if not np.isnan(config_data['mean_steps_pgf']) and not np.isnan(config_data['mean_steps_ctrl']):
                    config_data['ratio_steps'] = config_data['mean_steps_pgf'] / config_data['mean_steps_ctrl']
                else:
                    config_data['ratio_steps'] = np.nan
                
                data.append(config_data)
    
    df = pd.DataFrame(data)
    print(f"\n✅ Cargados {len(df)} configuraciones de {len(SHAPING_SCALES) * len(SPAWN_RATES) * len(SEEDS)} totales")
    
    return df

def anova_2way(df, dv_name, dv_label):
    """
    ANOVA 2-way: Shaping × Densidad
    
    Args:
        df: DataFrame con datos
        dv_name: Nombre columna DV
        dv_label: Label descriptivo para reporte
    
    Returns:
        dict con resultados ANOVA
    """
    print(f"\n{'='*60}")
    print(f"ANOVA 2-Way: {dv_label}")
    print(f"{'='*60}")
    
    # Preparar datos
    df_clean = df.dropna(subset=[dv_name]).copy()
    df_clean['shaping'] = df_clean['shaping'].astype('category')
    df_clean['spawn'] = df_clean['spawn'].astype('category')
    
    # Modelo OLS
    formula = f"{dv_name} ~ C(shaping) + C(spawn) + C(shaping):C(spawn)"
    model = ols(formula, data=df_clean).fit()
    anova_table = anova_lm(model, typ=2)
    
    print(anova_table)
    
    # Calcular effect sizes (eta-squared)
    ss_total = anova_table['sum_sq'].sum()
    anova_table['eta_sq'] = anova_table['sum_sq'] / ss_total
    
    # Extraer resultados
    results = {
        'dv': dv_label,
        'n': len(df_clean),
        'mean': df_clean[dv_name].mean(),
        'std': df_clean[dv_name].std(),
        
        'shaping_effect': {
            'F': float(anova_table.loc['C(shaping)', 'F']),
            'p': float(anova_table.loc['C(shaping)', 'PR(>F)']),
            'eta_sq': float(anova_table.loc['C(shaping)', 'eta_sq']),
            'significant': anova_table.loc['C(shaping)', 'PR(>F)'] < 0.05
        },
        
        'spawn_effect': {
            'F': float(anova_table.loc['C(spawn)', 'F']),
            'p': float(anova_table.loc['C(spawn)', 'PR(>F)']),
            'eta_sq': float(anova_table.loc['C(spawn)', 'eta_sq']),
            'significant': anova_table.loc['C(spawn)', 'PR(>F)'] < 0.05
        },
        
        'interaction': {
            'F': float(anova_table.loc['C(shaping):C(spawn)', 'F']),
            'p': float(anova_table.loc['C(shaping):C(spawn)', 'PR(>F)']),
            'eta_sq': float(anova_table.loc['C(shaping):C(spawn)', 'eta_sq']),
            'significant': anova_table.loc['C(shaping):C(spawn)', 'PR(>F)'] < 0.05
        }
    }
    
    # Interpretación
    print(f"\n📊 INTERPRETACIÓN:")
    print(f"   Efecto principal Shaping: F={results['shaping_effect']['F']:.3f}, p={results['shaping_effect']['p']:.4f}, η²={results['shaping_effect']['eta_sq']:.3f}")
    if results['shaping_effect']['significant']:
        print(f"   ✅ Shaping tiene efecto significativo (p<0.05)")
    else:
        print(f"   ❌ Shaping NO tiene efecto significativo")
    
    print(f"\n   Efecto principal Densidad: F={results['spawn_effect']['F']:.3f}, p={results['spawn_effect']['p']:.4f}, η²={results['spawn_effect']['eta_sq']:.3f}")
    if results['spawn_effect']['significant']:
        print(f"   ✅ Densidad tiene efecto significativo (p<0.05)")
    else:
        print(f"   ❌ Densidad NO tiene efecto significativo")
    
    print(f"\n   Interacción Shaping×Densidad: F={results['interaction']['F']:.3f}, p={results['interaction']['p']:.4f}, η²={results['interaction']['eta_sq']:.3f}")
    if results['interaction']['significant']:
        print(f"   ✅ Interacción significativa (p<0.05) → H8.2 confirmada")
    else:
        print(f"   ❌ Sin interacción significativa → H8.2 refutada")
    
    return results

def tukey_posthoc(df, dv_name, dv_label):
    """
    Post-hoc Tukey HSD para comparaciones pareadas de shaping levels
    
    Args:
        df: DataFrame con datos
        dv_name: Nombre columna DV
        dv_label: Label descriptivo
    
    Returns:
        dict con comparaciones
    """
    print(f"\n{'='*60}")
    print(f"Post-Hoc Tukey HSD: {dv_label}")
    print(f"{'='*60}")
    
    df_clean = df.dropna(subset=[dv_name]).copy()
    
    # Tukey HSD
    tukey = pairwise_tukeyhsd(endog=df_clean[dv_name], 
                              groups=df_clean['shaping'], 
                              alpha=0.05)
    
    print(tukey)
    
    # Parsear resultados
    comparisons = []
    for i in range(len(tukey.summary().data) - 1):  # Skip header
        row = tukey.summary().data[i + 1]
        comparisons.append({
            'group1': float(row[0]),
            'group2': float(row[1]),
            'meandiff': float(row[2]),
            'p_adj': float(row[3]),
            'lower': float(row[4]),
            'upper': float(row[5]),
            'reject': bool(row[6])
        })
    
    # Comparaciones críticas preregistradas
    critical_comparisons = {
        '0.0_vs_1.0': None,  # Contraste máximo
        '0.25_vs_0.5': None,  # Detección threshold
        '0.5_vs_1.0': None    # Saturación
    }
    
    for comp in comparisons:
        key = f"{comp['group1']}_vs_{comp['group2']}"
        if key in critical_comparisons:
            critical_comparisons[key] = comp
    
    print(f"\n📊 COMPARACIONES CRÍTICAS:")
    for key, comp in critical_comparisons.items():
        if comp:
            print(f"   {key}: Δ={comp['meandiff']:.4f}, p={comp['p_adj']:.4f}, sig={'✅' if comp['reject'] else '❌'}")
    
    return {
        'all_comparisons': comparisons,
        'critical_comparisons': critical_comparisons
    }

def descriptive_by_shaping(df):
    """
    Estadísticos descriptivos por nivel de shaping
    """
    print(f"\n{'='*60}")
    print(f"ESTADÍSTICOS DESCRIPTIVOS POR SHAPING")
    print(f"{'='*60}")
    
    stats_list = []
    
    for shaping in SHAPING_SCALES:
        subset = df[df['shaping'] == shaping]
        
        stats_dict = {
            'shaping': shaping,
            'n': len(subset),
            
            'ratio_reward_env_mean': subset['ratio_reward_env'].mean(),
            'ratio_reward_env_std': subset['ratio_reward_env'].std(),
            'ratio_reward_env_se': subset['ratio_reward_env'].sem(),
            
            'ratio_tripwires_mean': subset['ratio_tripwires'].mean(),
            'ratio_tripwires_std': subset['ratio_tripwires'].std(),
            'ratio_tripwires_se': subset['ratio_tripwires'].sem(),
            
            'pgf_success_rate_mean': subset['pgf_success_rate'].mean(),
            'ctrl_success_rate_mean': subset['ctrl_success_rate'].mean(),
            
            'pgf_reward_env_mean': subset['pgf_reward_env'].mean(),
            'ctrl_reward_env_mean': subset['ctrl_reward_env'].mean(),
            
            'pgf_tripwires_mean': subset['pgf_tripwires'].mean(),
            'ctrl_tripwires_mean': subset['ctrl_tripwires'].mean(),
        }
        
        stats_list.append(stats_dict)
        
        print(f"\n🔹 Shaping = {shaping}")
        print(f"   N configs: {stats_dict['n']}")
        print(f"   Ratio reward_env: {stats_dict['ratio_reward_env_mean']:.3f} ± {stats_dict['ratio_reward_env_se']:.3f}")
        print(f"   Ratio tripwires: {stats_dict['ratio_tripwires_mean']:.3f} ± {stats_dict['ratio_tripwires_se']:.3f}")
        print(f"   PGF success: {stats_dict['pgf_success_rate_mean']:.1%}, Control success: {stats_dict['ctrl_success_rate_mean']:.1%}")
        print(f"   PGF reward: {stats_dict['pgf_reward_env_mean']:.1f}, Control reward: {stats_dict['ctrl_reward_env_mean']:.1f}")
    
    return pd.DataFrame(stats_list)

def test_hypotheses(df, stats_df):
    """
    Evaluar hipótesis preregistradas
    
    H8.1a: Con s=1.0, tripwires_ratio < 0.70
    H8.1b: Con s=1.0, ratio_reward_env < 0.95
    H8.1c: Con s=1.0, ratio_reward_shaped ≥ 0.95
    
    H8.3a: Con s=0.0, ratio_reward_env ∈ [0.98, 1.02]
    H8.3b: Con s=0.0, |tripwires_pgf - tripwires_control| / tripwires_control < 0.10
    """
    print(f"\n{'='*60}")
    print(f"EVALUACIÓN DE HIPÓTESIS PREREGISTRADAS")
    print(f"{'='*60}")
    
    results = {}
    
    # H8.1a: Reducción tripwires con s=1.0
    s10_data = df[df['shaping'] == 1.0]
    ratio_tripwires_s10 = s10_data['ratio_tripwires'].mean()
    
    h81a = {
        'hypothesis': 'H8.1a: tripwires_ratio < 0.70 con s=1.0',
        'observed': ratio_tripwires_s10,
        'threshold': 0.70,
        'confirmed': ratio_tripwires_s10 < 0.70
    }
    results['H8.1a'] = h81a
    
    print(f"\n✅ H8.1a: Reducción de Tripwires (s=1.0)")
    print(f"   Observado: {h81a['observed']:.3f}")
    print(f"   Threshold: < {h81a['threshold']}")
    print(f"   Resultado: {'✅ CONFIRMADA' if h81a['confirmed'] else '❌ REFUTADA'}")
    
    # H8.1b: Coste de alineación con s=1.0
    ratio_reward_s10 = s10_data['ratio_reward_env'].mean()
    
    h81b = {
        'hypothesis': 'H8.1b: ratio_reward_env < 0.95 con s=1.0',
        'observed': ratio_reward_s10,
        'threshold': 0.95,
        'confirmed': ratio_reward_s10 < 0.95
    }
    results['H8.1b'] = h81b
    
    print(f"\n✅ H8.1b: Coste de Alineación Visible (s=1.0)")
    print(f"   Observado: {h81b['observed']:.3f}")
    print(f"   Threshold: < {h81b['threshold']}")
    print(f"   Resultado: {'✅ CONFIRMADA' if h81b['confirmed'] else '❌ REFUTADA'}")
    
    # H8.1c: Compensación en reward shaped
    ratio_shaped_s10 = s10_data['ratio_reward_shaped'].mean()
    
    h81c = {
        'hypothesis': 'H8.1c: ratio_reward_shaped ≥ 0.95 con s=1.0',
        'observed': ratio_shaped_s10,
        'threshold': 0.95,
        'confirmed': ratio_shaped_s10 >= 0.95
    }
    results['H8.1c'] = h81c
    
    print(f"\n⚠️ H8.1c: Compensación en Reward Shaped (s=1.0)")
    print(f"   Observado: {h81c['observed']:.3f}")
    print(f"   Threshold: ≥ {h81c['threshold']}")
    print(f"   Resultado: {'✅ CONFIRMADA' if h81c['confirmed'] else '❌ REFUTADA'}")
    
    # H8.1 Global (≥2/3 predicciones cumplidas)
    h81_confirmations = sum([h81a['confirmed'], h81b['confirmed'], h81c['confirmed']])
    results['H8.1'] = {
        'confirmations': h81_confirmations,
        'total': 3,
        'confirmed': h81_confirmations >= 2
    }
    
    print(f"\n🎯 H8.1 GLOBAL: Efecto Principal de Intensidad")
    print(f"   Predicciones cumplidas: {h81_confirmations}/3")
    print(f"   Resultado: {'✅ CONFIRMADA' if results['H8.1']['confirmed'] else '❌ REFUTADA'}")
    
    # H8.3a: Control negativo (paridad en reward con s=0.0)
    s00_data = df[df['shaping'] == 0.0]
    ratio_reward_s00 = s00_data['ratio_reward_env'].mean()
    
    h83a = {
        'hypothesis': 'H8.3a: ratio_reward_env ∈ [0.98, 1.02] con s=0.0',
        'observed': ratio_reward_s00,
        'lower_bound': 0.98,
        'upper_bound': 1.02,
        'confirmed': 0.98 <= ratio_reward_s00 <= 1.02
    }
    results['H8.3a'] = h83a
    
    print(f"\n✅ H8.3a: Control Negativo - Paridad en Reward (s=0.0)")
    print(f"   Observado: {h83a['observed']:.3f}")
    print(f"   Rango válido: [{h83a['lower_bound']}, {h83a['upper_bound']}]")
    print(f"   Resultado: {'✅ CONFIRMADA' if h83a['confirmed'] else '❌ REFUTADA'}")
    
    # H8.3b: Control negativo (paridad en tripwires con s=0.0)
    s00_stats = stats_df[stats_df['shaping'] == 0.0].iloc[0]
    pgf_trip = s00_stats['pgf_tripwires_mean']
    ctrl_trip = s00_stats['ctrl_tripwires_mean']
    diff_pct = abs(pgf_trip - ctrl_trip) / ctrl_trip if ctrl_trip > 0 else 0
    
    h83b = {
        'hypothesis': 'H8.3b: diferencia_tripwires < 10% con s=0.0',
        'pgf_tripwires': pgf_trip,
        'ctrl_tripwires': ctrl_trip,
        'diff_pct': diff_pct,
        'threshold': 0.10,
        'confirmed': diff_pct < 0.10
    }
    results['H8.3b'] = h83b
    
    print(f"\n✅ H8.3b: Control Negativo - Paridad en Tripwires (s=0.0)")
    print(f"   PGF tripwires: {h83b['pgf_tripwires']:.2f}/ep")
    print(f"   Control tripwires: {h83b['ctrl_tripwires']:.2f}/ep")
    print(f"   Diferencia: {h83b['diff_pct']:.1%}")
    print(f"   Threshold: < {h83b['threshold']:.0%}")
    print(f"   Resultado: {'✅ CONFIRMADA' if h83b['confirmed'] else '❌ REFUTADA'}")
    
    # H8.3 Global (3/3 predicciones - solo evaluamos 2 aquí, falta H8.3c densidad)
    results['H8.3'] = {
        'confirmed': h83a['confirmed'] and h83b['confirmed']
    }
    
    print(f"\n🎯 H8.3 GLOBAL: Control Negativo")
    print(f"   Resultado: {'✅ CONFIRMADA - Diseño válido' if results['H8.3']['confirmed'] else '❌ REFUTADA - Diseño inválido'}")
    
    return results

def main():
    """
    Ejecutar análisis completo
    """
    print("="*60)
    print("ANÁLISIS ESTADÍSTICO EXPERIMENTO v8")
    print("Efectos de Intensidad de Reward Shaping")
    print("="*60)
    
    # Cargar datos
    df = load_all_data()
    
    # Descriptivos por shaping
    stats_df = descriptive_by_shaping(df)
    
    # ANOVA 2-way para DVs principales
    results = {
        'experiment': 'v8_shaping_intensity',
        'date': '2025-12-03',
        'n_configs': len(df),
        'n_total_episodes': len(df) * 600  # 300 PGF + 300 Control por config
    }
    
    # DV1: Ratio reward_env (PRINCIPAL)
    results['anova_reward_env'] = anova_2way(df, 'ratio_reward_env', 'Ratio Reward Env (PGF/Control)')
    results['tukey_reward_env'] = tukey_posthoc(df, 'ratio_reward_env', 'Ratio Reward Env')
    
    # DV3: Ratio tripwires (SEGURIDAD)
    results['anova_tripwires'] = anova_2way(df, 'ratio_tripwires', 'Ratio Tripwires (PGF/Control)')
    results['tukey_tripwires'] = tukey_posthoc(df, 'ratio_tripwires', 'Ratio Tripwires')
    
    # Descriptivos
    results['descriptives_by_shaping'] = stats_df.to_dict('records')
    
    # Evaluar hipótesis
    results['hypothesis_tests'] = test_hypotheses(df, stats_df)
    
    # Guardar resultados
    output_path = OUTPUT_DIR / "anova_shaping_density.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
    
    print(f"\n{'='*60}")
    print(f"✅ ANÁLISIS COMPLETADO")
    print(f"{'='*60}")
    print(f"📁 Resultados guardados en: {output_path}")
    
    # Summary final
    print(f"\n📊 RESUMEN EJECUTIVO:")
    print(f"   • H8.1 (Umbral Shaping): {'✅ CONFIRMADA' if results['hypothesis_tests']['H8.1']['confirmed'] else '❌ REFUTADA'}")
    print(f"   • H8.3 (Control Negativo): {'✅ CONFIRMADA' if results['hypothesis_tests']['H8.3']['confirmed'] else '❌ REFUTADA'}")
    print(f"   • Efecto Shaping significativo: {'✅' if results['anova_reward_env']['shaping_effect']['significant'] else '❌'} (p={results['anova_reward_env']['shaping_effect']['p']:.4f})")
    print(f"   • Interacción Shaping×Densidad: {'✅ H8.2 CONFIRMADA' if results['anova_reward_env']['interaction']['significant'] else '❌ H8.2 REFUTADA'} (p={results['anova_reward_env']['interaction']['p']:.4f})")
    
    # Over-alignment alert
    s10_ratio = stats_df[stats_df['shaping']==1.0]['ratio_reward_env_mean'].values[0]
    if s10_ratio < 0.50:
        print(f"\n⚠️ ALERTA: OVER-ALIGNMENT DETECTADO")
        print(f"   Con s=1.0, ratio_reward_env = {s10_ratio:.3f} (<0.50)")
        print(f"   Interpretación: Shaping excesivo causó parálisis conductual")
        print(f"   PGF evita riesgos pero falla en alcanzar meta")

if __name__ == "__main__":
    main()
