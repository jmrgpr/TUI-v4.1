import pandas as pd
import glob

print("="*80)
print("ANÁLISIS COMPLETO SMOKE TEST")
print("="*80)

# Analizar DQN-Control files
print("\n### DQN-CONTROL FILES ###")
for seed in [123, 456]:
    try:
        df = pd.read_csv(f'results/smoke_test/dqn_control_easy_seed{seed}_episodes.csv')
        print(f"\n--- Seed {seed} ---")
        print(f"Agentes en archivo: {df['Agente'].unique()}")
        for ag in df['Agente'].unique():
            data = df[df['Agente']==ag]['Recompensa']
            print(f"  {ag}: n={len(data)}, media={data.mean():.2f}, min={data.min():.2f}, max={data.max():.2f}, >0={(data>0).sum()}/{len(data)}")
    except Exception as e:
        print(f"Error en seed {seed}: {e}")

# Analizar TUI/PGF files
print("\n\n### TUI/PGF FILES ###")
for seed in [123, 456]:
    try:
        df = pd.read_csv(f'results/smoke_test/tui_pgf_easy_seed{seed}_episodes.csv')
        print(f"\n--- Seed {seed} ---")
        print(f"Agentes en archivo: {df['Agente'].unique()}")
        for ag in df['Agente'].unique():
            data = df[df['Agente']==ag]['Recompensa']
            print(f"  {ag}: n={len(data)}, media={data.mean():.2f}, min={data.min():.2f}, max={data.max():.2f}, >0={(data>0).sum()}/{len(data)}")
    except Exception as e:
        print(f"Error en seed {seed}: {e}")

print("\n" + "="*80)
