import pandas as pd
import numpy as np
import os

DATA_DIR = 'results/v11/data'
MASTER = 'results/master_results.csv'
OUT_CSV = os.path.join(DATA_DIR, 'bootstrap_nonparam_v11.csv')
OUT_MD = os.path.join(DATA_DIR, 'bootstrap_nonparam_v11.md')

CANONICAL = [0.5, 1.0, 1.5, 2.0, 3.0]
def map_to_group(x):
    try:
        if pd.isna(x):
            return None
        s = float(x)
    except:
        return None
    diffs = [(abs(s - c), c) for c in CANONICAL]
    diffs.sort()
    return diffs[0][1]

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
    df = pd.read_csv(MASTER)
    if df.empty:
        raise RuntimeError('Master CSV empty; cannot run bootstrap non-parametric')
    # ensure reward_total numeric and drop NA
    df['reward_total'] = pd.to_numeric(df['reward_total'], errors='coerce')
    df['risk_group'] = df['risk_scale'].apply(map_to_group) if 'risk_scale' in df.columns else None
    rows = []
    for risk in sorted(df['risk_group'].dropna().unique()):
        sub = df[df['risk_group'] == risk]
        ctrl = sub[sub['agent']=='control']
        if ctrl.empty:
            continue
        ctrl_vals = ctrl['reward_total'].dropna().values
        for agent in sorted(sub['agent'].unique()):
            if agent == 'control':
                continue
            ag_vals = sub[sub['agent']==agent]['reward_total'].dropna().values
            if len(ag_vals) < 2 or len(ctrl_vals) < 2:
                continue
            mean_diff, ci_lo, ci_hi, p = bootstrap_diff(ag_vals, ctrl_vals)
            rows.append({'agent':agent, 'risk_group':risk, 'mean_diff':mean_diff, 'ci95_lo':ci_lo, 'ci95_hi':ci_hi, 'p_boot_nonparam':p, 'n_agent':len(ag_vals), 'n_control':len(ctrl_vals)})
    out = pd.DataFrame(rows)
    os.makedirs(DATA_DIR, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write('# Bootstrap No Paramétrico — v11\n\n')
        f.write('Bootstrap no paramétrico (resampling per-run de `reward_total`) para la diferencia de medias vs control, por `risk_group` canónico.\n\n')
        f.write(out.to_string(index=False))
    print('Wrote', OUT_CSV, OUT_MD)

if __name__ == "__main__":
    main()
