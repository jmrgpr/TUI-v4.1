import pandas as pd
import sys

paths = [
    'results/v11/data/bootstrap_stats_v11.csv',
    'results/v11/data/bootstrap_nonparam_from_episodes_v11.csv',
    'results/v11/data/stats_summary_v11.csv'
]

# NaNs esperados por archivo (ej.: p-values solo aplican a ciertos grupos/agentes)
ALLOWED_NA_COLUMNS_BY_PATH = {
    'results/v11/data/stats_summary_v11.csv': {'p_boot', 'p_boot_holm'},
}
ok = True
for p in paths:
    try:
        df = pd.read_csv(p)
    except Exception as e:
        print('ERROR reading', p, e)
        ok = False
        continue
    na = df.isna().sum()
    allowed = ALLOWED_NA_COLUMNS_BY_PATH.get(p, set())
    unexpected_cols = [c for c in df.columns if c not in allowed]
    total_na = int(df[unexpected_cols].isna().sum().sum())
    print(p, 'shape', df.shape, 'total NaNs', int(total_na))
    if total_na > 0:
        print('NaNs per column:\n', na[na > 0].to_dict())
        ok = False

if not ok:
    sys.exit(2)
print('All checks passed (no unexpected NaNs)')
