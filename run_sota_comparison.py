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
    Entrena un agente PPO (State-of-the-Art) y guarda resultados compatibles con Fase 2.
    """
    print(f"=== Entrenando PPO SOTA en Risk Scale {risk_scale} ===")

    # 1. Entorno vectorizado
    env = make_vec_env(lambda: SimbiosisGymEnv(risk_scale=risk_scale), n_envs=4, seed=seed)

    # 2. Configuración PPO estándar
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
        verbose=0, # Menos ruido en consola
        seed=seed
    )

    # 3. Entrenar
    model.learn(total_timesteps=total_timesteps)

    # 4. Evaluación Final (Rigurosa)
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
    print("\n✅ Comparación SOTA completada. Archivo guardado: results/sota_ppo_global_summary.csv")