import argparse
import os
import subprocess
import sys
from pathlib import Path

# F8: replicación quirúrgica (H1-only) para cerrar CFR sin Holm.

BASE_SEEDS_DEFAULT = list(range(601, 621))  # 20 seeds -> n=40 runs por grupo (2 grids)
EXPAND_SEEDS_DEFAULT = list(range(621, 631))  # +10 seeds -> +20 runs por grupo

GRIDS_DEFAULT = [8, 16]
PGF_MIX_DEFAULT = [0.0]  # por defecto: solo S0-H vs C-H (H1-only)

STAKES_TOKEN = "stkH"
STAKES_MODE = "high"

RISK_SCALE = 1.2
RISK_LEVEL = "high"
RED_TEAM_PROB_DEFAULT = 0.03

BUDGET_BSTAR = 40
EPISODES_DEFAULT = 200

RAW_DIR = Path("results/v11/F8/raw")


def mix_to_token(value: float) -> str:
    v = float(value)
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    if "." not in s:
        return f"m{s}p0"
    a, b = s.split(".", 1)
    return f"m{a}p{b}"


def prob_to_token(value: float) -> str:
    v = float(value)
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    if "." not in s:
        return f"rt{s}p0"
    a, b = s.split(".", 1)
    return f"rt{a}p{b}"


def build_cmd(
    *,
    grid: int,
    seed: int,
    pgf_mix: float,
    episodes: int,
    red_team_prob: float,
    output_prefix: str,
) -> list[str]:
    return [
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
        str(RISK_SCALE),
        "--risk_level",
        str(RISK_LEVEL),
        "--red_team",
        "--red_team_prob",
        str(red_team_prob),
        "--pgf_mix",
        str(pgf_mix),
        "--stakes",
        STAKES_MODE,
        "--budget",
        str(BUDGET_BSTAR),
        "--output_prefix",
        output_prefix,
    ]


