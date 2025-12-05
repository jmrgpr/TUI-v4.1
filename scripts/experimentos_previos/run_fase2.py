import subprocess
import os

def run_fase2_experiments():
    """
    Lanza la serie de experimentos para la Fase 2 del proyecto TUI.
    """
    print("Iniciando la ejecución de experimentos de la Fase 2...")

    # Parámetros de la experimentación
    episodes = 1000
    seeds = [42, 123, 456, 789]
    output_dir = "results/fase2"
    os.makedirs(output_dir, exist_ok=True)

    for seed in seeds:
        print(f"\n===== LANZANDO EXPERIMENTO CON SEMILLA: {seed} =====")
        output_prefix = os.path.join(output_dir, f"seed_{seed}")
        command = [
            "python",
            "sim/prototipo_rl_simbiosis.py",
            "--episodes", str(episodes),
            "--seed", str(seed),
            "--risk_sweep",
            "--dqn_control",
            "--output_prefix", output_prefix
        ]
        try:
            subprocess.run(command, check=True)
            print(f"===== EXPERIMENTO CON SEMILLA {seed} COMPLETADO =====\n")
        except subprocess.CalledProcessError as e:
            print(f"ERROR en el experimento con semilla {seed}: {e}")
            break
    print("Todos los experimentos de la Fase 2 han finalizado.")

if __name__ == "__main__":
    run_fase2_experiments()
