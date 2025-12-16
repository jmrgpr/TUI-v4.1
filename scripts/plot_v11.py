import os
import math
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    src = os.path.join('results', 'v11', 'data', 'episodic_metrics_v11_full.csv')
    outdir = os.path.join('results', 'v11', 'plots')
    os.makedirs(outdir, exist_ok=True)

    df = pd.read_csv(src)

    # Ensure risk_group exists; if empty, try to map from risk_scale
    if 'risk_group' not in df.columns or df['risk_group'].isnull().all():
        def map_risk(x):
            try:
                v = float(x)
            except Exception:
                return 'unknown'
            # canonical grid
            grid = [0.5, 1.0, 1.5, 2.0, 3.0]
            return min(grid, key=lambda g: abs(g - v))
        df['risk_group'] = df['risk_scale'].apply(map_risk)

    # Clean agent and numeric columns
    df['agent'] = df['agent'].astype(str)
    df['risk_group'] = df['risk_group'].astype(str)
    # Use 'median' as summary metric for plotting (per-run median reward)
    df['median'] = pd.to_numeric(df['median'], errors='coerce')
    plot_df = df.dropna(subset=['median'])

    # Order risk groups for consistent layout
    try:
        risk_order = sorted({float(x) for x in plot_df['risk_group'] if x not in ('nan','unknown')})
        risk_order = [str(x) for x in risk_order]
    except Exception:
        risk_order = sorted(plot_df['risk_group'].unique())

    # Violin plot (one column per risk_group)
    sns.set(style='whitegrid')
    try:
        g = sns.catplot(
            data=plot_df,
            x='agent', y='median', col='risk_group',
            col_order=risk_order if len(risk_order) > 0 else None,
            kind='violin', sharey=True, height=4, aspect=1.2)
        g.set_titles('risk_group = {col_name}')
        g.fig.suptitle('Violin plot: median reward por agent y risk_group', y=1.02)
        violin_png = os.path.join(outdir, 'violin_by_risk_agent.png')
        violin_svg = os.path.join(outdir, 'violin_by_risk_agent.svg')
        g.savefig(violin_png, bbox_inches='tight', dpi=200)
        g.savefig(violin_svg, bbox_inches='tight')
        plt.close(g.fig)
    except Exception as e:
        print('Error generando violín:', e)

    # Boxplot (same layout)
    try:
        g2 = sns.catplot(
            data=plot_df,
            x='agent', y='median', col='risk_group',
            col_order=risk_order if len(risk_order) > 0 else None,
            kind='box', sharey=True, height=4, aspect=1.2)
        g2.set_titles('risk_group = {col_name}')
        g2.fig.suptitle('Boxplot: median reward por agent y risk_group', y=1.02)
        box_png = os.path.join(outdir, 'box_by_risk_agent.png')
        box_svg = os.path.join(outdir, 'box_by_risk_agent.svg')
        g2.savefig(box_png, bbox_inches='tight', dpi=200)
        g2.savefig(box_svg, bbox_inches='tight')
        plt.close(g2.fig)
    except Exception as e:
        print('Error generando boxplot:', e)

    print('Plots guardados en', outdir)


if __name__ == '__main__':
    main()
