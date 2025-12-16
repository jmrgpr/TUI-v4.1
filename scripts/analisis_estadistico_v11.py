import pandas as pd
import numpy as np
import os
import re
from math import erf

inpath = 'reports/phase2/summary_agent_risk.csv'
data_dir = 'results/v11/data'
out_csv = f'{data_dir}/stats_summary_v11.csv'
out_md = f'{data_dir}/stats_report_v11.md'

CANONICAL = [0.5, 1.0, 1.5, 2.0, 3.0]
def map_to_group(scale):
    try:
        if pd.isna(scale):
            return None
        s = float(scale)
    except:
        return None
    diffs = [(abs(s - c), c) for c in CANONICAL]
    diffs.sort()
    return diffs[0][1]

# Robust read: first two rows contain multi-line header; parse them and then read data
raw = pd.read_csv(inpath, header=None, dtype=str)
header0 = raw.iloc[0].fillna('')
header1 = raw.iloc[1].fillna('')
names = []
for a,b in zip(header0, header1):
    a = str(a).strip()
    b = str(b).strip()
    if a and a.lower()!='nan':
        if b and b.lower()!='nan':
            nm = f"{a}_{b}"
        else:
            nm = a
    else:
        nm = b
    nm = re.sub(r'[^0-9a-zA-Z_]', '_', nm.strip().lower())
    names.append(nm)

# Now read data skipping header rows
df = pd.read_csv(inpath, header=None, skiprows=2, names=names)

# Convert numeric columns
for c in df.columns:
    if c not in ['agent','risk_scale']:
        df[c] = pd.to_numeric(df[c], errors='coerce')

# create or normalize a canonical grouping column `risk_group`
if 'risk_group' in df.columns:
    df['risk_group'] = pd.to_numeric(df['risk_group'], errors='coerce')
else:
    # try to coerce existing risk_scale to numeric and map to nearest canonical
    if 'risk_scale' in df.columns:
        df['risk_scale'] = pd.to_numeric(df['risk_scale'], errors='coerce')
        df['risk_group'] = df['risk_scale'].apply(map_to_group)
    else:
        df['risk_group'] = None

print('DEBUG: columns ->', df.columns.tolist())

# Map probable column names to canonical 'agent' and 'risk_scale' if present
col_map = {}
for c in df.columns:
    if 'agent' in c:
        col_map[c] = 'agent'
    if 'risk' in c and 'scale' in c:
        col_map[c] = 'risk_scale'
if col_map:
    df = df.rename(columns=col_map)

# Select rows with reward_total_mean
print('DEBUG: sample agent/risk ->')
try:
    print(df[['agent','risk_scale']].head())
except Exception as e:
    print('DEBUG: cannot print agent/risk -', e)
if 'reward_total_mean' not in df.columns:
    # try alternative names
    candidates = [c for c in df.columns if 'reward' in c and 'mean' in c]
    if candidates:
        reward_col = candidates[0]
        std_col = reward_col.replace('mean','std')
        count_col = reward_col.replace('mean','count')
        df = df.rename(columns={reward_col:'reward_total_mean', std_col:'reward_total_std', count_col:'reward_total_count'})

# Build summary
rows = []
groups = df[['agent','risk_group']].drop_duplicates()
for _, g in groups.iterrows():
    agent = g['agent']
    risk = g['risk_group']
    sel = df[(df['agent']==agent) & (df['risk_group']==risk)]
    if sel.empty:
        continue
    mean = sel['reward_total_mean'].iloc[0]
    std = sel['reward_total_std'].iloc[0]
    n = int(sel['reward_total_count'].iloc[0]) if not np.isnan(sel['reward_total_count'].iloc[0]) else (int(sel['pgf_neto_count'].iloc[0]) if 'pgf_neto_count' in sel.columns else None)
    if n is None or n<=0 or np.isnan(std) or np.isnan(mean):
        continue
    se = std/np.sqrt(n)
    ci95_lo = mean - 1.96*se
    ci95_hi = mean + 1.96*se
    # write canonical grouped risk as 'risk_scale' for compatibility
    rows.append({'agent':agent,'risk_scale':risk,'n':n,'mean':mean,'std':std,'ci95_lo':ci95_lo,'ci95_hi':ci95_hi})

summary = pd.DataFrame(rows)
print('DEBUG: summary columns ->', summary.columns.tolist())

# Compute Cohen's d vs control per risk
es = []
for risk in summary['risk_scale'].unique():
    ctrl = summary[(summary['agent']=='control') & (summary['risk_scale']==risk)]
    if ctrl.empty:
        continue
    m2 = ctrl['mean'].values[0]
    s2 = ctrl['std'].values[0]
    n2 = ctrl['n'].values[0]
    for _, r in summary[summary['risk_scale']==risk].iterrows():
        if r['agent']=='control':
            d = 0.0
        else:
            m1 = r['mean']; s1 = r['std']; n1 = r['n']
            # pooled std
            pooled = np.sqrt(((n1-1)*s1*s1 + (n2-1)*s2*s2)/(n1+n2-2)) if (n1+n2-2)>0 else np.nan
            d = (m1 - m2)/pooled if pooled>0 else np.nan
        es.append({'agent':r['agent'],'risk_scale':risk,'cohens_d':d})

es_df = pd.DataFrame(es)

# Merge
out = summary.merge(es_df, on=['agent','risk_scale'])

# Compute approximate p-value (z-test) vs control using pooled std (normal approx)
pvals = []
for _, row in out.iterrows():
    agent = row['agent']
    risk = row['risk_scale']
    m1 = row['mean']; s1 = row['std']; n1 = row['n']
    ctrl = out[(out['agent']=='control') & (out['risk_scale']==risk)]
    if ctrl.empty:
        p = np.nan
    else:
        m2 = float(ctrl['mean'].iloc[0]); s2 = float(ctrl['std'].iloc[0]); n2 = int(ctrl['n'].iloc[0])
        pooled = np.sqrt(((n1-1)*s1*s1 + (n2-1)*s2*s2)/(n1+n2-2)) if (n1+n2-2)>0 else np.nan
        if pooled>0:
            se_diff = pooled * np.sqrt(1.0/n1 + 1.0/n2)
            z = (m1 - m2) / se_diff if se_diff>0 else 0.0
            p = 2*(1 - 0.5*(1 + erf(abs(z)/np.sqrt(2))))
        else:
            p = np.nan
    pvals.append(p)

out['p_value_vs_control'] = pvals

# Save CSV and markdown report
os.makedirs(os.path.dirname(out_csv), exist_ok=True)
out.to_csv(out_csv, index=False)

with open(out_md,'w',encoding='utf-8') as f:
    f.write('# Estadística descriptiva e inferencial mínima — v11\n\n')
    f.write('Fuente: `reports/phase2/summary_agent_risk.csv`\n\n')
    f.write('Tabla: n, media, std, IC95%, Cohen\'s d vs control y p-value (normal approx) por risk_scale.\n\n')
    f.write(out.to_string(index=False))
    f.write('\n')

print('Done:', out_csv, out_md)
