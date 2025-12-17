
# Bootstrap no-paramétrico real sobre recompensas crudas de episodios
import pandas as pd
import numpy as np
import os
from glob import glob

DATA_DIR = 'results/v11/data'
RAW_DIR = 'results/v11/F2_redteam'
OUT_CSV = os.path.join(DATA_DIR, 'bootstrap_stats_v11.csv')
OUT_MD = os.path.join(DATA_DIR, 'bootstrap_stats_v11.md')
B = 5000
RANDOM_SEED = 2025

def two_sided_pval(samples):
    obs = np.mean(samples)
    return np.mean(np.abs(samples) >= abs(obs))

def get_episode_rewards_from_rows(rows):
    rewards = []
    for path in rows:
        try:
            p = os.path.normpath(path)
            if not os.path.exists(p):
                # try relative to repo root
                p = os.path.normpath(os.path.join(os.getcwd(), path))
            df = pd.read_csv(p)
            if 'Recompensa' in df.columns:
                rewards.extend(df['Recompensa'].values)
            elif 'reward_total' in df.columns:
                rewards.extend(df['reward_total'].values)
            elif 'Recompensa_total' in df.columns:
                rewards.extend(df['Recompensa_total'].values)
            else:
                # try common numeric columns
                numcols = df.select_dtypes(include=[np.number]).columns
                if len(numcols) > 0:
                    rewards.extend(df[numcols[0]].values)
        except Exception as e:
            print(f'Warning: no se pudo leer {path}: {e}')
    return np.array(rewards)

def main():
    np.random.seed(RANDOM_SEED)
    episodic_path = os.path.join(DATA_DIR, 'episodic_metrics_v11_full.csv')
    if not os.path.exists(episodic_path):
        raise RuntimeError(f'episodic metrics not found: {episodic_path}')
    episodic = pd.read_csv(episodic_path)
    episodic = episodic.dropna(subset=['agent'])
    rows_out = []
    for (risk, agent), grp in episodic.groupby(['risk_scale', 'agent']):
        # collect file paths
        file_paths = grp['file'].dropna().unique().tolist()
        rewards = get_episode_rewards_from_rows(file_paths)
        if agent == 'control':
            # store control rewards per risk
            ctrl_rewards = rewards
            continue
        # ensure we have control rewards for this risk
        ctrl_grp = episodic[(episodic['risk_scale'] == risk) & (episodic['agent'] == 'control')]
        ctrl_paths = ctrl_grp['file'].dropna().unique().tolist()
        ctrl_rewards = get_episode_rewards_from_rows(ctrl_paths)
        if len(rewards) < 2 or len(ctrl_rewards) < 2:
            continue
        diffs = []
        n1, n2 = len(rewards), len(ctrl_rewards)
        for _ in range(B):
            samp1 = np.random.choice(rewards, size=n1, replace=True)
            samp2 = np.random.choice(ctrl_rewards, size=n2, replace=True)
            diffs.append(np.mean(samp1) - np.mean(samp2))
        diffs = np.array(diffs)
        ci_lo, ci_hi = np.percentile(diffs, [2.5, 97.5])
        # adjusted p-value: (count + 1)/(B + 1)
        obs = np.mean(diffs)
        count = np.sum(np.abs(diffs) >= abs(obs))
        pval = float((count + 1) / (B + 1))
        mean_diff = obs
        rows_out.append({'agent':agent, 'risk_scale':risk, 'mean_diff':mean_diff, 'ci95_lo':ci_lo, 'ci95_hi':ci_hi, 'p_boot':pval})
    out = pd.DataFrame(rows_out)
    os.makedirs(DATA_DIR, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write('# Bootstrap no-paramétrico real — v11\n\n')
        f.write('Se generaron estimaciones bootstrap no-paramétricas (remuestreo con reemplazo de recompensas crudas de episodios) para la diferencia de medias vs control por `risk_scale`.\n\n')
        if out.empty:
            f.write('No se encontraron datos para generar bootstrap.\n')
        else:
            f.write(out.to_string(index=False))
    print('Wrote', OUT_CSV, OUT_MD)

if __name__ == "__main__":
    main()
