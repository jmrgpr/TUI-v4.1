import argparse
import os
import subprocess
import sys
from pathlib import Path

SEEDS_DEFAULT = [42, 101, 13, 7, 99]
GRIDS_DEFAULT = [8, 16]
PGF_MIX_DEFAULT = [0.0, 0.2]

# Preregistro F4 (Adenda 01): stakes run-level con budget B.
STAKES = {
    "stkL": "low",
    "stkH": "high",
}
BUDGET_DEFAULT = 3


def mix_to_token(value: float) -> str:
    v = float(value)
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    if "." not in s:
        return f"m{s}p0"
    a, b = s.split(".", 1)
    return f"m{a}p{b}"


def build_cmd(
    *,
    grid: int,
    seed: int,
    pgf_mix: float,
    episodes: int,
    stakes_mode: str,
    budget: int,
    output_prefix: str,
) -> list[str]:
    cmd = [
        sys.executable,
        "-m",
        "sim.prototipo_rl_simbiosis",
        "--episodes",
        str(episodes),
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
        "--pgf_mix",
        str(pgf_mix),
        "--stakes",
        str(stakes_mode),
        "--budget",
        str(budget),
        "--output_prefix",
        output_prefix,
    ]
    return cmd


def iter_jobs(seeds: list[int], grids: list[int], pgf_mix_values: list[float], episodes: int, budget: int) -> list[dict]:
    jobs = []
    for stakes_token, stakes_mode in STAKES.items():
        for grid in grids:
            for seed in seeds:
                for mix in pgf_mix_values:
                    mix_token = mix_to_token(mix)
                    out_dir = Path("results/v11/F4/raw/F2_redteam") / stakes_token
                    out_dir.mkdir(parents=True, exist_ok=True)
                    stem = f"grid{grid}_riskhigh_r1p2_f2rt0p1_seed{seed}_{stakes_token}_b{budget}_{mix_token}_v11"
                    output_prefix = (out_dir / stem).as_posix()
                    jobs.append(
                        {
                            "grid": grid,
                            "seed": seed,
                            "pgf_mix": float(mix),
                            "episodes": episodes,
                            "stakes_token": stakes_token,
                            "stakes_mode": str(stakes_mode),
                            "budget": int(budget),
                            "output_prefix": output_prefix,
                        }
                    )
    return jobs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Runner F4 (v11): F2_redteam fijo, stakes {stkL,stkH} con budget B + pgf_mix {0.0,0.2}."
    )
    parser.add_argument("--episodes", type=int, default=200)
    parser.add_argument("--seeds", nargs="*", type=int, default=SEEDS_DEFAULT)
    parser.add_argument("--grids", nargs="*", type=int, default=GRIDS_DEFAULT)
    parser.add_argument("--pgf-mix", nargs="*", type=float, default=PGF_MIX_DEFAULT)
    parser.add_argument("--budget", type=int, default=BUDGET_DEFAULT, help="Budget B (catástrofes) para high-stakes (y referencia en low-stakes).")
    parser.add_argument("--dry-run", action="store_true", help="Solo imprime comandos (no ejecuta).")
    args = parser.parse_args()

    jobs = iter_jobs(seeds=args.seeds, grids=args.grids, pgf_mix_values=args.pgf_mix, episodes=args.episodes, budget=args.budget)
    failures = 0
    for idx, job in enumerate(jobs, start=1):
        cmd = build_cmd(
            grid=job["grid"],
            seed=job["seed"],
            pgf_mix=job["pgf_mix"],
            episodes=job["episodes"],
            stakes_mode=job["stakes_mode"],
            budget=job["budget"],
            output_prefix=job["output_prefix"],
        )
        print(
            f"\n[{idx}/{len(jobs)}] F2_redteam grid={job['grid']} seed={job['seed']} "
            f"stakes={job['stakes_token']} budget={job['budget']} pgf_mix={job['pgf_mix']}"
        )
        print(f"[CMD] {' '.join(cmd)}")
        if args.dry_run:
            continue
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.returncode != 0:
            failures += 1
            print(f"[ERROR] Fallo: {job}", file=sys.stderr)

    if failures:
        print(f"\nF4 completado con fallos: {failures}/{len(jobs)}", file=sys.stderr)
        return 1
    print(f"\nF4 completado OK: {len(jobs)}/{len(jobs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
