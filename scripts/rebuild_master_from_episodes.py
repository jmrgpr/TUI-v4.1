import os
import re
import pandas as pd


def find_reward_column(cols):
    candidates = ['reward_total', 'reward', 'Recompensa', 'Recompensa_total', 'recompensa', 'median']
    for c in candidates:
        if c in cols:
            return c
    for c in cols:
        lc = c.lower()
        if 'reward' in lc or 'recomp' in lc:
            return c
    return None


def extract_seed(fname):
    m = re.search(r'seed(\d+)', fname)
    if m:
        return int(m.group(1))
    m2 = re.search(r'_(\d{1,4})_v\d', fname)
    if m2:
        return int(m2.group(1))
    return None


def extract_risk(fname):
    # patterns: r1p2 -> 1.2, risklow/riskhigh -> map
    m = re.search(r'r(\d)p(\d)', fname)
    if m:
        return float(m.group(1)) + float(m.group(2)) / 10.0
    if 'risklow' in fname.lower():
        return 0.5
    if 'riskhigh' in fname.lower():
        return 1.5
    return None


def main():
    base = os.path.join('results', 'v11')
    rows = []
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.lower().endswith('episodes.csv') or 'episodes' in f.lower():
                path = os.path.join(root, f)
                rel_norm = os.path.relpath(path).replace("\\", "/").lower()
                # Evitar duplicados: no usar los CSV agregados en raw/ ni los archivados
                if "/raw/" in rel_norm or "/archived/" in rel_norm:
                    continue
                # Evitar archivos de debug
                if "test_debug_run" in rel_norm:
                    continue
                try:
                    df = pd.read_csv(path)
                except Exception:
                    try:
                        df = pd.read_csv(path, encoding='latin1')
                    except Exception:
                        continue
                col = find_reward_column(list(df.columns))
                if col is None:
                    continue
                vals = pd.to_numeric(df[col], errors='coerce').dropna()
                if vals.empty:
                    continue
                reward_mean = float(vals.mean())
                episodes = int(len(df))
                agent = None
                # try known agent cols
                for ac in ('agent', 'Agente', 'Agent'):
                    if ac in df.columns:
                        agent = df[ac].astype(str).iloc[0]
                        break
                if agent is None:
                    # try folder name
                    parts = root.split(os.sep)
                    if parts:
                        agent = parts[-1]
                seed = extract_seed(f)
                risk_scale = extract_risk(f)
                rows.append({
                    'agent': agent,
                    'seed': seed,
                    'episodes': episodes,
                    'steps': None,
                    'risk_scale': risk_scale,
                    'reward_total': reward_mean,
                    'filename': os.path.relpath(path)
                })

    out = os.path.join('results', 'master_results_clean.csv')
    pd.DataFrame(rows).to_csv(out, index=False)
    print('Wrote', out, 'rows:', len(rows))


if __name__ == '__main__':
    main()
