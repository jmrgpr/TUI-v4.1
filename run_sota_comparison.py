import os
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
from sim.sota_wrapper import SimbiosisGymEnv
import warnings
warnings.filterwarnings("ignore")

def run_sota_comparison(risk_scale=1.0, total_timesteps=100000, seed=42, output_prefix="results/sota_ppo"):
    """
    Entrena un agente PPO (State-of-the-Art) en el entorno SimbiosisEnv
    y guarda resultados compatibles con el formato de la Fase 2.
    """
    print(f"=== Entrenando PPO SOTA en Risk Scale {risk_scale} ===")

    # 1. Crear entorno vectorizado para entrenamiento eficiente
    env = make_vec_env(lambda: SimbiosisGymEnv(risk_scale=risk_scale), n_envs=4, seed=seed)

    # 2. Configurar PPO con hiperparámetros estándar
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.0,
        verbose=1,
        seed=seed
    )

    # 3. Callback para evaluación periódica
    eval_env = SimbiosisGymEnv(risk_scale=risk_scale)
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=f"{output_prefix}_best_model/",
        log_path=f"{output_prefix}_logs/",
        eval_freq=10000,
        deterministic=True,
        render=False
    )

    # 4. Entrenar el modelo
    model.learn(total_timesteps=total_timesteps, callback=eval_callback)

    # 5. Evaluar el modelo entrenado en múltiples episodios
    print("\n=== Evaluando PPO entrenado ===")
    eval_episodes = 100
    rewards = []
    pgf_neto_list = []
    pgf_bruto_list = []
    pgf_costo_list = []
    tripwire_list = []

    for ep in range(eval_episodes):
        obs, _ = eval_env.reset(seed=seed + ep)
        done = False
        truncated = False
        episode_reward = 0
        episode_pgf_neto = 0
        episode_pgf_bruto = 0
        episode_pgf_costo = 0
        episode_tripwire = 0

        while not (done or truncated):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = eval_env.step(action)
            episode_reward += reward

            # Extraer métricas PGF del info (asumiendo que el wrapper las pasa)
            if 'pgf_neto' in info:
                episode_pgf_neto += info['pgf_neto']
            if 'pgf_bruto' in info:
                episode_pgf_bruto += info['pgf_bruto']
            if 'pgf_costo' in info:
                episode_pgf_costo += info['pgf_costo']
            if 'tripwire' in info:
                episode_tripwire += info['tripwire']

        rewards.append(episode_reward)
        pgf_neto_list.append(episode_pgf_neto)
        pgf_bruto_list.append(episode_pgf_bruto)
        pgf_costo_list.append(episode_pgf_costo)
        tripwire_list.append(episode_tripwire)

    # 6. Calcular promedios
    avg_reward = np.mean(rewards)
    avg_pgf_neto = np.mean(pgf_neto_list)
    avg_pgf_bruto = np.mean(pgf_bruto_list)
    avg_pgf_costo = np.mean(pgf_costo_list)
    avg_tripwire = np.mean(tripwire_list)

    print(".2f")
    print(".4f")
    print(".4f")
    print(".4f")
    print(".4f")
    print(".4f")
    # 7. Guardar resultados en formato compatible con Fase 2
    results_df = pd.DataFrame({
        'risk_scale': [risk_scale],
        'agent': ['ppo_sota'],
        'avg_pgf_neto': [avg_pgf_neto],
        'avg_pgf_bruto': [avg_pgf_bruto],
        'avg_pgf_costo': [avg_pgf_costo],
        'avg_tripwire': [avg_tripwire],
        'avg_reward': [avg_reward]
    })

    output_file = f"{output_prefix}_risk{risk_scale}_summary.csv"
    results_df.to_csv(output_file, index=False)
    print(f"Resultados guardados en: {output_file}")

    # 8. Guardar modelo entrenado
    model.save(f"{output_prefix}_risk{risk_scale}_model")
    print(f"Modelo guardado en: {output_prefix}_risk{risk_scale}_model.zip")

    return results_df

if __name__ == "__main__":
    # Ejecutar comparación SOTA para diferentes niveles de riesgo
    risk_scales = [0.5, 1.0, 1.5, 2.0, 3.0]
    all_results = []

    for risk in risk_scales:
        result = run_sota_comparison(risk_scale=risk, total_timesteps=50000)  # Reducido para prueba rápida
        all_results.append(result)

    # Combinar todos los resultados
    combined_df = pd.concat(all_results, ignore_index=True)
    combined_df.to_csv("results/sota_ppo_global_summary.csv", index=False)
    print("\nResumen global guardado en: results/sota_ppo_global_summary.csv")