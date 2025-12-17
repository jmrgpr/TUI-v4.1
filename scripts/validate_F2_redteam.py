import os
import pandas as pd
import json

def find_reward_col(df):
    candidates = ['reward_total','reward','reward_episode','reward_mean','reward_total_episode','Recompensa','Recompensa_total','Recompensa_media']
    for c in candidates:
        if c in df.columns:
            return c
    numerics = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    return numerics[-1] if numerics else None

def analyze():
    master = pd.read_csv(os.path.join('results','master_results.csv'))
    mask = master['filename'].str.contains('results\\v11\\F2_redteam', na=False, regex=False)
    subset = master[mask].copy()
    report = []
    for idx, row in subset.iterrows():
        fn = row['filename']
        rel = fn.replace('\\','/')
        path = os.path.join(os.getcwd(), rel)
        entry = {'index': int(idx), 'filename': fn, 'master_reward': row.get('reward_total')}
        if not os.path.exists(path):
            entry.update({'exists': False, 'n': None, 'source_mean': None, 'source_std': None, 'match': False, 'error':'missing file'})
            report.append(entry)
            continue
        try:
            df = pd.read_csv(path)
            col = find_reward_col(df)
            if col is None:
                entry.update({'exists': True, 'n': 0, 'source_mean': None, 'source_std': None, 'match': False, 'error':'no reward col'})
                report.append(entry)
                continue
            vals = pd.to_numeric(df[col], errors='coerce').dropna()
            n = int(len(vals))
            mean = float(vals.mean()) if n>0 else None
            std = float(vals.std(ddof=1)) if n>1 else (0.0 if n==1 else None)
            match = False
            try:
                m = float(row.get('reward_total'))
                tol = max(1e-6, abs(m)*1e-3)
                if mean is not None and abs(m-mean) <= tol:
                    match = True
            except Exception:
                pass
            entry.update({'exists': True, 'n': n, 'source_mean': mean, 'source_std': std, 'match': match, 'error': None})
        except Exception as e:
            entry.update({'exists': True, 'n': None, 'source_mean': None, 'source_std': None, 'match': False, 'error': str(e)})
        report.append(entry)

    outdir = os.path.join('results','v11','data')
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir,'validation_F2_redteam_report.csv')
    pd.DataFrame(report).to_csv(outpath, index=False)
    # summary
    total = len(report)
    missing = sum(1 for r in report if not r['exists'])
    mismatches = sum(1 for r in report if r['exists'] and r['match']==False)
    print('F2_redteam validation: total_rows', total, 'missing_files', missing, 'mismatches', mismatches, 'report:', outpath)

if __name__ == '__main__':
    analyze()
