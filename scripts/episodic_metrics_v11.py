import pandas as pd
import numpy as np
import os
from pathlib import Path

root = Path('results/v11')
data_dir = root / 'data'
out_csv = data_dir / 'episodic_metrics_v11.csv'
out_md = data_dir / 'episodic_metrics_v11.md'
out_csv_full = data_dir / 'episodic_metrics_v11_full.csv'
out_md_full = data_dir / 'episodic_metrics_v11_full.md'

# utility: max drawdown of cumulative reward series
def max_drawdown(series):
    cum = series.cumsum()
    peak = cum.expanding(min_periods=1).max()
    drawdown = peak - cum
    return drawdown.max()

# find all episode CSVs
files = list(root.rglob('*_episodes.csv'))
if not files:
    raise FileNotFoundError(f'No episode CSVs found under {root}')

rows = []
CANONICAL = [0.5, 1.0, 1.5, 2.0, 3.0]
def map_to_group(scale):
    try:
        if scale is None:
            return None
        s = float(scale)
    except:
        return None
    diffs = [(abs(s - c), c) for c in CANONICAL]
    diffs.sort()
    return diffs[0][1]
for f in files:
    stem = f.stem
    # attempt to parse risk and seed from filename like grid8_riskhigh_r1p2_seed42_v11_episodes
    risk_scale = None
    seed = None
    parts = stem.split('_')
    for p in parts:
        if p.startswith('r') and 'p' in p:
            # r1p2 -> 1.2
            risk_scale = float(p[1:].replace('p','.'))
        if p.startswith('seed'):
            try:
                seed = int(p.replace('seed',''))
            except:
                seed = None
    try:
        df = pd.read_csv(f)
    except Exception as e:
        print(f'[WARN] cannot read {f}: {e}')
        continue
    if 'Agente' not in df.columns and 'agent' in df.columns:
        df = df.rename(columns={'agent':'Agente'})
    if 'Recompensa' not in df.columns and 'Reward' in df.columns:
        df = df.rename(columns={'Reward':'Recompensa'})
    for agent, g in df.groupby('Agente'):
        rewards = g['Recompensa'].astype(float)
        n = len(rewards)
        if n==0:
            continue
        median = rewards.median()
        q1 = rewards.quantile(0.25)
        q3 = rewards.quantile(0.75)
        iqr = q3 - q1
        pct_trip = 100.0 * (g['Tripwires'].astype(float) > 0).mean() if 'Tripwires' in g.columns else np.nan
        # CVaR 95% (mean of worst 5%)
        cutoff = rewards.quantile(0.05)
        cvar95 = rewards[rewards <= cutoff].mean()
        md = max_drawdown(rewards)
        risk_group = map_to_group(risk_scale)
        rows.append({'agent':agent,'risk_scale':risk_scale,'risk_group':risk_group,'seed':seed,'file':str(f),'n':n,'median':median,'iqr':iqr,'pct_tripwires':pct_trip,'cvar95':cvar95,'max_drawdown':md})

if not rows:
    raise RuntimeError('No rows generated')

out_df = pd.DataFrame(rows)
# save full per-file table (preserves raw parsed risk_scale and seed)
os.makedirs(out_csv.parent, exist_ok=True)
out_df.to_csv(out_csv_full, index=False)

# aggregate across files by agent and canonical risk_group for peer-review aggregation
agg = out_df.groupby(['agent','risk_group']).agg({'n':'sum','median':'median','iqr':'median','pct_tripwires':'mean','cvar95':'mean','max_drawdown':'mean'}).reset_index()
# expose the grouped/canonical risk as 'risk_scale' for compatibility with downstream reports
agg = agg.rename(columns={'risk_group':'risk_scale'})
agg.to_csv(out_csv, index=False)

with open(out_md,'w',encoding='utf-8') as f:
    f.write('# Métricas por episodio — v11\n\n')
    f.write('Mediana, IQR, %Tripwires, CVaR(95%), Max Drawdown por `agent` y `risk_group` (campo `risk_scale` en esta tabla = valor canónico más cercano).\n\n')
    f.write(agg.to_string(index=False))

with open(out_md_full,'w',encoding='utf-8') as f:
    f.write('# Métricas por episodio — v11 (completo)\n\n')
    f.write('Tabla completa con `risk_scale` tal como se parseó del filename y `risk_group` mapeado a la rejilla canónica.\n\n')
    f.write(out_df.to_string(index=False))

print('Wrote', out_csv, out_md, 'and full table', out_csv_full, out_md_full)
