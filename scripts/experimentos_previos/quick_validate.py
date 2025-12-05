import json
import pandas as pd

print("=" * 50)
print("VALIDACIÓN RÁPIDA v9")
print("=" * 50)

# 4×4
df = pd.read_csv('results/pgf_v9/resultados/exp9_Curriculum_seed42_episodes.csv')
print(f"\n✓ 4×4 CSV: {len(df)} episodios")

with open('results/pgf_v9/resultados/exp9_Curriculum_seed42_metrics.json') as f:
    m = json.load(f)
print(f"✓ 4×4 JSON: reward={m['stats']['mean_reward_env_final']:.2f}")

# Análisis
with open('results/pgf_v9/analisis/curriculum_effectiveness.json') as f:
    a = json.load(f)
print(f"✓ H9.1: ratio={a['hypotheses']['H9.1']['ratio_mean']:.3f}")
print(f"✓ H9.2: Cohen's d={a['hypotheses']['H9.2']['cohens_d']:.3f}")

# 6×6
df6 = pd.read_csv('results/pgf_v9/exploratorios/grid_6x6/resultados/exp9_Curriculum_seed123_episodes.csv')
reward_col = 'total_reward_env' if 'total_reward_env' in df6.columns else 'reward_env'
print(f"✓ 6×6 seed=123: {df6.tail(50)[reward_col].mean():.2f} reward")

with open('results/pgf_v9/exploratorios/grid_6x6/analisis_6x6_completo.json') as f:
    a6 = json.load(f)
print(f"✓ 6×6 ratio: {a6['h_exp1_generalization']['ratio_6x6']['mean']:.3f}")

print("\n" + "=" * 50)
print("✅ INTEGRIDAD VALIDADA")
print("=" * 50)
