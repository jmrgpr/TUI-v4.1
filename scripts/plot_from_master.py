import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    master = 'results/master_results_clean.csv' if os.path.exists('results/master_results_clean.csv') else 'results/master_results.csv'
    outdir = os.path.join('results', 'v11', 'plots')
    os.makedirs(outdir, exist_ok=True)

    df = pd.read_csv(master)
    # ensure numeric
    df['reward_total'] = pd.to_numeric(df['reward_total'], errors='coerce')
    # map risk_group from risk_scale if present
    if 'risk_scale' in df.columns:
        try:
            df['risk_group'] = df['risk_scale'].astype(float).round(1)
        except Exception:
            df['risk_group'] = df['risk_scale'].apply(lambda x: str(x))
    else:
        df['risk_group'] = 'unknown'

    df = df.dropna(subset=['agent','reward_total'])

    sns.set(style='whitegrid')

    # Boxplot by agent, faceted by risk_group
    try:
        g = sns.catplot(data=df, x='agent', y='reward_total', col='risk_group', kind='box', sharey=True, height=4, aspect=1.2)
        g.fig.suptitle('Boxplot reward_total por agent y risk_group', y=1.02)
        box_png = os.path.join(outdir, 'box_by_master_risk_agent.png')
        g.savefig(box_png, bbox_inches='tight', dpi=200)
        plt.close(g.fig)
    except Exception as e:
        print('Boxplot error:', e)

    # Violin
    try:
        g2 = sns.catplot(data=df, x='agent', y='reward_total', col='risk_group', kind='violin', sharey=True, height=4, aspect=1.2)
        g2.fig.suptitle('Violin reward_total por agent y risk_group', y=1.02)
        violin_png = os.path.join(outdir, 'violin_by_master_risk_agent.png')
        g2.savefig(violin_png, bbox_inches='tight', dpi=200)
        plt.close(g2.fig)
    except Exception as e:
        print('Violin error:', e)

    print('Plots saved in', outdir)


if __name__ == '__main__':
    main()
