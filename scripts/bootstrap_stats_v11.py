import pandas as pd
import numpy as np
import os
from math import erf

DATA_DIR = 'results/v11/data'
IN_CSV = os.path.join(DATA_DIR, 'stats_summary_v11.csv')
OUT_CSV = os.path.join(DATA_DIR, 'bootstrap_stats_v11.csv')
OUT_MD = os.path.join(DATA_DIR, 'bootstrap_stats_v11.md')

B = 5000
RANDOM_SEED = 2025

def two_sided_pval(samples):
    # samples: array of bootstrap differences
    # p-value approximate: proportion of samples with sign opposite or beyond observed 0
    obs = np.mean(samples)
    # two-sided: proportion with abs >= abs(obs)
    return np.mean(np.abs(samples) >= abs(obs))

def main():
    df = pd.read_csv(IN_CSV)
    # expect columns: agent, risk_scale, n, mean, std, ci95_lo, ci95_hi, cohens_d?, p_value_vs_control?
    if df.empty:
        raise RuntimeError('Empty input stats file')
    agents = df['agent'].unique()
    rows = []
    np.random.seed(RANDOM_SEED)
    for risk in sorted(df['risk_scale'].unique()):
        grp = df[df['risk_scale'] == risk]
        ctrl = grp[grp['agent']=='control']
        if ctrl.empty:
            continue
        m2 = float(ctrl['mean'].iloc[0]); s2 = float(ctrl['std'].iloc[0]); n2 = int(ctrl['n'].iloc[0])
        for _, r in grp.iterrows():
            agent = r['agent']
            if agent == 'control':
                continue
            m1 = float(r['mean']); s1 = float(r['std']); n1 = int(r['n'])
            diffs = []
            for _ in range(B):
                # parametric sampling (normal) as confirmatory approx
                samp1 = np.random.normal(loc=m1, scale=s1, size=n1)
                samp2 = np.random.normal(loc=m2, scale=s2, size=n2)
                diffs.append(np.mean(samp1) - np.mean(samp2))
            diffs = np.array(diffs)
            ci_lo, ci_hi = np.percentile(diffs, [2.5, 97.5])
            pval = two_sided_pval(diffs)
            mean_diff = np.mean(diffs)
            rows.append({'agent':agent, 'risk_scale':risk, 'mean_diff':mean_diff, 'ci95_lo':ci_lo, 'ci95_hi':ci_hi, 'p_boot':pval})
    out = pd.DataFrame(rows)
    os.makedirs(DATA_DIR, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write('# Bootstrap confirmatorio (parametric approx) — v11\n\n')
        f.write('Se generaron estimaciones bootstrap paramétricas (muestreo normal) para la diferencia de medias vs control por `risk_scale`. Esto es confirmatorio y asume distribución aproximadamente normal de reward_total por run; recomendamos bootstrap no paramétrico si se dispone de raw per-run reward_total.\n\n')
        f.write(out.to_string(index=False))
    print('Wrote', OUT_CSV, OUT_MD)

if __name__ == "__main__":
    main()
