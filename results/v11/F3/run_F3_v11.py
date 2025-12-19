import argparse
import os
import subprocess
import sys
from pathlib import Path

SEEDS_DEFAULT = [42, 101, 13, 7, 99]
GRIDS_DEFAULT = [8, 16]
PGF_MIX_DEFAULT = [0.0, 0.2]


def mix_to_token(value: float) -> str:
    v = float(value)
    # token estable: 0.2 -> m0p2, 0.0 -> m0p0, 0.35 -> m0p35
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    if "." not in s:
        return f"m{s}p0"
    a, b = s.split(".", 1)
    return f"m{a}p{b}"


def build_cmd(
    *,
    condition: str,
    grid: int,
    seed: int,
    pgf_mix: float,
    episodes: int,
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
        "--dqn_control",
        "--pgf_mix",
        str(pgf_mix),
        "--output_prefix",
        output_prefix,
    ]
    if condition == "F2_redteam":
        cmd.extend(["--red_team", "--red_team_prob", "0.1"])
    return cmd


def iter_jobs(seeds: list[int], grids: list[int], pgf_mix_values: list[float], episodes: int) -> list[dict]:
    jobs = []
    for condition in ("F1_highrisk", "F2_redteam"):
        for grid in grids:
            for seed in seeds:
                for mix in pgf_mix_values:
                    mix_token = mix_to_token(mix)
                    cond_token = "f1" if condition == "F1_highrisk" else "f2rt0p1"
                    out_dir = Path("results/v11/F3/raw") / condition
                    out_dir.mkdir(parents=True, exist_ok=True)
                    stem = f"grid{grid}_riskhigh_r1p2_{cond_token}_seed{seed}_{mix_token}_v11"
                    output_prefix = (out_dir / stem).as_posix()
                    jobs.append(
                        {
                            "condition": condition,
                            "grid": grid,
                            "seed": seed,
                            "pgf_mix": float(mix),
                            "episodes": episodes,
                            "output_prefix": output_prefix,
                        }
                    )
    return jobs


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner F3 (v11): ejecuta F1_highrisk y F2_redteam con pgf_mix {0.0,0.2}.")
    parser.add_argument("--episodes", type=int, default=200)
    parser.add_argument("--seeds", nargs="*", type=int, default=SEEDS_DEFAULT)
    parser.add_argument("--grids", nargs="*", type=int, default=GRIDS_DEFAULT)
    parser.add_argument("--pgf-mix", nargs="*", type=float, default=PGF_MIX_DEFAULT)
    parser.add_argument("--dry-run", action="store_true", help="Solo imprime comandos (no ejecuta).")
    args = parser.parse_args()

    jobs = iter_jobs(seeds=args.seeds, grids=args.grids, pgf_mix_values=args.pgf_mix, episodes=args.episodes)
    failures = 0
    for idx, job in enumerate(jobs, start=1):
        cmd = build_cmd(
            condition=job["condition"],
            grid=job["grid"],
            seed=job["seed"],
            pgf_mix=job["pgf_mix"],
            episodes=job["episodes"],
            output_prefix=job["output_prefix"],
        )
        print(f"\n[{idx}/{len(jobs)}] {job['condition']} grid={job['grid']} seed={job['seed']} pgf_mix={job['pgf_mix']}")
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
        print(f"\nF3 completado con fallos: {failures}/{len(jobs)}", file=sys.stderr)
        return 1
    print(f"\nF3 completado OK: {len(jobs)}/{len(jobs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

