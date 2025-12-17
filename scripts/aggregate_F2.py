import pandas as pd
import glob

files=sorted(glob.glob('results/v11/F2_redteam/raw/**/*_episodes.csv', recursive=True))
allrows=[]
for f in files:
    try:
        df=pd.read_csv(f)
    except Exception:
        continue
    if 'Recompensa' in df.columns:
        reward = pd.to_numeric(df['Recompensa'], errors='coerce')
    elif 'reward' in df.columns:
        reward = pd.to_numeric(df['reward'], errors='coerce')
    else:
        nums=[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        reward = pd.to_numeric(df[nums[0]], errors='coerce') if nums else pd.Series([])
    agent_col = 'Agente' if 'Agente' in df.columns else ('agent' if 'agent' in df.columns else None)
    agent = df[agent_col] if agent_col else pd.Series(['unknown']*len(reward))
    tmp = pd.DataFrame({'agent': agent, 'reward': reward})
    allrows.append(tmp)
if not allrows:
    print('No episode files found')
else:
    big = pd.concat(allrows, ignore_index=True)
    big = big.dropna(subset=['reward'])
    grp = big.groupby('agent')['reward'].agg(['count','mean','std']).reset_index()
    print(grp.to_string(index=False))
