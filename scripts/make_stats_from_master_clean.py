import os
import pandas as pd

def main():
    src = os.path.join('results', 'master_results_clean.csv')
    outdir = os.path.join('results', 'v11', 'data')
    os.makedirs(outdir, exist_ok=True)
    df = pd.read_csv(src)
    # group by agent and risk_scale
    grp = df.groupby(['agent', 'risk_scale'])['reward_total'].agg(['count','mean','std']).reset_index()
    grp = grp.rename(columns={'count':'n','mean':'mean','std':'std'})
    out = os.path.join(outdir, 'stats_summary_v11.csv')
    grp.to_csv(out, index=False)
    print('Wrote', out)

if __name__ == '__main__':
    main()
