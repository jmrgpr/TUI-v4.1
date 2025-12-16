import pandas as pd
master_path = 'results/master_results_clean.csv' if os.path.exists('results/master_results_clean.csv') else 'results/master_results.csv'
m = pd.read_csv(master_path)
print('Using master file:', master_path)
print('rows:', len(m))
print('agent unique sample:', m['agent'].dropna().unique()[:20])
print('counts by agent (non-null reward_total):')
print(m[~m['reward_total'].isna()].groupby('agent').size().sort_values(ascending=False).head(20))
print('\nNon-null reward_total total:', m['reward_total'].notna().sum())
print('Sample rows with agent and reward_total:')
print(m[m['reward_total'].notna()].head(10))
