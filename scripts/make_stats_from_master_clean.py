import os
import pandas as pd

"""
DEPRECATED:
Este script fue reemplazado por `scripts/analisis_estadistico_v11.py`, que:
- Agrupa por fase/agent/risk y soporta multiples metricas (reward_total y reward_env_total)
- Integra bootstrap por run/seed para F2
"""

def main():
    src = os.path.join('results', 'master_results_clean.csv')
    outdir = os.path.join('results', 'v11', 'data')
    os.makedirs(outdir, exist_ok=True)
    df = pd.read_csv(src)
    # group by agent and risk_scale
    grp = df.groupby(['agent', 'risk_scale'])['reward_total'].agg(['count','mean','std']).reset_index()
    grp = grp.rename(columns={'count':'n','mean':'mean','std':'std'})
    # mark groups with small n and replace NaN std with 0 to avoid NaNs in downstream files
    grp['note'] = grp['n'].apply(lambda x: 'n<2' if x < 2 else 'ok')
    grp['std'] = grp['std'].fillna(0.0)
    out = os.path.join(outdir, 'stats_summary_v11.csv')
    grp.to_csv(out, index=False)
    print('Wrote', out)

if __name__ == '__main__':
    main()
