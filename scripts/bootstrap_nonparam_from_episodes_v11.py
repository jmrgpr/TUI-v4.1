import pandas as pd
import numpy as np
import os
from pathlib import Path

ROOT = Path('results/v11')
DATA_DIR = ROOT / 'data'
OUT_CSV = DATA_DIR / 'bootstrap_nonparam_from_episodes_v11.csv'
OUT_MD = DATA_DIR / 'bootstrap_nonparam_from_episodes_v11.md'

CANONICAL = [0.5, 1.0, 1.5, 2.0, 3.0]
def parse_risk_from_stem(stem: str):
    # attempt patterns like r1p2 or risk1.0
    parts = stem.split('_')
    for p in parts:
        if p.startswith('r') and 'p' in p:
            try:
                return float(p[1:].replace('p', '.'))
            except:
                pass
        if p.startswith('risk'):
            try:
                return float(p.replace('risk', '').replace('r', ''))
            except:
                pass
    return None

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

def read_episode_files(root=ROOT):
    rows = []
    files = list(root.rglob('*_episodes.csv'))
    for f in files:
        stem = f.stem
        risk = parse_risk_from_stem(stem)
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        # normalize column names
        if 'Agente' not in df.columns and 'agent' in df.columns:
            df = df.rename(columns={'agent':'Agente'})
        if 'Recompensa' not in df.columns and 'Reward' in df.columns:
            df = df.rename(columns={'Reward':'Recompensa'})
        if 'Agente' not in df.columns or 'Recompensa' not in df.columns:
            continue
        for agent, g in df.groupby('Agente'):
            mean_reward = g['Recompensa'].astype(float).mean()
            n = len(g)
            rows.append({'agent':agent, 'risk_scale':risk, 'risk_group':map_to_group(risk), 'mean_reward':mean_reward, 'n_episodes':n, 'file':str(f)})
    return pd.DataFrame(rows)

def bootstrap_diff(a_vals, b_vals, B=5000, seed=2025):
    rng = np.random.default_rng(seed)
    diffs = []
    n1 = len(a_vals); n2 = len(b_vals)
    for _ in range(B):
        samp1 = rng.choice(a_vals, size=n1, replace=True)
        samp2 = rng.choice(b_vals, size=n2, replace=True)
        diffs.append(np.mean(samp1) - np.mean(samp2))
    diffs = np.array(diffs)
    ci_lo, ci_hi = np.percentile(diffs, [2.5, 97.5])
    p = np.mean(np.abs(diffs) >= abs(np.mean(diffs)))
    return np.mean(diffs), ci_lo, ci_hi, p

def main():
    per_run = read_episode_files()
    if per_run.empty:
        raise RuntimeError('No episode-derived per-run rows found')
    rows = []
    for risk in sorted(per_run['risk_group'].dropna().unique()):
        grp = per_run[per_run['risk_group']==risk]
        ctrl = grp[grp['agent']=='control']
        if ctrl.empty:
            continue
        ctrl_vals = ctrl['mean_reward'].values
        for agent in sorted(grp['agent'].unique()):
            if agent == 'control':
                continue
            ag_vals = grp[grp['agent']==agent]['mean_reward'].values
            if len(ag_vals) < 2 or len(ctrl_vals) < 2:
                continue
            mean_diff, ci_lo, ci_hi, p = bootstrap_diff(ag_vals, ctrl_vals)
            rows.append({'agent':agent, 'risk_group':risk, 'mean_diff':mean_diff, 'ci95_lo':ci_lo, 'ci95_hi':ci_hi, 'p_boot_nonparam':p, 'n_agent':len(ag_vals), 'n_control':len(ctrl_vals)})
    out = pd.DataFrame(rows)
    os.makedirs(DATA_DIR, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write('# Bootstrap No Paramétrico desde archivos de episodios — v11\n\n')
        f.write('Se generan estimaciones bootstrap no paramétricas (resampling per-run de la media de recompensa por archivo) para la diferencia de medias vs control, por `risk_group`.\n\n')
        f.write(out.to_string(index=False))
    print('Wrote', OUT_CSV, OUT_MD)

if __name__ == '__main__':
    main()
