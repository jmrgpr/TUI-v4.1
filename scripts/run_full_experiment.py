"""
Pipeline experimental automatizado TUI + PGF vs SOTA.
Ejecución en serie de:
- Barridos PGF (default y tuning) para seeds 42/123/456.
- Re-run de robustez (500 episodios) con la mejor config PGF.
- Comparativo SOTA (run_sota_comparison.py).
- Consolidación de resultados (consolidate_results.py).
"""

import subprocess
import time
from pathlib import Path

# Configuración principal
seeds = [42, 123, 456]
episodes_default = 200
episodes_robust = 500
pgf_tuning = {"kappa": 2.0, "lambda": 0.05, "mix": 0.8}

# Comandos base
def_cmd = (
    "python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes {episodes} --seed {seed} "
    "--output_prefix results/sweep/fase2/seed{seed}/sweep_default --dqn_control"
)
tune_cmd = (
    "python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes {episodes} --seed {seed} "
    "--pgf_kappa {kappa} --pgf_lambda {lambda_} --pgf_mix {mix} "
    "--output_prefix results/sweep/fase2/seed{seed}/sweep_tuning --dqn_control"
)
sota_cmd = "python run_sota_comparison.py"
consolidate_cmd = "python scripts/consolidate_results.py"


def ensure_output_dir(cmd: str) -> None:
    """Crea la carpeta de salida si se usa --output_prefix."""
    parts = cmd.split()
    for i, part in enumerate(parts):
        if part.startswith("--output_prefix"):
            prefix = part.split("=")[-1] if "=" in part else parts[i + 1]
            Path(prefix).parent.mkdir(parents=True, exist_ok=True)
            break


def run(cmd: str, log_file: Path | None = None) -> None:
    """Ejecuta un comando y registra resultado; continúa aunque falle."""
    ensure_output_dir(cmd)
    print(f"\nEjecutando / Running: {cmd}")
    start = time.time()
    result = subprocess.run(cmd, shell=True)
    elapsed = time.time() - start
    msg = f"[OK] {cmd} ({elapsed:.1f}s)" if result.returncode == 0 else f"[ERROR] {cmd}"
    print(msg)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    if result.returncode != 0:
        print("Advertencia: el comando falló, se registra y continúa.")


def main() -> None:
    log_path = Path("results/experiment_log.txt")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("# Log de ejecucion experimental\n", encoding="utf-8")

    # 1. Barridos default PGF
    for seed in seeds:
        run(def_cmd.format(episodes=episodes_default, seed=seed), log_file=log_path)

    # 2. Barridos tuning PGF
    for seed in seeds:
        run(
            tune_cmd.format(
                episodes=episodes_default,
                seed=seed,
                kappa=pgf_tuning["kappa"],
                lambda_=pgf_tuning["lambda"],
                mix=pgf_tuning["mix"],
            ),
            log_file=log_path,
        )

    # 3. Robustez: mejor config con 500 episodios
    run(
        tune_cmd.format(
            episodes=episodes_robust,
            seed=seeds[0],
            kappa=pgf_tuning["kappa"],
            lambda_=pgf_tuning["lambda"],
            mix=pgf_tuning["mix"],
        ),
        log_file=log_path,
    )

    # 4. Comparativo SOTA
    run(sota_cmd, log_file=log_path)

    # 5. Consolidar resultados
    run(consolidate_cmd, log_file=log_path)

    print(
        "\nPipeline experimental completo. Revisa results/master_results.csv "
        "y results/experiment_log.txt para análisis y trazabilidad.\n"
        "Full experimental pipeline complete. Check results/master_results.csv "
        "and results/experiment_log.txt for analysis and traceability."
    )


if __name__ == "__main__":
    main()
