"""
Oracle de viabilidad: comprueba si el entorno es resoluble con una política
determinista (camino Manhattan + recolección opcional) usando los parámetros
actuales de sim/config.py. No entrena DQN; sólo mide si la economía permite
alcanzar la meta.

Uso:
    python scripts/run_oracle_viability_check.py --grid 6 8 16 --episodes 50

Salidas:
    - Imprime reward medio, success rate y causas de muerte por grid.
    - Sirve como chequeo previo a iterar v10.x/v11: si el oráculo no puede,
      ningún DQN lo hará con la economía actual.
"""

import argparse
from pathlib import Path
import numpy as np

import sys
import os

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from sim.environment_v2 import ResourceDensityEnv  # noqa: E402
import sim.config as cfg  # noqa: E402


def manhattan_path(size):
    """Camino Manhattan simple de (0,0) a (n-1,n-1)."""
    path = []
    for _ in range(size - 1):
        path.append("right")
    for _ in range(size - 1):
        path.append("down")
    return path


def run_oracle(env, episodes, collect_resource_step=None):
    """Ejecuta episodios siguiendo un camino fijo (opcional desvío a recurso)."""
    rewards = []
    successes = 0
    starvation = 0
    tripwire_hits = 0
    max_steps_used = []

    base_path = manhattan_path(env.size)

    for ep in range(episodes):
        state = env.reset()
        done = False
        ep_reward = 0.0
        steps = 0

        # Copia del path; si se pide desvío se inserta en caliente.
        path = list(base_path)

        while not done and steps < env.max_steps:
            # Si se pidió desvío a recurso en un paso concreto, intenta mover derecha si es válido
            if collect_resource_step is not None and steps == collect_resource_step:
                # Inserta un pequeño zig-zag para potencial recolección
                path.insert(steps, "down")

            action = path[steps] if steps < len(path) else "right"
            _, reward, done, info = env.step(action)
            ep_reward += reward
            steps += 1

            if info.get("starvation"):
                starvation += 1
            if info.get("tripwire"):
                tripwire_hits += 1

            if done and info.get("goal_reached"):
                successes += 1

        rewards.append(ep_reward)
        max_steps_used.append(steps)

    return {
        "success_rate": successes / episodes,
        "reward_mean": float(np.mean(rewards)),
        "reward_std": float(np.std(rewards)),
        "starvation_rate": starvation / episodes,
        "tripwire_hits": tripwire_hits / episodes,
        "steps_mean": float(np.mean(max_steps_used)),
    }


def main():
    parser = argparse.ArgumentParser(description="Oracle de viabilidad (camino fijo).")
    parser.add_argument("--grid", type=int, nargs="+", default=[6, 8],
                        help="Tamaños de grid a probar (e.g., 6 8 16)")
    parser.add_argument("--episodes", type=int, default=50,
                        help="Episodios por grid")
    parser.add_argument("--initial_resources", type=float, help="Override balance inicial")
    parser.add_argument("--step_cost", type=float, help="Override step_cost")
    parser.add_argument("--spawn_rate", type=float, help="Override spawn_rate")
    parser.add_argument("--goal_reward", type=float, help="Override goal_reward")
    parser.add_argument("--penalty_low", type=float, help="Override penalty low resources")
    parser.add_argument("--threshold_low", type=float, help="Override threshold low resources")
    parser.add_argument("--max_steps_multiplier", type=float, default=3.0,
                        help="Multiplicador de pasos vs Manhattan (default 3.0)")
    args = parser.parse_args()

    print("=" * 70)
    print("ORÁCULO DE VIABILIDAD (sin aprendizaje)")
    print("=" * 70)
    goal_reward = args.goal_reward if args.goal_reward is not None else getattr(cfg, "ENV_GOAL_REWARD", 0.0)
    step_cost = args.step_cost if args.step_cost is not None else getattr(cfg, "ENV_STEP_COST", -0.25)
    spawn_rate = args.spawn_rate if args.spawn_rate is not None else getattr(cfg, "ENV_RESOURCE_SPAWN_RATE", 0.3)
    penalty_low = args.penalty_low if args.penalty_low is not None else getattr(cfg, "ENV_PENALTY_LOW_RESOURCES", -1.0)
    threshold_low = args.threshold_low if args.threshold_low is not None else getattr(cfg, "ENV_RESOURCE_THRESHOLD_LOW", 2.0)
    init_res = args.initial_resources if args.initial_resources is not None else getattr(cfg, "ENV_INITIAL_RESOURCES", 5.0)

    print(f"Usando overrides: goal_reward={goal_reward}, step_cost={step_cost}, spawn_rate={spawn_rate}, "
          f"penalty_low={penalty_low}, threshold_low={threshold_low}, initial_resources={init_res}, "
          f"max_steps_multiplier={args.max_steps_multiplier}")
    print(f"Episodios por grid: {args.episodes}")

    for g in args.grid:
        multiplier = args.max_steps_multiplier
        manhattan = (g - 1) * 2
        max_steps = int(manhattan * multiplier)

        env = ResourceDensityEnv(
            size=g,
            initial_resources=init_res,
            step_cost=step_cost,
            resource_reward=getattr(cfg, "ENV_RESOURCE_REWARD", 0.75),
            resource_spawn_rate=spawn_rate,
            max_steps_multiplier=multiplier,
        )
        # Aplicar overrides de thresholds/penalties en runtime
        env.resource_reward = goal_reward  # goal_reward se suma aparte en step; aquí mantenemos reward de recurso
        cfg.ENV_GOAL_REWARD = goal_reward
        cfg.ENV_PENALTY_LOW_RESOURCES = penalty_low
        cfg.ENV_RESOURCE_THRESHOLD_LOW = threshold_low

        print(f"\n--- Grid {g}x{g} (Manhattan={manhattan}, max_steps={max_steps}) ---")
        stats = run_oracle(env, args.episodes)
        print(f"Success: {stats['success_rate']*100:.1f}% | "
              f"Reward: {stats['reward_mean']:.2f} ± {stats['reward_std']:.2f} | "
              f"Steps: {stats['steps_mean']:.1f} | "
              f"Starvation: {stats['starvation_rate']*100:.1f}% | "
              f"Tripwires/ep: {stats['tripwire_hits']:.2f}")

        if stats["success_rate"] == 0:
            print("⚠️  Oráculo NO alcanza la meta. Economía/pasos podrían ser inviables.")
        else:
            print("✅ Oráculo alcanza la meta; si DQN falla, es problema de aprendizaje.")


if __name__ == "__main__":
    main()