def iter_jobs(*, seeds: list[int], grids: list[int], pgf_mix_values: list[float], episodes: int, red_team_prob: float) -> list[dict]:
    jobs: list[dict] = []
    rt_token = prob_to_token(red_team_prob)
    out_dir = RAW_DIR / "F2_redteam" / STAKES_TOKEN / rt_token
    out_dir.mkdir(parents=True, exist_ok=True)
    for grid in grids:
        for seed in seeds:
            for mix in pgf_mix_values:
                mix_token = mix_to_token(mix)
                stem = (
                    f"grid{grid}_riskhigh_r1p2_f2{rt_token}_seed{seed}_"
                    f"{STAKES_TOKEN}_b{int(BUDGET_BSTAR)}_{mix_token}_v11"
                )
                output_prefix = (out_dir / stem).as_posix()
                jobs.append(
                    {
                        "grid": int(grid),
                        "seed": int(seed),
                        "red_team_prob": float(red_team_prob),
                        "pgf_mix": float(mix),
                        "episodes": int(episodes),
                        "budget": int(BUDGET_BSTAR),
                        "output_prefix": output_prefix,
                    }
                )
    return jobs


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner F8 (v11): replicación H1-only (CFR, B=40).")
    parser.add_argument("--stage", choices=["confirm", "expand", "all"], default="confirm")
    parser.add_argument("--episodes", type=int, default=EPISODES_DEFAULT)
    parser.add_argument("--red-team-prob", type=float, default=RED_TEAM_PROB_DEFAULT)

    parser.add_argument("--seeds", nargs="*", type=int, default=BASE_SEEDS_DEFAULT)
    parser.add_argument("--expand-seeds", nargs="*", type=int, default=EXPAND_SEEDS_DEFAULT)
    parser.add_argument("--grids", nargs="*", type=int, default=GRIDS_DEFAULT)
    parser.add_argument("--pgf-mix", nargs="*", type=float, default=PGF_MIX_DEFAULT)

    parser.add_argument("--dry-run", action="store_true", help="Solo imprime el plan y los comandos (no ejecuta).")
    args = parser.parse_args()

    episodes = int(args.episodes)
    red_team_prob = float(args.red_team_prob)
    rt_token = prob_to_token(red_team_prob)

    seeds_confirm = [int(x) for x in args.seeds]
    seeds_expand = [int(x) for x in args.expand_seeds]
    grids = [int(x) for x in args.grids]
    mixes = [float(x) for x in args.pgf_mix]

    confirm_jobs = iter_jobs(seeds=seeds_confirm, grids=grids, pgf_mix_values=mixes, episodes=episodes, red_team_prob=red_team_prob)
    expand_jobs = iter_jobs(seeds=seeds_expand, grids=grids, pgf_mix_values=mixes, episodes=episodes, red_team_prob=red_team_prob)

    def expected_canonical(jobs: list[dict]) -> int:
        total = 0
        for job in jobs:
            total += 2 if float(job["pgf_mix"]) == 0.0 else 1
        return total

    print(f"[PLAN] Config: rt={rt_token}, B={BUDGET_BSTAR}, episodes={episodes}, grids={grids}, mixes={mixes}")
    print(f"[PLAN] Confirmatorio raw jobs: {len(confirm_jobs)} (seeds={len(seeds_confirm)})")
    print(f"[PLAN] Canónico esperado tras organize_F8_results.py (confirm): {expected_canonical(confirm_jobs)} CSV")
    print(f"[PLAN] Expansión raw jobs: {len(expand_jobs)} (seeds={len(seeds_expand)})")
    print(f"[PLAN] Canónico esperado tras organize_F8_results.py (expand): {expected_canonical(expand_jobs)} CSV")

    if args.dry_run:
        jobs_to_print: list[tuple[str, list[dict]]] = []
        if args.stage in {"confirm", "all"}:
            jobs_to_print.append(("CONFIRM", confirm_jobs))
        if args.stage in {"expand", "all"}:
            jobs_to_print.append(("EXPAND", expand_jobs))
        for label, jobs in jobs_to_print:
            for idx, job in enumerate(jobs, start=1):
                cmd = build_cmd(
                    grid=job["grid"],
                    seed=job["seed"],
                    pgf_mix=job["pgf_mix"],
                    episodes=job["episodes"],
                    red_team_prob=job["red_team_prob"],
                    output_prefix=job["output_prefix"],
                )
                print(
                    f"\n[{label} {idx}/{len(jobs)}] grid={job['grid']} seed={job['seed']} "
                    f"B={job['budget']} p={job['red_team_prob']} pgf_mix={job['pgf_mix']}"
                )
                print(f"[CMD] {' '.join(cmd)}")
        return 0

    failures = 0

    def run_jobs(label: str, jobs: list[dict]) -> None:
        nonlocal failures
        for idx, job in enumerate(jobs, start=1):
            cmd = build_cmd(
                grid=job["grid"],
                seed=job["seed"],
                pgf_mix=job["pgf_mix"],
                episodes=job["episodes"],
                red_team_prob=job["red_team_prob"],
                output_prefix=job["output_prefix"],
            )
            print(
                f"\n[{label} {idx}/{len(jobs)}] grid={job['grid']} seed={job['seed']} "
                f"B={job['budget']} p={job['red_team_prob']} pgf_mix={job['pgf_mix']}"
            )
            print(f"[CMD] {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            if result.returncode != 0:
                failures += 1
                print(f"[ERROR] Fallo: {job}", file=sys.stderr)

    if args.stage in {"confirm", "all"}:
        run_jobs("CONFIRM", confirm_jobs)
    if args.stage in {"expand", "all"}:
        run_jobs("EXPAND", expand_jobs)

    if failures:
        print(f"\nF8 completado con fallos: {failures}", file=sys.stderr)
        return 1

    print("\nF8 completado OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

