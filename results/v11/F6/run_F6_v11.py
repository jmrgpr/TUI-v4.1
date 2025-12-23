import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# F6: high-stakes fijo B=3; se calibra solo red_team_prob para evitar ceiling effect de CFR.

PILOT_PROBS_DEFAULT = [0.03, 0.05, 0.07]
PILOT_SEEDS_DEFAULT = [9001, 9002, 9003, 9004, 9005]
PILOT_GRID_DEFAULT = 16

CONFIRM_SEEDS_DEFAULT = [123, 314, 271, 404, 808]
CONFIRM_GRIDS_DEFAULT = [8, 16]
PGF_MIX_DEFAULT = [0.0, 0.2]

STAKES_TOKEN = "stkH"
STAKES_MODE = "high"
BUDGET_DEFAULT = 3

RISK_SCALE = 1.2
RISK_LEVEL = "high"

RAW_DIR = Path("results/v11/F6/raw")
ANALYSIS_DIR = Path("results/v11/F6/analysis")
PSTAR_JSON = ANALYSIS_DIR / "f6_pilot_selection_v11.json"


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
    return cmd


def iter_pilot_jobs(*, probs: list[float], seeds: list[int], grid: int, episodes: int, budget: int) -> list[dict]:
    jobs = []
    for p in probs:
        token = prob_to_token(p)
        out_dir = RAW_DIR / "PILOT" / token
        out_dir.mkdir(parents=True, exist_ok=True)
        for seed in seeds:
            stem = f"grid{grid}_riskhigh_r1p2_f2{token}_seed{seed}_{STAKES_TOKEN}_b{budget}_m0p0_v11"
            output_prefix = (out_dir / stem).as_posix()
            jobs.append(
                {
                    "stage": "pilot",
                    "grid": int(grid),
                    "seed": int(seed),
                    "red_team_prob": float(p),
                    "pgf_mix": 0.0,
                    "episodes": int(episodes),
                    "budget": int(budget),
                    "output_prefix": output_prefix,
                }
            )
    return jobs


def iter_confirm_jobs(
    *,
    red_team_prob: float,
    seeds: list[int],
    grids: list[int],
    pgf_mix_values: list[float],
    episodes: int,
    budget: int,
) -> list[dict]:
    jobs = []
    token = prob_to_token(red_team_prob)
    out_dir = RAW_DIR / "F2_redteam" / STAKES_TOKEN / token
    out_dir.mkdir(parents=True, exist_ok=True)
    for grid in grids:
        for seed in seeds:
            for mix in pgf_mix_values:
                mix_token = mix_to_token(mix)
                stem = f"grid{grid}_riskhigh_r1p2_f2{token}_seed{seed}_{STAKES_TOKEN}_b{budget}_{mix_token}_v11"
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


