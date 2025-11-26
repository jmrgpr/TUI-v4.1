# Reconstruye un master limpio a partir de los CSV del sweep,
# agregando risk_scale, seed, agent y reward/tripwires unificados.

import re
from pathlib import Path
import pandas as pd


SWEEP_ROOT = Path(__file__).resolve().parent.parent / "data" / "sweep" / "fase2_full"
OUTPUT_CSV = Path(__file__).resolve().parent.parent / "data" / "master_results_clean_fixed.csv"


AGENT_MAP = {
    "dqn_control": ("Recompensa_dqn_control", "Tripwires_dqn_control"),
    "control": ("Recompensa_control", "Tripwires_control"),
    "simbiosis": ("Recompensa_simbiosis", "Tripwires_simbiosis"),
    "tui": ("Recompensa_tui", "Tripwires_tui"),
}


def infer_agent(name: str) -> str | None:
    if "dqn_control" in name:
        return "dqn_control"
    if "simbiosis" in name:
        return "simbiosis"
    if re.search(r"_tui(\.|_|$)", name):
        return "tui"
    if "control" in name:
        return "control"
    return None


def infer_risk(name: str) -> float | None:
    m = re.search(r"risk([0-9\.]+)", name)
    return float(m.group(1)) if m else None


def infer_seed(path: Path) -> int | None:
    m = re.search(r"seed[_-]?(\d+)", path.as_posix())
    return int(m.group(1)) if m else None


def process_file(path: Path) -> pd.DataFrame | None:
    agent = infer_agent(path.name)
    risk = infer_risk(path.name)
    seed = infer_seed(path)
    if agent is None or risk is None or seed is None:
        print(f"[WARN] No se pudo inferir agent/risk/seed para {path}")
        return None
    reward_col, trip_col = AGENT_MAP.get(agent, (None, None))
    df = pd.read_csv(path)
    if reward_col not in df.columns or trip_col not in df.columns:
        print(f"[WARN] Faltan columnas esperadas en {path}")
        return None
    out = pd.DataFrame(
        {
            "Episodio": df["Episodio"] if "Episodio" in df.columns else None,
            "risk_scale": risk,
            "seed": seed,
            "agent": agent,
            "reward": df[reward_col],
            "tripwires": df[trip_col],
        }
    )
    # Mantener otras métricas si existen
    for col in ["PGF_Bruto_Avg", "PGF_Costo_Avg", "avg_pgf_neto", "avg_pgf_bruto", "avg_pgf_costo", "avg_tripwire", "avg_reward"]:
        if col in df.columns:
            out[col] = df[col]
    return out


def main():
    frames = []
    for csv in SWEEP_ROOT.rglob("*.csv"):
        if "summary" in csv.name.lower():
            continue
        df = process_file(csv)
        if df is not None:
            frames.append(df)
    if not frames:
        raise SystemExit("No se generó ningún dataframe; revisa la estructura de data/sweep.")
    master = pd.concat(frames, ignore_index=True)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(OUTPUT_CSV, index=False)
    print(f"[OK] Master reconstruido con {len(master)} filas -> {OUTPUT_CSV}")
    # Resumen rápido
    print(master.groupby(["agent", "risk_scale"])["reward"].agg(["mean", "std", "count"]).round(3))


if __name__ == "__main__":
    main()
