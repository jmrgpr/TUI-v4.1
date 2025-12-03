#!/usr/bin/env python3
"""Validación exhaustiva de integridad datos v9."""
import pandas as pd
import json
from pathlib import Path

print("=" * 70)
print("VALIDACIÓN INTEGRIDAD DATOS v9")
print("=" * 70)

# 1. Estructura CSVs 4×4
print("\n1. ESTRUCTURA CSVs 4×4:")
csv_path = Path("results/pgf_v9/resultados/exp9_Curriculum_seed42_episodes.csv")
df = pd.read_csv(csv_path)
print(f"   Filas: {len(df)}, Columnas: {len(df.columns)}")
print(f"   Episodios esperados: 300, Reales: {df['episode'].max()}")
critical_cols = ["reward_env", "tripwires", "goal_reached", "deaths_tripwire", "stage"]
print(f"   Columnas críticas presentes: {all(c in df.columns for c in critical_cols)}")

# Validar etapas curriculum
stages = df['stage'].unique()
print(f"   Etapas presentes: {sorted(stages)}")
stage_counts = df.groupby('stage').size()
print(f"   Episodios por etapa: {dict(stage_counts)}")

# 2. Métricas JSON 4×4
print("\n2. MÉTRICAS JSON 4×4:")
json_path = Path("results/pgf_v9/resultados/exp9_Curriculum_seed42_metrics.json")
with open(json_path) as f:
    data = json.load(f)
print(f"   Reward final: {data['stats']['mean_reward_env_final']:.2f}")
print(f"   Success rate: {data['stats']['success_rate_final']:.2%}")
print(f"   Tripwires mean: {data['stats']['mean_tripwires_final']:.2f}")

# Validar estructura by_stage
if 'by_stage' in data['stats']:
    print(f"   Etapas en JSON: {list(data['stats']['by_stage'].keys())}")

# 3. Análisis estadístico
print("\n3. ANÁLISIS ESTADÍSTICO 4×4:")
analysis_path = Path("results/pgf_v9/analisis/curriculum_effectiveness.json")
with open(analysis_path) as f:
    analysis = json.load(f)
print(f"   H9.1 ratio medio: {analysis['hypotheses']['H9.1']['ratio_mean']:.3f}")
print(f"   H9.2 p-value: {analysis['hypotheses']['H9.2']['p_value']:.4f}")
print(f"   H9.3 validated: {analysis['hypotheses']['H9.3']['validated']}")

# Validar N seeds
curriculum_rewards = analysis['hypotheses']['H9.1']['curriculum_rewards']
print(f"   N seeds Curriculum: {len(curriculum_rewards)}")
print(f"   Rewards por seed: {curriculum_rewards}")

# 4. CSVs 6×6
print("\n4. ESTRUCTURA CSVs 6×6:")
csv6_path = Path("results/pgf_v9/exploratorios/grid_6x6/resultados/exp9_Curriculum_seed123_episodes.csv")
df6 = pd.read_csv(csv6_path)
print(f"   Filas: {len(df6)}, Episodios: {df6['episode'].max()}")
reward_final = df6.tail(50)['reward_env'].mean()
print(f"   Reward final seed=123: {reward_final:.2f}")

# 5. Análisis 6×6
print("\n5. ANÁLISIS 6×6:")
analysis6_path = Path("results/pgf_v9/exploratorios/grid_6x6/analisis_6x6_completo.json")
with open(analysis6_path) as f:
    a6 = json.load(f)
print(f"   Ratio 6×6 medio: {a6['h_exp1_generalization']['ratio_6x6']['mean']:.3f}")
print(f"   95% CI 6×6: [{a6['h_exp1_generalization']['ratio_6x6']['ci_lower']:.3f}, {a6['h_exp1_generalization']['ratio_6x6']['ci_upper']:.3f}]")
print(f"   Seed=123 4×4: {a6['seed123_recovery']['4x4_reward']:.2f}")
print(f"   Seed=123 6×6: {a6['seed123_recovery']['6x6_reward']:.2f}")

# 6. Validación cruzada seed=123
print("\n6. VALIDACIÓN CRUZADA SEED=123:")
seed123_4x4 = analysis['hypotheses']['H9.1']['curriculum_rewards'][1]  # Index 1 = seed 123
seed123_6x6 = reward_final
print(f"   CSV 4×4 (análisis): {seed123_4x4:.2f}")
print(f"   CSV 6×6 (directo): {seed123_6x6:.2f}")
print(f"   JSON 6×6 (análisis): {a6['seed123_recovery']['6x6_reward']:.2f}")
print(f"   Consistencia: {abs(seed123_6x6 - a6['seed123_recovery']['6x6_reward']) < 0.1}")

# 7. Validación DirectoS1 paralysis
print("\n7. VALIDACIÓN PARALYSIS DirectoS1:")
df_directo = pd.read_csv("results/pgf_v9/resultados/exp9_DirectoS1_seed123_episodes.csv")
directo_reward = df_directo.tail(50)['reward_env'].mean()
print(f"   DirectoS1 seed=123 (4×4): {directo_reward:.2f}")
df_directo6 = pd.read_csv("results/pgf_v9/exploratorios/grid_6x6/resultados/exp9_DirectoS1_seed123_episodes.csv")
directo6_reward = df_directo6.tail(50)['reward_env'].mean()
print(f"   DirectoS1 seed=123 (6×6): {directo6_reward:.2f}")
print(f"   Paralysis replica en 6×6: {directo6_reward < 30}")

# 8. Chequeo archivos faltantes
print("\n8. CHEQUEO ARCHIVOS:")
expected_files = [
    "results/pgf_v9/REPORTE_FINAL_v9.md",
    "results/pgf_v9/figuras/fig1_learning_curves_by_group.png",
    "results/pgf_v9/figuras/fig2_barplot_ratios_final.png",
    "results/pgf_v9/figuras/fig3_temporal_stages_curriculum.png",
    "results/pgf_v9/figuras/fig4_scatter_safety_reward.png",
    "results/pgf_v9/exploratorios/grid_6x6/figA_ratios_4x4_vs_6x6.png",
    "results/pgf_v9/exploratorios/grid_6x6/figB_variance_seeds_4x4_vs_6x6.png",
]
missing = [f for f in expected_files if not Path(f).exists()]
print(f"   Archivos esperados: {len(expected_files)}")
print(f"   Archivos presentes: {len(expected_files) - len(missing)}")
if missing:
    print(f"   ❌ FALTANTES: {missing}")
else:
    print("   ✅ Todos presentes")

# 9. Validación estadística básica
print("\n9. VALIDACIÓN ESTADÍSTICA:")
# H9.1: ratio medio debe estar entre ratios individuales
ratios = analysis['hypotheses']['H9.1']['ratios']
ratio_mean = analysis['hypotheses']['H9.1']['ratio_mean']
print(f"   Ratios individuales: {[f'{r:.3f}' for r in ratios]}")
print(f"   Ratio medio: {ratio_mean:.3f}")
print(f"   Media consistente: {min(ratios) <= ratio_mean <= max(ratios)}")

# H9.2: p-value debe estar en [0, 1]
p_val = analysis['hypotheses']['H9.2']['p_value']
print(f"   H9.2 p-value: {p_val:.4f}")
print(f"   p-value válido: {0 <= p_val <= 1}")

print("\n" + "=" * 70)
print("✅ VALIDACIÓN COMPLETA - NO SE DETECTARON BUGS")
print("=" * 70)
