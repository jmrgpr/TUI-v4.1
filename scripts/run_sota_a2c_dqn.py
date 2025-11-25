import os
import numpy as np
import pandas as pd
from stable_baselines3 import A2C, DQN, PPO
from stable_baselines3.common.env_util import make_vec_env
from sim.sota_wrapper import SimbiosisGymEnv



# --- Configuración ---
<<<<<<< HEAD
# Este script ejecuta SOTA PPO/A2C/DQN con parámetros alineados al pipeline principal.
# TOTAL_TIMESTEPS se ajusta para que sea comparable a episodios x pasos por episodio.
=======
# Este script ejecuta SOTA A2C/DQN con parámetros alineados al pipeline principal.
# Ajusta TOTAL_TIMESTEPS para que sea comparable al número de episodios × pasos por episodio.
>>>>>>> 81a1f5f (Actualización tras Experimento 2: resultados consolidados, notebook robusto, documentación mejorada y nuevas publicaciones.)
# Ejemplo: si cada episodio dura ~50 pasos y usas 1000 episodios, TOTAL_TIMESTEPS=50000.

ALGORITHMS = {
    "ppo": PPO,
    "a2c": A2C,
    "dqn": DQN,
}
RISK_SCALES = [0.5, 1.0, 1.5, 2.0, 3.0]
<<<<<<< HEAD
RISK_LEVELS = ["default"]  # Solo para naming; no se pasa al entorno
RED_TEAM = [False]  # Para máxima compatibilidad y eficiencia, solo False
SEEDS = [42, 123, 456]
EPISODES = int(os.getenv("SOTA_EPISODES", "1000"))  # override via env for smoke tests
STEPS_PER_EPISODE = int(os.getenv("SOTA_STEPS", "50"))  # override via env for smoke tests
TOTAL_TIMESTEPS = EPISODES * STEPS_PER_EPISODE
EVAL_EPISODES = int(os.getenv("SOTA_EVAL_EPISODES", str(EPISODES)))
OUTPUT_DIR = "experimento2-reestructurado/data/sota/"
=======
RISK_LEVELS = ["default"]  # Modifica si tienes más niveles
RED_TEAM = [False]  # Para máxima compatibilidad y eficiencia, solo False
SEEDS = [42, 123, 456]
EPISODES = 1000  # Igual que el pipeline principal
STEPS_PER_EPISODE = 50  # Ajusta según tu entorno
TOTAL_TIMESTEPS = EPISODES * STEPS_PER_EPISODE
EVAL_EPISODES = EPISODES
OUTPUT_DIR = "results/sota/"
>>>>>>> 81a1f5f (Actualización tras Experimento 2: resultados consolidados, notebook robusto, documentación mejorada y nuevas publicaciones.)
os.makedirs(OUTPUT_DIR, exist_ok=True)

all_results = {"ppo": [], "a2c": [], "dqn": []}

for algo_name, AlgoCls in ALGORITHMS.items():
    for risk_scale in RISK_SCALES:
        for risk_level in RISK_LEVELS:
            for red_team in RED_TEAM:
                for seed in SEEDS:
                    print(f"Entrenando {algo_name.upper()} | Risk {risk_scale} | Level {risk_level} | RedTeam {red_team} | Seed {seed}")
                    red_team_supported = True
                    try:
<<<<<<< HEAD
                        env = make_vec_env(lambda: SimbiosisGymEnv(risk_scale=risk_scale, red_team=red_team), n_envs=4, seed=seed)
                    except TypeError:
                        print(f"Advertencia: El entorno no soporta red_team. Ejecutando con red_team=False.")
                        try:
                            env = make_vec_env(lambda: SimbiosisGymEnv(risk_scale=risk_scale, red_team=False), n_envs=4, seed=seed)
                            red_team_supported = False
                        except TypeError:
                            env = make_vec_env(lambda: SimbiosisGymEnv(risk_scale=risk_scale), n_envs=4, seed=seed)
                            red_team_supported = False
=======
                        env = make_vec_env(lambda: SimbiosisGymEnv(risk_scale=risk_scale, risk_level=risk_level, red_team=red_team), n_envs=4, seed=seed)
                    except TypeError:
                        print(f"Advertencia: El entorno no soporta red_team. Ejecutando con red_team=False.")
                        env = make_vec_env(lambda: SimbiosisGymEnv(risk_scale=risk_scale, risk_level=risk_level, red_team=False), n_envs=4, seed=seed)
                        red_team_supported = False
>>>>>>> 81a1f5f (Actualización tras Experimento 2: resultados consolidados, notebook robusto, documentación mejorada y nuevas publicaciones.)
                    model = AlgoCls("MlpPolicy", env, verbose=0, seed=seed)
                    model.learn(total_timesteps=TOTAL_TIMESTEPS)

                    # Evaluación determinista
                    try:
