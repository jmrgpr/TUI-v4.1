"""
Oráculo con PROPUESTA USUARIO: balance 8.0, step_cost -0.15, penalty_low -0.5
Valida empíricamente si mejora viabilidad 16×16 manteniendo 6×6.

Uso:
    python scripts/run_oracle_viability_proposed.py --grid 6 8 16 --episodes 50
"""

import argparse
from pathlib import Path
import numpy as np
import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from sim.environment_v2 import ResourceDensityEnv  # noqa: E402


def manhattan_path(size):
    """Camino Manhattan simple de (0,0) a (n-1,n-1)."""
    path = []
    for _ in range(size - 1):
        path.append("right")
    for _ in range(size - 1):
        path.append("down")
    return path


def run_oracle(env, episodes):
    """Ejecuta episodios siguiendo camino Manhattan óptimo."""
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

        path = list(base_path)

        while not done and steps < env.max_steps:
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
    parser = argparse.ArgumentParser(description="Oráculo config PROPUESTA.")
    parser.add_argument("--grid", type=int, nargs="+", default=[6, 8, 16],
                        help="Tamaños de grid (e.g., 6 8 16)")
    parser.add_argument("--episodes", type=int, default=50,
                        help="Episodios por grid")
    args = parser.parse_args()

    # PROPUESTA USUARIO
    PROPOSED_CONFIG = {
        "initial_resources": 8.0,       # v10.9: 5.0 → 8.0 (+60%)
        "step_cost": -0.15,             # v10.9: -0.25 → -0.15 (-40% fricción)
        "penalty_low": -0.5,            # v10.9: -1.0 → -0.5 (-50% castigo)
        "threshold_low": 1.0,           # Mantener v10.9
        "goal_reward": 20.0,            # Mantener v10.9
        "spawn_rate": 0.40,             # Mantener v10.9
        "max_steps_multiplier": 3.0     # 3.0 para NO timeout antes que autonomía
    }

    print("=" * 70)
    print("ORÁCULO CON PROPUESTA USUARIO")
    print("=" * 70)
    print(f"Config PROPUESTA:")
    print(f"  initial_resources: {PROPOSED_CONFIG['initial_resources']} (v10.9: 5.0)")
    print(f"  step_cost: {PROPOSED_CONFIG['step_cost']} (v10.9: -0.25)")
    print(f"  penalty_low: {PROPOSED_CONFIG['penalty_low']} (v10.9: -1.0)")
    print(f"  threshold_low: {PROPOSED_CONFIG['threshold_low']}")
    print(f"  goal_reward: {PROPOSED_CONFIG['goal_reward']}")
    print(f"  spawn_rate: {PROPOSED_CONFIG['spawn_rate']}")
    print(f"Episodios por grid: {args.episodes}\n")

    # Autonomía matemática
    autonomia = PROPOSED_CONFIG["initial_resources"] / abs(PROPOSED_CONFIG["step_cost"])
    print(f"Autonomía matemática: {autonomia:.1f} pasos\n")

    for g in args.grid:
        manhattan = (g - 1) * 2
        max_steps = int(manhattan * PROPOSED_CONFIG["max_steps_multiplier"])

        env = ResourceDensityEnv(
            size=g,
            initial_resources=PROPOSED_CONFIG["initial_resources"],
            step_cost=PROPOSED_CONFIG["step_cost"],
            resource_reward=0.75,
            resource_spawn_rate=PROPOSED_CONFIG["spawn_rate"],
            max_steps_multiplier=PROPOSED_CONFIG["max_steps_multiplier"],
        )

        print(f"--- Grid {g}×{g} (Manhattan={manhattan}, max_steps={max_steps}) ---")
        margen_matematico = autonomia - manhattan
        print(f"   Autonomía vs Manhattan: {autonomia:.1f} vs {manhattan} = {margen_matematico:+.1f} pasos ({(margen_matematico/manhattan)*100:+.1f}%)")
        
        stats = run_oracle(env, args.episodes)
        print(f"   Success: {stats['success_rate']*100:.1f}% | "
              f"Reward: {stats['reward_mean']:.2f} ± {stats['reward_std']:.2f} | "
              f"Steps: {stats['steps_mean']:.1f} | "
              f"Starvation: {stats['starvation_rate']*100:.1f}% | "
              f"Tripwires/ep: {stats['tripwire_hits']:.2f}\n")

        if stats["success_rate"] == 0:
            print(f"   ❌ INVIABLE: Oráculo no puede ganar con config propuesta.\n")
        elif stats["success_rate"] < 1.0:
            print(f"   ⚠️  MARGINAL: Success {stats['success_rate']*100:.1f}% indica economía justa.\n")
        else:
            print(f"   ✅ VIABLE: Oráculo 100% success, DQN puede aprender.\n")

    print("=" * 70)
    print("VEREDICTO")
    print("=" * 70)
    print("Si oráculo 100% success en TODOS los grids:")
    print("  → Economía VIABLE, problema es EXPLORACIÓN DQN")
    print("  → Implementar como v11 base + curriculum/shaped rewards")
    print("\nSi oráculo falla en 16×16:")
    print("  → Requiere ajuste adicional balance/step_cost")
    print("  → Considerar recursos regenerativos o spawn_rate mayor")


if __name__ == "__main__":
    main()
