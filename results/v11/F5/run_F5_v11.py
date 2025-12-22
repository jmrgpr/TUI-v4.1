import argparse
import os
import subprocess
import sys
from pathlib import Path

SEEDS_DEFAULT = [123, 314, 271, 404, 808]
GRIDS_DEFAULT = [8, 16]
PGF_MIX_DEFAULT = [0.0, 0.2]

STAKES_TOKEN = "stkH"
STAKES_MODE = "high"
BUDGET_DEFAULT = 3

# Nota importante (evitar confusión):
# - `sim.prototipo_rl_simbiosis` ejecuta por defecto dos agentes por corrida: `control` y `simbiosis`.
# - F5 define 3 grupos (C-H, S0-H, S2-H) con 10 runs cada uno (total 30 canónicos).
# - Este runner lanza 20 comandos (grid × seed × pgf_mix). Los 30 canónicos se obtienen al organizar y aplicar
#   la regla anti-duplicados:
#   - Para `pgf_mix=0.0` se exportan `control` + `simbiosis` (2 CSV canónicos por corrida).
#   - Para `pgf_mix>0.0` se exporta solo `simbiosis` (evita duplicar `control`).


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
        STAKES_MODE,
        "--budget",
        str(budget),
        "--output_prefix",
        output_prefix,
    ]
    return cmd


def iter_jobs(seeds: list[int], grids: list[int], pgf_mix_values: list[float], episodes: int, budget: int) -> list[dict]:
    jobs = []
    for grid in grids:
        for seed in seeds:
            for mix in pgf_mix_values:
                mix_token = mix_to_token(mix)
                out_dir = Path("results/v11/F5/raw/F2_redteam") / STAKES_TOKEN
                out_dir.mkdir(parents=True, exist_ok=True)
                stem = f"grid{grid}_riskhigh_r1p2_f2rt0p1_seed{seed}_{STAKES_TOKEN}_b{budget}_{mix_token}_v11"
                output_prefix = (out_dir / stem).as_posix()
                jobs.append(
                    {
                        "grid": int(grid),
                        "seed": int(seed),
                        "pgf_mix": float(mix),
                        "episodes": int(episodes),
                        "budget": int(budget),
                        "output_prefix": output_prefix,
                    }
                )
    return jobs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Runner F5 (v11): F2_redteam fijo, high-stakes (stkH) con budget B=3; endpoint primario episodes_completed."
    )
    parser.add_argument("--episodes", type=int, default=200)
    parser.add_argument("--seeds", nargs="*", type=int, default=SEEDS_DEFAULT)
    parser.add_argument("--grids", nargs="*", type=int, default=GRIDS_DEFAULT)
    parser.add_argument("--pgf-mix", nargs="*", type=float, default=PGF_MIX_DEFAULT)
    parser.add_argument("--budget", type=int, default=BUDGET_DEFAULT, help="Budget B (catástrofes) para high-stakes (debe ser 3 si sigues el preregistro).")
    parser.add_argument("--dry-run", action="store_true", help="Solo imprime comandos (no ejecuta).")
    args = parser.parse_args()

    if 0.0 not in [float(x) for x in args.pgf_mix]:
        raise SystemExit("[ERROR] F5 requiere incluir pgf_mix=0.0 (S0) para exportar el baseline `control` sin duplicados.")

    jobs = iter_jobs(seeds=args.seeds, grids=args.grids, pgf_mix_values=args.pgf_mix, episodes=args.episodes, budget=args.budget)
    expected_canonical_csv = 0
    for job in jobs:
        expected_canonical_csv += 2 if float(job["pgf_mix"]) == 0.0 else 1
    print(f"[PLAN] Raw jobs: {len(jobs)} (cada job ejecuta control+simbiosis)")
    print(f"[PLAN] Canónico esperado tras organize_F5_results.py: {expected_canonical_csv} CSV (meta preregistro: 30)")

    failures = 0
    for idx, job in enumerate(jobs, start=1):
        cmd = build_cmd(
            grid=job["grid"],
            seed=job["seed"],
            pgf_mix=job["pgf_mix"],
            episodes=job["episodes"],
            budget=job["budget"],
            output_prefix=job["output_prefix"],
        )
        print(f"\n[{idx}/{len(jobs)}] F2_redteam grid={job['grid']} seed={job['seed']} budget={job['budget']} pgf_mix={job['pgf_mix']}")
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
        print(f"\nF5 completado con fallos: {failures}/{len(jobs)}", file=sys.stderr)
        return 1
    print(f"\nF5 completado OK: {len(jobs)}/{len(jobs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

