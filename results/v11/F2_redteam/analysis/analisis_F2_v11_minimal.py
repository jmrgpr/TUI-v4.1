import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path("results/v11/F2_redteam")
CANONICAL_DOC = Path("results/v11/CANONICAL_DATASET_v11.md")
AGENTS = {"control", "dqn_control", "simbiosis"}


def canonical_csvs():
    for path in sorted(BASE_DIR.rglob("*_episodes.csv")):
        parts = [p.lower() for p in path.parts]
        if "archived" in parts:
            continue
        if not any(p.startswith("grid") for p in parts):
            continue
        if "riskhigh" not in parts:
            continue
        agent = path.parent.name
        if agent not in AGENTS:
            continue
        yield path


def detect_reward_column(df: pd.DataFrame) -> str:
    for candidate in ("Recompensa", "reward_total", "reward"):
        if candidate in df.columns:
            return candidate
    # fallback to first numeric column
    numeric = df.select_dtypes(include="number").columns
    return numeric[0] if numeric.any() else "Recompensa"


def parse_seed(path: Path) -> str:
    name = path.name.lower()
    if "seed" in name:
        try:
            return [part[4:] for part in name.split("_") if part.startswith("seed")][0]
        except Exception:
            return ""
    return ""


def load_attack_config(csv_path: Path) -> dict:
    json_path = csv_path.with_name(csv_path.name.replace("_episodes.csv", ".json"))
    if not json_path.exists():
        return {}
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data.get("config", {})


def analyze_files():
    records = []
    for path in canonical_csvs():
        try:
            df = pd.read_csv(path)
        except Exception as exc:
            print(f"[WARN] no se pudo leer {path}: {exc}")
            continue
        reward_col = detect_reward_column(df)
        reward = pd.to_numeric(df[reward_col], errors="coerce")
        trip_col = next((c for c in df.columns if "Tripwire" in c), None)
        trip_pct = 100.0 * (pd.to_numeric(df[trip_col], errors="coerce") > 0).mean() if trip_col else 0.0
        config = load_attack_config(path)
        records.append(
            {
                "grid": next((part for part in path.parts if part.startswith("grid")), ""),
                "agent": path.parent.name,
                "seed": parse_seed(path),
                "mean_reward": float(reward.mean()),
                "std_reward": float(reward.std(ddof=1)) if len(reward) > 1 else 0.0,
                "n": len(reward),
                "trip_pct": trip_pct,
                "attack_enabled": config.get("red_team", False),
                "attack_params": ";".join(f"{k}={v}" for k, v in sorted(config.items())),
                "path": path.as_posix(),
            }
        )
    return pd.DataFrame(records)


def main():
    df = analyze_files()
    if df.empty:
        print("No se encontraron CSV canónicos para F2.")
        return
    print(f"Información monitoreada ({len(df)} archivos) — consulta {CANONICAL_DOC}:")
    summary = df.groupby("agent").agg(
        seeds=("seed", lambda x: ", ".join(sorted(set(s for s in x if s)))),
        mean_reward=("mean_reward", "mean"),
        std_reward=("std_reward", "mean"),
        n=("n", "sum"),
        attack_enabled=("attack_enabled", "any"),
    )
    print(summary.to_string())

    try:
        df.boxplot(column="mean_reward", by="agent")
        plt.suptitle("")
        plt.title("Media de recompensa por agente (F2 canonical)")
        plt.tight_layout()
        out_path = Path("results/v11/plots/f2_redteam_mean_reward_boxplot.png")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path, dpi=150)
        plt.close()
        print(f"Plot guardado en: {out_path}")
    except Exception as exc:
        print(f"[WARN] no se pudo generar el gráfico: {exc}")


if __name__ == "__main__":
    main()
