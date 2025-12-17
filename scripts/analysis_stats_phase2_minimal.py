import pandas as pd
import numpy as np

# Minimal statistical analysis for Phase2 sweep artifacts (NOT v11 series).
# Input: `reports/phase2/summary_agent_risk.csv`
# Output: `reports/phase2/analysis_stats_summary.csv`

IN_PATH = "reports/phase2/summary_agent_risk.csv"
OUT_PATH = "reports/phase2/analysis_stats_summary.csv"

def bootstrap_ci(data, n_boot=1000, alpha=0.05):
    boot_means = []
    n = len(data)
    for _ in range(n_boot):
        sample = np.random.choice(data, size=n, replace=True)
        boot_means.append(np.mean(sample))
    lower = np.percentile(boot_means, 100 * (alpha/2))
    upper = np.percentile(boot_means, 100 * (1 - alpha/2))
    return lower, upper


def cohens_d(x, y):
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    pooled_std = np.sqrt(((nx-1)*np.var(x, ddof=1) + (ny-1)*np.var(y, ddof=1)) / dof)
    if pooled_std == 0:
        return np.nan
    return (np.mean(x) - np.mean(y)) / pooled_std


def analyze():
    df = pd.read_csv(IN_PATH)
    # Expect columns: agent, risk, total_reward, tripwires, robustez
    rows = []
    agents = df['agent'].unique()
    risks = sorted(df['risk'].unique()) if 'risk' in df.columns else [None]
    for agent in agents:
        for risk in (risks if risks!=[None] else [None]):
            if risk is None:
                sub = df[df['agent']==agent]
            else:
                sub = df[(df['agent']==agent)&(df['risk']==risk)]
            if sub.empty:
                continue
            rewards = sub['total_reward'].values
            n = len(rewards)
            mean = np.mean(rewards)
            std = np.std(rewards, ddof=1)
            median = np.median(rewards)
            iqr = np.percentile(rewards,75)-np.percentile(rewards,25)
            pct_tripwires = sub['tripwires'].mean() if 'tripwires' in sub.columns else np.nan
            # CVaR 0.95 (average of worst 5%)
            cvar95 = np.mean(np.sort(rewards)[:max(1, int(0.05*len(rewards)))])
            # max drawdown on reward series (per episode if available)
            # here approximate from cumulative max drop
            cumsum = np.cumsum(rewards - np.mean(rewards))
            cummax = np.maximum.accumulate(cumsum)
            drawdown = np.min(cumsum - cummax)
            lower, upper = bootstrap_ci(rewards)
            rows.append({
                'agent': agent,
                'risk': risk,
                'n': n,
                'mean': mean,
                'std': std,
                'median': median,
                'iqr': iqr,
                'pct_tripwires': pct_tripwires,
                'cvar95': cvar95,
                'max_drawdown': drawdown,
                'ci95_lower': lower,
                'ci95_upper': upper
            })
    out = pd.DataFrame(rows)
    out.to_csv(OUT_PATH, index=False)
    print('Wrote', OUT_PATH)

if __name__ == '__main__':
    analyze()
