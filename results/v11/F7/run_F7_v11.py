import argparse
import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# F7: high-stakes run-level; se calibra solo budget B para evitar ceiling effect de CFR.

PILOT_BUDGETS_DEFAULT = [3, 5, 10, 20, 40]
PILOT_SEEDS_DEFAULT = [9001, 9002, 9003, 9004, 9005]
PILOT_GRID_DEFAULT = 16

CONFIRM_SEEDS_DEFAULT = [123, 314, 271, 404, 808]
CONFIRM_GRIDS_DEFAULT = [8, 16]
PGF_MIX_DEFAULT = [0.0, 0.2]

STAKES_TOKEN = "stkH"
STAKES_MODE = "high"

RISK_SCALE = 1.2
RISK_LEVEL = "high"
RED_TEAM_PROB_DEFAULT = 0.03

RAW_DIR = Path("results/v11/F7/raw")
ANALYSIS_DIR = Path("results/v11/F7/analysis")
BSTAR_JSON = ANALYSIS_DIR / "f7_pilot_selection_v11.json"


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
    budget: int,
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
        str(budget),
        "--output_prefix",
        output_prefix,
    ]


def iter_pilot_jobs(*, budgets: list[int], seeds: list[int], grid: int, episodes: int, red_team_prob: float) -> list[dict]:
    jobs: list[dict] = []
    rt_token = prob_to_token(red_team_prob)
    for b in budgets:
        out_dir = RAW_DIR / "PILOT" / rt_token / f"b{int(b)}"
        out_dir.mkdir(parents=True, exist_ok=True)
        for seed in seeds:
            stem = f"grid{grid}_riskhigh_r1p2_f2{rt_token}_seed{seed}_{STAKES_TOKEN}_b{int(b)}_m0p0_v11"
            output_prefix = (out_dir / stem).as_posix()
            jobs.append(
                {
                    "stage": "pilot",
                    "grid": int(grid),
                    "seed": int(seed),
                    "red_team_prob": float(red_team_prob),
                    "pgf_mix": 0.0,
                    "episodes": int(episodes),
                    "budget": int(b),
                    "output_prefix": output_prefix,
                }
            )
    return jobs


def iter_confirm_jobs(
    *,
    budget: int,
    red_team_prob: float,
    seeds: list[int],
    grids: list[int],
    pgf_mix_values: list[float],
    episodes: int,
) -> list[dict]:
    jobs: list[dict] = []
    rt_token = prob_to_token(red_team_prob)
    out_dir = RAW_DIR / "F2_redteam" / STAKES_TOKEN / rt_token
    out_dir.mkdir(parents=True, exist_ok=True)
    for grid in grids:
        for seed in seeds:
            for mix in pgf_mix_values:
                mix_token = mix_to_token(mix)
                stem = f"grid{grid}_riskhigh_r1p2_f2{rt_token}_seed{seed}_{STAKES_TOKEN}_b{int(budget)}_{mix_token}_v11"
                output_prefix = (out_dir / stem).as_posix()
                jobs.append(
                    {
                        "stage": "confirm",
                        "grid": int(grid),
                        "seed": int(seed),
                        "red_team_prob": float(red_team_prob),
                        "pgf_mix": float(mix),
                        "episodes": int(episodes),
                        "budget": int(budget),
                        "output_prefix": output_prefix,
                    }
                )
    return jobs


