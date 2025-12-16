import pandas as pd
m = pd.read_csv('results/master_results.csv')
print('rows:', len(m))
print('agent unique sample:', m['agent'].dropna().unique()[:20])
print('counts by agent (non-null reward_total):')
print(m[~m['reward_total'].isna()].groupby('agent').size().sort_values(ascending=False).head(20))
print('\nNon-null reward_total total:', m['reward_total'].notna().sum())
print('Sample rows with agent and reward_total:')
print(m[m['reward_total'].notna()].head(10))
