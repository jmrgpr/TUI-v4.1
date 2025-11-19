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

def run_sota_comparison(
    risk_scale: float = 1.0,
    total_timesteps: int = 100000,
    seed: int = 42,
    steps_per_episode: int = 50,
    eval_episodes: int = 100,
    output_prefix: str = "results/Experimento2/data/sota",
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
    total_episodes = total_timesteps // steps_per_episode
    pgf_bruto_list = []
    pgf_costo_list = []

    tripwire_count = 0
    tripwire_list = []
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
            "risk_level": ["default"],
            "red_team": [False],
            "seed": [int(seed)],
            "agent": [agent_label],
            "episodes": [total_episodes],
            "steps_per_episode": [steps_per_episode],
            "eval_episodes": [eval_episodes],
            "total_timesteps": [total_timesteps],
            "avg_pgf_neto": [np.mean(pgf_neto_list)],
            "avg_pgf_bruto": [np.mean(pgf_bruto_list)],
            "avg_pgf_costo": [np.mean(pgf_costo_list)],
            "avg_tripwire": [avg_tripwire],
            "avg_reward": [avg_reward],
            "robustez": [np.nan],
            "flexibilidad": [np.nan],
        }
    )

    os.makedirs(output_prefix, exist_ok=True)
    out_csv = (
        f"{output_prefix}/{algo}/sota_{algo}_seed{seed}_risk{risk_scale}"
        f"_leveldefault_redfalse_episodes{total_episodes}_steps{steps_per_episode}.csv"
    )
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    results_df.to_csv(out_csv, index=False)
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
        out_dir = "results/Experimento2/data/sota"
        os.makedirs(f"{out_dir}/{algo}", exist_ok=True)
        algo_df.to_csv(f"{out_dir}/{algo}/sota_{algo}_global_summary.csv", index=False)
        combined_all.append(algo_df)

    out_dir = "results/Experimento2/data/sota"
    pd.concat(combined_all, ignore_index=True).to_csv(f"{out_dir}/sota_all_global_summary.csv", index=False)
    print(
        "\nComparacion SOTA completada. Archivos guardados en results/Experimento2/data/sota/<algo>/sota_<algo>_global_summary.csv y results/Experimento2/data/sota/sota_all_global_summary.csv"
    )

        truncated = False
        episode_reward = 0
        episode_pgf_neto = 0
        episode_pgf_bruto = 0
        episode_pgf_costo = 0
        episode_tripwire = 0

        ep_reward = 0
        # Listas temporales para promediar por episodio
        ep_pgf_neto = []
        ep_pgf_bruto = []
        ep_pgf_costo = []

        while not done:
            # Usamos deterministic=False para permitir que PPO use su estrategia exploratoria aprendida
            # (En deterministic=True se observó colapso/congelamiento en risk alto)
            action, _ = model.predict(obs, deterministic=False)
            obs, reward, done, _, info = eval_env.step(action)
            
            ep_reward += reward
            if info.get('tripwire'):
                tripwire_count += 1
            
            # Capturar métricas PGF del wrapper
            if 'pgf_neto' in info: ep_pgf_neto.append(info['pgf_neto'])
            if 'pgf_bruto' in info: ep_pgf_bruto.append(info['pgf_bruto'])
            if 'pgf_costo' in info: ep_pgf_costo.append(info['pgf_costo'])

        rewards.append(ep_reward)
        pgf_neto_list.append(np.mean(ep_pgf_neto) if ep_pgf_neto else 0.0)
        pgf_bruto_list.append(np.mean(ep_pgf_bruto) if ep_pgf_bruto else 0.0)
        pgf_costo_list.append(np.mean(ep_pgf_costo) if ep_pgf_costo else 0.0)

    # 5. Guardar Resultados
    avg_reward = np.mean(rewards)
    avg_tripwire = tripwire_count / eval_episodes
    
    results_df = pd.DataFrame({
        'risk_scale': [risk_scale],
        'agent': ['ppo_sota'],
        'avg_pgf_neto': [np.mean(pgf_neto_list)],
        'avg_pgf_bruto': [np.mean(pgf_bruto_list)],
        'avg_pgf_costo': [np.mean(pgf_costo_list)],
        'avg_tripwire': [avg_tripwire],
        'avg_reward': [avg_reward]
    })

    # Guardar CSV individual
    os.makedirs("results", exist_ok=True)
    results_df.to_csv(f"{output_prefix}_risk{risk_scale}_summary.csv", index=False)
    print(f"   > Resultado Risk {risk_scale}: Reward={avg_reward:.2f} | PGF Bruto={np.mean(pgf_bruto_list):.4f}")

    return results_df

if __name__ == "__main__":
    # Ejecutar barrido completo
    risk_scales = [0.5, 1.0, 1.5, 2.0, 3.0]
    all_results = []

    for risk in risk_scales:
        result = run_sota_comparison(risk_scale=risk, total_timesteps=50000)
        all_results.append(result)

    combined_df = pd.concat(all_results, ignore_index=True)
    combined_df.to_csv("results/sota_ppo_global_summary.csv", index=False)

    print("\nResumen global guardado en: results/sota_ppo_global_summary.csv")
    print("\n✅ Comparación SOTA completada. Archivo guardado: results/sota_ppo_global_summary.csv")
