import os
import numpy as np
import pandas as pd
import warnings
from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.env_util import make_vec_env
from sim.sota_wrapper import SimbiosisGymEnv

warnings.filterwarnings("ignore")

ALGORITHMS = {
    "ppo": PPO,
    "a2c": A2C,
    "dqn": DQN,  # alternativa discreta en lugar de SAC (requiere acciones continuas)
}


def run_sota_comparison(  # pragma: no cover - se ejecuta fuera de las pruebas unitarias
    risk_scale: float = 1.0,
    total_timesteps: int = 100000,
    seed: int = 42,
    output_prefix: str = "results/sota",
    algo: str = "ppo",
):
    """
    Entrena un agente SOTA (PPO/A2C/DQN) y guarda resultados compatibles con Fase 2.
    """
    algo = algo.lower()
    if algo not in ALGORITHMS:
        raise ValueError(f"Algoritmo no soportado: {algo}")
    AlgoCls = ALGORITHMS[algo]
    agent_label = f"{algo}_sota"

    print(f"=== Entrenando {agent_label.upper()} en Risk Scale {risk_scale} ===")

    env = make_vec_env(lambda: SimbiosisGymEnv(risk_scale=risk_scale), n_envs=4, seed=seed)

    model = AlgoCls("MlpPolicy", env, verbose=0, seed=seed)

    model.learn(total_timesteps=total_timesteps)

    print(f"   > Evaluando modelo (Risk {risk_scale})...")
    eval_env = SimbiosisGymEnv(risk_scale=risk_scale)
    eval_episodes = 100

    rewards = []
    pgf_neto_list = []
    pgf_bruto_list = []
    pgf_costo_list = []
    tripwire_count = 0

    for ep in range(eval_episodes):
        obs, _ = eval_env.reset(seed=seed + ep)
        done = False
        ep_reward = 0
        ep_pgf_neto = []
        ep_pgf_bruto = []
        ep_pgf_costo = []

        while not done:
            action, _ = model.predict(obs, deterministic=False)
            obs, reward, done, _, info = eval_env.step(action)

            ep_reward += reward
            if info.get("tripwire"):
                tripwire_count += 1

            if "pgf_neto" in info:
                ep_pgf_neto.append(info["pgf_neto"])
            if "pgf_bruto" in info:
                ep_pgf_bruto.append(info["pgf_bruto"])
            if "pgf_costo" in info:
                ep_pgf_costo.append(info["pgf_costo"])

        rewards.append(ep_reward)
        pgf_neto_list.append(np.mean(ep_pgf_neto) if ep_pgf_neto else 0.0)
        pgf_bruto_list.append(np.mean(ep_pgf_bruto) if ep_pgf_bruto else 0.0)
        pgf_costo_list.append(np.mean(ep_pgf_costo) if ep_pgf_costo else 0.0)

    avg_reward = np.mean(rewards)
    avg_tripwire = tripwire_count / eval_episodes

    results_df = pd.DataFrame(
        {
            "risk_scale": [risk_scale],
            "agent": [agent_label],
            "avg_pgf_neto": [np.mean(pgf_neto_list)],
            "avg_pgf_bruto": [np.mean(pgf_bruto_list)],
            "avg_pgf_costo": [np.mean(pgf_costo_list)],
            "avg_tripwire": [avg_tripwire],
            "avg_reward": [avg_reward],
        }
    )

    os.makedirs("results", exist_ok=True)
    results_df.to_csv(f"{output_prefix}_{algo}_risk{risk_scale}_summary.csv", index=False)
    print(
        f"   > Resultado {agent_label} Risk {risk_scale}: Reward={avg_reward:.2f} | PGF Bruto={np.mean(pgf_bruto_list):.4f}"
    )

    return results_df


if __name__ == "__main__":  # pragma: no cover - bloque CLI
    risk_scales = [0.5, 1.0, 1.5, 2.0, 3.0]
    algorithms = ["ppo", "a2c", "dqn"]
    combined_all = []

    for algo in algorithms:
        all_results = []
        for risk in risk_scales:
            result = run_sota_comparison(risk_scale=risk, total_timesteps=50000, algo=algo)
            all_results.append(result)
        algo_df = pd.concat(all_results, ignore_index=True)
        algo_df.to_csv(f"results/sota_{algo}_global_summary.csv", index=False)
        combined_all.append(algo_df)

    pd.concat(combined_all, ignore_index=True).to_csv("results/sota_all_global_summary.csv", index=False)
    print(
        "\nComparacion SOTA completada. Archivos guardados en results/sota_<algo>_global_summary.csv y results/sota_all_global_summary.csv"
    )