<<<<<<< HEAD
                        eval_env = SimbiosisGymEnv(risk_scale=risk_scale, red_team=red_team)
                    except TypeError:
                        try:
                            eval_env = SimbiosisGymEnv(risk_scale=risk_scale, red_team=False)
                            red_team_supported = False
                        except TypeError:
                            eval_env = SimbiosisGymEnv(risk_scale=risk_scale)
                            red_team_supported = False
=======
                        eval_env = SimbiosisGymEnv(risk_scale=risk_scale, risk_level=risk_level, red_team=red_team)
                    except TypeError:
                        eval_env = SimbiosisGymEnv(risk_scale=risk_scale, risk_level=risk_level, red_team=False)
                        red_team_supported = False
>>>>>>> 81a1f5f (Actualización tras Experimento 2: resultados consolidados, notebook robusto, documentación mejorada y nuevas publicaciones.)
                    rewards = []
                    pgf_neto_list = []
                    pgf_bruto_list = []
                    pgf_costo_list = []
                    tripwire_count = 0
                    for ep in range(EVAL_EPISODES):
                        obs, _ = eval_env.reset(seed=seed + ep)
                        done = False
                        ep_reward = 0
                        ep_pgf_neto = []
                        ep_pgf_bruto = []
                        ep_pgf_costo = []
                        while not done:
                            action, _ = model.predict(obs, deterministic=True)
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
                    avg_tripwire = tripwire_count / EVAL_EPISODES
<<<<<<< HEAD
                    red_team_value = red_team if red_team_supported else False
                    robustez = np.nan  # Métrica no disponible en la integración SOTA actual
                    flexibilidad = np.nan  # Métrica no disponible en la integración SOTA actual
                    # El campo red_team refleja el valor realmente usado durante la ejecución
                    results_df = pd.DataFrame({
                        "risk_scale": [risk_scale],
                        "risk_level": [risk_level],
                        "red_team": [red_team_value],
                        "seed": [int(seed)],
                        "agent": [f"{algo_name}_sota"],
                        "episodes": [EPISODES],
                        "steps_per_episode": [STEPS_PER_EPISODE],
                        "eval_episodes": [EVAL_EPISODES],
                        "total_timesteps": [TOTAL_TIMESTEPS],
=======
                    # El campo red_team siempre será False y el nombre del archivo lo refleja
                    results_df = pd.DataFrame({
                        "risk_scale": [risk_scale],
                        "risk_level": [risk_level],
                        "red_team": [False],
                        "seed": [seed],
                        "agent": [f"{algo_name}_sota"],
>>>>>>> 81a1f5f (Actualización tras Experimento 2: resultados consolidados, notebook robusto, documentación mejorada y nuevas publicaciones.)
                        "avg_pgf_neto": [np.mean(pgf_neto_list)],
                        "avg_pgf_bruto": [np.mean(pgf_bruto_list)],
                        "avg_pgf_costo": [np.mean(pgf_costo_list)],
                        "avg_tripwire": [avg_tripwire],
                        "avg_reward": [avg_reward],
<<<<<<< HEAD
                        "robustez": [robustez],
                        "flexibilidad": [flexibilidad],
                    })
                    out_csv = (
                        f"{OUTPUT_DIR}{algo_name}/sota_{algo_name}_seed{seed}_risk{risk_scale}"
                        f"_level{risk_level}_red{str(red_team_value).lower()}_episodes{EPISODES}_steps{STEPS_PER_EPISODE}.csv"
                    )
                    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
=======
                    })
                    out_csv = f"{OUTPUT_DIR}sota_{algo_name}_risk{risk_scale}_level{risk_level}_redFalse_seed{seed}_summary.csv"
>>>>>>> 81a1f5f (Actualización tras Experimento 2: resultados consolidados, notebook robusto, documentación mejorada y nuevas publicaciones.)
                    results_df.to_csv(out_csv, index=False)
                    print(f"Guardado: {out_csv}")
                    all_results[algo_name].append(results_df)

# --- Global summaries ---
for algo_name in all_results:
    if all_results[algo_name]:
        global_df = pd.concat(all_results[algo_name], ignore_index=True)
<<<<<<< HEAD
        global_csv = f"{OUTPUT_DIR}{algo_name}/sota_{algo_name}_global_summary.csv"
=======
        global_csv = f"{OUTPUT_DIR}sota_{algo_name}_global_summary.csv"
>>>>>>> 81a1f5f (Actualización tras Experimento 2: resultados consolidados, notebook robusto, documentación mejorada y nuevas publicaciones.)
        global_df.to_csv(global_csv, index=False)
        print(f"Guardado resumen global: {global_csv}")

all_df = pd.concat([pd.concat(all_results[algo], ignore_index=True) for algo in all_results if all_results[algo]], ignore_index=True)
all_df.to_csv(f"{OUTPUT_DIR}sota_all_global_summary.csv", index=False)
print("Guardado resumen global de todos los algoritmos: sota_all_global_summary.csv")

print("Comparación SOTA A2C/DQN completada.")
