#!/usr/bin/env python3
"""
Placeholder para Experimento 3: búsqueda de hiperparámetros PGF en TUI.

Idea:
- Mantener seeds/risks/episodes iguales a Exp1/Exp2.
- Barrer kappa, lambda, mix en mallas discretas.
- Generar CSV en results/exp_tui_pgf_search_v3/results/ con nombres consistentes.
- Llamar al consolidado y producir un ranking por safety_adj_reward / sau_beta2.

Nota: no ejecuta nada aún; definir grids y lanzar cuando se dé luz verde.
"""

import itertools
import subprocess
from pathlib import Path

# Matriz fija para comparabilidad
SEEDS = [42, 123, 456]
RISKS = [0.5, 1.0, 1.5, 2.0, 3.0]
EPISODES = 200

# Grids (ajustar antes de correr)
KAPPAS = [0.5, 1.0, 1.5, 2.0]
LAMBDAS = [0.05, 0.1, 0.2]
MIXES = [0.3, 0.5, 0.8]

OUTPUT_BASE = Path("results/exp_tui_pgf_search_v3/results")
LOG_FILE = Path("results/exp_tui_pgf_search_v3/search_log.txt")


def format_cmd(seed, risk, kappa, lambd, mix):
    out_dir = OUTPUT_BASE / f"seed{seed}" / f"k{float(kappa)}_l{float(lambd)}_m{float(mix)}"
    out_dir.mkdir(parents=True, exist_ok=True)
    return (
        f"python sim/prototipo_rl_simbiosis.py "
        f"--episodes {EPISODES} "
        f"--seed {seed} "
        f"--risk_scale {risk} "
        f"--pgf_kappa {kappa} "
        f"--pgf_lambda {lambd} "
        f"--pgf_mix {mix} "
        f"--output_prefix {out_dir}/risk{risk}"
    )


def main():  # pragma: no cover
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    cmds = []
    for seed, risk, kappa, lambd, mix in itertools.product(SEEDS, RISKS, KAPPAS, LAMBDAS, MIXES):
        cmds.append(format_cmd(seed, risk, kappa, lambd, mix))

    print(f"Total comandos a ejecutar: {len(cmds)}")
    print("Ejemplo:", cmds[0] if cmds else "N/A")
    print("Este script es un placeholder; ejecutar manualmente o envolver con parallel si se aprueba.")
    LOG_FILE.write_text("# run_search_pgf.py placeholder\n# Define grids y lanza cuando estés listo.\n")

    # Descomenta para ejecutar secuencial (pesado):
    # for cmd in cmds:
    #     res = subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    raise SystemExit(main())

