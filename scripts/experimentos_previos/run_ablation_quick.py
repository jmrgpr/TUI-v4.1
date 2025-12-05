#!/usr/bin/env python3
"""
Runner mínimo para la ablación TUI (only / PGF light / PGF heavy) con la misma
matriz de seeds/risks/episodios que el experimento 1. Genera CSVs en
results/sweep/fase2_instrumented y luego llama al consolidado.

Uso:
    python scripts/run_ablation_quick.py          # full (3 seeds × 5 risks)
    python scripts/run_ablation_quick.py --test   # rápido (1 seed × 2 risks)
"""

import subprocess
import sys
import time
from pathlib import Path

SEEDS = [42, 123, 456]
RISKS = [0.5, 1.0, 1.5, 2.0, 3.0]
EPISODES = 200

# Variantes de TUI
TUI_CONFIGS = {
    "tui_only": {"kappa": 0.0, "lambda": 0.0, "mix": 0.0},
    "tui_pgf_light": {"kappa": 1.0, "lambda": 0.1, "mix": 0.5},
    "tui_pgf_heavy": {"kappa": 2.0, "lambda": 0.05, "mix": 0.8},
}

OUTPUT_BASE = Path("results/sweep/fase2_instrumented")
LOG_FILE = Path("results/experiment2_log.txt")


def run_cmd(cmd: str) -> bool:
    """Ejecuta comando (string) y loguea salida/estado."""
    print("\n" + "=" * 70)
    print(f"EJECUTANDO: {cmd}")
    print("=" * 70)
    start = time.time()
    result = subprocess.run(cmd, shell=True)
    elapsed = time.time() - start
    status = "OK" if result.returncode == 0 else "FAILED"
    msg = f"[{status}] {cmd} ({elapsed:.1f}s)"
    print(msg)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    return result.returncode == 0


def main():
    test_mode = "--test" in sys.argv
    seeds = [SEEDS[0]] if test_mode else SEEDS
    risks = RISKS[:2] if test_mode else RISKS

    LOG_FILE.write_text(f"# Experimento 2 - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    total = len(seeds) * len(risks) * len(TUI_CONFIGS)
    success = 0
    failed = []

    print("=" * 70)
    print("EXPERIMENTO 2: ABLACIÓN TUI + PGF")
    print("=" * 70)
    print(f"Modo: {'TEST (1 seed × 2 risks)' if test_mode else 'FULL (3 seeds × 5 risks)'}")
    print(f"Seeds: {seeds}")
    print(f"Risks: {risks}")
    print(f"Episodes: {EPISODES}")
    print(f"Configs: {list(TUI_CONFIGS.keys())}")
    print(f"Total experimentos: {total}")
    print("=" * 70)

    for config_name, params in TUI_CONFIGS.items():
        print("\n" + "#" * 70)
        print(f"CONFIG: {config_name} | kappa={params['kappa']}, lambda={params['lambda']}, mix={params['mix']}")
        print("#" * 70)
        for seed in seeds:
            for risk in risks:
                output_dir = OUTPUT_BASE / f"seed{seed}" / config_name
                output_dir.mkdir(parents=True, exist_ok=True)
                # CSV tendrá prefijo consistente para que el consolidado extraiga metadatos
                cmd = (
                    f"python sim/prototipo_rl_simbiosis.py "
                    f"--episodes {EPISODES} "
                    f"--seed {seed} "
                    f"--risk_scale {risk} "
                    f"--pgf_kappa {params['kappa']} "
                    f"--pgf_lambda {params['lambda']} "
                    f"--pgf_mix {params['mix']} "
                    f"--output_prefix {output_dir}/risk{risk}"
                )
                if run_cmd(cmd):
                    success += 1
                else:
                    failed.append((config_name, seed, risk))

    print("\n" + "=" * 70)
    print("CONSOLIDANDO RESULTADOS")
    print("=" * 70)
    run_cmd("python scripts/consolidate_results.py")

    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    print(f"Exitosos: {success}/{total}")
    print(f"Fallidos: {len(failed)}")
    if failed:
        print("\nExperimentos fallidos:")
        for cfg, seed, risk in failed:
            print(f"  - {cfg} (seed={seed}, risk={risk})")

    print("\nSiguiente paso: revisar results/master_results.csv y ejecutar analysis_phase2.ipynb")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
