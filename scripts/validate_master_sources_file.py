import os
import pandas as pd
import sys
from validate_master_sources import find_reward_column, read_table


def validate(master_path, outpath):
    df = pd.read_csv(master_path)
    report_rows = []
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
        path = os.path.join(os.getcwd(), filename)
        if not os.path.exists(path):
            report_rows.append({'index': i, 'filename': filename, 'exists': False, 'reason': 'missing file', 'master_reward': master_reward, 'source_reward_mean': None, 'match': False})
            missing_files += 1
            continue
        tbl = read_table(path)
        if tbl is None or tbl.empty:
            report_rows.append({'index': i, 'filename': filename, 'exists': True, 'reason': 'unreadable or empty', 'master_reward': master_reward, 'source_reward_mean': None, 'match': False})
            continue
        col = find_reward_column(list(tbl.columns))
        if col is None:
            report_rows.append({'index': i, 'filename': filename, 'exists': True, 'reason': 'no reward column', 'master_reward': master_reward, 'source_reward_mean': None, 'match': False})
            continue
        vals = pd.to_numeric(tbl[col], errors='coerce').dropna()
        source_mean = float(vals.mean()) if len(vals) > 0 else None
        match = False
        if source_mean is not None and master_reward is not None and not pd.isna(master_reward):
            try:
                master_val = float(master_reward)
                tol = max(1e-6, abs(master_val) * 1e-3)
                if abs(master_val - source_mean) <= tol:
                    match = True
                else:
                    mismatches += 1
            except Exception:
                pass
        report_rows.append({'index': i, 'filename': filename, 'exists': True, 'reason': None, 'master_reward': master_reward, 'source_reward_mean': source_mean, 'match': match})

    rep_df = pd.DataFrame(report_rows)
    rep_df.to_csv(outpath, index=False)
    summary = {'total_rows': len(df), 'missing_files': missing_files, 'mismatches': mismatches, 'missing_agent': missing_agent, 'report_file': outpath}
    return summary


if __name__ == '__main__':
    master = sys.argv[1] if len(sys.argv) > 1 else os.path.join('results', 'master_results_clean.csv')
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join('results', 'v11', 'data', 'validation_master_sources_clean.csv')
    s = validate(master, out)
    print('Validation summary:', s)
