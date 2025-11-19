import pandas as pd
from pathlib import Path

seed_dir = Path('results/pgf_v10_multiseed/seeds/seed_0042')
timestamp = '102250'

phases = [
    ('4x4', 4, 80.0),
    ('6x6', 6, 20.0),
    ('8x8', 8, 10.0)
]

results = []
for phase, grid, gate in phases:
    files = list(seed_dir.glob(f'phase*{phase}_20251205_{timestamp}.csv'))
    if not files:
        print(f"❌ No se encontró phase {phase} con timestamp {timestamp}")
        continue
    
    df = pd.read_csv(files[0])
    success_last_100 = df['success'].tail(100).mean()
    
    results.append({
        'seed': 42,
        'phase': phase,
        'grid_size': grid,
        'episodes': len(df),
        'success_rate_total': df['success'].mean(),
        'success_last_100': success_last_100,
        'gate': gate,
        'gate_passed': (success_last_100 * 100) >= gate,
        'first_success_episode': df[df['success']==1].index[0] if len(df[df['success']==1]) > 0 else None,
        'convergence_episode': -1
    })
    print(f"✓ {phase}: {success_last_100:.2%}")

df_summary = pd.DataFrame(results)
output_path = seed_dir / f'curriculum_summary_{timestamp}.csv'
df_summary.to_csv(output_path, index=False)
print(f"\n✅ Guardado: {output_path}")
print(df_summary[['phase','success_last_100','gate_passed']].to_string(index=False))