def load_control_budget_exhausted(json_path: Path) -> bool:
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    ctrl = payload.get("control", {})
    run_metrics = ctrl.get("run_metrics", {}) if isinstance(ctrl, dict) else {}
    val = run_metrics.get("budget_exhausted")
    if isinstance(val, bool):
        return val
    if val in (0, 1):
        return bool(val)
    # Fallback: si no existe, inferir desde CSV (Starvation sum >= B)
    csv_path = json_path.with_name(f"{json_path.stem}_episodes.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"Faltan run_metrics y CSV para inferir budget_exhausted: {json_path.as_posix()}")
    import pandas as pd  # local import para mantener runner liviano

    df = pd.read_csv(csv_path)
    if "Starvation" not in df.columns:
        raise ValueError(f"Falta columna Starvation en {csv_path.as_posix()}")
    starvation = pd.to_numeric(df["Starvation"], errors="coerce").fillna(0).astype(int)
    return int(starvation.sum()) >= int(run_metrics.get("catastrophe_budget", BUDGET_DEFAULT))


def select_p_star(*, probs: list[float], seeds: list[int]) -> dict:
    """
    Aplica la regla preregistrada de selección de p* a partir de los JSON del piloto.
    """
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in probs:
        token = prob_to_token(p)
        base = RAW_DIR / "PILOT" / token
        if not base.exists():
            raise FileNotFoundError(f"Falta directorio piloto: {base} (corre el piloto primero)")
        vals = []
        for seed in seeds:
            json_path = base / f"grid{PILOT_GRID_DEFAULT}_riskhigh_r1p2_f2{token}_seed{seed}_{STAKES_TOKEN}_b{BUDGET_DEFAULT}_m0p0_v11.json"
            if not json_path.exists():
                raise FileNotFoundError(f"Falta JSON piloto: {json_path.as_posix()}")
            vals.append(1 if load_control_budget_exhausted(json_path) else 0)
        cfr = float(sum(vals) / len(vals))
        rows.append({"red_team_prob": float(p), "token": token, "n": len(vals), "cfr_control": cfr})

    # Regla preregistrada: elegir CFR más cercano a 0.5 dentro de [0.3,0.7]; si no, el más cercano; empate -> p menor.
    def key_in_range(row):
        cfr = row["cfr_control"]
        in_range = 0.3 <= cfr <= 0.7
        return (0 if in_range else 1, abs(cfr - 0.5), row["red_team_prob"])

    best = sorted(rows, key=key_in_range)[0]
    selection = {
        "phase": "F6",
        "series": "v11",
        "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "pilot": {
            "grid": PILOT_GRID_DEFAULT,
            "seeds": list(seeds),
            "candidates": list(probs),
            "rows": rows,
            "rule": "closest-to-0.5 within [0.3,0.7], else closest-to-0.5; tie -> smallest p",
        },
        "p_star": float(best["red_team_prob"]),
        "p_star_token": str(best["token"]),
        "cfr_control_p_star": float(best["cfr_control"]),
    }
    PSTAR_JSON.write_text(json.dumps(selection, indent=2), encoding="utf-8")
    return selection


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Runner F6 (v11): piloto calibra red_team_prob para evitar saturación de CFR con B=3; luego corre confirmatorio con p* fijo."
    )
    parser.add_argument("--episodes", type=int, default=200)
    parser.add_argument("--budget", type=int, default=BUDGET_DEFAULT)
    parser.add_argument("--pilot-probs", nargs="*", type=float, default=PILOT_PROBS_DEFAULT)
    parser.add_argument("--pilot-seeds", nargs="*", type=int, default=PILOT_SEEDS_DEFAULT)
    parser.add_argument("--pilot-grid", type=int, default=PILOT_GRID_DEFAULT)
    parser.add_argument("--seeds", nargs="*", type=int, default=CONFIRM_SEEDS_DEFAULT)
    parser.add_argument("--grids", nargs="*", type=int, default=CONFIRM_GRIDS_DEFAULT)
    parser.add_argument("--pgf-mix", nargs="*", type=float, default=PGF_MIX_DEFAULT)
    parser.add_argument("--stage", type=str, default="all", choices=["pilot", "select", "confirm", "all"])
    parser.add_argument("--dry-run", action="store_true", help="Solo imprime comandos (no ejecuta).")
    args = parser.parse_args()

    if args.budget != BUDGET_DEFAULT:
        print(f"[WARN] Budget distinto al preregistro (esperado {BUDGET_DEFAULT}): budget={args.budget}")

    if 0.0 not in [float(x) for x in args.pgf_mix]:
        raise SystemExit("[ERROR] F6 requiere incluir pgf_mix=0.0 (S0) para exportar el baseline `control` sin duplicados.")

    pilot_jobs = iter_pilot_jobs(
        probs=[float(x) for x in args.pilot_probs],
        seeds=[int(x) for x in args.pilot_seeds],
        grid=int(args.pilot_grid),
        episodes=int(args.episodes),
        budget=int(args.budget),
    )

    p_star = None
    p_star_token = None
    if PSTAR_JSON.exists():
        sel = json.loads(PSTAR_JSON.read_text(encoding="utf-8"))
        p_star = float(sel.get("p_star"))
        p_star_token = str(sel.get("p_star_token"))

    confirm_jobs_preview = []
    if p_star is not None:
        confirm_jobs_preview = iter_confirm_jobs(
            red_team_prob=p_star,
            seeds=[int(x) for x in args.seeds],
            grids=[int(x) for x in args.grids],
            pgf_mix_values=[float(x) for x in args.pgf_mix],
            episodes=int(args.episodes),
            budget=int(args.budget),
        )

    # Plan
    print(f"[PLAN] Piloto raw jobs: {len(pilot_jobs)} (p ∈ {sorted(set(args.pilot_probs))}, grid={args.pilot_grid}, seeds={len(args.pilot_seeds)})")
    if p_star is None:
        print("[PLAN] p* aun no seleccionado (correr --stage pilot y luego --stage select).")
    else:
        expected_canonical_confirm = 0
        for job in confirm_jobs_preview:
            expected_canonical_confirm += 2 if float(job["pgf_mix"]) == 0.0 else 1
        print(f"[PLAN] p* detectado: {p_star} ({p_star_token})")
        print(f"[PLAN] Confirmatorio raw jobs: {len(confirm_jobs_preview)}")
        print(f"[PLAN] Canónico esperado tras organize_F6_results.py (solo confirmatorio): {expected_canonical_confirm} CSV (meta preregistro: 30)")

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
            print(f"\n[PILOT {idx}/{len(pilot_jobs)}] grid={job['grid']} seed={job['seed']} p={job['red_team_prob']} budget={job['budget']}")
            print(f"[CMD] {' '.join(cmd)}")
        if p_star is not None:
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
                    f"p={job['red_team_prob']} budget={job['budget']} pgf_mix={job['pgf_mix']}"
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
            print(f"\n[{label} {idx}/{len(jobs)}] grid={job['grid']} seed={job['seed']} p={job['red_team_prob']} budget={job['budget']} pgf_mix={job['pgf_mix']}")
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
        selection = select_p_star(probs=[float(x) for x in args.pilot_probs], seeds=[int(x) for x in args.pilot_seeds])
        p_star = float(selection["p_star"])
        p_star_token = str(selection["p_star_token"])
        print(f"\n[SELECT] p* seleccionado: {p_star} ({p_star_token}), CFR_control={selection['cfr_control_p_star']}")

    if args.stage in {"confirm", "all"}:
        if p_star is None:
            raise SystemExit("[ERROR] No hay p* seleccionado. Corre --stage select o ejecuta --stage all.")
        confirm_jobs = iter_confirm_jobs(
            red_team_prob=float(p_star),
            seeds=[int(x) for x in args.seeds],
            grids=[int(x) for x in args.grids],
            pgf_mix_values=[float(x) for x in args.pgf_mix],
            episodes=int(args.episodes),
            budget=int(args.budget),
        )
        run_jobs("CONFIRM", confirm_jobs)

    if failures:
        print(f"\nF6 completado con fallos: {failures}", file=sys.stderr)
        return 1

    print("\nF6 completado OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

