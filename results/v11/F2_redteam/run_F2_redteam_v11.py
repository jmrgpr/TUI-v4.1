import os
import sys
import subprocess

# Parametros globales
SEEDS = [42, 101, 13, 7, 99]
GRIDS = [8, 16]


def build_cmd(grid: int, seed: int) -> list[str]:
    return [
        sys.executable,
        "-m",
        "sim.prototipo_rl_simbiosis",
        "--episodes",
        "200",
        "--seed",
        str(seed),
        "--grid_size",
        str(grid),
        "--risk_scale",
        "1.2",
        "--risk_level",
        "high",
        "--red_team",
        "--red_team_prob",
        "0.1",
        "--dqn_control",
        "--pgf_mix",
        "0.2",
        "--output_prefix",
        f"results/v11/F2_redteam/raw/grid{grid}_riskhigh_r1p2_seed{seed}_v11",
    ]


def main() -> int:
    failures = 0
    for grid in GRIDS:
        for seed in SEEDS:
            cmd = build_cmd(grid=grid, seed=seed)
            print(f"\n[DEBUG] Ejecutando en cwd={os.getcwd()}:")
            print(f"[DEBUG] Comando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(f"[DEBUG] Codigo de retorno: {result.returncode}")
            if result.stdout:
                print(f"[STDOUT]\n{result.stdout}")
            if result.stderr:
                print(f"[STDERR]\n{result.stderr}")
            if result.returncode != 0:
                failures += 1
                print(f"[ERROR] El comando fallo para grid={grid}, seed={seed}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

