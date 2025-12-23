import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from sim import config
from sim.runner import run_experiment


DEFAULT_SEEDS = [42, 101, 13]
DEFAULT_GRID = 16
DEFAULT_EPISODES = 200

DEFAULT_RISK_SCALE = 1.2
DEFAULT_RISK_LEVEL = "high"

# Congelado para RV1: usamos red_team=True con prob baja para evitar colapsos inmediatos.
DEFAULT_RED_TEAM_PROB = 0.03


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def mesi_rv(early_mean: float) -> float:
    return float(max(0.05 * abs(float(early_mean)), 0.5))


def compute_early_late(values: list[float], *, early_n: int = 50, late_start: int = 150) -> tuple[float, float, float]:
    if len(values) < early_n:
        raise ValueError(f"Se esperan >= {early_n} episodios para early_mean; recibido {len(values)}")
    if len(values) < late_start + 1:
        raise ValueError(f"Se esperan >= {late_start+1} episodios para late_mean; recibido {len(values)}")
    early = float(np.mean(values[:early_n]))
    late = float(np.mean(values[late_start:]))
    return early, late, float(late - early)


def write_run_episode_csv(path: Path, rewards: list[float], starvation: list[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["episode", "reward_total", "starvation"])
        for i, (r, s) in enumerate(zip(rewards, starvation), start=1):
            w.writerow([i, float(r), int(s)])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Runner RV1 (v11 post-errata): valida persistencia del agente por run + robustez de shape + señal mínima de aprendizaje."
    )
    parser.add_argument("--episodes", type=int, default=DEFAULT_EPISODES)
    parser.add_argument("--grid", type=int, default=DEFAULT_GRID)
    parser.add_argument("--seeds", nargs="*", type=int, default=DEFAULT_SEEDS)
    parser.add_argument("--risk-scale", type=float, default=DEFAULT_RISK_SCALE)
    parser.add_argument("--risk-level", type=str, default=DEFAULT_RISK_LEVEL)
    parser.add_argument("--red-team-prob", type=float, default=DEFAULT_RED_TEAM_PROB)
    parser.add_argument("--dry-run", action="store_true", help="Solo imprime el plan (no ejecuta).")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Ejecuta un smoke test corto (20 episodios, 1 seed) en carpeta _tmp (no canónico).",
    )
    args = parser.parse_args()

    base_dir = Path("results/v11/RV1")
    raw_dir = base_dir / ("_tmp_smoke" if args.smoke else "raw")
    out_metrics_csv = base_dir / "rv1_run_metrics.csv"
    out_invariants_json = base_dir / "rv1_invariants.json"
    out_closure_md = base_dir / "RV1_CLOSURE_REPORT.md"

    episodes = int(20 if args.smoke else args.episodes)
    grid = int(args.grid)
    seeds = [int(s) for s in (args.seeds[:1] if args.smoke else args.seeds)]

    frozen = {
        "series": "v11",
        "phase": "RV1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "episodes": episodes,
        "grid_size": grid,
        "stakes_mode": "low",
        "catastrophe_budget": None,
        "risk_scale": float(args.risk_scale),
        "risk_level": str(args.risk_level),
        "red_team": True,
        "red_team_prob": float(args.red_team_prob),
        "red_team_impact": float(config.EXP_CONFIG.get("red_team_impact", -1.0)),
        "red_team_move_tripwire_prob": float(config.EXP_CONFIG.get("red_team_move_tripwire_prob", 0.4)),
        "red_team_add_shock_prob": float(config.EXP_CONFIG.get("red_team_add_shock_prob", 0.3)),
        "red_team_block_prob": float(config.EXP_CONFIG.get("red_team_block_prob", 0.3)),
        "state_mode": "abstract",
        "conditions": ["C (Control-DQN)", "S0 (Simbiosis pgf_mix=0.0)"],
        "seeds": list(seeds),
    }

    print("[PLAN] RV1 runs:")
    print(f"  episodes={episodes}, grid={grid}, seeds={seeds}")
    print(f"  risk_scale={frozen['risk_scale']}, risk_level={frozen['risk_level']}, red_team_prob={frozen['red_team_prob']}")
    print("  conditions: C (Control-DQN), S0 (Simbiosis pgf_mix=0.0)")
    if args.smoke:
        print("  mode: SMOKE (_tmp_smoke; no canónico)")
    if args.dry_run:
        return 0

    # Freeze EXP_CONFIG for determinism.
    config.EXP_CONFIG["red_team_prob"] = float(args.red_team_prob)
    # (Otros parámetros ya están definidos en config; se dejan sin override.)

    rows: list[dict] = []
    invariants_runs: list[dict] = []

    def run_condition(*, label: str, seed: int, use_pgf: bool, pgf_mix: float) -> dict:
        return run_experiment(
            episodes=episodes,
            seed=seed,
            risk_scale=float(args.risk_scale),
            risk_level=str(args.risk_level),
            red_team=True,
            agent_name=label,
            use_pgf=use_pgf,
            use_dqn=True,
            pgf_mix=float(pgf_mix),
            grid_size=grid,
            stakes_mode="low",
            catastrophe_budget=None,
            state_mode="abstract",
            record_invariants=True,
        )

    # Stop rules: abort immediately if invariants fail in first seed of any condition.
    for seed in seeds:
        for cond_key, cond in [
            ("C", {"label": "Control-DQN", "use_pgf": False, "pgf_mix": 0.0}),
            ("S0", {"label": "Simbiosis", "use_pgf": True, "pgf_mix": 0.0}),
        ]:
            print(f"\n[RUN] seed={seed} cond={cond_key}")
            payload = run_condition(label=cond["label"], seed=seed, use_pgf=cond["use_pgf"], pgf_mix=cond["pgf_mix"])

            rewards = [float(x) for x in payload.get("total_rewards", [])]
            starvation = [int(x) for x in payload.get("starvation_evol", [])]
            if len(rewards) != len(starvation):
                raise RuntimeError(f"Mismatch rewards/starvation: {len(rewards)} vs {len(starvation)} (seed={seed}, cond={cond_key})")

            if args.smoke:
                early_mean = float("nan")
                late_mean = float("nan")
                delta_learn = float("nan")
                starv_early = float("nan")
                starv_late = float("nan")
                delta_starv = float("nan")
                mesi = float("nan")
                e1_pass = False
            else:
                early_mean, late_mean, delta_learn = compute_early_late(rewards)
                starv_early = float(np.mean(starvation[:50]))
                starv_late = float(np.mean(starvation[150:]))
                delta_starv = float(starv_late - starv_early)

                mesi = mesi_rv(early_mean)
                e1_pass = bool(delta_learn >= mesi)

            inv = payload.get("rv1_invariants") or {}
            agent_ids = [int(x) for x in inv.get("agent_id_by_episode", [])]
            unique_agent_ids = len(set(agent_ids)) if agent_ids else 0
            mem_sizes = [int(x) for x in inv.get("dqn_memory_size_by_episode", [])]
            learn_steps = [int(x) for x in inv.get("dqn_learn_steps_by_episode", [])]

            i1_agent_id_pass = bool(agent_ids and unique_agent_ids == 1)
            i1_counters_pass = bool(mem_sizes and learn_steps and mem_sizes[-1] >= mem_sizes[0] and learn_steps[-1] >= learn_steps[0])
            i1_pass = bool(i1_agent_id_pass and i1_counters_pass)
            i2_pass = bool(int(inv.get("state_dim", -1)) > 0 and str(inv.get("state_mode", "")) == "abstract")

            if seed == seeds[0] and not (i1_pass and i2_pass):
                raise SystemExit(
                    f"[STOP] Invariante falló en primer seed (seed={seed}, cond={cond_key}): "
                    f"I1={i1_pass} (agent_id={i1_agent_id_pass}, counters={i1_counters_pass}) I2={i2_pass}"
                )

            run_id = f"rv1_grid{grid}_seed{seed}_{cond_key.lower()}"
            raw_json = raw_dir / f"{run_id}.json"
            raw_csv = raw_dir / f"{run_id}_episodes.csv"
            raw_dir.mkdir(parents=True, exist_ok=True)
            write_run_episode_csv(raw_csv, rewards, starvation)
            raw_json.write_text(
                json.dumps(
                    {
                        "config": payload.get("config", {}),
                        "run_metrics": payload.get("run_metrics", {}),
                        "total_rewards": rewards,
                        "starvation_evol": starvation,
                        "rv1_invariants": inv,
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            rows.append(
                {
                    "phase": "RV1",
                    "series": "v11",
                    "condition": cond_key,
                    "seed": seed,
                    "grid": grid,
                    "episodes": episodes,
                    "risk_scale": float(args.risk_scale),
                    "risk_level": str(args.risk_level),
                    "red_team_prob": float(args.red_team_prob),
                    "early_mean": early_mean,
                    "late_mean": late_mean,
                    "delta_learn": delta_learn,
                    "mesi_rv": mesi,
                    "e1_pass": int(e1_pass),
                    "starv_rate_early": starv_early,
                    "starv_rate_late": starv_late,
                    "delta_starv": delta_starv,
                    "i1_pass": int(i1_pass),
                    "i2_pass": int(i2_pass),
                    "agent_id_unique": unique_agent_ids,
                    "dqn_memory_start": mem_sizes[0] if mem_sizes else 0,
                    "dqn_memory_end": mem_sizes[-1] if mem_sizes else 0,
                    "dqn_learn_steps_start": learn_steps[0] if learn_steps else 0,
                    "dqn_learn_steps_end": learn_steps[-1] if learn_steps else 0,
                }
            )
            invariants_runs.append(
                {
                    "run_id": run_id,
                    "condition": cond_key,
                    "seed": seed,
                    "grid": grid,
                    "rv1_invariants": inv,
                }
            )

    # Write canonical artifacts (tracked).
    if not args.smoke:
        out_metrics_csv.parent.mkdir(parents=True, exist_ok=True)
        with out_metrics_csv.open("w", newline="", encoding="utf-8") as f:
            fieldnames = list(rows[0].keys()) if rows else []
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

        out_invariants_json.write_text(
            json.dumps({"frozen": frozen, "runs": invariants_runs}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        # Decision logic (per prereg).
        df = {("C", s): None for s in seeds}
        # Build per-condition counts.
        pass_by_cond = {"C": 0, "S0": 0}
        inv_i1_all = all(r["i1_pass"] == 1 for r in rows)
        inv_i2_all = all(r["i2_pass"] == 1 for r in rows)
        for r in rows:
            if r["e1_pass"] == 1:
                pass_by_cond[r["condition"]] += 1
        e1_pass_all = all(pass_by_cond[c] >= 2 for c in pass_by_cond)
        overall_pass = bool(inv_i1_all and inv_i2_all and e1_pass_all)

        hash_metrics = sha256_file(out_metrics_csv)
        hash_inv = sha256_file(out_invariants_json)

        closure_lines = [
            "# RV1_CLOSURE_REPORT — Repair Validation (v11 post-errata)",
            "",
            f"**Serie:** v11 (post-errata)  ",
            f"**Fase:** RV1 — Repair Validation  ",
            f"**Fecha de cierre:** {datetime.now().strftime('%Y-%m-%d')} (America/Puerto_Rico)  ",
            f"**Estado:** {'PASS' if overall_pass else 'FAIL'}",
            "",
            "## 1) Resumen ejecutivo",
            "",
            "- Objetivo: validar persistencia del agente por run + robustez de shape + señal mínima de aprendizaje intra-run.",
            f"- Decisión: **{'GO (PASS)' if overall_pass else 'NO-GO (FAIL)'}**.",
            f"- Invariantes: I1(all)={'PASS' if inv_i1_all else 'FAIL'}, I2(all)={'PASS' if inv_i2_all else 'FAIL'}.",
            f"- Señal mínima E1 (>=2/3 seeds por condición): C={pass_by_cond['C']}/3, S0={pass_by_cond['S0']}/3 ⇒ {'PASS' if e1_pass_all else 'FAIL'}.",
            "",
            "## 2) Setup congelado (según preregistro)",
            "",
            f"- episodes={episodes}, grid={grid}, seeds={seeds}",
            f"- risk_scale={float(args.risk_scale)}, risk_level={str(args.risk_level)}, red_team_prob={float(args.red_team_prob)}",
            "- stakes=LOW (sin budget)",
            "- condiciones: C (Control-DQN), S0 (Simbiosis pgf_mix=0.0)",
            "",
            "## 3) Artefactos",
            "",
            f"- Metrics (canónico): `{out_metrics_csv.as_posix()}` (sha256={hash_metrics})",
            f"- Invariants (canónico): `{out_invariants_json.as_posix()}` (sha256={hash_inv})",
            f"- Raw (local-only): `{raw_dir.as_posix()}`",
            "",
            "## 4) Siguiente paso",
            "",
            "- Si PASS: se habilita re-intentar una fase confirmatoria (F7+) bajo el nuevo régimen (agente persistente).",
            "- Si FAIL: no ejecutar F7; corregir instrumentación/runner y repetir RV1.",
            "",
        ]
        out_closure_md.write_text("\n".join(closure_lines), encoding="utf-8")

        print(f"\n[OK] Escrito: {out_metrics_csv.as_posix()}")
        print(f"[OK] Escrito: {out_invariants_json.as_posix()}")
        print(f"[OK] Escrito: {out_closure_md.as_posix()}")
        print(f"[DECISION] {'PASS/GO' if overall_pass else 'FAIL/NO-GO'}")
    else:
        print(f"\n[OK] Smoke outputs (local-only): {raw_dir.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
