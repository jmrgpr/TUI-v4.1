import os
from pathlib import Path

# Parámetros globales
seeds = [42, 101, 13, 7, 99]
grids = [8, 16]
base_cmd = (
    "python -m sim.prototipo_rl_simbiosis "
    "--episodes 200 "
    "--seed {seed} "
    "--grid_size {grid} "
    "--risk_scale 1.2 "
    "--risk_level high "
    "--red_team "
    "--dqn_control "
    "--pgf_mix 0.2 "
    "--output_prefix results/v11/F2_redteam/raw/grid{grid}_riskhigh_r1p2_seed{seed}_v11"
)

def main():
    import subprocess
    for grid in grids:
        for seed in seeds:
            cmd = base_cmd.format(grid=grid, seed=seed)
            print(f"\n[DEBUG] Ejecutando en cwd={os.getcwd()}:")
            print(f"[DEBUG] Comando: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(f"[DEBUG] Código de retorno: {result.returncode}")
            if result.stdout:
                print(f"[STDOUT]\n{result.stdout}")
            if result.stderr:
                print(f"[STDERR]\n{result.stderr}")
            if result.returncode != 0:
                print(f"[ERROR] El comando falló para grid={grid}, seed={seed}")

if __name__ == "__main__":
    main()
