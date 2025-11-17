"""
Script oficial Fase 4: Escalabilidad v10 (16x16)
Ejecuta los experimentos F4a (sin regularización) y F4b (con regularización) para seeds 42 y 101.
"""
import sys
import os
import pandas as pd
from pathlib import Path
# Añadir la raíz del proyecto al sys.path para importar sim correctamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.runner import run_experiment

def run_f4(config_name, regularization, seed, episodes, outdir):
    result = run_experiment(
        episodes=episodes,
        seed=seed,
        risk_scale=1.0,
        agent_name="DQN-Control",
        use_pgf=False,
        use_dqn=True,
        grid_size=16,
        regularization=regularization
    )
    df = pd.DataFrame({
        'episode': list(range(episodes)),
        'total_reward': result['total_rewards'],
        'pgf_mean': [sum(p)/len(p) if p else 0 for p in result['pgf_evol']],
        'success': [1 if r > 0 else 0 for r in result['total_rewards']],
        'steps': [len(p) for p in result['pgf_evol']]
    })
    outpath = Path(outdir) / f'{config_name}_seed{seed}.csv'
    outpath.parent.mkdir(exist_ok=True)
    df.to_csv(outpath, index=False)
    print(f"Resultados guardados en {outpath}")

if __name__ == "__main__":
    episodes = 3000
    # F4a: sin regularización
    for seed in [42, 101]:
        run_f4('config_E_16x16_noreg', False, seed, episodes, 'results/pgf_v10_scalability/config_E_16x16_noreg/')
    # F4b: con regularización
    for seed in [42, 101]:
        run_f4('config_F_16x16_reg', True, seed, episodes, 'results/pgf_v10_scalability/config_F_16x16_reg/')
