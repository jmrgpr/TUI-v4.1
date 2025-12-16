import pandas as pd
import sys

paths = [
    'results/v11/data/bootstrap_stats_v11.csv',
    'results/v11/data/bootstrap_nonparam_from_episodes_v11.csv',
    'results/v11/data/stats_summary_v11.csv'
]
ok = True
for p in paths:
    try:
        df = pd.read_csv(p)
    except Exception as e:
        print('ERROR reading', p, e)
        ok = False
        continue
    na = df.isna().sum()
    total_na = na.sum()
    print(p, 'shape', df.shape, 'total NaNs', int(total_na))
    if total_na > 0:
        print('NaNs per column:\n', na[na>0].to_dict())
        ok = False

if not ok:
    sys.exit(2)
print('All checks passed (no unexpected NaNs)')
