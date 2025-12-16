import pandas as pd
import numpy as np
from pathlib import Path
import os

root = Path('results/v11')
data_dir = root / 'data'
out_csv = data_dir / 'f2_final_checks.csv'
out_md = data_dir / 'f2_final_checks.md'

files = list(root.rglob('*_episodes.csv'))
if not files:
    raise FileNotFoundError(f'No episode CSVs found under {root}')

rows = []
for f in files:
    try:
        df = pd.read_csv(f)
    except Exception as e:
        print(f'[WARN] cannot read {f}: {e}')
        continue
    if 'Agente' not in df.columns and 'agent' in df.columns:
        df = df.rename(columns={'agent':'Agente'})
    # try to extract seed from filename
    stem = f.stem
    seed = None
    for part in stem.split('_'):
        if part.startswith('seed'):
            try:
                seed = int(part.replace('seed',''))
            except:
                seed = None
    for agent, g in df.groupby('Agente'):
        n = len(g)
        mean = g['Recompensa'].astype(float).mean()
        std = g['Recompensa'].astype(float).std()
        pct_trip = 100.0 * (g['Tripwires'].astype(float) > 0).mean() if 'Tripwires' in g.columns else np.nan
        rows.append({'file':str(f),'agent':agent,'seed':seed,'n':n,'mean_reward':mean,'std_reward':std,'pct_tripwires':pct_trip})

if not rows:
    raise RuntimeError('No seed-level rows generated')

df_seeds = pd.DataFrame(rows)
# compute expected n per agent/risk_scale by mode
expected_n = df_seeds['n'].median()

# detect seeds with n << expected (less than 90%)
df_seeds['low_n'] = df_seeds['n'] < 0.9 * expected_n

# flag outliers by mean_reward zscore per agent
flags = []
for agent, g in df_seeds.groupby('agent'):
    if len(g) < 2:
        g['z_mean'] = 0.0
    else:
        g['z_mean'] = (g['mean_reward'] - g['mean_reward'].mean())/g['mean_reward'].std(ddof=0)
    # pct_trip zscore
    if 'pct_tripwires' in g.columns:
        if g['pct_tripwires'].std(ddof=0) == 0:
            g['z_trip'] = 0.0
        else:
            g['z_trip'] = (g['pct_tripwires'] - g['pct_tripwires'].mean())/g['pct_tripwires'].std(ddof=0)
    else:
        g['z_trip'] = 0.0
    df_seeds.loc[g.index, 'z_mean'] = g['z_mean']
    df_seeds.loc[g.index, 'z_trip'] = g['z_trip']

# Outlier if abs(z_mean) > 3 or abs(z_trip) > 3
df_seeds['outlier'] = (df_seeds['z_mean'].abs() > 3) | (df_seeds['z_trip'].abs() > 3) | df_seeds['low_n']

os.makedirs(out_csv.parent, exist_ok=True)
df_seeds.to_csv(out_csv, index=False)

with open(out_md,'w',encoding='utf-8') as f:
    f.write('# F2 Final Checks — Seeds y Outliers\n\n')
    f.write(f'Archivos inspeccionados: {len(files)}\n\n')
    f.write('Criterios: seed con `n` < 90% mediana de episodios → flag `low_n`; outlier si |z(mean_reward)|>3 o |z(%tripwires)|>3.\n\n')
    f.write('Tabla por seed:\n\n')
    f.write(df_seeds.to_string(index=False))
    f.write('\n\n')
    flagged = df_seeds[df_seeds['outlier']]
    f.write('Seeds marcados como potencialmente problemáticos:\n\n')
    if flagged.empty:
        f.write('Ninguno.\n')
    else:
        f.write(flagged.to_string(index=False))

print('Wrote', out_csv, out_md)