def load_control_budget_exhausted(*, json_path: Path, budget: int) -> bool:
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    ctrl = payload.get("control", {})
    run_metrics = ctrl.get("run_metrics", {}) if isinstance(ctrl, dict) else {}
    val = run_metrics.get("budget_exhausted")
    if isinstance(val, bool):
        return val
    if val in (0, 1):
        return bool(val)

    # Fallback: inferir desde CSV (starvation sum >= B), filtrando por agente=control.
    csv_path = json_path.with_name(f"{json_path.stem}_episodes.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"Faltan run_metrics y CSV para inferir budget_exhausted: {json_path.as_posix()}")
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "Agente" not in (reader.fieldnames or []) or "Starvation" not in (reader.fieldnames or []):
            raise ValueError(f"CSV raw no tiene columnas Agente/Starvation: {csv_path.as_posix()}")
        starvation_sum = 0
        for row in reader:
            agente = (row.get("Agente") or "").strip().lower()
            if agente != "control":
                continue
            starvation_sum += int(float(row.get("Starvation") or 0))
    return int(starvation_sum) >= int(budget)


def select_b_star(*, budgets: list[int], seeds: list[int], grid: int, episodes: int, red_team_prob: float) -> dict:
    rt_token = prob_to_token(red_team_prob)
    rows: list[dict] = []
    cfr_by_b: dict[int, float] = {}
    missing: list[str] = []

    for b in budgets:
        out_dir = RAW_DIR / "PILOT" / rt_token / f"b{int(b)}"
        exhausted = 0
        total = 0
        for seed in seeds:
            stem = f"grid{grid}_riskhigh_r1p2_f2{rt_token}_seed{seed}_{STAKES_TOKEN}_b{int(b)}_m0p0_v11"
            json_path = out_dir / f"{stem}.json"
            if not json_path.exists():
                missing.append(json_path.as_posix())
                continue
            total += 1
            if load_control_budget_exhausted(json_path=json_path, budget=int(b)):
                exhausted += 1
        if total != len(seeds):
            raise FileNotFoundError(f"Faltan JSON del piloto para B={b}: {missing[:3]}{'...' if len(missing)>3 else ''}")
        cfr = float(exhausted / total) if total else float("nan")
        cfr_by_b[int(b)] = cfr
        rows.append({"budget_B": int(b), "n": int(total), "cfr_control": float(cfr)})

    # regla determinística: elegir CFR más cercano a 0.5 y dentro [0.3,0.7], tie-break menor B
    candidates = sorted((b, cfr) for b, cfr in cfr_by_b.items())

    def dist_to_half(item: tuple[int, float]) -> float:
        return abs(float(item[1]) - 0.5)

    in_band = [(b, cfr) for b, cfr in candidates if 0.3 <= float(cfr) <= 0.7]
    pool = in_band if in_band else candidates
    pool_sorted = sorted(pool, key=lambda x: (dist_to_half(x), x[0]))
    b_star, cfr_star = pool_sorted[0]

    selection = {
        "phase": "F7",
        "series": "v11",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pilot": {
            "grid": int(grid),
            "seeds": [int(x) for x in seeds],
            "candidates": [int(x) for x in budgets],
            "rows": rows,
            "rule": "closest-to-0.5 within [0.3,0.7], else closest-to-0.5; tie -> smallest B",
        },
        "red_team_prob": float(red_team_prob),
        "rt_token": rt_token,
        "B_star": int(b_star),
        "B_star_token": f"b{int(b_star)}",
        "cfr_control_B_star": float(cfr_star),
    }
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    BSTAR_JSON.write_text(json.dumps(selection, indent=2, ensure_ascii=False), encoding="utf-8")
    return selection


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner F7 (v11): piloto de B, selección B*, confirmatorio CFR.")
    parser.add_argument("--stage", choices=["pilot", "select", "confirm", "all"], default="all")
    parser.add_argument("--episodes", type=int, default=200)
    parser.add_argument("--red-team-prob", type=float, default=RED_TEAM_PROB_DEFAULT)

    parser.add_argument("--pilot-budgets", nargs="*", type=int, default=PILOT_BUDGETS_DEFAULT)
    parser.add_argument("--pilot-seeds", nargs="*", type=int, default=PILOT_SEEDS_DEFAULT)
    parser.add_argument("--pilot-grid", type=int, default=PILOT_GRID_DEFAULT)

    parser.add_argument("--seeds", nargs="*", type=int, default=CONFIRM_SEEDS_DEFAULT)
    parser.add_argument("--grids", nargs="*", type=int, default=CONFIRM_GRIDS_DEFAULT)
    parser.add_argument("--pgf-mix", nargs="*", type=float, default=PGF_MIX_DEFAULT)

    parser.add_argument("--dry-run", action="store_true", help="Solo imprime el plan y los comandos (no ejecuta).")
    args = parser.parse_args()

    episodes = int(args.episodes)
    red_team_prob = float(args.red_team_prob)

    pilot_jobs = iter_pilot_jobs(
        budgets=[int(b) for b in args.pilot_budgets],
        seeds=[int(s) for s in args.pilot_seeds],
        grid=int(args.pilot_grid),
        episodes=episodes,
        red_team_prob=red_team_prob,
    )

    b_star: int | None = None
    rt_token = prob_to_token(red_team_prob)
    if BSTAR_JSON.exists():
        sel = json.loads(BSTAR_JSON.read_text(encoding="utf-8"))
        b_star = int(sel.get("B_star"))

    confirm_jobs_preview: list[dict] = []
    if b_star is not None:
        confirm_jobs_preview = iter_confirm_jobs(
            budget=int(b_star),
            red_team_prob=red_team_prob,
            seeds=[int(x) for x in args.seeds],
            grids=[int(x) for x in args.grids],
            pgf_mix_values=[float(x) for x in args.pgf_mix],
            episodes=episodes,
        )

    print(
        f"[PLAN] Piloto raw jobs: {len(pilot_jobs)} (B ∈ {sorted(set(args.pilot_budgets))}, grid={args.pilot_grid}, seeds={len(args.pilot_seeds)})"
    )
    if b_star is None:
        print("[PLAN] B* aún no seleccionado (correr --stage pilot y luego --stage select).")
    else:
        expected_canonical_confirm = 0
        for job in confirm_jobs_preview:
            expected_canonical_confirm += 2 if float(job["pgf_mix"]) == 0.0 else 1
        print(f"[PLAN] B* detectado: {b_star} (rt={rt_token})")
        print(f"[PLAN] Confirmatorio raw jobs: {len(confirm_jobs_preview)}")
        print(f"[PLAN] Canónico esperado tras organize_F7_results.py (solo confirmatorio): {expected_canonical_confirm} CSV (meta preregistro: 30)")

    if args.dry_run:
        for idx, job in enumerate(pilot_jobs, start=1):
            cmd = build_cmd(
                grid=job["grid"],
                seed=job["seed"],
                pgf_mix=job["pgf_mix"],
                episodes=job["episodes"],
                budget=job["budget"],
                red_team_prob=job["red_team_prob"],
                output_prefix=job["output_prefix"],
            )
            print(f"\n[PILOT {idx}/{len(pilot_jobs)}] grid={job['grid']} seed={job['seed']} B={job['budget']} p={job['red_team_prob']}")
            print(f"[CMD] {' '.join(cmd)}")
        if b_star is not None:
            for idx, job in enumerate(confirm_jobs_preview, start=1):
                cmd = build_cmd(
                    grid=job["grid"],
                    seed=job["seed"],
                    pgf_mix=job["pgf_mix"],
                    episodes=job["episodes"],
                    budget=job["budget"],
                    red_team_prob=job["red_team_prob"],
                    output_prefix=job["output_prefix"],
                )
                print(
                    f"\n[CONFIRM {idx}/{len(confirm_jobs_preview)}] grid={job['grid']} seed={job['seed']} "
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
                budget=job["budget"],
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

    if args.stage in {"pilot", "all"}:
        run_jobs("PILOT", pilot_jobs)

    if args.stage in {"select", "all"}:
        selection = select_b_star(
            budgets=[int(x) for x in args.pilot_budgets],
            seeds=[int(x) for x in args.pilot_seeds],
            grid=int(args.pilot_grid),
            episodes=episodes,
            red_team_prob=red_team_prob,
        )
        b_star = int(selection["B_star"])
        print(f"\n[SELECT] B* seleccionado: {b_star} (CFR_control={float(selection['cfr_control_B_star']):.3f})")

    if args.stage in {"confirm", "all"}:
        if b_star is None:
            raise SystemExit("[ERROR] No hay B* seleccionado. Corre --stage select o ejecuta --stage all.")
        confirm_jobs = iter_confirm_jobs(
            budget=int(b_star),
            red_team_prob=red_team_prob,
            seeds=[int(x) for x in args.seeds],
            grids=[int(x) for x in args.grids],
            pgf_mix_values=[float(x) for x in args.pgf_mix],
            episodes=episodes,
        )
        run_jobs("CONFIRM", confirm_jobs)

    if failures:
        print(f"\nF7 completado con fallos: {failures}", file=sys.stderr)
        return 1

    print("\nF7 completado OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
