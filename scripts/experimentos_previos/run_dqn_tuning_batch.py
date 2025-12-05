"""
Script batch para tuning de DQN (EXP02–EXP06)
-------------------------------------------------
Ejecuta secuencialmente los experimentos tuning de DQN-Control en el entorno easy,
guardando los resultados y asegurando la trazabilidad de hiperparámetros.

- EXP02: Learning Rate bajo
- EXP03: Learning Rate aún más bajo
- EXP04: Gamma reducido
- EXP05: Epsilon inicial alto y decaimiento lento
- EXP06: Epsilon inicial bajo y decaimiento rápido

Todos los comandos y parámetros están documentados en results/smoke_test/README.md.

Uso:
    python scripts/run_dqn_tuning_batch.py

Requiere: Tener sim/prototipo_rl_simbiosis.py accesible y dependencias instaladas.
"""
import subprocess
import sys
from datetime import datetime

# Configuración general
EPISODES = 500
SEED = 42
RISK_SCALE = 0.5
OUTPUT_DIR = "results/smoke_test/"
BASE_CMD = [sys.executable, "sim/prototipo_rl_simbiosis.py", "--episodes", str(EPISODES), "--seed", str(SEED), "--risk_scale", str(RISK_SCALE), "--dqn_control", "--lambda_gaming", "0.0"]

# Experimentos tuning DQN
EXPERIMENTS = [
    {
        "name": "EXP02 – Learning Rate bajo",
        "output": f"{OUTPUT_DIR}dqn_xy_lr5e4",
        "params": ["--learning_rate", "0.0005"]
    },
    {
        "name": "EXP03 – Learning Rate aún más bajo",
        "output": f"{OUTPUT_DIR}dqn_xy_lr1e4",
        "params": ["--learning_rate", "0.0001"]
    },
    {
        "name": "EXP04 – Gamma reducido",
        "output": f"{OUTPUT_DIR}dqn_xy_gamma095",
        "params": ["--gamma", "0.95"]
    },
    {
        "name": "EXP05 – Epsilon inicial alto y decaimiento lento",
        "output": f"{OUTPUT_DIR}dqn_xy_eps1_decay",
        "params": ["--epsilon", "1.0", "--epsilon_decay", "0.999", "--epsilon_end", "0.1"]
    },
    {
        "name": "EXP06 – Epsilon inicial bajo y decaimiento rápido",
        "output": f"{OUTPUT_DIR}dqn_xy_eps01_decay",
        "params": ["--epsilon", "0.1", "--epsilon_decay", "0.95", "--epsilon_end", "0.01"]
    },
]

def run_experiment(exp):
    """
    Ejecuta un experimento de tuning DQN y guarda el log.
    """
    cmd = BASE_CMD + ["--output_prefix", exp["output"]] + exp["params"]
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ejecutando: {exp['name']}")
    print("Comando:", " ".join(cmd))
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("\n--- STDOUT ---\n", result.stdout)
        print("\n--- STDERR ---\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error en {exp['name']}:", e)
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)

def main():
    print("\nBatch tuning DQN (EXP02–EXP06)")
    print("Todos los hiperparámetros y resultados se guardan en los JSON/CSV de salida.")
    for exp in EXPERIMENTS:
        run_experiment(exp)
    print("\nBatch tuning finalizado. Verifica los outputs en:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
