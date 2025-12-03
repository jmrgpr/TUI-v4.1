"""
Diagnóstico: Investigar anomalía en control negativo (s=0.0)
Esperado: ratio ≈ 1.0 (paridad)
Observado: ratio = 1.284 (diferencia significativa)
"""
import pandas as pd

df = pd.read_csv('results/pgf_v8/resultados/exp8_shaping0.0_spawn0.25_seed42_episodes.csv')

pgf = df[df['agent_type'] == 'PGF']
ctrl = df[df['agent_type'] == 'Control']

print("=" * 60)
print("DIAGNÓSTICO: Control Negativo s=0.0 (sin shaping)")
print("=" * 60)

print("\n📊 ESTADÍSTICAS REWARD:")
print(f"PGF:     mean={pgf['total_reward_env'].mean():.3f}, std={pgf['total_reward_env'].std():.3f}")
print(f"Control: mean={ctrl['total_reward_env'].mean():.3f}, std={ctrl['total_reward_env'].std():.3f}")
print(f"Ratio:   {pgf['total_reward_env'].mean() / ctrl['total_reward_env'].mean():.3f} (esperado: ~1.0)")

print("\n🚨 ESTADÍSTICAS TRIPWIRES:")
print(f"PGF:     sum={pgf['tripwires_triggered'].sum()}, mean={pgf['tripwires_triggered'].mean():.2f}/ep")
print(f"Control: sum={ctrl['tripwires_triggered'].sum()}, mean={ctrl['tripwires_triggered'].mean():.2f}/ep")
print(f"Ratio:   {pgf['tripwires_triggered'].sum() / max(1, ctrl['tripwires_triggered'].sum()):.3f} (esperado: ~1.0)")

print("\n📈 EPISODIOS INDIVIDUALES:")
print("\nPGF:")
print(pgf[['episode', 'total_reward_env', 'tripwires_triggered', 'resources_collected', 'steps_to_goal']].to_string())

print("\nControl:")
print(ctrl[['episode', 'total_reward_env', 'tripwires_triggered', 'resources_collected', 'steps_to_goal']].to_string())

print("\n" + "=" * 60)
print("INTERPRETACIÓN:")
print("=" * 60)

if pgf['tripwires_triggered'].sum() > ctrl['tripwires_triggered'].sum() * 1.5:
    print("⚠️ PGF pisa MÁS tripwires que Control sin shaping")
    print("   Posible causa: Diferencia en seeding/inicialización")
    print("   Acción: Verificar configure_all_seeds() se llama ANTES de crear env")
elif abs(pgf['total_reward_env'].mean() / ctrl['total_reward_env'].mean() - 1.0) > 0.05:
    print("⚠️ Diferencia significativa en reward sin shaping (>5%)")
    print("   Posible causa: Entornos no idénticos entre PGF y Control")
    print("   Acción: Verificar que tripwires se generan con MISMA semilla")
else:
    print("✓ Control negativo PASA (diferencia <5%)")
