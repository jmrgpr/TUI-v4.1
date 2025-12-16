import os
import csv
import json
import math
import pandas as pd


def find_reward_column(cols):
    candidates = ['reward_total', 'reward', 'Recompensa', 'Recompensa_total', 'recompensa', 'median']
    for c in candidates:
        if c in cols:
            return c
    # try fuzzy: lower-case contains 'reward' or 'recomp'
    for c in cols:
        lc = c.lower()
        if 'reward' in lc or 'recomp' in lc:
            return c
    return None


def read_table(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        try:
            return pd.read_csv(path)
        except Exception:
            # try with latin1
            return pd.read_csv(path, encoding='latin1')
    elif ext == '.json':
        with open(path, 'r', encoding='utf8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    else:
        return None


def main():
    # prefer cleaned master when available
    candidate = os.path.join('results', 'master_results_clean.csv')
    if os.path.exists(candidate):
        master = candidate
    else:
        master = os.path.join('results', 'master_results.csv')
    outdir = os.path.join('results', 'v11', 'data')
    os.makedirs(outdir, exist_ok=True)
    report_rows = []

    df = pd.read_csv(master)
    total = len(df)
    missing_files = 0
    mismatches = 0
    missing_agent = 0

    for i, row in df.iterrows():
        filename = row.get('filename')
        master_reward = row.get('reward_total') if 'reward_total' in row.index else None
        agent = row.get('agent') if 'agent' in row.index else None
        if pd.isna(agent):
            missing_agent += 1
        if not filename or pd.isna(filename):
            report_rows.append({'index': i, 'filename': None, 'exists': False, 'reason': 'no filename', 'master_reward': master_reward, 'source_reward_mean': None, 'match': False})
            continue
        # Try several candidate base locations for the filename
        candidates = [
            os.path.join(os.getcwd(), filename),
            os.path.join(os.getcwd(), 'results', 'v11', 'data', filename),
            os.path.join(os.getcwd(), 'results', 'v11', filename),
            os.path.join(os.getcwd(), 'results', filename),
            os.path.join(os.getcwd(), 'results', 'v11', 'archived', filename),
        ]
        path = None
        for c in candidates:
            if os.path.exists(c):
                path = c
                break
        if path is None:
            missing_files += 1
            report_rows.append({'index': i, 'filename': filename, 'exists': False, 'reason': 'missing file', 'master_reward': master_reward, 'source_reward_mean': None, 'match': False})
            continue
        # try to read
        tbl = read_table(path)
        if tbl is None or tbl.empty:
            report_rows.append({'index': i, 'filename': filename, 'exists': True, 'reason': 'unreadable or empty', 'master_reward': master_reward, 'source_reward_mean': None, 'match': False})
            continue
        col = find_reward_column(list(tbl.columns))
        if col is None:
            report_rows.append({'index': i, 'filename': filename, 'exists': True, 'reason': 'no reward column', 'master_reward': master_reward, 'source_reward_mean': None, 'match': False})
            continue
        # compute mean
        try:
            vals = pd.to_numeric(tbl[col], errors='coerce').dropna()
            if len(vals) == 0:
                source_mean = None
            else:
                source_mean = float(vals.mean())
        except Exception:
            source_mean = None
        match = False
        if source_mean is not None and master_reward is not None and not pd.isna(master_reward):
            try:
                master_val = float(master_reward)
                # tolerance relative or absolute
                tol = max(1e-6, abs(master_val) * 1e-3)
                if abs(master_val - source_mean) <= tol:
                    match = True
                else:
                    mismatches += 1
            except Exception:
                pass

        report_rows.append({'index': i, 'filename': filename, 'exists': True, 'reason': None, 'master_reward': master_reward, 'source_reward_mean': source_mean, 'match': match})

    rep_df = pd.DataFrame(report_rows)
    out = os.path.join(outdir, 'validation_master_sources.csv')
    rep_df.to_csv(out, index=False)

    summary = {
        'total_rows': total,
        'missing_files': missing_files,
        'mismatches': mismatches,
        'missing_agent': missing_agent,
        'report_file': out
    }
    print('Validation summary:', summary)


if __name__ == '__main__':
    main()
