"""
Pipeline experimental automatizado TUI + PGF vs SOTA.
Parametrizable por CLI para evitar hardcoding:
  --seeds 42 123 456
  --episodes_default 200
  --episodes_robust 500
  --pgf_kappa 2.0 --pgf_lambda 0.05 --pgf_mix 0.8
  --output_base results/sweep/fase2
  --stop_on_fail (para abortar en errores)
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", nargs="+", type=int, default=[42, 123, 456], help="Lista de semillas")
    p.add_argument("--episodes_default", type=int, default=200, help="Episodios por barrido")
    p.add_argument("--episodes_robust", type=int, default=500, help="Episodios para rerun de robustez")
    p.add_argument("--pgf_kappa", type=float, default=2.0, help="PGF kappa tuning")
    p.add_argument("--pgf_lambda", type=float, default=0.05, help="PGF lambda tuning")
    p.add_argument("--pgf_mix", type=float, default=0.8, help="PGF mix tuning")
    p.add_argument("--output_base", type=str, default="results/sweep/fase2", help="Base para archivos de salida")
    p.add_argument("--risk_level", type=str, default="low", choices=["low", "high"], help="Nivel de riesgo para intervención")
    p.add_argument("--red_team", action="store_true", help="Activar modo red team/perturbaciones")
    p.add_argument("--sigma_thr", type=float, default=None, help="Umbral de gating por incertidumbre")
    p.add_argument("--gamma_lcb", type=float, default=None, help="Factor prudencial LCB")
    p.add_argument("--lambda_gaming", type=float, default=None, help="Penalización por gaming")
    p.add_argument("--stop_on_fail", action="store_true", help="Abortar pipeline ante un error")
    return p.parse_args()


def ensure_output_dir(cmd: str) -> None:
    parts = cmd.split()
    for i, part in enumerate(parts):
        if part.startswith("--output_prefix"):
            prefix = part.split("=")[-1] if "=" in part else parts[i + 1]
            Path(prefix).parent.mkdir(parents=True, exist_ok=True)
            break


def run(cmd: str, stop_on_fail: bool, log_file: Path | None = None) -> bool:
    ensure_output_dir(cmd)
    print(f"\nEjecutando / Running: {cmd}")
    start = time.time()
    result = subprocess.run(cmd, shell=True)
    elapsed = time.time() - start
    ok = result.returncode == 0
    msg = f"[OK] {cmd} ({elapsed:.1f}s)" if ok else f"[ERROR] {cmd}"
    print(msg)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    if not ok and stop_on_fail:
        sys.exit(result.returncode or 1)
    return ok


def main():
    args = parse_args()

    common_flags = ""
    if args.red_team:
        common_flags += " --red_team"
    if args.sigma_thr is not None:
        common_flags += f" --sigma_thr {args.sigma_thr}"
    if args.gamma_lcb is not None:
        common_flags += f" --gamma_lcb {args.gamma_lcb}"
    if args.lambda_gaming is not None:
        common_flags += f" --lambda_gaming {args.lambda_gaming}"

    def_cmd = (
        "python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes {episodes} --seed {seed} "
        f"--risk_level {args.risk_level}"
        f"{common_flags} "
        f"--output_prefix {args.output_base}/seed{{seed}}/sweep_default --dqn_control"
    )
    tune_cmd = (
        "python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes {episodes} --seed {seed} "
        f"--pgf_kappa {args.pgf_kappa} --pgf_lambda {args.pgf_lambda} --pgf_mix {args.pgf_mix} "
        f"--risk_level {args.risk_level}"
        f"{common_flags} "
        f"--output_prefix {args.output_base}/seed{{seed}}/sweep_tuning --dqn_control"
    )
    tui_cmd = (
        "python sim/prototipo_rl_simbiosis.py --risk_sweep --episodes {episodes} --seed {seed} "
        f"--pgf_kappa {args.pgf_kappa} --pgf_lambda {args.pgf_lambda} --pgf_mix {args.pgf_mix} "
        f"--risk_level {args.risk_level}"
        f"{common_flags} "
        f"--output_prefix {args.output_base}/seed{{seed}}/sweep_tui --tui_only --dqn_control"
    )
    sota_cmd = "python run_sota_comparison.py"
    consolidate_cmd = "python scripts/consolidate_results.py"

    log_path = Path("results/experiment_log.txt")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("# Log de ejecucion experimental\n", encoding="utf-8")

    # Barridos default
    for seed in args.seeds:
        run(def_cmd.format(episodes=args.episodes_default, seed=seed), args.stop_on_fail, log_file=log_path)

    # Barridos tuning
    for seed in args.seeds:
        run(tune_cmd.format(episodes=args.episodes_default, seed=seed), args.stop_on_fail, log_file=log_path)

    # TUI/PGF puro (sin DQN-Control) + variantes previas para comparacion
    for seed in args.seeds:
        run(tui_cmd.format(episodes=args.episodes_default, seed=seed), args.stop_on_fail, log_file=log_path)

    # Robustez (usar primera seed como referencia)
    run(
        tune_cmd.format(episodes=args.episodes_robust, seed=args.seeds[0]),
        args.stop_on_fail,
        log_file=log_path,
    )

    # SOTA
    run(sota_cmd, args.stop_on_fail, log_file=log_path)

    # Consolidar
    run(consolidate_cmd, args.stop_on_fail, log_file=log_path)

    print(
        "\nPipeline experimental completo. Revisa results/master_results.csv "
        "y results/experiment_log.txt para analisis y trazabilidad."
    )


if __name__ == "__main__":
    main()
